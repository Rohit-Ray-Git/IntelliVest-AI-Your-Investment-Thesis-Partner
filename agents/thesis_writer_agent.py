# agents/thesis_writer_agent.py

import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from utils.llm import call_groq_deepseek

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("Missing GOOGLE_API_KEY in .env")

genai.configure(api_key=GOOGLE_API_KEY)

class ThesisWriterAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def generate_thesis(self, content: str, sentiment: str, valuation: str, company_name: str) -> str:
        prompt = f"""
You are a professional investment analyst. Based on the following financial article markdown and insights,
generate a detailed and professional investment thesis.

Include:
1. **Summary of the Company and Market Tone**
2. **Sentiment Stance and Justification**
3. **Valuation Status with Key Metrics**
4. **Final Investment Recommendation** — Buy, Hold, Sell
5. **Mention whether it is a good time to invest, or not — and when would be better with reasoning.**

Company Name: {company_name}

--- Article Content ---
{content}

--- Sentiment Analysis ---
{sentiment}

--- Valuation Insight ---
{valuation}

Respond in markdown format.
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
                return f"❌ Failed to generate thesis: {fallback_error}"


# ✅ Quick test
if __name__ == "__main__":
    async def test():
        dummy_content = "Nvidia reported record earnings driven by strong demand for its GPUs across AI and data centers."
        dummy_sentiment = "**Sentiment:** Positive\nNvidia's performance exceeded expectations with record-breaking growth in the AI sector."
        dummy_valuation = "**Valuation:** Fairly Valued\nNvidia's P/E is high, but justified by its aggressive growth and dominant AI positioning."
        agent = ThesisWriterAgent()
        thesis = await agent.generate_thesis(
            content=dummy_content,
            sentiment=dummy_sentiment,
            valuation=dummy_valuation,
            company_name="Nvidia"
        )
        print(thesis)

    asyncio.run(test())
