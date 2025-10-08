import os
import subprocess
import tempfile

def test_environment():
    print("🔍 TESTING ENVIRONMENT DIFFERENCES")
    
    print("📋 Python executable:", sys.executable)
    print("📋 Current working directory:", os.getcwd())
    print("📋 User:", os.getenv('USER'))
    print("📋 PATH:", os.getenv('PATH'))
    
    # Test git command
    print("\n🔧 Testing git command...")
    result = subprocess.run(['git', '--version'], capture_output=True, text=True)
    print("Git version:", result.stdout.strip())
    
    # Test simple clone in current environment
    print("\n🔄 Testing clone in current environment...")
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_dir = os.path.join(temp_dir, 'repo')
        
        try:
            result = subprocess.run([
                'git', 'clone', '--depth', '1', 
                'https://gitlab.com/yoyox/ai-dast-sast.git', 
                repo_dir
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ Clone successful in test environment")
                print(f"📂 Contents: {os.listdir(repo_dir)}")
            else:
                print(f"❌ Clone failed: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Clone error: {e}")

if __name__ == "__main__":
    test_environment()

