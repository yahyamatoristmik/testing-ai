import os
import django
import tempfile
import subprocess
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from sast_report.models import ScanJob, Repository, VulnerabilityReport
from django.contrib.auth.models import User

def test_scan_with_problematic_files():
    print("🧪 TESTING SCAN WITH PROBLEMATIC FILES")
    
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
        
        # Buat files dengan BANYAK security issues yang jelas
        with open(os.path.join(repo_dir, 'app.py'), 'w') as f:
            f.write('''# Application with OBVIOUS security issues
import os
import subprocess
from flask import request
import sqlite3

# HARDCODED SECRETS - should be detected by p/secrets
API_KEY = "sk_live_1234567890abcdef"
PASSWORD = "super_secret_password_123"
PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC..."

# SQL INJECTION VULNERABILITY
def get_user_data(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # This is SQL injection!
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return cursor.fetchall()

# COMMAND INJECTION
def run_command(cmd):
    # This is command injection!
    result = subprocess.check_output(cmd, shell=True)
    return result

# PATH TRAVERSAL
def read_user_file(filename):
    # Path traversal vulnerability
    with open(f"/home/user/files/{filename}", "r") as f:
        return f.read()

# HARDCODED JWT SECRET
JWT_SECRET = "my_jwt_secret_key_12345"

# UNSAFE DESERIALIZATION
import pickle
def load_data(data):
    return pickle.loads(data)

# WEAK CRYPTO
import hashlib
def hash_password(password):
    # Using weak MD5 hashing
    return hashlib.md5(password.encode()).hexdigest()
''')
        
        # Buat JavaScript file dengan issues
        with open(os.path.join(repo_dir, 'app.js'), 'w') as f:
            f.write('''// JavaScript with security issues
const crypto = require('crypto');

// Hardcoded JWT secret
const JWT_SECRET = 'my_jwt_secret_123';

// SQL injection in JavaScript
function getUser(username) {
    const query = "SELECT * FROM users WHERE username = '" + username + "'";
    return db.query(query);
}

// XSS vulnerability
function displayMessage(message) {
    document.getElementById('message').innerHTML = message;
}

// Weak random generator
function generateToken() {
    return Math.random().toString(36).substring(2);
}

// Hardcoded API keys
const STRIPE_KEY = 'sk_test_1234567890abcdef';
const AWS_KEY = 'AKIAIOSFODNN7EXAMPLE';
''')
        
        # Buat Java file dengan issues
        with open(os.path.join(repo_dir, 'App.java'), 'w') as f:
            f.write('''// Java with security issues
import java.sql.*;

public class App {
    // Hardcoded password
    private static final String DB_PASSWORD = "db_password_123";
    
    // SQL injection
    public static void getUser(String userId) throws SQLException {
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost/test", "user", DB_PASSWORD);
        Statement stmt = conn.createStatement();
        // SQL injection here!
        String query = "SELECT * FROM users WHERE id = " + userId;
        ResultSet rs = stmt.executeQuery(query);
    }
    
    // Hardcoded crypto key
    private static final byte[] CRYPTO_KEY = "1234567890123456".getBytes();
}
''')
        
        print(f"📁 Created problematic files in: {repo_dir}")
        print(f"📂 Files: {os.listdir(repo_dir)}")
        
        # Test dengan berbagai config Semgrep
        configs_to_test = [
            ['--config', 'p/secrets'],
            ['--config', 'p/security-audit'],
            ['config', 'p/ci'],
            ['--config', 'auto'],
            ['--config', 'p/python', '--config', 'p/secrets'],
            ['--config', 'p/javascript', '--config', 'p/secrets'],
        ]
        
        total_issues = 0
        
        for i, config in enumerate(configs_to_test):
            print(f"\n🔧 Testing config {i+1}: {config}")
            
            try:
                # Build command
                semgrep_cmd = ['semgrep', '--json', '--quiet'] + config + ['/src']
                
                result = subprocess.run([
                    'docker', 'run', '--rm', '-v', f'{repo_dir}:/src',
                    'returntocorp/semgrep:latest'
                ] + semgrep_cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode in [0, 1]:
                    findings = json.loads(result.stdout)
                    issues = len(findings.get('results', []))
                    total_issues += issues
                    
                    print(f"📊 Found {issues} issues with config {config}")
                    
                    if issues > 0:
                        for j, finding in enumerate(findings.get('results', [])[:2]):  # Show first 2
                            print(f"   {j+1}. {finding.get('check_id')} - {finding.get('extra', {}).get('message')}")
                
                else:
                    print(f"❌ Config failed: {result.stderr[:200]}")
                    
            except Exception as e:
                print(f"❌ Config test error: {e}")
        
        # Update scan job dengan hasil
        scan_job.status = 'completed'
        scan_job.findings_count = total_issues
        scan_job.log = f"Test completed. Found {total_issues} total issues across all configs."
        scan_job.save()
        
        print(f"\n📈 TOTAL ISSUES FOUND: {total_issues}")

if __name__ == "__main__":
    test_scan_with_problematic_files()
