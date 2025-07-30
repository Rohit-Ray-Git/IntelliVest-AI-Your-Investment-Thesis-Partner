#!/usr/bin/env python3
"""
IntelliVest AI - Complete Application Launcher
This script handles the entire application startup process:
1. Activates virtual environment
2. Starts FastAPI backend
3. Opens frontend in browser
4. Provides status updates
"""

import subprocess
import sys
import os
import time
import webbrowser
import signal
import threading
from pathlib import Path

# Load environment variables from .env file
def load_env():
    """Load environment variables from .env file"""
    env_file = Path(".env")
    if env_file.exists():
        print("📁 Loading environment variables from .env file")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ Environment variables loaded")

class IntelliVestLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_process = None
        self.running = True
        
    def print_banner(self):
        """Print application banner"""
        print("=" * 60)
        print("🚀 IntelliVest AI - Investment Thesis Generator")
        print("=" * 60)
        print("📊 Backend API: http://127.0.0.1:8001")
        print("🌐 Frontend UI: file://" + str(self.project_root / "frontend" / "index.html"))
        print("📖 API Docs: http://127.0.0.1:8001/docs")
        print("=" * 60)
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        try:
            import playwright
            import litellm
            import fastapi
            import uvicorn
            print("✅ All dependencies are installed")
            return True
        except ImportError as e:
            print(f"❌ Missing dependency: {e}")
            print("Please run: pip install -r requirements.txt")
            return False
            
    def install_playwright_browsers(self):
        """Install Playwright browsers if needed"""
        print("🌐 Installing Playwright browsers...")
        try:
            subprocess.run([sys.executable, "-m", "playwright", "install"], 
                         check=True, capture_output=True)
            print("✅ Playwright browsers installed")
        except subprocess.CalledProcessError:
            print("⚠️ Playwright browser installation failed, but continuing...")
            
    def start_backend(self):
        """Start the FastAPI backend server"""
        print("📊 Starting backend API server...")
        
        try:
            # Start the backend server
            self.backend_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn",
                "api.main:app",
                "--host", "127.0.0.1",
                "--port", "8001",
                "--reload"
            ], cwd=self.project_root)
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Check if server is running
            if self.backend_process.poll() is None:
                print("✅ Backend server started successfully")
                return True
            else:
                print("❌ Backend server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
            
    def open_frontend(self):
        """Open the frontend in the default browser"""
        print("🌐 Opening frontend in browser...")
        
        frontend_path = self.project_root / "frontend" / "index.html"
        
        if frontend_path.exists():
            try:
                webbrowser.open(frontend_path.as_uri())
                print("✅ Frontend opened in browser")
                return True
            except Exception as e:
                print(f"❌ Error opening frontend: {e}")
                return False
        else:
            print("❌ Frontend file not found")
            return False
            
    def wait_for_backend(self, timeout=30):
        """Wait for backend to be ready"""
        print("⏳ Waiting for backend to be ready...")
        
        import requests
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get("http://127.0.0.1:8001/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Backend is ready!")
                    return True
            except:
                pass
            time.sleep(1)
            
        print("❌ Backend did not respond within timeout")
        return False
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n🛑 Shutting down IntelliVest AI...")
        self.running = False
        if self.backend_process:
            self.backend_process.terminate()
        sys.exit(0)
        
    def run(self):
        """Main launcher function"""
        try:
            # Load environment variables
            load_env()
            
            # Setup signal handlers
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            # Print banner
            self.print_banner()
            
            # Check dependencies
            if not self.check_dependencies():
                return False
                
            # Install Playwright browsers
            self.install_playwright_browsers()
            
            # Start backend
            if not self.start_backend():
                return False
                
            # Wait for backend to be ready
            if not self.wait_for_backend():
                print("⚠️ Backend may not be fully ready, but continuing...")
                
            # Open frontend
            if not self.open_frontend():
                print("⚠️ Could not open frontend automatically")
                print(f"Please manually open: {self.project_root / 'frontend' / 'index.html'}")
                
            # Success message
            print("\n🎉 IntelliVest AI is now running!")
            print("=" * 60)
            print("📊 Backend API: http://127.0.0.1:8001")
            print("🌐 Frontend UI: file://" + str(self.project_root / "frontend" / "index.html"))
            print("📖 API Docs: http://127.0.0.1:8001/docs")
            print("=" * 60)
            print("Press Ctrl+C to stop the application")
            print("=" * 60)
            
            # Keep the application running
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Application stopped by user")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        finally:
            if self.backend_process:
                print("🛑 Stopping backend server...")
                self.backend_process.terminate()
                self.backend_process.wait()
            print("✅ Application shutdown complete")

def main():
    """Main entry point"""
    launcher = IntelliVestLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 