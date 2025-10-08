import os
import django
import tempfile
import subprocess
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, Repository, VulnerabilityReport
from django.contrib.auth.models import User

def test_scan_with_mock():
    print("🧪 TESTING SCAN WITH MOCK DATA")
    
    user = User.objects.get(username='admin')
    repository = Repository.objects.filter(scm_profile__user=user).first()
    
    # Buat scan job
    scan_job = ScanJob.objects.create(
        user=user,
        repository=repository,
        branch='main',
        status='running'
    )
    
    print(f"🎯 Created scan job #{scan_job.id}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_dir = os.path.join(temp_dir, 'repo')
        os.makedirs(repo_dir)
        
        # Buat mock files dengan security issues
        with open(os.path.join(repo_dir, 'app.py'), 'w') as f:
            f.write('''# Test application with security issues
import os

# Hardcoded credentials - should be detected
DB_PASSWORD = "mysecretpassword123"
API_KEY = "sk_live_1234567890abcdef"

def login(username, password):
    # SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return query

def read_file(filename):
    # Path traversal vulnerability
    with open(f"/var/www/uploads/{filename}", "r") as f:
        return f.read()
''')
        
        print(f"📁 Created mock files in: {repo_dir}")
        print(f"📂 Files: {os.listdir(repo_dir)}")
        
        # Run semgrep menggunakan Docker (sama seperti tasks.py)
        try:
            print("🐳 Running Semgrep with Docker...")
            result = subprocess.run([
                'docker', 'run', '--rm', '-v', f'{repo_dir}:/src',
                'returntocorp/semgrep:latest',
                'semgrep', '--json', '--config', 'auto', '/src'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode in [0, 1]:
                print("✅ Semgrep executed successfully")
                
                # Parse results
                findings = json.loads(result.stdout)
                issue_count = len(findings.get('results', []))
                
                print(f"📊 Found {issue_count} security issues")
                
                # Update scan job
                scan_job.status = 'completed'
                scan_job.findings_count = issue_count
                scan_job.log = f"Mock scan completed. Found {issue_count} issues.\nOutput: {result.stdout[:500]}..."
                scan_job.save()
                
                # Create sample vulnerability reports
                for i, finding in enumerate(findings.get('results', [])[:3]):
                    VulnerabilityReport.objects.create(
                        scan_job=scan_job,
                        rule_id=finding.get('check_id', f'rule_{i}'),
                        severity='HIGH',
                        confidence='HIGH',
                        file_path=finding.get('path', 'app.py').replace('/src/', ''),
                        line_number=finding.get('start', {}).get('line', 1),
                        message=finding.get('extra', {}).get('message', 'Security issue found'),
                        description="This is a test vulnerability",
                        recommendation="Fix the security issue",
                        code_snippet=finding.get('extra', {}).get('lines', 'Code snippet'),
                    )
                
                print(f"💾 Created {min(3, issue_count)} vulnerability reports")
                
            else:
                print(f"❌ Semgrep failed: {result.stderr}")
                scan_job.status = 'failed'
                scan_job.log = f"Semgrep failed: {result.stderr}"
                scan_job.save()
                
        except Exception as e:
            print(f"❌ Mock test failed: {e}")
            scan_job.status = 'failed'
            scan_job.log = f"Test failed: {str(e)}"
            scan_job.save()

if __name__ == "__main__":
    test_scan_with_mock()
