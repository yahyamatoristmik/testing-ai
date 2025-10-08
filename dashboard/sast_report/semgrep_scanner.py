import os
import json
import subprocess
import tempfile
from .models import ScanJob, VulnerabilityReport

def run_semgrep_scan(job_id):
    try:
        job = ScanJob.objects.get(id=job_id)
        job.status = 'running'
        job.save()
        
        print(f"Starting Semgrep scan for: {job.repository.name}")
        
        # Create temp directory
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Clone repository
            clone_cmd = f"git clone {job.repository.url} {tmp_dir}/repo"
            result = subprocess.run(clone_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                job.status = 'failed'
                job.save()
                return False
            
            # Run Semgrep via Docker
            semgrep_cmd = f"""
            docker run --rm -v "{tmp_dir}/repo:/src" \\
            returntocorp/semgrep semgrep scan \\
            --config=auto \\
            --json \\
            --output=/src/semgrep_results.json \\
            /src
            """
            
            result = subprocess.run(semgrep_cmd, shell=True, capture_output=True, text=True)
            
            # Parse results
            results_file = f"{tmp_dir}/repo/semgrep_results.json"
            if os.path.exists(results_file):
                with open(results_file, 'r') as f:
                    semgrep_data = json.load(f)
                
                # Create vulnerability reports from Semgrep results
                vulnerabilities_created = 0
                for result in semgrep_data.get('results', []):
                    # Map Semgrep severity to our system
                    severity_map = {
                        'ERROR': 'HIGH',
                        'WARNING': 'MEDIUM', 
                        'INFO': 'LOW'
                    }
                    
                    VulnerabilityReport.objects.create(
                        scan_job=job,
                        rule_id=result.get('check_id', 'unknown'),
                        severity=severity_map.get(result.get('extra', {}).get('severity', 'INFO'), 'LOW'),
                        file_path=result.get('path', '').replace(f"{tmp_dir}/repo/", ""),
                        line_number=result.get('start', {}).get('line', 0),
                        message=result.get('extra', {}).get('message', ''),
                        description=f"Semgrep finding: {result.get('check_id', '')}",
                        recommendation=result.get('extra', {}).get('fix', ''),
                        metadata={
                            'tool': 'semgrep',
                            'confidence': result.get('extra', {}).get('confidence', 'medium'),
                            'impact': result.get('extra', {}).get('impact', ''),
                            'likelihood': result.get('extra', {}).get('likelihood', '')
                        }
                    )
                    vulnerabilities_created += 1
                
                job.status = 'completed'
                job.findings_count = vulnerabilities_created
                job.save()
                
                print(f"Semgrep scan completed. Found {vulnerabilities_created} vulnerabilities.")
                return True
            else:
                job.status = 'failed'
                job.save()
                print("Semgrep results file not found")
                return False
                
    except Exception as e:
        print(f"Semgrep scan error: {e}")
        job.status = 'failed'
        job.save()
        return False
