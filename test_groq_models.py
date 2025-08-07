#!/usr/bin/env python3
"""
🧪 Groq Models Test
===================

Check available Groq models
"""

import os
from dotenv import load_dotenv

def test_groq_models():
    """Test available Groq models"""
    print("🧪 Testing Groq Models...")
    
    # Load environment variables
    load_dotenv()
    
    try:
        import requests
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("❌ Groq API key not found")
            return
        
        # Get available models
        response = requests.get(
            'https://api.groq.com/openai/v1/models',
            headers={'Authorization': f'Bearer {api_key}'},
            timeout=10
        )
        
        if response.status_code == 200:
            models = response.json()
            print("✅ Available Groq Models:")
            for model in models['data']:
                print(f"  - {model['id']}")
        else:
            print(f"❌ Error getting models: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_groq_models() 