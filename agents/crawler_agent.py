# agents/crawler_agent.py

import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode

class CrawlerAgent:
    def __init__(self):
        # Browser settings (headless by default)
        self.browser_config = BrowserConfig(headless=True)
        self.run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS  # ensure fresh content
        )

    async def crawl_and_extract(self, url: str):
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=self.run_config
            )
            return {
                "url": result.url,
                "markdown": result.markdown
            }

    async def crawl_multiple(self, urls: list[str]):
        docs = []
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            for url in urls:
                try:
                    res = await crawler.arun(url=url, config=self.run_config)
                    docs.append({"url": res.url, "markdown": res.markdown})
                except Exception as e:
                    print(f"❌ Error crawling {url}: {e}")
        return docs

# 🧪 Test run
if __name__ == "__main__":
    async def test():
        agent = CrawlerAgent()
        test_urls = [
            "https://www.cnbc.com/2025/07/earnings-report-example-company.html",
            "https://finance.example.com/investment-thesis-sample"  # This will fail
        ]
        docs = await agent.crawl_multiple(test_urls)
        for doc in docs:
            if doc and doc.get("markdown"):
                print(f"\n📰 URL: {doc['url']}\n--- Markdown Preview ---\n{doc['markdown'][:500]}...\n")
            else:
                print(f"\n⚠️ Skipped invalid document: {doc}")
    
    asyncio.run(test())

