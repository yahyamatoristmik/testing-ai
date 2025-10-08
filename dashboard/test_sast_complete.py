#!/usr/bin/env python
"""
Complete SAST System Test
Tests SCM integration, scanning, and views together
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
sys.path.append('/home/dj/ai-evaluator/dashboard')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User, Group
from sast_report.models import *
from sast_report.views import *

def setup_test_data():
    """Setup test user and basic data"""
    print("🔧 SETTING UP TEST DATA")
    
    # Create test user
    user, created = User.objects.get_or_create(
        username='sast_test_user',
        defaults={
            'email': 'sast_test@example.com',
            'is_staff': True
        }
    )
    user.set_password('testpass123')
    user.save()
    
    # Create SCM profile
    scm_profile, created = UserSCMProfile.objects.get_or_create(
        user=user,
        scm_type='github',
        defaults={
            'access_token': 'test_token_123',
            'username': 'testuser'
        }
    )
    
    # Create test repository
    repo, created = Repository.objects.get_or_create(
        scm_profile=scm_profile,
        repo_id='test-repo-123',
        defaults={
            'name': 'SAST Test Repository',
            'url': 'https://github.com/testuser/sast-test-repo',
            'description': 'Repository for SAST system testing'
        }
    )
    
    print(f"  ✅ User: {user.username}")
    print(f"  ✅ SCM Profile: {scm_profile.scm_type}")
    print(f"  ✅ Repository: {repo.name}")
    
    return user, scm_profile, repo

def test_views(user):
    """Test all views using RequestFactory"""
    print("\\n🌐 TESTING VIEWS")
    
    factory = RequestFactory()
    views_to_test = [
        ('Dashboard', dashboard, '/sast-report/'),
        ('SCM Config', scm_config, '/sast-report/scm-config/'),
        ('Trigger Scan', trigger_scan, '/sast-report/trigger-scan/'),
        ('Scan Jobs', scan_jobs, '/sast-report/scan-jobs/'),
    ]
    
    for name, view_func, path in views_to_test:
        try:
            request = factory.get(path)
            request.user = user
            response = view_func(request)
            status = '✅' if response.status_code == 200 else '⚠️'
            print(f"  {status} {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ❌ {name} error: {e}")

def test_scan_workflow(user, repo):
    """Test complete scan workflow"""
    print("\\n🔍 TESTING SCAN WORKFLOW")
    
    # Step 1: Create scan job
    print("  1. Creating scan job...")
    scan_job = ScanJob.objects.create(
        user=user,
        repository=repo,
        branch='main',
        status='completed'
    )
    print(f"     ✅ Scan job #{scan_job.id} created")
    
    # Step 2: Add vulnerability findings
    print("  2. Adding vulnerability findings...")
    test_vulnerabilities = [
        {
            'rule_id': 'python.sql-injection',
            'severity': 'HIGH',
            'file_path': 'app/models.py',
            'line_number': 42,
            'message': 'Potential SQL injection vulnerability',
            'description': 'User input used directly in SQL query without parameterization',
            'recommendation': 'Use parameterized queries or ORM'
        },
        {
            'rule_id': 'python.hardcoded-secret',
            'severity': 'MEDIUM', 
            'file_path': 'config/settings.py',
            'line_number': 15,
            'message': 'Hardcoded API key detected',
            'description': 'Sensitive credentials stored in source code',
            'recommendation': 'Use environment variables for sensitive data'
        },
        {
            'rule_id': 'python.command-injection',
            'severity': 'HIGH',
            'file_path': 'utils/helpers.py', 
            'line_number': 88,
            'message': 'Potential command injection vulnerability',
            'description': 'Unsanitized user input used in system commands',
            'recommendation': 'Use subprocess with explicit arguments'
        }
    ]
    
    for vuln_data in test_vulnerabilities:
        VulnerabilityReport.objects.create(scan_job=scan_job, **vuln_data)
    
    # Step 3: Update scan statistics
    scan_job.findings_count = len(test_vulnerabilities)
    scan_job.high_count = 2
    scan_job.medium_count = 1
    scan_job.save()
    
    print(f"     ✅ Added {scan_job.findings_count} vulnerabilities")
    print(f"     ✅ Severity breakdown - High: {scan_job.high_count}, Medium: {scan_job.medium_count}")
    
    return scan_job

def test_vulnerability_report(user, scan_job):
    """Test vulnerability report view"""
    print("\\n📊 TESTING VULNERABILITY REPORT")
    
    factory = RequestFactory()
    
    try:
        request = factory.get(f'/sast-report/vulnerability-report/{scan_job.id}/')
        request.user = user
        response = vulnerability_report(request, scan_job.id)
        status = '✅' if response.status_code == 200 else '⚠️'
        print(f"  {status} Vulnerability Report: HTTP {response.status_code}")
        
        # Check if vulnerabilities are accessible
        vulns = VulnerabilityReport.objects.filter(scan_job=scan_job)
        print(f"  ✅ {len(vulns)} vulnerabilities in report")
        
        # Show severity breakdown
        severity_counts = vulns.values('severity').annotate(count=models.Count('id'))
        for severity in severity_counts:
            print(f"     - {severity['severity']}: {severity['count']}")
            
    except Exception as e:
        print(f"  ❌ Vulnerability Report error: {e}")

def test_dashboard_stats(user):
    """Test dashboard statistics"""
    print("\\n📈 TESTING DASHBOARD STATISTICS")
    
    factory = RequestFactory()
    
    try:
        request = factory.get('/sast-report/')
        request.user = user
        response = dashboard(request)
        
        if response.status_code == 200:
            print("  ✅ Dashboard loaded successfully")
            
            # Check scan statistics
            total_scans = ScanJob.objects.filter(user=user).count()
            completed_scans = ScanJob.objects.filter(user=user, status='completed').count()
            total_findings = VulnerabilityReport.objects.filter(scan_job__user=user).count()
            
            print(f"     - Total scans: {total_scans}")
            print(f"     - Completed scans: {completed_scans}") 
            print(f"     - Total findings: {total_findings}")
        else:
            print(f"  ⚠️ Dashboard returned HTTP {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Dashboard error: {e}")

if __name__ == '__main__':
    print("🚀 STARTING COMPLETE SAST SYSTEM TEST")
    print("=" * 50)
    
    # Setup test environment
    user, scm_profile, repo = setup_test_data()
    
    # Run tests
    test_views(user)
    scan_job = test_scan_workflow(user, repo)
    test_vulnerability_report(user, scan_job)
    test_dashboard_stats(user)
    
    print("\\n" + "=" * 50)
    print("🎉 COMPLETE SAST SYSTEM TEST FINISHED")
    print("\\n📊 FINAL STATISTICS:")
    print(f"   - Users: {User.objects.count()}")
    print(f"   - SCM Profiles: {UserSCMProfile.objects.count()}")
    print(f"   - Repositories: {Repository.objects.count()}")
    print(f"   - Scan Jobs: {ScanJob.objects.count()}")
    print(f"   - Vulnerabilities: {VulnerabilityReport.objects.count()}")
