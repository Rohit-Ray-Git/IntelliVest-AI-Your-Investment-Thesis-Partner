#!/usr/bin/env python3
"""
🧪 LiteLLM Connection Test
==========================

Test LiteLLM connectivity which is used by the Streamlit app
"""

import os
from dotenv import load_dotenv

def test_litellm_connection():
    """Test LiteLLM connection"""
    print("🧪 Testing LiteLLM Connection...")
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Test LiteLLM with Google Gemini
        from litellm import completion
        
        print("🔑 Testing Google Gemini via LiteLLM...")
        
        response = completion(
            model="gemini/gemini-2.5-flash",
            messages=[{"role": "user", "content": "Hello, this is a test message."}],
            api_key=os.getenv('GOOGLE_API_KEY'),
            max_tokens=50
        )
        
        print("✅ LiteLLM Google API test successful!")
        print(f"📝 Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ LiteLLM Google API Error: {e}")
        print(f"🔍 Error Type: {type(e).__name__}")
    
    try:
        # Test LiteLLM with Groq
        print("\n🔑 Testing Groq via LiteLLM...")
        
        response = completion(
            model="groq/llama3.1-70b-8192",
            messages=[{"role": "user", "content": "Hello, this is a test message."}],
            api_key=os.getenv('GROQ_API_KEY'),
            max_tokens=50
        )
        
        print("✅ LiteLLM Groq API test successful!")
        print(f"📝 Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ LiteLLM Groq API Error: {e}")
        print(f"🔍 Error Type: {type(e).__name__}")

if __name__ == "__main__":
    test_litellm_connection() 