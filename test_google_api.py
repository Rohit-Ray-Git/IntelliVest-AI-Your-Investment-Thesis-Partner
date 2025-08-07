#!/usr/bin/env python3
"""
🧪 Google API Test Script
========================

Test Google Gemini API with the provided key
"""

import os
from dotenv import load_dotenv

def test_google_api():
    """Test Google API functionality"""
    print("🧪 Testing Google Gemini API...")
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ Google API key not found")
        return
    
    print(f"🔑 API Key found: {api_key[:10]}...")
    
    try:
        # Test with a simple request
        import requests
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": "Hello, this is a test message."
                }]
            }]
        }
        
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Google API is working correctly!")
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                print("✅ Generated response successfully!")
            else:
                print("⚠️ No response generated")
        else:
            print(f"❌ API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing Google API: {e}")

if __name__ == "__main__":
    test_google_api() 