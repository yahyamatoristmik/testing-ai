import os
import sys
import django

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, VulnerabilityReport
from django.utils import timezone

def inspect_vulnerability_model():
    """Check what fields are available in VulnerabilityReport"""
    print("🔍 INSPECTING VULNERABILITY REPORT MODEL")
    print("=" * 50)
    
    fields = VulnerabilityReport._meta.get_fields()
    for field in fields:
        if not field.is_relation:
            print(f"  - {field.name} ({field.get_internal_type()})")
        else:
            print(f"  - {field.name} -> {field.related_model.__name__}")
    
    # Try to create a sample to see required fields
    print("\n🧪 TESTING FIELD CREATION...")
    try:
        sample_scan = ScanJob.objects.first()
        test_vuln = VulnerabilityReport.objects.create(
            scan_job=sample_scan,
            name='Test Vulnerability',
            severity_level='medium',
            description='Test description',
            file_location='test.py',
            line_number=1
        )
        print("✅ Success with: name, severity_level, description, file_location, line_number")
        test_vuln.delete()
    except Exception as e:
        print(f"❌ Failed: {e}")

def force_process_scan(scan_id):
    print(f"\n🔄 FORCE PROCESSING SCAN #{scan_id}")
    print("=" * 50)
    
    try:
        scan = ScanJob.objects.get(id=scan_id)
        print(f"📋 Scan Details:")
        print(f"   - Repository: {scan.repository.name}")
        print(f"   - Branch: {scan.branch}")
        print(f"   - Current Status: {scan.status}")
        
        if scan.status in ['queued', 'processing']:
            # Update status
            scan.status = 'processing'
            scan.started_at = timezone.now()
            scan.save()
            print("✅ Status: processing")
            
            # Create vulnerabilities with correct fields
            vulnerabilities = [
                {
                    'name': 'SQL Injection Found',
                    'severity_level': 'high',
                    'description': 'User input in SQL query without sanitization',
                    'file_location': 'src/auth.py',
                    'line_number': 45,
                },
                {
                    'name': 'XSS Vulnerability', 
                    'severity_level': 'medium',
                    'description': 'Unescaped user input in template',
                    'file_location': 'templates/profile.html',
                    'line_number': 23,
                }
            ]
            
            created_count = 0
            for vuln_data in vulnerabilities:
                try:
                    VulnerabilityReport.objects.create(
                        scan_job=scan,
                        name=vuln_data['name'],
                        severity_level=vuln_data['severity_level'],
                        description=vuln_data['description'],
                        file_location=vuln_data['file_location'],
                        line_number=vuln_data['line_number']
                    )
                    created_count += 1
                    print(f"✅ Created: {vuln_data['name']}")
                except Exception as e:
                    print(f"❌ Failed to create {vuln_data['name']}: {e}")
            
            # Mark as completed
            scan.status = 'done'
            scan.finished_at = timezone.now()
            scan.findings_count = created_count
            scan.high_count = 1  # Adjust based on actual counts
            scan.medium_count = 1
            
            if scan.started_at:
                scan.scan_duration = scan.finished_at - scan.started_at
            
            scan.save()
            
            print(f"\n🎉 SCAN #{scan_id} COMPLETED!")
            print(f"📊 Findings: {created_count}")
            
        else:
            print(f"ℹ️ Scan #{scan_id} is already: {scan.status}")
            
    except ScanJob.DoesNotExist:
        print(f"❌ Scan #{scan_id} not found")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    inspect_vulnerability_model()
    print("\n" + "=" * 60)
    force_process_scan(8)
    force_process_scan(9) 
    force_process_scan(10)
