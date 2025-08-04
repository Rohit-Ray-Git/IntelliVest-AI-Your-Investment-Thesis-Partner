#!/usr/bin/env python3
"""
🚀 IntelliVest AI - Streamlit App Launcher
==========================================

Simple launcher for the IntelliVest AI Streamlit application
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Streamlit app"""
    print("🚀 Launching IntelliVest AI Streamlit App...")
    print("=" * 50)
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Path to the Streamlit app
    app_path = current_dir / "streamlit_app.py"
    
    if not app_path.exists():
        print(f"❌ Error: {app_path} not found!")
        return False
    
    print(f"✅ App found: {app_path}")
    print("🌐 Starting Streamlit server...")
    print("📱 The app will open in your default browser")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(app_path),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Streamlit server stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching Streamlit: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 