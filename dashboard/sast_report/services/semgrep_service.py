# sast_report/services/semgrep_service.py
import json
import subprocess
import tempfile
import os
import shutil
from datetime import datetime
from django.utils import timezone
from django.db import transaction

from ..models import ScanJob, VulnerabilityReport

def run_semgrep_scan(scan_job_id):
    """
    Run semgrep scan and save results to database
    """
    try:
        scan_job = ScanJob.objects.get(id=scan_job_id)
        scan_job.status = 'running'
        scan_job.started_at = timezone.now()
        scan_job.save()
        
        print(f"🚀 Starting semgrep scan for {scan_job.repository.name}")
        
        # Create temp directory for cloning
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = os.path.join(temp_dir, 'repo')
            output_path = os.path.join(temp_dir, 'semgrep_results.json')
            
            # Clone repository
            clone_success = clone_repository(scan_job.repository, repo_path, scan_job.branch)
            if not clone_success:
                scan_job.status = 'failed'
                scan_job.log += "\nFailed to clone repository"
                scan_job.save()
                return False
            
            # Run semgrep scan
            try:
                # Run semgrep command
                cmd = [
                    'semgrep', 'scan',
                    '--config', 'auto',
                    '--json',
                    '--output', output_path,
                    '--quiet',
                    repo_path
                ]
                
                print(f"🔧 Running command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
                
                if result.returncode != 0 and result.returncode != 1:  # semgrep returns 1 when findings are found
                    print(f"❌ Semgrep failed with return code: {result.returncode}")
                    print(f"Stderr: {result.stderr}")
                    raise Exception(f"Semgrep failed: {result.stderr}")
                
                # Parse results
                if os.path.exists(output_path):
                    with open(output_path, 'r') as f:
                        semgrep_data = json.load(f)
                else:
                    # If no output file, try to parse stdout
                    try:
                        semgrep_data = json.loads(result.stdout)
                    except:
                        semgrep_data = {'results': []}
                
                # Process findings
                process_semgrep_results(scan_job, semgrep_data)
                
                # Update scan job
                scan_job.finished_at = timezone.now()
                scan_job.status = 'completed'
                scan_job.save()
                
                print(f"✅ Scan completed successfully with {scan_job.findings_count} findings")
                return True
                
            except subprocess.TimeoutExpired:
                scan_job.status = 'failed'
                scan_job.log += "\nScan timed out after 30 minutes"
                scan_job.save()
                print("❌ Scan timed out")
                return False
            except Exception as e:
                scan_job.status = 'failed'
                scan_job.log += f"\nScan error: {str(e)}"
                scan_job.save()
                print(f"❌ Scan failed: {e}")
                return False
                
    except ScanJob.DoesNotExist:
        print(f"❌ Scan job {scan_job_id} not found")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def clone_repository(repository, clone_path, branch='main'):
    """
    Clone repository to temporary directory
    """
    try:
        # For public repositories, use the URL directly
        clone_url = repository.url
        
        cmd = ['git', 'clone', '--depth', '1', '--branch', branch, clone_url, clone_path]
        
        print(f"📥 Cloning {repository.name} from {clone_url}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(f"❌ Clone failed: {result.stderr}")
            return False
            
        print(f"✅ Successfully cloned {repository.name}")
        return True
        
    except Exception as e:
        print(f"❌ Clone error: {e}")
        return False

def process_semgrep_results(scan_job, semgrep_data):
    """
    Process semgrep results and save to database
    """
    try:
        with transaction.atomic():
            # Delete existing vulnerabilities for this scan
            VulnerabilityReport.objects.filter(scan_job=scan_job).delete()
            
            findings_count = 0
            critical_count = 0
            high_count = 0
            medium_count = 0
            low_count = 0
            info_count = 0
            
            # Process each finding
            for finding in semgrep_data.get('results', []):
                try:
                    # Map semgrep severity to our levels
                    severity_map = {
                        'ERROR': 'HIGH',
                        'WARNING': 'MEDIUM', 
                        'INFO': 'INFO'
                    }
                    
                    semgrep_severity = finding.get('extra', {}).get('severity', 'INFO')
                    severity = severity_map.get(semgrep_severity, 'INFO')
                    
                    # Get file path relative to repo root
                    file_path = finding.get('path', '')
                    if file_path.startswith('/tmp/'):
                        # Extract just the filename if it's a temp path
                        file_path = os.path.basename(file_path)
                    
                    # Create vulnerability record
                    vulnerability = VulnerabilityReport(
                        scan_job=scan_job,
                        rule_id=finding.get('check_id', 'unknown'),
                        severity=severity,
                        confidence='HIGH',  # Semgrep generally has high confidence
                        file_path=file_path,
                        line_number=finding.get('start', {}).get('line', 0),
                        message=finding.get('extra', {}).get('message', 'No message'),
                        description=finding.get('extra', {}).get('message', 'No description'),
                        recommendation="Review the code and apply appropriate security fixes.",
                        code_snippet=finding.get('extra', {}).get('lines', ''),
                        metadata=json.dumps({
                            'semgrep_severity': semgrep_severity,
                            'confidence': finding.get('extra', {}).get('confidence', ''),
                            'impact': finding.get('extra', {}).get('impact', ''),
                            'likelihood': finding.get('extra', {}).get('likelihood', ''),
                            'raw_data': finding  # Store complete finding for reference
                        })
                    )
                    vulnerability.save()
                    
                    # Update counters
                    findings_count += 1
                    if severity == 'CRITICAL':
                        critical_count += 1
                    elif severity == 'HIGH':
                        high_count += 1
                    elif severity == 'MEDIUM':
                        medium_count += 1
                    elif severity == 'LOW':
                        low_count += 1
                    else:
                        info_count += 1
                        
                    print(f"  📝 Saved vulnerability: {severity} - {vulnerability.rule_id}")
                        
                except Exception as e:
                    print(f"⚠️ Error processing finding: {e}")
                    continue
            
            # Update scan job counts
            scan_job.findings_count = findings_count
            scan_job.critical_count = critical_count
            scan_job.high_count = high_count
            scan_job.medium_count = medium_count
            scan_job.low_count = low_count
            scan_job.info_count = info_count
            
            print(f"📊 Scan statistics: {findings_count} total, {critical_count} critical, {high_count} high, {medium_count} medium, {low_count} low, {info_count} info")
            
    except Exception as e:
        print(f"❌ Error processing semgrep results: {e}")
        raise
