# start_app.py

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting IntelliVest AI Backend...")
    # Use the virtual environment's Python executable
    python_exe = sys.executable
    backend_process = subprocess.Popen([
        python_exe, "-m", "uvicorn", 
        "api.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000",
        "--reload"
    ])
    return backend_process

def start_frontend():
    """Start the frontend HTTP server"""
    print("🌐 Starting Frontend Server...")
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return None
    
    os.chdir(frontend_dir)
    frontend_process = subprocess.Popen([
        sys.executable, "-m", "http.server", "3000"
    ])
    os.chdir("..")
    return frontend_process

def main():
    print("🎯 IntelliVest AI - Full Stack Application")
    print("=" * 50)
    
    # Start backend
    backend_process = start_backend()
    time.sleep(3)  # Wait for backend to start
    
    # Start frontend
    frontend_process = start_frontend()
    time.sleep(2)  # Wait for frontend to start
    
    print("\n✅ Application Started Successfully!")
    print("=" * 50)
    print("📊 Backend API: http://localhost:8000")
    print("🌐 Frontend UI: http://localhost:3000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("=" * 50)
    print("Press Ctrl+C to stop all servers")
    
    # Open browser
    try:
        webbrowser.open("http://localhost:3000")
    except:
        pass
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Servers stopped")

if __name__ == "__main__":
    main() 