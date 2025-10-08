import os
import django
import tempfile
import subprocess
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, Repository, UserSCMProfile
from django.contrib.auth.models import User

def test_real_repository_scan():
    print("🧪 TESTING REAL REPOSITORY SCAN")
    
    user = User.objects.get(username='admin')
    scm_profile = UserSCMProfile.objects.get(user=user, scm_type='gitlab')
    repository = Repository.objects.filter(scm_profile=scm_profile).first()
    
    if not repository:
        print("❌ No repository found")
        return
    
    print(f"📦 Testing real repository: {repository.name}")
    
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
        
        # Clone repository (seperti di tasks.py)
        print("🔄 Cloning repository...")
        try:
            clone_url = f"https://gitlab.com/yoyox/{repository.name}"
            result = subprocess.run([
                'git', 'clone', '--depth', '1', clone_url, repo_dir
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"❌ Clone failed: {result.stderr}")
                scan_job.status = 'failed'
                scan_job.log = f"Clone failed: {result.stderr}"
                scan_job.save()
                return
            
            print("✅ Repository cloned successfully")
            print(f"📂 Contents: {os.listdir(repo_dir)}")
            
        except Exception as e:
            print(f"❌ Clone error: {e}")
            scan_job.status = 'failed'
            scan_job.log = f"Clone error: {str(e)}"
            scan_job.save()
            return
        
        # Run Semgrep dengan config yang agresif
        print("🐳 Running Semgrep scan...")
        try:
            result = subprocess.run([
                'docker', 'run', '--rm', '-v', f'{repo_dir}:/src',
                'returntocorp/semgrep:latest',
                'semgrep', '--json', '--quiet',
                '--config', 'p/security-audit',
                '--config', 'p/secrets', 
                '--config', 'p/ci',
                '--config', 'p/python',
                '--config', 'p/javascript',
                '/src'
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode in [0, 1]:
                findings = json.loads(result.stdout)
                issues = len(findings.get('results', []))
                
                print(f"📊 Found {issues} security issues in real repository")
                
                # Update scan job
                scan_job.status = 'completed'
                scan_job.findings_count = issues
                scan_job.log = f"Real repository scan completed. Found {issues} issues.\n"
                
                # Add sample of findings to log
                if issues > 0:
                    for i, finding in enumerate(findings.get('results', [])[:3]):
                        scan_job.log += f"\n{i+1}. {finding.get('check_id')} - {finding.get('path')}:{finding.get('start', {}).get('line')}"
                
                scan_job.save()
                
                print("✅ Real repository scan completed successfully")
                
            else:
                print(f"❌ Semgrep failed: {result.stderr}")
                scan_job.status = 'failed'
                scan_job.log = f"Semgrep failed: {result.stderr}"
                scan_job.save()
                
        except Exception as e:
            print(f"❌ Scan error: {e}")
            scan_job.status = 'failed'
            scan_job.log = f"Scan error: {str(e)}"
            scan_job.save()

if __name__ == "__main__":
    test_real_repository_scan()
