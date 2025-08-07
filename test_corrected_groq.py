#!/usr/bin/env python3
"""
🧪 Corrected Groq Models Test
=============================

Test the corrected Groq model names
"""

import os
from dotenv import load_dotenv

def test_corrected_groq():
    """Test corrected Groq models"""
    print("🧪 Testing Corrected Groq Models...")
    
    # Load environment variables
    load_dotenv()
    
    try:
        from litellm import completion
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("❌ Groq API key not found")
            return
        
        # Test the corrected model names
        models_to_test = [
            "groq/llama3-70b-8192",
            "groq/llama-3.3-70b-versatile",
            "groq/deepseek-r1-distill-llama-70b"
        ]
        
        for model in models_to_test:
            print(f"\n🔑 Testing {model}...")
            try:
                response = completion(
                    model=model,
                    messages=[{"role": "user", "content": "Hello, this is a test."}],
                    api_key=api_key,
                    max_tokens=50
                )
                print(f"✅ {model} - SUCCESS!")
                print(f"📝 Response: {response.choices[0].message.content}")
            except Exception as e:
                print(f"❌ {model} - FAILED: {e}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_corrected_groq() 