# utils/search.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise EnvironmentError("Missing TAVILY_API_KEY in .env file")

def search_company_news(company: str, max_results: int = 5) -> list:
    """
    Uses Tavily API to search for recent and relevant news articles about a company.
    Returns a list of article URLs.
    """
    url = "https://api.tavily.com/search"

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": f"{company} stock financial news earnings report site:cnbc.com OR site:reuters.com OR site:bloomberg.com OR site:investor.{company.lower().replace(' ', '')}.com",
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return [item["url"] for item in data.get("results", [])]
    except Exception as e:
        print(f"❌ Tavily search failed: {e}")
        return []
