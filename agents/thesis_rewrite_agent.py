# agents/thesis_rewrite_agent.py

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

class ThesisRewriteAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def revise_thesis(self, thesis_markdown: str, critique: str, company_name: str) -> str:
        prompt = f"""
You are a senior investment advisor. Your task is to revise the following investment thesis based on the provided critique.

Company: {company_name}

--- Original Thesis ---
{thesis_markdown}

--- Critique Feedback ---
{critique}

Improve the structure, remove biases, include missing information, and make the recommendation sharper. Your output should be professional and in markdown format.
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
                return f"❌ Failed to revise thesis: {fallback_error}"
