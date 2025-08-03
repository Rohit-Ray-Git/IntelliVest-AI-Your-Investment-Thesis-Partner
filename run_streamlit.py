#!/usr/bin/env python3
"""
🚀 IntelliVest AI - Streamlit Launcher
======================================

This script launches the professional Streamlit UI for IntelliVest AI.
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'plotly',
        'pandas',
        'asyncio',
        'dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_environment():
    """Check environment configuration"""
    print("\n🔧 Checking environment configuration...")
    
    # Check for .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Load and check key environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        required_keys = [
            'GOOGLE_API_KEY',
            'GROQ_API_KEY'
        ]
        
        missing_keys = []
        for key in required_keys:
            if not os.getenv(key):
                missing_keys.append(key)
                print(f"❌ {key} not found")
            else:
                print(f"✅ {key} configured")
        
        if missing_keys:
            print(f"\n⚠️ Missing API keys: {', '.join(missing_keys)}")
            print("Please add them to your .env file")
            return False
    else:
        print("⚠️ .env file not found")
        print("Please create a .env file with your API keys")
        return False
    
    return True

def launch_streamlit():
    """Launch the Streamlit application"""
    print("\n🚀 Launching IntelliVest AI Streamlit Interface...")
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Streamlit command
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(current_dir / "streamlit_app.py"),
        "--server.port", "8501",
        "--server.address", "localhost",
        "--browser.gatherUsageStats", "false",
        "--theme.base", "light",
        "--theme.primaryColor", "#1f77b4",
        "--theme.backgroundColor", "#ffffff",
        "--theme.secondaryBackgroundColor", "#f0f2f6",
        "--theme.textColor", "#262730"
    ]
    
    try:
        print("📊 Starting Streamlit server...")
        print("🌐 The application will open in your browser automatically")
        print("🔗 Manual URL: http://localhost:8501")
        print("\n" + "="*50)
        
        # Launch Streamlit
        subprocess.run(cmd, cwd=current_dir)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Streamlit application stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching Streamlit: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("="*60)
    print("🚀 IntelliVest AI - Streamlit Launcher")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing packages.")
        return
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please configure your API keys.")
        return
    
    # Launch Streamlit
    print("\n🎯 All checks passed! Launching application...")
    launch_streamlit()

if __name__ == "__main__":
    main() 