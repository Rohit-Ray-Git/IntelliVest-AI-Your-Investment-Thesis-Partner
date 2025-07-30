# agents/crawler_agent.py

import asyncio
import aiohttp
from crawl4ai.html2text import html2text
from tqdm import tqdm

class CrawlerAgent:
    def __init__(self):
        self.session = None
        
    async def _init_session(self):
        """Initialize aiohttp session"""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
            
    async def _fetch_and_extract(self, url: str):
        """Fetch HTML and extract markdown using crawl4ai"""
        try:
            print(f"🔍 Crawling: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            async with self.session.get(url, headers=headers, allow_redirects=True) as response:
                if response.status != 200:
                    return {"url": url, "markdown": f"❌ Error: HTTP {response.status}"}
                
                html = await response.text()
                
                # Use crawl4ai to convert HTML to markdown
                markdown = html2text(html)
                
                # Check if we got meaningful content
                if len(markdown.strip()) < 100:  # Less than 100 characters
                    return {"url": url, "markdown": f"❌ Error: Insufficient content extracted (only {len(markdown.strip())} characters)"}
                
                print(f"✅ Successfully extracted {len(markdown)} characters from {url}")
                return {"url": url, "markdown": markdown}
                
        except Exception as e:
            print(f"❌ Error crawling {url}: {e}")
            return {"url": url, "markdown": f"❌ Error: {e}"}

    async def crawl_multiple(self, urls):
        """Crawl multiple URLs using crawl4ai"""
        results = []
        
        try:
            await self._init_session()
            
            for url in tqdm(urls, desc="🔎 Scraping"):
                result = await self._fetch_and_extract(url)
                results.append(result)
                
        except Exception as e:
            print(f"❌ Error in crawler: {e}")
            # Return error results for all URLs
            return [{"url": url, "markdown": f"❌ Error: Crawler failed - {e}"} for url in urls]
        finally:
            if self.session:
                await self.session.close()
                self.session = None

        return results

# ✅ Standalone Test
if __name__ == "__main__":
    test_urls = [
        "https://www.nvidia.com/en-us/",
        "https://www.cnbc.com/quotes/NVDA"
    ]

    async def run_test():
        agent = CrawlerAgent()
        results = await agent.crawl_multiple(test_urls)
        for res in results:
            print("\n---")
            print(f"URL: {res['url']}")
            print(f"Markdown length: {len(res['markdown'])}")
            print(f"Markdown preview:\n{res['markdown'][:500]}...")

    asyncio.run(run_test())
