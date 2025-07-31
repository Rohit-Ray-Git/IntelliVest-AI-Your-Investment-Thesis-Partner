"""
🧪 Test Groq Models for CrewAI
=============================

Test which Groq models work with CrewAI.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

def test_groq_models():
    """Test different Groq models"""
    
    models_to_test = [
        "llama3.1-70b-8192",
        "llama3.1-8b-8192", 
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "deepseek-r1-distill-llama-70b"
    ]
    
    for model in models_to_test:
        print(f"\n🧪 Testing model: {model}")
        try:
            llm = ChatOpenAI(
                model=model,
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE"),
                temperature=0.7
            )
            
            # Test a simple completion
            response = llm.invoke("Say 'Hello from Groq!'")
            print(f"✅ {model} works: {response.content[:50]}...")
            
        except Exception as e:
            print(f"❌ {model} failed: {str(e)[:100]}...")

if __name__ == "__main__":
    test_groq_models() 