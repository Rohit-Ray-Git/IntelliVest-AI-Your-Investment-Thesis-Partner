# setup_api.py
"""
API Key Setup Script for IntelliVest AI
This script helps you set up your API keys for the AI features.
"""

import os
from pathlib import Path

def setup_api_keys():
    print("🔑 IntelliVest AI - API Key Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    
    if env_file.exists():
        print("📁 Found existing .env file")
        with open(env_file, 'r') as f:
            content = f.read()
            if "GOOGLE_API_KEY" in content:
                print("✅ Google API key already configured")
            if "GROQ_API_KEY" in content:
                print("✅ Groq API key already configured")
    else:
        print("📁 Creating new .env file")
    
    print("\n🔧 To enable AI features, you need to set up API keys:")
    print("\n1. **Google API Key (for Gemini):**")
    print("   - Go to: https://makersuite.google.com/app/apikey")
    print("   - Create a new API key")
    print("   - Add to .env file: GOOGLE_API_KEY=your_key_here")
    
    print("\n2. **Groq API Key (for Llama/Mixtral):**")
    print("   - Go to: https://console.groq.com/keys")
    print("   - Create a new API key")
    print("   - Add to .env file: GROQ_API_KEY=your_key_here")
    
    print("\n📝 Example .env file content:")
    print("GOOGLE_API_KEY=your_gemini_api_key_here")
    print("GROQ_API_KEY=your_groq_api_key_here")
    
    print("\n💡 Note: You can use either or both API keys.")
    print("   The application will work with fallback responses if no keys are provided.")
    
    # Create .env file if it doesn't exist
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write("# IntelliVest AI API Keys\n")
            f.write("# Add your API keys below:\n\n")
            f.write("GOOGLE_API_KEY=your_gemini_api_key_here\n")
            f.write("GROQ_API_KEY=your_groq_api_key_here\n")
        print("\n✅ Created .env file template")
        print("📝 Please edit the .env file and add your actual API keys")
    
    print("\n🚀 After setting up API keys, restart the application:")
    print("   python run_app.py")

if __name__ == "__main__":
    setup_api_keys() 