# main.py

import asyncio
from agents.crawler_agent import fetch_articles
from agents.sentiment_agent import SentimentAgent
from agents.valuation_agent import ValuationAgent
from agents.thesis_writer_agent import ThesisWriterAgent
from agents.critic_agent import CriticAgent


async def main():
    print("\n🚀 Starting IntelliVest AI Investment Thesis Pipeline...")

    # Step 1: Crawl a URL
    url = "https://www.cnbc.com/2025/07/earnings-report-example-company.html"  # Change as needed
    print(f"\n🌐 Crawling URL: {url}")
    articles = await fetch_articles([url])
    if not articles or articles[0] is None:
        print("❌ Failed to fetch article.")
        return
    markdown = articles[0]["markdown"]

    # Step 2: Sentiment Analysis
    print("\n🧠 Running Sentiment Analysis...")
    sentiment_agent = SentimentAgent()
    sentiment_result = await sentiment_agent.analyze_sentiment(markdown)

    # Step 3: Valuation
    print("\n💸 Running Valuation...")
    valuation_agent = ValuationAgent()
    valuation_result = await valuation_agent.estimate_valuation(markdown)

    # Step 4: Generate Investment Thesis
    print("\n📄 Generating Investment Thesis...")
    thesis_agent = ThesisWriterAgent()
    thesis = await thesis_agent.generate_thesis(markdown, sentiment_result, valuation_result)

    # Step 5: Critique the Thesis
    print("\n🧐 Running Thesis Critique...")
    critic = CriticAgent()
    critique = await critic.critique_thesis(thesis)

    # Final Output
    print("\n✅ Pipeline Complete.")
    print("\n--- Investment Thesis ---\n")
    print(thesis)
    print("\n--- Critique ---\n")
    print(critique)


if __name__ == "__main__":
    asyncio.run(main())
