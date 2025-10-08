from .semgrep_scanner import run_semgrep_scan

def run_scan_job(job_id):
    """Run SAST scan using Semgrep"""
    return run_semgrep_scan(job_id)
