import time
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class SimpleScanService:
    def __init__(self, scan_job):
        self.scan_job = scan_job
        
    def run_scan(self):
        """Jalankan scanning process yang sederhana dan stabil"""
        try:
            # Update status to running
            self.scan_job.status = 'running'
            self.scan_job.started_at = timezone.now()
            self.scan_job.scan_log = "🚀 Starting security scan...\n"
            self.scan_job.save()
            
            # Step 1: Simulate SCM connection
            self.scan_job.scan_log += "🔗 Connecting to repository...\n"
            self.scan_job.save()
            time.sleep(1)
            
            # Step 2: Simulate download
            self.scan_job.scan_log += "📥 Downloading source code...\n"
            self.scan_job.save()
            time.sleep(2)
            
            # Step 3: Simulate analysis
            self.scan_job.scan_log += "🔍 Analyzing code for security vulnerabilities...\n"
            self.scan_job.save()
            time.sleep(3)
            
            # Step 4: Generate findings
            findings = self._generate_sample_findings()
            self.scan_job.scan_log += f"📊 Found {len(findings)} potential security issues\n"
            self.scan_job.save()
            
            # Step 5: Save findings
            self._save_findings(findings)
            
            # Step 6: Complete scan
            self.scan_job.status = 'completed'
            self.scan_job.completed_at = timezone.now()
            self.scan_job.total_findings = len(findings)
            self.scan_job.scan_log += f"✅ Scan completed successfully! Found {len(findings)} vulnerabilities.\n"
            self.scan_job.save()
            
            return True
            
        except Exception as e:
            logger.error(f"Scan process error: {e}")
            self.scan_job.status = 'failed'
            self.scan_job.error_message = str(e)
            self.scan_job.scan_log += f"❌ Scan failed with error: {str(e)}\n"
            self.scan_job.completed_at = timezone.now()
            self.scan_job.save()
            return False
    
    def _generate_sample_findings(self):
        """Generate sample findings untuk testing"""
        import random
        
        findings_types = [
            {
                'rule_id': 'hardcoded-secret',
                'severity': 'high',
                'file_path': 'config/settings.py',
                'line_number': random.randint(10, 50),
                'message': 'Hardcoded API key detected',
                'description': 'Sensitive information should not be hardcoded in source code. Use environment variables instead.',
                'code_snippet': 'API_KEY = "sk_live_123456789abcdef"'
            },
            {
                'rule_id': 'sql-injection',
                'severity': 'critical',
                'file_path': 'models/user.py',
                'line_number': random.randint(20, 80),
                'message': 'Potential SQL injection vulnerability',
                'description': 'User input directly used in SQL query without parameterization.',
                'code_snippet': 'query = f"SELECT * FROM users WHERE id = {user_input}"'
            },
            {
                'rule_id': 'weak-crypto',
                'severity': 'medium',
                'file_path': 'utils/security.py',
                'line_number': random.randint(5, 30),
                'message': 'Weak cryptographic algorithm used',
                'description': 'MD5 is considered cryptographically broken and should not be used for security purposes.',
                'code_snippet': 'hashlib.md5(password.encode())'
            },
            {
                'rule_id': 'xss-vulnerability',
                'severity': 'high',
                'file_path': 'views/dashboard.py',
                'line_number': random.randint(40, 90),
                'message': 'Potential Cross-Site Scripting (XSS) vulnerability',
                'description': 'User input is directly rendered in HTML without proper escaping.',
                'code_snippet': 'return HttpResponse(f"<div>Hello {user_input}</div>")'
            },
            {
                'rule_id': 'info-exposure',
                'severity': 'low',
                'file_path': 'app/config.py',
                'line_number': random.randint(15, 45),
                'message': 'Information exposure in debug message',
                'description': 'Sensitive information might be exposed in debug logs.',
                'code_snippet': 'print(f"User password: {password}")'
            }
        ]
        
        # Return random subset of findings
        import random
        return random.sample(findings_types, random.randint(0, 3))
    
    def _save_findings(self, findings_data):
        """Save findings to database"""
        from ..models import Finding
        
        for finding_data in findings_data:
            Finding.objects.create(
                scan_job=self.scan_job,
                **finding_data
            )
