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

    async def revise_thesis(self, *, thesis_markdown: str, critique: str, company_name: str) -> str:
        prompt = f"""
You are an experienced investment thesis analyst.

Revise the following investment thesis to address the issues highlighted in the critique while preserving the professional tone, core ideas, and formatting.

Include the following in the improved version:
1. Fix factual inconsistencies (e.g. pricing, ratios).
2. Add missing valuation metrics if feasible.
3. Strengthen or clarify weak reasoning.
4. Keep markdown structure clean and readable.
5. Ensure the company name "{company_name}" is accurately used throughout.

--- Original Investment Thesis ---
{thesis_markdown}

--- Critique and Recommendations ---
{critique}

Respond with the complete revised thesis in markdown.
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


# ✅ Quick test
if __name__ == "__main__":
    async def test():
        dummy_thesis = "## Thesis\nBuy Apple stock because it's awesome."
        dummy_critique = "- Add valuation data\n- Include P/E ratio\n- Tone down optimism"
        agent = ThesisRewriteAgent()
        revised = await agent.revise_thesis(
            thesis_markdown=dummy_thesis,
            critique=dummy_critique,
            company_name="Apple"
        )
        print(revised)

    asyncio.run(test())
