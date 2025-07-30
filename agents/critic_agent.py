# agents/critic_agent.py

import asyncio
from utils.ai_client import ai_client

class CriticAgent:
    def __init__(self):
        pass

    async def critique_thesis(self, thesis_markdown: str, company_name: str) -> str:
        """Critique the investment thesis for potential biases and gaps"""
        
        prompt = f"""
        Critically analyze the following investment thesis for {company_name} and identify potential issues, biases, or gaps in the analysis.
        
        **Investment Thesis:**
        {thesis_markdown}
        
        Provide a constructive critique that includes:
        1. Potential biases in the analysis
        2. Missing information or data gaps
        3. Alternative viewpoints or counter-arguments
        4. Assumptions that may be questionable
        5. Areas where the analysis could be strengthened
        6. Risk factors that may have been overlooked
        
        Be objective and constructive in your critique. Focus on improving the quality and robustness of the investment thesis.
        """
        
        messages = [
            {"role": "system", "content": "You are a senior investment analyst specializing in critical analysis and risk assessment of investment theses."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            result = await ai_client.get_completion(messages, max_tokens=2000)
            return result
        except Exception as e:
            print(f"❌ Thesis critique failed: {e}")
            return "Thesis critique could not be completed due to technical issues. Please try again later."


# ✅ Standalone test
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
        result = await agent.critique_thesis(dummy_thesis, company_name="Example Inc.")
        print("\n🧠 [Critique Output]\n", result)

    asyncio.run(test())
