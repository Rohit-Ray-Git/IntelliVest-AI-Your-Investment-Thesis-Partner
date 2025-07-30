# agents/thesis_writer_agent.py

import asyncio
from utils.ai_client import ai_client

class ThesisWriterAgent:
    def __init__(self):
        pass

    async def generate_thesis(self, content: str, sentiment: str, valuation: str, company_name: str) -> str:
        """Generate investment thesis based on content, sentiment, and valuation"""
        
        prompt = f"""
        Generate a comprehensive investment thesis for {company_name} based on the following information:
        
        **Company Content Analysis:**
        {content[:6000]}
        
        **Sentiment Analysis:**
        {sentiment}
        
        **Valuation Analysis:**
        {valuation}
        
        Create a professional investment thesis that includes:
        1. Executive Summary
        2. Company Overview
        3. Investment Thesis (Bull/Bear case)
        4. Key Investment Drivers
        5. Risk Factors
        6. Valuation Summary
        7. Investment Recommendation
        
        Format your response in clear markdown with proper headings and structure.
        Be objective and data-driven in your analysis.
        """
        
        messages = [
            {"role": "system", "content": "You are a senior investment analyst with expertise in equity research and investment thesis development."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            result = await ai_client.get_completion(messages, max_tokens=3000)
            return result
        except Exception as e:
            print(f"❌ Thesis generation failed: {e}")
            return "Investment thesis could not be generated due to technical issues. Please try again later."


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
