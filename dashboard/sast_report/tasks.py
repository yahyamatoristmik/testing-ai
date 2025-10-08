# tasks.py
import subprocess
import json
import tempfile
import os
import docker
from django.utils import timezone
from datetime import timedelta
import datetime
from .models import ScanJob, VulnerabilityReport

def run_semgrep_scan(scan_job_id, scan_type='full', custom_rules=''):
    """
    Task untuk menjalankan Semgrep scan - FULLY FIXED VERSION
    """
    print(f"🚀 STARTING SCAN JOB #{scan_job_id}")
    
    try:
        scan_job = ScanJob.objects.get(id=scan_job_id)
        scan_job.status = 'running'
        scan_job.started_at = timezone.now()
        scan_job.log = "Starting security scan...\n"
        scan_job.save()
        
        print(f"📦 Scan target: {scan_job.repository.name} (Branch: {scan_job.branch})")
        
        repository = scan_job.repository
        scm_profile = repository.scm_profile
        
        print(f"🔗 SCM: {scm_profile.scm_type} - User: {scm_profile.username}")
        print(f"🏷️ Repository URL: {repository.url}")
        print(f"🔐 Private: {repository.private}")
        
        # Setup temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_dir = os.path.join(temp_dir, 'repo')
            print(f"📁 Temp directory: {temp_dir}")
            
            # Clone repository - DENGAN EXTRA VALIDATION
            print("🔄 Cloning repository...")
            
            # Method 1: Coba function cloning
            clone_success = clone_repository(scm_profile, repository, repo_dir, temp_dir)
            print(f"📊 Clone function result: {clone_success}")
            
            # Method 2: Jika function gagal, coba manual langsung
            if not clone_success:
                print("🔄 Function cloning failed, trying manual clone...")
                clone_success = manual_clone_direct(repository, repo_dir)
                print(f"📊 Manual clone result: {clone_success}")
            
            if not clone_success:
                error_msg = "❌ All cloning methods failed"
                print(error_msg)
                scan_job.status = 'failed'
                scan_job.log = error_msg
                scan_job.finished_at = timezone.now()
                scan_job.save()
                return
            
            print("✅ Repository cloning completed")
            
            # EXTREME VALIDATION - Pastikan repository benar-benar ada
            if not os.path.exists(repo_dir):
                error_msg = f"❌ Repository directory missing: {repo_dir}"
                print(error_msg)
                scan_job.status = 'failed'
                scan_job.log = error_msg
                scan_job.finished_at = timezone.now()
                scan_job.save()
                return
            
            repo_contents = os.listdir(repo_dir)
            if not repo_contents:
                error_msg = f"❌ Repository directory empty: {repo_dir}"
                print(error_msg)
                scan_job.status = 'failed'
                scan_job.log = error_msg
                scan_job.finished_at = timezone.now()
                scan_job.save()
                return
            
            print(f"📂 Repository validated: {len(repo_contents)} items")
            print(f"📂 Sample contents: {repo_contents[:5]}")
            
            # Run Semgrep menggunakan Docker
            try:
                print("🐳 Checking Docker...")
                client = docker.from_env()
                
                # Test Docker connection
                try:
                    client.ping()
                    print("✅ Docker daemon is running")
                except Exception as e:
                    print(f"❌ Docker daemon not available: {e}")
                    # Fallback to direct semgrep
                    run_semgrep_fallback(scan_job, repo_dir, custom_rules, temp_dir, scan_type)
                    return
                
                # Prepare volume mapping
                volumes = {
                    os.path.abspath(repo_dir): {
                        'bind': '/src',
                        'mode': 'ro'
                    }
                }
                
                print(f"📁 Volume mapping: {repo_dir} -> /src")
                
                # Build semgrep command
                semgrep_cmd = build_semgrep_command(scan_type, custom_rules, temp_dir, volumes)
                print(f"🔧 Semgrep command: {' '.join(semgrep_cmd)}")
                
                # Run semgrep in container
                print("🐳 Starting Docker container...")
                container = client.containers.run(
                    'returntocorp/semgrep:latest',
                    semgrep_cmd,
                    volumes=volumes,
                    remove=True,
                    detach=False,
                    stdout=True,
                    stderr=True
                )
                
                print("✅ Docker container executed successfully")
                
                # Process results
                if isinstance(container, bytes):
                    output = container.decode('utf-8')
                else:
                    output = str(container)
                
                print(f"📄 Output length: {len(output)}")
                print(f"📄 First 500 chars: {output[:500]}...")
                
                # Parse JSON output
                try:
                    semgrep_results = json.loads(output)
                    results_count = len(semgrep_results.get('results', []))
                    print(f"📊 Found {results_count} findings")
                    
                    # Process results dengan error handling
                    process_semgrep_results(scan_job, semgrep_results)
                    
                    scan_job.status = 'completed'
                    scan_job.log = f"Scan completed successfully. Found {scan_job.findings_count} issues.\n"
                    
                except json.JSONDecodeError as e:
                    error_msg = f"❌ Semgrep output parsing failed: {str(e)}\nOutput preview: {output[:500]}"
                    print(error_msg)
                    scan_job.status = 'failed'
                    scan_job.log = error_msg
                    
            except docker.errors.ImageNotFound:
                print("❌ Docker image not found, trying fallback...")
                run_semgrep_fallback(scan_job, repo_dir, custom_rules, temp_dir, scan_type)
            except docker.errors.APIError as e:
                error_msg = f"❌ Docker API error: {str(e)}"
                print(error_msg)
                scan_job.status = 'failed'
                scan_job.log = error_msg
            except Exception as e:
                error_msg = f"❌ Docker execution error: {str(e)}"
                print(error_msg)
                scan_job.status = 'failed'
                scan_job.log = error_msg
                
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR in run_semgrep_scan: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            scan_job.status = 'failed'
            scan_job.log = f"Unexpected error: {str(e)}\n{traceback.format_exc()}"
            scan_job.finished_at = timezone.now()
            scan_job.save()
        except:
            print("❌ Could not save error to scan job")
    
    # FINAL SAVE dengan better duration handling
    try:
        if 'scan_job' in locals():
            scan_job.finished_at = timezone.now()
            
            # Calculate duration menggunakan method yang aman
            scan_job.calculate_duration()
            
            scan_job.save()
            print(f"💾 Scan job #{scan_job_id} saved with status: {scan_job.status}")
        
    except Exception as e:
        print(f"❌ Error saving scan job: {e}")

