# main.py

import asyncio
from agents.crawler_agent import CrawlerAgent
from agents.sentiment_agent import SentimentAgent
from agents.valuation_agent import ValuationAgent
from agents.thesis_writer_agent import ThesisWriterAgent
from agents.critic_agent import CriticAgent
from utils.search import search_company_news

print("🚀 IntelliVest AI — Investment Thesis Generator")

async def main():
    company = input("\n📌 Enter company or stock name to research: ").strip()

    print(f"\n🔍 Searching news for: {company}")
    urls = search_company_news(company)

    if not urls:
        print("❌ No results found. Please try a different company name.")
        return

    print("\n🌐 Crawling and extracting articles...")
    crawler = CrawlerAgent()
    documents = await crawler.crawl_multiple(urls)

    combined_md = "\n\n".join([doc["markdown"] for doc in documents if doc.get("markdown")])

    if not combined_md.strip():
        print("❌ Unable to extract valid article content. Try different sources.")
        return

    print("\n🧠 Running Sentiment Analysis...")
    sentiment_agent = SentimentAgent()
    sentiment = await sentiment_agent.analyze_sentiment(combined_md)

    print("\n💸 Running Valuation...")
    valuation_agent = ValuationAgent()
    valuation = await valuation_agent.estimate_valuation(combined_md)

    print("\n📄 Generating Investment Thesis...")
    thesis_agent = ThesisWriterAgent()
    thesis = await thesis_agent.generate_thesis(
        content=combined_md,
        sentiment=sentiment,
        valuation=valuation,
        company_name=company  # corrected keyword
    )

    print("\n🧐 Running Thesis Critique...")
    critic_agent = CriticAgent()
    critique = await critic_agent.critique_thesis(thesis)

    print("\n✅ Pipeline Complete.")
    print("\n--- Investment Thesis ---\n")
    print(thesis)

    print("\n--- Critique ---\n")
    print(critique)

if __name__ == "__main__":
    asyncio.run(main())
