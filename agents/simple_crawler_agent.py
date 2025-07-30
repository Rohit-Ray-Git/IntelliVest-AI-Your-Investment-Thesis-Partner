# agents/simple_crawler_agent.py

import asyncio
import requests
from bs4 import BeautifulSoup
from crawl4ai.html2text import html2text
from tqdm import tqdm
import time


class SimpleCrawlerAgent:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    async def _fetch_and_extract(self, url: str):
        try:
            print(f"🔍 Crawling: {url}")
            
            # Add delay to be respectful
            await asyncio.sleep(1)
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse with BeautifulSoup first
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            html = str(soup)
            markdown = html2text(html)
            
            # Check if we got meaningful content
            if len(markdown.strip()) < 100:
                return {"url": url, "markdown": f"❌ Error: Insufficient content extracted (only {len(markdown.strip())} characters)"}
            
            print(f"✅ Successfully extracted {len(markdown)} characters from {url}")
            return {"url": url, "markdown": markdown}
            
        except requests.RequestException as e:
            print(f"❌ Request error for {url}: {e}")
            return {"url": url, "markdown": f"❌ Error: Request failed - {e}"}
        except Exception as e:
            print(f"❌ Error crawling {url}: {e}")
            return {"url": url, "markdown": f"❌ Error: {e}"}

    async def crawl_multiple(self, urls):
        results = []
        
        # Create tasks for concurrent execution
        tasks = [self._fetch_and_extract(url) for url in urls]
        
        # Execute with progress bar
        for i, task in enumerate(tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="🔎 Scraping")):
            result = await task
            results.append(result)
        
        return results


# ✅ Standalone Test
if __name__ == "__main__":
    test_urls = [
        "https://www.nvidia.com/en-us/",
        "https://www.cnbc.com/quotes/NVDA"
    ]

    async def run_test():
        agent = SimpleCrawlerAgent()
        results = await agent.crawl_multiple(test_urls)
        for res in results:
            print("\n---")
            print(f"URL: {res['url']}\nMarkdown:\n{res['markdown'][:1000]}...")

    asyncio.run(run_test()) 