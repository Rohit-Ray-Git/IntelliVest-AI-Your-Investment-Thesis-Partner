# test_models.py
"""
Test script to verify available AI models and their status
"""

import os
from utils.ai_client import RobustAIClient

def test_models():
    print("🧪 Testing AI Models Configuration")
    print("=" * 50)
    
    # Load environment variables
    env_file = ".env"
    if os.path.exists(env_file):
        print("📁 Loading environment variables...")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ Environment variables loaded")
    
    # Test AI client
    client = RobustAIClient()
    
    print(f"\n📊 Available Providers: {len(client.providers)}")
    for i, provider in enumerate(client.providers, 1):
        print(f"   {i}. {provider}")
    
    if not client.providers:
        print("\n⚠️ No API keys found!")
        print("💡 Run: python get_api_keys.py for setup instructions")
        print("🚀 Or continue with fallback responses: python run_app.py")
    else:
        print(f"\n✅ {len(client.providers)} AI providers configured")
        print("🚀 Ready to use: python run_app.py")

if __name__ == "__main__":
    test_models() 