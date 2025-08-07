#!/usr/bin/env python3
"""
🔑 API Key Test Script
======================

Test if API keys are loaded correctly from .env file
"""

import os
from dotenv import load_dotenv

def test_api_keys():
    """Test if API keys are loaded correctly"""
    print("🔑 Testing API Key Loading...")
    
    # Load environment variables
    load_dotenv()
    
    # Check each API key
    api_keys = {
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
        'TAVILY_API_KEY': os.getenv('TAVILY_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY')
    }
    
    print("\n📋 API Key Status:")
    for key, value in api_keys.items():
        status = "✅ SET" if value else "❌ NOT SET"
        print(f"  {key}: {status}")
    
    # Test if we can make a simple API call
    if api_keys['GOOGLE_API_KEY']:
        print("\n🧪 Testing Google API connectivity...")
        try:
            import requests
            response = requests.get(
                'https://generativelanguage.googleapis.com/v1beta/models',
                headers={'Authorization': f'Bearer {api_keys["GOOGLE_API_KEY"]}'},
                timeout=10
            )
            print(f"✅ Google API Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Google API Error: {e}")
    else:
        print("\n⚠️ Google API key not set - cannot test connectivity")
    
    if api_keys['GROQ_API_KEY']:
        print("\n🧪 Testing Groq API connectivity...")
        try:
            import requests
            response = requests.get(
                'https://api.groq.com/openai/v1/models',
                headers={'Authorization': f'Bearer {api_keys["GROQ_API_KEY"]}'},
                timeout=10
            )
            print(f"✅ Groq API Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Groq API Error: {e}")
    else:
        print("\n⚠️ Groq API key not set - cannot test connectivity")

if __name__ == "__main__":
    test_api_keys() 