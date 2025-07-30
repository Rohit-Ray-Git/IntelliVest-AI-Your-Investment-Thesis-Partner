# agents/sentiment_agent.py

import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from utils.llm import call_groq_deepseek  # fallback function

# --- Load .env and Configure Gemini ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found in .env or environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

class SentimentAgent:
    def __init__(self):
        self.template = """
You are a financial sentiment analysis expert.
Analyze the following financial report or article and classify the overall sentiment as:
1. Positive
2. Negative
3. Neutral

Also, provide a short justification.

Text:
"""

    async def analyze_sentiment(self, markdown_text: str) -> str:
        prompt = self.template + markdown_text

        try:
            # Attempt Gemini
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = await asyncio.to_thread(model.generate_content, prompt)
            return response.text.strip()

        except Exception as e:
            print("[Gemini Failed] Falling back to Groq. Reason:", str(e))
            try:
                # Fallback to Groq LLM
                return call_groq_deepseek(prompt).strip()
            except Exception as e2:
                return f"[Error]: {str(e2)}"

# ----------------- Test -------------------

async def test():
    agent = SentimentAgent()
    dummy_md = """
Example Co. reported a 30% increase in Q2 earnings compared to last year, exceeding analyst expectations. Revenue growth was driven by strong demand in the AI sector.
"""
    result = await agent.analyze_sentiment(dummy_md)
    print("\n[Sentiment Result]\n", result)

if __name__ == "__main__":
    asyncio.run(test())