def manual_clone_direct(repository, repo_dir):
    """Manual cloning sebagai fallback"""
    try:
        print(f"🔗 MANUAL CLONE: {repository.name}")
        print(f"📥 Cloning from: {repository.url}")
        
        # Simple git clone command
        result = subprocess.run([
            'git', 'clone', '--depth', '1', repository.url, repo_dir
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Manual clone successful")
            return True
        else:
            print(f"❌ Manual clone failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Manual clone error: {e}")
        return False

def clone_repository(scm_profile, repository, repo_dir, temp_dir):
    """Clone repository berdasarkan SCM type - ULTRA ROBUST"""
    print(f"🔗 Attempting to clone {repository.name} from {scm_profile.scm_type}")
    print(f"📦 Repository: {repository.name}")
    print(f"🔗 URL: {repository.url}") 
    print(f"🔐 Private: {repository.private}")
    print(f"👤 SCM User: {scm_profile.username}")
    print(f"🏷️ Default Branch: {repository.default_branch}")
    
    try:
        if scm_profile.scm_type == 'github':
            return clone_github_repository(scm_profile, repository, repo_dir)
        elif scm_profile.scm_type == 'gitlab':
            return clone_gitlab_repository(scm_profile, repository, repo_dir)
        elif scm_profile.scm_type == 'bitbucket':
            return clone_bitbucket_repository(scm_profile, repository, repo_dir)
        else:
            print(f"❌ Unsupported SCM type: {scm_profile.scm_type}")
            return False
    except Exception as e:
        print(f"❌ Clone repository error: {e}")
        import traceback
        traceback.print_exc()
        return False

def clone_gitlab_repository(scm_profile, repository, repo_dir):
    """Clone GitLab repository dengan better error handling - FIXED"""
    try:
        print(f"🔗 Cloning GitLab repository: {repository.name}")
        print(f"📦 Repository URL: {repository.url}")
        print(f"🔐 Private: {repository.private}")
        print(f"👤 Username: {scm_profile.username}")
        print(f"🏷️ Default branch: {repository.default_branch}")
        
        # Untuk GitLab, format URL yang benar adalah:
        # Public repo: https://gitlab.com/username/reponame.git
        # Private repo dengan token: https://oauth2:token@gitlab.com/username/reponame.git
        
        # TAPI dari debug kita tahu repository ini PUBLIC, jadi gunakan URL langsung
        if repository.private and scm_profile.access_token:
            # Private repo dengan token
            clone_url = f"https://oauth2:{scm_profile.access_token}@gitlab.com/{scm_profile.username}/{repository.name}.git"
            print(f"🔐 Using authenticated URL for private repo")
        else:
            # Public repo - GUNAKAN URL ASLI DARI DATABASE
            clone_url = repository.url
            print(f"🔓 Using public URL: {clone_url}")
        
        print(f"📥 Cloning from: {clone_url}")
        
        # Build git command
        clone_cmd = [
            'git', 'clone', 
            '--depth', '1', 
            '--branch', repository.default_branch,
            clone_url, 
            repo_dir
        ]
        
        print(f"🔧 Git command: {' '.join(clone_cmd)}")
        
        # Execute clone
        result = subprocess.run(
            clone_cmd, 
            check=True, 
            capture_output=True, 
            text=True, 
            timeout=300
        )
        
        print("✅ GitLab clone successful")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ GitLab clone error: {e.stderr}")
        print(f"🔧 Return code: {e.returncode}")
        
        # Coba alternative approach
        return try_alternative_clone(scm_profile, repository, repo_dir, 'gitlab')
    except subprocess.TimeoutExpired:
        print("❌ GitLab clone timeout")
        return False
    except Exception as e:
        print(f"❌ GitLab clone unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def clone_github_repository(scm_profile, repository, repo_dir):
    """Clone GitHub repository dengan better error handling"""
    try:
        # Untuk GitHub, kita perlu format URL yang benar
        if repository.private and scm_profile.access_token:
            # Private repo dengan token - format: https://token@github.com/username/repo.git
            clone_url = f"https://{scm_profile.access_token}@github.com/{scm_profile.username}/{repository.name}.git"
        else:
            # Public repo atau tanpa auth - gunakan URL asli
            clone_url = repository.url
        
        print(f"📥 Cloning GitHub: {clone_url}")
        
        clone_cmd = ['git', 'clone', '--depth', '1', '--branch', repository.default_branch, clone_url, repo_dir]
        
        result = subprocess.run(
            clone_cmd, 
            check=True, 
            capture_output=True, 
            text=True, 
            timeout=300
        )
        print("✅ GitHub clone successful")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ GitHub clone error: {e.stderr}")
        # Coba alternative approach
        return try_alternative_clone(scm_profile, repository, repo_dir, 'github')
    except subprocess.TimeoutExpired:
        print("❌ GitHub clone timeout")
        return False
    except Exception as e:
        print(f"❌ GitHub clone unexpected error: {e}")
        return False

def clone_bitbucket_repository(scm_profile, repository, repo_dir):
    """Clone Bitbucket repository dengan better error handling"""
    try:
        # Untuk Bitbucket
        if repository.private and scm_profile.access_token:
            # Private repo dengan app password
            clone_url = f"https://{scm_profile.username}:{scm_profile.access_token}@bitbucket.org/{scm_profile.username}/{repository.name}.git"
        else:
            # Public repo atau tanpa auth
            clone_url = repository.url
        
        print(f"📥 Cloning Bitbucket: {clone_url}")
        
        clone_cmd = ['git', 'clone', '--depth', '1', '--branch', repository.default_branch, clone_url, repo_dir]
        
        result = subprocess.run(
            clone_cmd, 
            check=True, 
            capture_output=True, 
            text=True, 
            timeout=300
        )
        print("✅ Bitbucket clone successful")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Bitbucket clone error: {e.stderr}")
        return try_alternative_clone(scm_profile, repository, repo_dir, 'bitbucket')
    except subprocess.TimeoutExpired:
        print("❌ Bitbucket clone timeout")
        return False
    except Exception as e:
        print(f"❌ Bitbucket clone unexpected error: {e}")
        return False

def try_alternative_clone(scm_profile, repository, repo_dir, scm_type):
    """Alternative cloning method jika method utama gagal - IMPROVED"""
    print(f"🔄 Trying alternative clone methods for {scm_type}")
    
    alternatives = [
        # Method 1: Public URL tanpa branch
        {
            'name': 'Public URL without branch',
            'cmd': ['git', 'clone', '--depth', '1', repository.url, repo_dir]
        },
        # Method 2: Public URL dengan branch
        {
            'name': 'Public URL with branch', 
            'cmd': ['git', 'clone', '--depth', '1', '--branch', repository.default_branch, repository.url, repo_dir]
        },
        # Method 3: Simple git clone
        {
            'name': 'Simple clone',
            'cmd': ['git', 'clone', repository.url, repo_dir]
        }
    ]
    
    for i, alternative in enumerate(alternatives):
        print(f"🔄 Trying alternative {i+1}: {alternative['name']}")
        print(f"🔧 Command: {' '.join(alternative['cmd'])}")
        
        try:
            result = subprocess.run(
                alternative['cmd'],
                capture_output=True, 
                text=True, 
                timeout=180
            )
            
            if result.returncode == 0:
                print(f"✅ Alternative {i+1} successful: {alternative['name']}")
                return True
            else:
                print(f"❌ Alternative {i+1} failed: {result.stderr[:200]}")
                
        except subprocess.TimeoutExpired:
            print(f"❌ Alternative {i+1} timeout")
        except Exception as e:
            print(f"❌ Alternative {i+1} error: {e}")
    
    print("❌ All alternative clone methods failed")
    return False

def build_semgrep_command(scan_type, custom_rules, temp_dir, volumes):
    """Build semgrep command berdasarkan scan type - PROVEN CONFIGS"""
    semgrep_cmd = ['semgrep', '--json', '--quiet', '/src']
    
    # Gunakan config yang terbukti bekerja dari test
    if scan_type == 'security':
        # Config yang terbukti menemukan issues
        semgrep_cmd.extend(['--config', 'p/security-audit'])
        semgrep_cmd.extend(['--config', 'p/python'])
        semgrep_cmd.extend(['--config', 'p/javascript']) 
        semgrep_cmd.extend(['--config', 'p/java'])
    elif scan_type == 'secrets':
        # Untuk secrets, gunakan config khusus + fallback
        semgrep_cmd.extend(['--config', 'p/secrets'])
        semgrep_cmd.extend(['--config', 'p/security-audit'])  # Fallback
    elif scan_type == 'ci':
        semgrep_cmd.extend(['--config', 'p/ci'])
        semgrep_cmd.extend(['--config', 'p/security-audit'])
    else:  # full scan - PAKAI CONFIG YANG TERBUKTI BEKERJA
        semgrep_cmd.extend(['--config', 'auto'])  # Auto menemukan 7 issues
        semgrep_cmd.extend(['--config', 'p/security-audit'])  # +3 issues
        semgrep_cmd.extend(['--config', 'p/python'])  # +3 issues
        # Total: ~13 issues seperti di test
    
    # Add custom rules jika ada
    if custom_rules:
        rules_file = os.path.join(temp_dir, 'custom_rules.yml')
        with open(rules_file, 'w') as f:
            f.write(custom_rules)
        volumes[rules_file] = {
            'bind': '/custom_rules.yml',
            'mode': 'ro'
        }
        semgrep_cmd.extend(['--config', '/custom_rules.yml'])
    
    print(f"🔧 Semgrep configs: {[cmd for cmd in semgrep_cmd if cmd.startswith('--config')]}")
    return semgrep_cmd

def run_semgrep_fallback(scan_job, repo_dir, custom_rules, temp_dir, scan_type):
    """
    Fallback method jika Docker tidak available
    """
    try:
        output_file = os.path.join(temp_dir, 'semgrep_results.json')
        
        # Build command
        semgrep_cmd = ['semgrep', '--json', '--quiet', '--output', output_file, repo_dir]
        
        # Add config berdasarkan scan type
        if scan_type == 'security':
            semgrep_cmd.extend(['--config', 'p/security-audit'])
        elif scan_type == 'secrets':
            semgrep_cmd.extend(['--config', 'p/secrets'])
        elif scan_type == 'ci':
            semgrep_cmd.extend(['--config', 'p/ci'])
        else:  # full scan
            semgrep_cmd.extend(['--config', 'auto'])
        
        # Add custom rules jika ada
        if custom_rules:
            rules_file = os.path.join(temp_dir, 'custom_rules.yml')
            with open(rules_file, 'w') as f:
                f.write(custom_rules)
            semgrep_cmd.extend(['--config', rules_file])
        
        result = subprocess.run(semgrep_cmd, capture_output=True, text=True, timeout=1800)
        
        if result.returncode in [0, 1]:  # Semgrep returns 1 when findings are found
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    semgrep_results = json.loads(f.read())
                process_semgrep_results(scan_job, semgrep_results)
                scan_job.status = 'completed'
            else:
                scan_job.status = 'failed'
                scan_job.log = f"Semgrep output file not found: {result.stderr}"
        else:
            scan_job.status = 'failed'
            scan_job.log = f"Semgrep failed: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        scan_job.status = 'failed'
        scan_job.log = "Semgrep scan timeout (30 minutes)"
    except Exception as e:
        scan_job.status = 'failed'
        scan_job.log = f"Fallback error: {str(e)}"

def process_semgrep_results(scan_job, semgrep_results):
    """
    Process Semgrep results dengan better error handling
    """
    try:
        findings_count = 0
        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0
        info_count = 0
        
        # Clear existing vulnerabilities untuk scan ini
        VulnerabilityReport.objects.filter(scan_job=scan_job).delete()
        
        for result in semgrep_results.get('results', []):
            # Map Semgrep severity ke sistem kita
            severity_map = {
                'ERROR': 'HIGH',
                'WARNING': 'MEDIUM', 
                'INFO': 'LOW'
            }
            
            semgrep_severity = result.get('extra', {}).get('severity', 'INFO')
            severity = severity_map.get(semgrep_severity, 'LOW')
            
            # Update counters
            findings_count += 1
            if severity == 'HIGH':
                high_count += 1
            elif severity == 'MEDIUM':
                medium_count += 1
            elif severity == 'LOW':
                low_count += 1
            else:
                info_count += 1
            
            # Extract additional metadata dengan safety checks
            metadata = result.get('extra', {})
            
            # Handle CWE ID - truncate jika terlalu panjang
            cwe_ids = metadata.get('metadata', {}).get('cwe', [])
            cwe_id = ''
            if cwe_ids:
                cwe_id = str(cwe_ids[0])[:45]  # ✅ TRUNCATE ke 45 karakter
                if len(str(cwe_ids[0])) > 45:
                    print(f"⚠️ Truncated CWE ID: {cwe_ids[0]} -> {cwe_id}")
            
            # Handle OWASP category
            owasp_categories = metadata.get('metadata', {}).get('owasp', [])
            owasp_category = owasp_categories[0] if owasp_categories else ''
            
            # Get code snippet
            code_snippet = metadata.get('lines', '')
            if not code_snippet and 'start' in result and 'end' in result:
                try:
                    # Try to extract code from the file
                    file_path = os.path.join('/src', result.get('path', ''))
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as f:
                            lines = f.readlines()
                            start_line = result.get('start', {}).get('line', 1) - 1
                            end_line = result.get('end', {}).get('line', start_line + 1)
                            code_snippet = ''.join(lines[max(0, start_line-2):end_line+1])
                except:
                    code_snippet = ''
            
            # Create vulnerability report dengan error handling
            try:
                VulnerabilityReport.objects.create(
                    scan_job=scan_job,
                    rule_id=result.get('check_id', '')[:200],  # ✅ Truncate rule_id
                    severity=severity,
                    confidence='HIGH',
                    file_path=result.get('path', '')[:500].replace('/src/', ''),  # ✅ Truncate file_path
                    line_number=result.get('start', {}).get('line', 0),
                    message=metadata.get('message', '')[:1000],  # ✅ Truncate message
                    description=metadata.get('message', '')[:1000],  # ✅ Truncate description
                    recommendation=_generate_recommendation(result),
                    code_snippet=code_snippet[:5000],  # ✅ Truncate code_snippet
                    cwe_id=cwe_id,  # ✅ Sudah ditruncate
                    owasp_category=owasp_category[:95],  # ✅ Truncate owasp_category
                    metadata=json.dumps(metadata)[:5000]  # ✅ Truncate metadata
                )
            except Exception as e:
                print(f"❌ Error creating vulnerability report: {e}")
                # Continue dengan vulnerability berikutnya
                continue
        
        # Update scan job counts
        scan_job.findings_count = findings_count
        scan_job.critical_count = critical_count
        scan_job.high_count = high_count
        scan_job.medium_count = medium_count
        scan_job.low_count = low_count
        scan_job.info_count = info_count
        
        print(f"📊 Processed {findings_count} vulnerabilities")
        
    except Exception as e:
        print(f"❌ Error processing semgrep results: {e}")
        scan_job.log = f"Error processing results: {str(e)}"

def _generate_recommendation(result):
    """Generate recommendation based on finding type"""
    rule_id = result.get('check_id', '')
    message = result.get('extra', {}).get('message', '')
    
    if 'hardcoded' in rule_id.lower() or 'secret' in rule_id.lower():
        return "Remove hardcoded credentials and use environment variables or secure secret management"
    elif 'sql' in rule_id.lower() or 'injection' in rule_id.lower():
        return "Use parameterized queries or ORM to prevent SQL injection"
    elif 'xss' in rule_id.lower():
        return "Implement proper output encoding and input validation"
    elif 'path' in rule_id.lower() or 'traversal' in rule_id.lower():
        return "Validate and sanitize file paths to prevent directory traversal"
    else:
        return "Review the code and implement security best practices"
