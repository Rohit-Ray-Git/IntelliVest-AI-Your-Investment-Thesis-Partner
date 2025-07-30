# utils/search.py

import os
import requests
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise EnvironmentError("Missing TAVILY_API_KEY in .env")

client = TavilyClient(api_key=TAVILY_API_KEY)

def is_live_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def search_company_news(company_name: str, max_results: int = 15):
    print(f"🔍 Searching Tavily for latest news on '{company_name}'...")

    try:
        results = client.search(
            query=f"{company_name} latest news stock financial earnings report",
            search_depth="advanced",
            max_results=max_results
        )
    except Exception as e:
        print(f"❌ Tavily search error: {e}")
        return []

    urls = [r["url"] for r in results.get("results", [])]
    live_urls = [url for url in urls if is_live_url(url)]

    print(f"✅ Found {len(live_urls)} live URLs.")
    return live_urls[:10]  # Return top 10 live articles
