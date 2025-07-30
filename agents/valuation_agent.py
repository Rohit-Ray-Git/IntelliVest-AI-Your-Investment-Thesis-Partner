# agents/valuation_agent.py

import asyncio
from utils.ai_client import ai_client

class ValuationAgent:
    def __init__(self):
        pass

    async def estimate_valuation(self, content: str) -> str:
        """Estimate company valuation based on content"""
        
        prompt = f"""
        Analyze the following content and provide a comprehensive valuation assessment for the company.
        Focus on financial metrics, market position, growth prospects, and industry trends.
        
        Content: {content[:8000]}  # Limit content length to avoid token limits
        
        Provide a valuation analysis with:
        1. Key financial metrics mentioned
        2. Market position and competitive advantages
        3. Growth prospects and risks
        4. Valuation methodology considerations
        5. Key factors affecting valuation
        
        Format your response as a structured analysis with clear sections.
        """
        
        messages = [
            {"role": "system", "content": "You are a financial analyst specializing in company valuation and financial analysis."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            result = await ai_client.get_completion(messages, max_tokens=2000)
            return result
        except Exception as e:
            print(f"❌ Valuation analysis failed: {e}")
            return "Valuation analysis could not be completed due to technical issues. Please try again later."


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
