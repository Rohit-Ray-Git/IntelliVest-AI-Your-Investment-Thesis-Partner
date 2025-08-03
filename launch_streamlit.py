#!/usr/bin/env python3
"""
🚀 IntelliVest AI - Streamlit Launcher
======================================

Simple launcher for the IntelliVest AI Streamlit interface.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Main launcher function"""
    print("="*60)
    print("🚀 IntelliVest AI - Streamlit Launcher")
    print("="*60)
    
    # Check if we're in the right directory
    current_dir = Path(__file__).parent
    if not (current_dir / "streamlit_app.py").exists():
        print("❌ Error: streamlit_app.py not found in current directory")
        return
    
    # Choose which app to run
    print("\n📱 Choose Streamlit Interface:")
    print("1. Basic Interface (streamlit_app.py)")
    print("2. Enhanced Interface (streamlit_app_enhanced.py)")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        app_file = "streamlit_app.py"
        print("🚀 Launching Basic Streamlit Interface...")
    elif choice == "2":
        app_file = "streamlit_app_enhanced.py"
        print("🚀 Launching Enhanced Streamlit Interface...")
    else:
        print("❌ Invalid choice. Using basic interface.")
        app_file = "streamlit_app.py"
    
    # Check if the chosen app exists
    if not (current_dir / app_file).exists():
        print(f"❌ Error: {app_file} not found")
        return
    
    # Launch Streamlit
    try:
        print(f"📊 Starting Streamlit server with {app_file}...")
        print("🌐 The application will open in your browser automatically")
        print("🔗 Manual URL: http://localhost:8501")
        print("\n" + "="*50)
        
        # Streamlit command
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            str(current_dir / app_file),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ]
        
        # Launch Streamlit
        subprocess.run(cmd, cwd=current_dir)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Streamlit application stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching Streamlit: {e}")

if __name__ == "__main__":
    main() 