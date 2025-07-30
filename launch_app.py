# launch_app.py
import webbrowser
import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🚀 Starting IntelliVest AI Application...")
    print()
    
    # Get the current directory
    current_dir = Path(__file__).parent
    frontend_path = current_dir / "frontend" / "index.html"
    
    # Open the HTML file directly in browser
    print("🌐 Opening frontend in browser...")
    webbrowser.open(frontend_path.as_uri())
    
    print()
    print("📊 Starting backend API...")
    
    # Start the backend API
    python_exe = current_dir / "venv" / "Scripts" / "python.exe"
    api_script = current_dir / "api" / "main.py"
    
    try:
        subprocess.run([
            str(python_exe),
            "-m", "uvicorn",
            "api.main:app",
            "--host", "127.0.0.1",
            "--port", "8001"
        ], cwd=current_dir)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

if __name__ == "__main__":
    main() 