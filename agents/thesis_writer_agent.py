# thesis_writer_agent.py
import sys
import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.llm import call_groq_deepseek

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found in .env")

genai.configure(api_key=GOOGLE_API_KEY)

class ThesisWriterAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def generate_thesis(self, markdown: str, sentiment: str, valuation: str) -> str:
        prompt = f"""
You are a professional investment analyst.

Given the following inputs:
- Financial article (in markdown)
- Sentiment analysis result
- Valuation summary

Write a concise yet professional **Investment Thesis** including:
1. Summary of the company and market tone
2. Sentiment stance and rationale
3. Valuation status with key metrics
4. Final investment recommendation (Buy/Hold/Sell) with reason

Use markdown formatting.

### Article:
{markdown}

### Sentiment:
{sentiment}

### Valuation Insight:
{valuation}
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[Gemini Error] {e}")
            print("[Fallback] Using Groq DeepSeek...")
            try:
                return await call_groq_deepseek(prompt)
            except Exception as fallback_error:
                return f"❌ Thesis Generation Failed: {fallback_error}"


# ------------------- TEST -------------------

if __name__ == "__main__":
    dummy_md = """
Example Inc. reported Q2 earnings with revenue of $1.2B, up 18% YoY.
Earnings per share beat expectations, and cloud revenue led the growth.
Debt levels remain low and the company is expanding into new markets.
"""
    dummy_sentiment = "**Sentiment:** Positive\n\n**Justification:** Strong earnings and growth."
    dummy_valuation = """
**Valuation:** Undervalued  
**P/E Ratio:** 15.5 (vs Industry 18)  
**Debt:** Low  
**Growth:** Stable  
Analyst consensus indicates upside.
"""

    agent = ThesisWriterAgent()

    async def test():
        result = await agent.generate_thesis(dummy_md, dummy_sentiment, dummy_valuation)
        print("\n🧾 [Generated Investment Thesis]\n", result)

    asyncio.run(test())
