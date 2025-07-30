# valuation_agent.py

import sys
import os
import asyncio
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import google.generativeai as genai
from utils.llm import call_groq_deepseek  # async function

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found in .env or environment variables")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)


class ValuationAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def estimate_valuation(self, markdown: str) -> str:
        prompt = f"""
You are a financial valuation expert.

Based on the following markdown financial article, estimate the company's valuation insights.

Include:
- Whether it is undervalued, fairly valued, or overvalued
- Mention of valuation ratios (P/E, PEG, DCF, etc.)
- Price estimate if applicable
- Justification for your reasoning

Respond in **markdown** format.

--- Article ---
{markdown}
"""
        try:
            # Gemini is synchronous — DO NOT await
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[Gemini Error] {e}")
            print("[Fallback] Using Groq DeepSeek instead...")
            try:
                return await call_groq_deepseek(prompt)  # ✅ await correctly
            except Exception as fallback_error:
                return f"❌ Valuation Failed: {fallback_error}"


# ------------------- TEST -------------------
if __name__ == "__main__":
    dummy_md = """
Example Inc. reported a P/E ratio of 15.5, slightly below the industry average of 18.
The company also has stable earnings growth and low debt.
Recent analyst reports indicate the stock may be undervalued.
"""

    agent = ValuationAgent()

    async def test():
        result = await agent.estimate_valuation(dummy_md)
        print("\n💰 [Valuation Result]\n", result)

    asyncio.run(test())
