import os
import django
import tempfile
import subprocess
import json
import docker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, Repository, UserSCMProfile
from django.contrib.auth.models import User
from django.utils import timezone

def debug_manual_scan():
    print("🐛 DEBUG MANUAL SCAN")
    
    user = User.objects.get(username='admin')
    scm_profile = UserSCMProfile.objects.get(user=user, scm_type='gitlab')
    repository = Repository.objects.filter(scm_profile=scm_profile).first()
    
    if not repository:
        print("❌ No repository found")
        return
    
    print(f"📦 Testing repository: {repository.name}")
    
    # Buat scan job manual
    scan_job = ScanJob.objects.create(
        user=user,
        repository=repository,
        branch='main',
        status='running',
        started_at=timezone.now()
    )
    
    print(f"🎯 Created scan job #{scan_job.id}")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_dir = os.path.join(temp_dir, 'repo')
            print(f"📁 Temp directory: {temp_dir}")
            
            # 1. Test Cloning
            print("\n1. 🔄 TESTING CLONING...")
            clone_url = f"https://gitlab.com/yoyox/{repository.name}"
            print(f"🔗 Clone URL: {clone_url}")
            
            result = subprocess.run([
                'git', 'clone', '--depth', '1', clone_url, repo_dir
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"❌ Clone failed: {result.stderr}")
                scan_job.status = 'failed'
                scan_job.log = f"Clone failed: {result.stderr}"
                scan_job.save()
                return
            
            print("✅ Clone successful")
            print(f"📂 Contents: {os.listdir(repo_dir)}")
            
            # 2. Test Docker
            print("\n2. 🐳 TESTING DOCKER...")
            try:
                client = docker.from_env()
                client.ping()
                print("✅ Docker daemon is running")
            except Exception as e:
                print(f"❌ Docker daemon error: {e}")
                scan_job.status = 'failed'
                scan_job.log = f"Docker error: {str(e)}"
                scan_job.save()
                return
            
            # 3. Test Semgrep Image
            print("\n3. 🔍 TESTING SEMGREP IMAGE...")
            try:
                # Pull image jika belum ada
                print("📥 Pulling semgrep image...")
                client.images.pull('returntocorp/semgrep:latest')
                print("✅ Semgrep image ready")
            except Exception as e:
                print(f"❌ Semgrep image error: {e}")
                scan_job.status = 'failed'
                scan_job.log = f"Semgrep image error: {str(e)}"
                scan_job.save()
                return
            
            # 4. Test Semgrep Execution
            print("\n4. 🚀 TESTING SEMGREP EXECUTION...")
            try:
                volumes = {
                    os.path.abspath(repo_dir): {
                        'bind': '/src',
                        'mode': 'ro'
                    }
                }
                
                print(f"📁 Volume mapping: {repo_dir} -> /src")
                
                # Run simple semgrep command
                container = client.containers.run(
                    'returntocorp/semgrep:latest',
                    ['semgrep', '--version'],
                    volumes=volumes,
                    remove=True,
                    detach=False,
                    stdout=True,
                    stderr=True
                )
                
                if isinstance(container, bytes):
                    output = container.decode('utf-8')
                else:
                    output = str(container)
                
                print(f"✅ Semgrep version: {output.strip()}")
                
            except Exception as e:
                print(f"❌ Semgrep execution error: {e}")
                scan_job.status = 'failed'
                scan_job.log = f"Semgrep execution error: {str(e)}"
                scan_job.save()
                return
            
            # 5. Test Actual Scan
            print("\n5. 🔧 TESTING ACTUAL SCAN...")
            try:
                semgrep_cmd = [
                    'semgrep', '--json', '--quiet',
                    '--config', 'auto',
                    '/src'
                ]
                
                print(f"🔧 Command: {' '.join(semgrep_cmd)}")
                
                container = client.containers.run(
                    'returntocorp/semgrep:latest',
                    semgrep_cmd,
                    volumes=volumes,
                    remove=True,
                    detach=False,
                    stdout=True,
                    stderr=True
                )
                
                if isinstance(container, bytes):
                    output = container.decode('utf-8')
                else:
                    output = str(container)
                
                print(f"📄 Output length: {len(output)}")
                
                # Parse results
                findings = json.loads(output)
                issues = len(findings.get('results', []))
                
                print(f"📊 Found {issues} security issues")
                
                # Update scan job
                scan_job.status = 'completed'
                scan_job.findings_count = issues
                scan_job.log = f"Debug scan completed. Found {issues} issues.\nOutput preview: {output[:500]}..."
                scan_job.save()
                
                print("✅ DEBUG SCAN COMPLETED SUCCESSFULLY")
                
            except Exception as e:
                print(f"❌ Actual scan error: {e}")
                scan_job.status = 'failed'
                scan_job.log = f"Actual scan error: {str(e)}"
                scan_job.save()
                
    except Exception as e:
        print(f"❌ DEBUG SCAN FAILED: {e}")
        import traceback
        traceback.print_exc()
        scan_job.status = 'failed'
        scan_job.log = f"Debug scan failed: {str(e)}\n{traceback.format_exc()}"
        scan_job.save()

if __name__ == "__main__":
    debug_manual_scan()
