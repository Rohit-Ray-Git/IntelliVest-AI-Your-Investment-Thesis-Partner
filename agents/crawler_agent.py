# agents/crawler_agent.py

import asyncio
from playwright.async_api import async_playwright
from crawl4ai.html2text import html2text
from tqdm import tqdm


class CrawlerAgent:
    def __init__(self):
        pass

    async def _fetch_and_extract(self, page, url: str):
        try:
            print(f"🔍 Crawling: {url}")
            await page.goto(url, timeout=30000)
            await page.wait_for_load_state("load")
            html = await page.content()
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
        results = []
        try:
            async with async_playwright() as playwright:
                # Try different browser options for better compatibility
                try:
                    browser = await playwright.chromium.launch(
                        headless=True,
                        args=['--no-sandbox', '--disable-dev-shm-usage']
                    )
                except Exception as e:
                    print(f"❌ Chromium launch failed: {e}")
                    # Fallback to firefox if chromium fails
                    try:
                        browser = await playwright.firefox.launch(headless=True)
                    except Exception as e2:
                        print(f"❌ Firefox launch also failed: {e2}")
                        # Return error results for all URLs
                        return [{"url": url, "markdown": f"❌ Error: Browser initialization failed - {e}"} for url in urls]
                
                context = await browser.new_context()
                page = await context.new_page()

                for url in tqdm(urls, desc="🔎 Scraping"):
                    result = await self._fetch_and_extract(page, url)
                    results.append(result)

                await browser.close()
        except Exception as e:
            print(f"❌ Error initializing crawler: {e}")
            # Return error results if browser fails to initialize
            return [{"url": url, "markdown": f"❌ Error: Browser initialization failed - {e}"} for url in urls]

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
            print(f"URL: {res['url']}\nMarkdown:\n{res['markdown'][:1000]}...")

    asyncio.run(run_test())
