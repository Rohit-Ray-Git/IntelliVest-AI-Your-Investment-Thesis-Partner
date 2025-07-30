# agents/sentiment_agent.py

import asyncio
from utils.ai_client import ai_client

class SentimentAgent:
    def __init__(self):
        pass

    async def analyze_sentiment(self, content: str) -> str:
        """Analyze sentiment of the given content"""
        
        prompt = f"""
        Analyze the sentiment of the following content about a company. 
        Focus on financial news, earnings reports, market reactions, and business developments.
        
        Content: {content[:8000]}  # Limit content length to avoid token limits
        
        Provide a sentiment analysis with:
        1. Overall sentiment (Positive/Negative/Neutral)
        2. Key factors influencing the sentiment
        3. Confidence level in the analysis
        4. Notable events or news that shaped the sentiment
        
        Format your response as a clear, structured analysis.
        """
        
        messages = [
            {"role": "system", "content": "You are a financial analyst specializing in sentiment analysis of company news and market data."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            result = await ai_client.get_completion(messages, max_tokens=2000)
            return result
        except Exception as e:
            print(f"❌ Sentiment analysis failed: {e}")
            return "Sentiment analysis could not be completed due to technical issues. Please try again later."

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
