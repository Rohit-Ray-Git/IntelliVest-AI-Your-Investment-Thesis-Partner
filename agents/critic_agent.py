# critic_agent.py
# critic_agent.py

import sys
import os
import asyncio
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import google.generativeai as genai
from utils.llm import call_groq_deepseek

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found in .env or environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

class CriticAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def critique_thesis(self, thesis_markdown: str) -> str:
        prompt = f"""
You are a professional investment analyst and critical reviewer.

Your job is to critique the following investment thesis:

1. Check for any biases or over-optimistic claims.
2. Identify missing information, risks, or contradictions.
3. Suggest improvements in reasoning, supporting data, or structure.
4. Output your feedback in **markdown format**.

--- Investment Thesis ---
{thesis_markdown}
"""

        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            print(f"[Gemini Error] {e}")
            print("[Fallback] Using Groq DeepSeek instead...")
            try:
                return call_groq_deepseek(prompt)
            except Exception as fallback_error:
                return f"❌ Critique Failed: {fallback_error}"


# Standalone test
if __name__ == "__main__":
    dummy_thesis = """
## 1. Summary of Company and Market Tone

Example Inc. showed strong growth. Everything is great.

## 2. Sentiment Stance

Positive.

## 3. Valuation Status

Undervalued.

## 4. Recommendation

Buy the stock.
"""
    agent = CriticAgent()

    async def test():
        result = await agent.critique_thesis(dummy_thesis)
        print("\n🧠 [Critique Output]\n", result)

    asyncio.run(test())
