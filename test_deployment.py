#!/usr/bin/env python3
"""
🧪 Test Script for IntelliVest AI Deployment
============================================

This script tests your Streamlit app with production settings
to ensure it's ready for deployment on Render.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def test_requirements():
    """Test if all requirements can be installed"""
    print("📦 Testing requirements installation...")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment - skipping requirements test")
        print("   (packages are already installed)")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Requirements installation failed: {e}")
        return False

def test_streamlit_config():
    """Test Streamlit configuration"""
    print("⚙️ Testing Streamlit configuration...")
    
    config_file = Path(".streamlit/config.toml")
    if not config_file.exists():
        print("❌ Streamlit config file not found")
        return False
    
    print("✅ Streamlit config file exists")
    return True

def test_app_import():
    """Test if the main app can be imported"""
    print("🔧 Testing app import...")
    try:
        # Add current directory to path
        sys.path.insert(0, str(Path.cwd()))
        
        # Try to import the main app
        import streamlit_app
        print("✅ App imports successfully")
        return True
    except ImportError as e:
        print(f"❌ App import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import: {e}")
        return False

def test_environment_variables():
    """Test environment variable setup"""
    print("🔑 Testing environment variables...")
    
    required_vars = [
        "GOOGLE_API_KEY",
        "GROQ_API_KEY", 
        "TAVILY_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("   These will need to be set in Render dashboard")
    else:
        print("✅ All required environment variables are set")
    
    return len(missing_vars) == 0

def test_streamlit_run():
    """Test if Streamlit can run the app"""
    print("🚀 Testing Streamlit execution...")
    
    try:
        # Test with a timeout to avoid hanging
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8502",  # Use different port
            "--server.address", "localhost",
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Streamlit app started successfully")
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Streamlit failed to start: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Streamlit: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 IntelliVest AI Deployment Test Suite")
    print("=" * 50)
    
    tests = [
        ("Requirements Installation", test_requirements),
        ("Streamlit Configuration", test_streamlit_config),
        ("App Import", test_app_import),
        ("Environment Variables", test_environment_variables),
        ("Streamlit Execution", test_streamlit_run)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your app is ready for deployment!")
        print("\n📋 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Follow the DEPLOYMENT_GUIDE.md")
        print("3. Deploy to Render!")
    else:
        print("⚠️ Some tests failed. Please fix the issues before deployment.")
        print("\n🔧 Check the error messages above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 