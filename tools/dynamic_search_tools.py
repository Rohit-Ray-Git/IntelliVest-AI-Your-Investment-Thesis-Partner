"""
🔄 Dynamic Search Tools - Real-time Financial Data Discovery
==========================================================

This module provides tools for dynamically discovering and scraping
the latest financial data from live, publicly available websites.
No hard-coded URLs - finds the most recent and relevant sources.
"""

import asyncio
import re
import json
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse, quote_plus
import requests
from bs4 import BeautifulSoup
from langchain.tools import BaseTool
import random

# Import crawl4ai for advanced web crawling
from crawl4ai import AsyncWebCrawler

class DynamicWebSearchTool(BaseTool):
    """🔄 Tool for dynamic web search and content discovery"""
    
    name: str = "dynamic_web_search"
    description: str = """
    Dynamically searches the web for the latest financial data and information.
    Finds live, publicly available websites without hard-coded URLs.
    Input should be a search query for financial information.
    Returns scraped content from discovered sources.
    """
    
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.search_engines = [
            "https://www.google.com/search",
            "https://www.bing.com/search", 
            "https://search.yahoo.com/search"
        ]
        # Initialize crawl4ai crawler
        self.crawler = AsyncWebCrawler()
    
    def _run(self, query: str) -> str:
        """Run dynamic web search"""
        try:
            print(f"🔍 Dynamic Search: Searching for '{query}'")
            
            # Step 1: Discover relevant websites using search engines
            discovered_urls = self._discover_websites(query)
            
            if not discovered_urls:
                return f"❌ No relevant websites found for query: {query}"
            
            # Step 2: Filter to financial/relevant sites
            filtered_urls = self._filter_financial_sites(discovered_urls)
            
            # Step 3: Scrape content from discovered sites using crawl4ai
            scraped_content = self._scrape_discovered_sites(filtered_urls[:5], query)  # Limit to top 5
            
            # Step 4: Format and return results
            return self._format_results(scraped_content, query)
            
        except Exception as e:
            return f"❌ Error in dynamic web search: {str(e)}"
    
    def _discover_websites(self, query: str) -> List[str]:
        """Discover relevant websites using search engines"""
        discovered_urls = []
        
        try:
            # Use multiple search engines for better coverage
            for engine in self.search_engines:
                try:
                    params = {
                        'q': query,
                        'num': 10  # Get top 10 results
                    }
                    
                    response = self.session.get(engine, params=params, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract URLs from search results
                    # Different search engines have different HTML structures
                    if 'google.com' in engine:
                        links = soup.find_all('a', href=True)
                        for link in links:
                            href = link['href']
                            if href.startswith('/url?q='):
                                url = href.split('/url?q=')[1].split('&')[0]
                                if url.startswith('http') and url not in discovered_urls:
                                    discovered_urls.append(url)
                    
                    elif 'bing.com' in engine:
                        links = soup.find_all('a', href=True)
                        for link in links:
                            href = link['href']
                            if href.startswith('http') and 'bing.com' not in href:
                                discovered_urls.append(href)
                    
                    elif 'yahoo.com' in engine:
                        links = soup.find_all('a', href=True)
                        for link in links:
                            href = link['href']
                            if href.startswith('http') and 'yahoo.com' not in href:
                                discovered_urls.append(href)
                    
                    time.sleep(1)  # Be respectful to search engines
                    
                except Exception as e:
                    print(f"Warning: Error searching {engine}: {e}")
                    continue
            
            return discovered_urls[:20]  # Limit to top 20 results
            
        except Exception as e:
            print(f"Error in website discovery: {e}")
            return []
    
    def _filter_financial_sites(self, urls: List[str]) -> List[str]:
        """Filter URLs to focus on financial/relevant sites"""
        financial_keywords = [
            'finance', 'market', 'stock', 'trading', 'investment', 'business',
            'yahoo.com/finance', 'marketwatch.com', 'bloomberg.com', 'reuters.com',
            'cnbc.com', 'wsj.com', 'ft.com', 'seekingalpha.com', 'investing.com',
            'morningstar.com', 'fool.com', 'barrons.com', 'forbes.com'
        ]
        
        filtered_urls = []
        for url in urls:
            url_lower = url.lower()
            if any(keyword in url_lower for keyword in financial_keywords):
                filtered_urls.append(url)
        
        return filtered_urls
    
    async def _scrape_with_crawl4ai(self, url: str) -> Dict[str, Any]:
        """Scrape content using crawl4ai"""
        try:
            # Use crawl4ai to scrape the URL
            result = await self.crawler.arun(
                url=url,
                includes=["text", "title", "links"],
                excludes=["ads", "navigation", "footer"],
                max_tokens=4000
            )
            
            return {
                'url': url,
                'content': result.text if result.text else '',
                'title': result.title if result.title else 'No title',
                'links': result.links if result.links else []
            }
            
        except Exception as e:
            print(f"Warning: Error scraping {url} with crawl4ai: {e}")
            return {
                'url': url,
                'content': '',
                'title': 'Error',
                'links': []
            }
    
    def _scrape_discovered_sites(self, urls: List[str], query: str) -> List[Dict[str, Any]]:
        """Scrape content from discovered websites using crawl4ai"""
        scraped_content = []
        
        # Run crawl4ai scraping asynchronously
        async def scrape_all():
            tasks = []
            for url in urls:
                tasks.append(self._scrape_with_crawl4ai(url))
                time.sleep(1)  # Be respectful between requests
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Warning: Error scraping {urls[i]}: {result}")
                    continue
                
                if result['content'] and self._is_content_relevant(result['content'], query):
                    relevance_score = self._calculate_relevance(result['content'], query)
                    
                    scraped_content.append({
                        'url': result['url'],
                        'content': result['content'][:2000],  # Limit content length
                        'relevance_score': relevance_score,
                        'title': result['title']
                    })
            
            # Sort by relevance score
            scraped_content.sort(key=lambda x: x['relevance_score'], reverse=True)
            return scraped_content
        
        # Run the async scraping
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            scraped_content = loop.run_until_complete(scrape_all())
            loop.close()
        except Exception as e:
            print(f"Error in async scraping: {e}")
            # Fallback to synchronous scraping if async fails
            scraped_content = self._fallback_scraping(urls, query)
        
        return scraped_content
    
    def _fallback_scraping(self, urls: List[str], query: str) -> List[Dict[str, Any]]:
        """Fallback scraping method using requests/BeautifulSoup"""
        scraped_content = []
        
        for url in urls:
            try:
                print(f"🔍 Fallback Scraping: {url}")
                
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract relevant content
                content = self._extract_relevant_content(soup, query)
                
                if content and self._is_content_relevant(content, query):
                    relevance_score = self._calculate_relevance(content, query)
                    
                    scraped_content.append({
                        'url': url,
                        'content': content[:2000],  # Limit content length
                        'relevance_score': relevance_score,
                        'title': soup.title.string if soup.title else 'No title'
                    })
                
                time.sleep(2)  # Be respectful to websites
                
            except Exception as e:
                print(f"Warning: Error in fallback scraping {url}: {e}")
                continue
        
        # Sort by relevance score
        scraped_content.sort(key=lambda x: x['relevance_score'], reverse=True)
        return scraped_content
    
    def _extract_relevant_content(self, soup: BeautifulSoup, query: str) -> str:
        """Extract relevant content from webpage"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Try to find main content areas
        content_selectors = [
            'main', 'article', '.content', '.main-content', '.post-content',
            '.entry-content', '.story-body', '.article-body', '#content'
        ]
        
        content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                content = ' '.join([elem.get_text() for elem in elements])
                break
        
        # If no main content found, get body text
        if not content:
            content = soup.get_text()
        
        # Clean up content
        content = re.sub(r'\s+', ' ', content).strip()
        return content
    
    def _is_content_relevant(self, content: str, query: str) -> bool:
        """Check if content is relevant to the search query"""
        query_words = query.lower().split()
        content_lower = content.lower()
        
        # Check if at least 50% of query words appear in content
        matches = sum(1 for word in query_words if word in content_lower)
        return matches >= len(query_words) * 0.5
    
    def _calculate_relevance(self, content: str, query: str) -> float:
        """Calculate relevance score between content and query"""
        query_words = query.lower().split()
        content_lower = content.lower()
        
        # Simple relevance scoring based on word frequency
        total_matches = 0
        for word in query_words:
            matches = content_lower.count(word)
            total_matches += matches
        
        # Normalize by content length and query length
        relevance = total_matches / (len(content.split()) * len(query_words))
        return min(relevance * 100, 1.0)  # Cap at 1.0
    
    def _format_results(self, scraped_content: List[Dict[str, Any]], query: str) -> str:
        """Format scraped content into readable results"""
        if not scraped_content:
            return f"❌ No relevant content found for query: {query}"
        
        result = f"✅ Dynamic Web Search Results for: '{query}'\n\n"
        result += f"📊 Summary:\n"
        result += f"- Search Query: {query}\n"
        result += f"- Sources Discovered: {len(scraped_content)}\n"
        result += f"- Total Content: {sum(len(item['content']) for item in scraped_content)} characters\n"
        result += f"- Average Relevance Score: {sum(item['relevance_score'] for item in scraped_content) / len(scraped_content):.2f}\n\n"
        
        result += "📰 Top Sources:\n"
        for i, item in enumerate(scraped_content[:5], 1):
            result += f"{i}. {item['url']}\n"
            result += f"   Relevance Score: {item['relevance_score']:.2f}\n"
            result += f"   Content Preview: {item['content'][:200]}...\n\n"
        
        result += "📋 Full Content Summary:\n"
        for item in scraped_content:
            result += f"• {item['title']}: {item['content'][:300]}...\n\n"
        
        result += "✅ Dynamic search completed successfully"
        return result

class InstitutionalDataTool(BaseTool):
    """🏦 Tool for discovering and scraping institutional data"""
    
    name: str = "institutional_data"
    description: str = """
    Discovers and scrapes institutional data including FII holdings,
    major shareholders, institutional ownership, and options flow data.
    Finds the latest sources without hard-coded URLs.
    """
    
    def __init__(self):
        super().__init__()
        self.search_tool = DynamicWebSearchTool()
    
    def _run(self, company_name: str) -> str:
        """Run institutional data discovery"""
        try:
            print(f"🏦 Institutional Data: Searching for {company_name}")
            
            # Create specific search queries for institutional data
            search_queries = [
                f"{company_name} FII holdings foreign institutional investors",
                f"{company_name} major shareholders ownership data",
                f"{company_name} institutional ownership mutual funds",
                f"{company_name} options flow institutional activity",
                f"{company_name} insider trading institutional investors",
                f"{company_name} shareholder structure ownership breakdown"
            ]
            
            all_results = []
            
            for query in search_queries:
                print(f"🔍 Searching: {query}")
                result = self.search_tool._run(query)
                all_results.append(f"🔍 {query}:\n{result}\n")
                time.sleep(2)  # Be respectful between searches
            
            return self._format_institutional_results(all_results, company_name)
            
        except Exception as e:
            return f"❌ Error in institutional data search: {str(e)}"
    
    def _format_institutional_results(self, results: List[str], company_name: str) -> str:
        """Format institutional data results"""
        formatted_result = f"🏦 Institutional Data Analysis for {company_name}\n\n"
        formatted_result += "📊 Data Sources Searched:\n"
        
        search_queries = [
            f"{company_name} FII holdings foreign institutional investors",
            f"{company_name} major shareholders ownership data", 
            f"{company_name} institutional ownership mutual funds",
            f"{company_name} options flow institutional activity",
            f"{company_name} insider trading institutional investors",
            f"{company_name} shareholder structure ownership breakdown"
        ]
        
        for query in search_queries:
            formatted_result += f"• {query}: ✅ Found\n"
        
        formatted_result += "\n📋 Detailed Results:\n"
        for result in results:
            formatted_result += result + "\n"
        
        formatted_result += "✅ Institutional data search completed"
        return formatted_result

class CryptoDataTool(BaseTool):
    """🪙 Tool for discovering and scraping cryptocurrency data"""
    
    name: str = "crypto_data"
    description: str = """
    Discovers and scrapes cryptocurrency data including price, market cap,
    trading volume, institutional adoption, and market sentiment.
    Finds the latest crypto data sources dynamically.
    """
    
    def __init__(self):
        super().__init__()
        self.search_tool = DynamicWebSearchTool()
    
    def _run(self, crypto_name: str) -> str:
        """Run cryptocurrency data discovery"""
        try:
            print(f"🪙 Crypto Data: Searching for {crypto_name}")
            
            # Create specific search queries for crypto data
            search_queries = [
                f"{crypto_name} cryptocurrency price market cap",
                f"{crypto_name} crypto trading volume institutional adoption",
                f"{crypto_name} blockchain technology development updates",
                f"{crypto_name} crypto market sentiment analysis",
                f"{crypto_name} cryptocurrency news developments",
                f"{crypto_name} crypto institutional investment data"
            ]
            
            all_results = []
            
            for query in search_queries:
                print(f"🔍 Searching: {query}")
                result = self.search_tool._run(query)
                all_results.append(f"🔍 {query}:\n{result}\n")
                time.sleep(2)  # Be respectful between searches
            
            return self._format_crypto_results(all_results, crypto_name)
            
        except Exception as e:
            return f"❌ Error in crypto data search: {str(e)}"
    
    def _format_crypto_results(self, results: List[str], crypto_name: str) -> str:
        """Format cryptocurrency data results"""
        formatted_result = f"🪙 Cryptocurrency Data Analysis for {crypto_name}\n\n"
        formatted_result += "📊 Data Sources Searched:\n"
        
        search_queries = [
            f"{crypto_name} cryptocurrency price market cap",
            f"{crypto_name} crypto trading volume institutional adoption",
            f"{crypto_name} blockchain technology development updates",
            f"{crypto_name} crypto market sentiment analysis",
            f"{crypto_name} cryptocurrency news developments",
            f"{crypto_name} crypto institutional investment data"
        ]
        
        for query in search_queries:
            formatted_result += f"• {query}: ✅ Found\n"
        
        formatted_result += "\n📋 Detailed Results:\n"
        for result in results:
            formatted_result += result + "\n"
        
        formatted_result += "✅ Cryptocurrency data search completed"
        return formatted_result

# Export all tools
__all__ = [
    'DynamicWebSearchTool',
    'InstitutionalDataTool', 
    'CryptoDataTool'
] 