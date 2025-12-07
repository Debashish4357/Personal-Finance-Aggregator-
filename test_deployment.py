#!/usr/bin/env python3
"""
Local deployment test script
Test your app before deploying to Railway
"""

import subprocess
import sys
import os

def test_docker_build():
    """Test Docker build"""
    print("🐳 Testing Docker build...")
    try:
        result = subprocess.run(
            ["docker", "build", "-t", "pfa-test", "."],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            print("✅ Docker build successful")
            return True
        else:
            print("❌ Docker build failed:")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker first.")
        return False

def test_requirements():
    """Test if all requirements can be installed"""
    print("📦 Testing requirements installation...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--dry-run"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ All requirements are valid")
            return True
        else:
            print("❌ Requirements installation failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error testing requirements: {e}")
        return False

def check_env_template():
    """Check if environment template exists"""
    print("🔧 Checking environment configuration...")
    
    env_template = ".env.template"
    if os.path.exists(env_template):
        print("✅ Environment template found")
        print("💡 Copy .env.template to .env and update with your values")
        return True
    else:
        print("❌ Environment template not found")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Railway deployment readiness...")
    print("=" * 50)
    
    tests = [
        ("Environment Template", check_env_template),
        ("Requirements", test_requirements),
        ("Docker Build", test_docker_build),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ Your app is ready for Railway deployment!")
        print("\n📖 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Connect your GitHub repo to Railway")
        print("3. Add PostgreSQL database in Railway")
        print("4. Set JWT_SECRET environment variable")
        print("5. Deploy!")
    else:
        print("❌ Please fix the failing tests before deploying")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)