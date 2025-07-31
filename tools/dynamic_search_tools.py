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
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from langchain.tools import BaseTool

# Import crawling functionality
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
        self.search_engines = [
            "https://www.google.com/search",
            "https://www.bing.com/search",
            "https://search.yahoo.com/search"
        ]
        self.crawler = AsyncWebCrawler()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _run(self, query: str) -> str:
        """Run dynamic web search"""
        try:
            print(f"🔍 Dynamic Search: Searching for '{query}'")
            
            # 1. Discover relevant websites
            discovered_urls = self._discover_websites(query)
            
            if not discovered_urls:
                return "❌ No relevant websites discovered"
            
            # 2. Filter for financial/relevant sites
            financial_urls = self._filter_financial_sites(discovered_urls)
            
            if not financial_urls:
                return "❌ No financial websites found"
            
            # 3. Scrape content from discovered sites
            scraped_content = self._scrape_discovered_sites(financial_urls, query)
            
            if not scraped_content:
                return "❌ No content could be scraped from discovered sites"
            
            # 4. Format and return results
            return self._format_results(scraped_content, query)
            
        except Exception as e:
            return f"❌ Error in dynamic web search: {str(e)}"
    
    def _discover_websites(self, query: str) -> List[str]:
        """Discover relevant websites using search engines"""
        discovered_urls = []
        
        try:
            # Use multiple search engines for better discovery
            for search_engine in self.search_engines:
                try:
                    # Create search URL
                    if "google" in search_engine:
                        search_url = f"{search_engine}?q={query.replace(' ', '+')}&num=10"
                    elif "bing" in search_engine:
                        search_url = f"{search_engine}?q={query.replace(' ', '+')}&count=10"
                    else:
                        search_url = f"{search_engine}?p={query.replace(' ', '+')}&n=10"
                    
                    # Get search results
                    response = self.session.get(search_url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Extract URLs from search results
                        if "google" in search_engine:
                            links = soup.find_all('a', href=True)
                            for link in links:
                                href = link['href']
                                if href.startswith('/url?q='):
                                    url = href.split('/url?q=')[1].split('&')[0]
                                    if url.startswith('http'):
                                        discovered_urls.append(url)
                        elif "bing" in search_engine:
                            links = soup.find_all('a', href=True)
                            for link in links:
                                href = link['href']
                                if href.startswith('http') and 'bing.com' not in href:
                                    discovered_urls.append(href)
                        else:
                            # Generic extraction
                            links = soup.find_all('a', href=True)
                            for link in links:
                                href = link['href']
                                if href.startswith('http'):
                                    discovered_urls.append(href)
                    
                    time.sleep(1)  # Be respectful to search engines
                    
                except Exception as e:
                    print(f"⚠️ Error with {search_engine}: {e}")
                    continue
            
            # Remove duplicates and limit results
            discovered_urls = list(set(discovered_urls))[:20]
            print(f"✅ Discovered {len(discovered_urls)} potential websites")
            
            return discovered_urls
            
        except Exception as e:
            print(f"❌ Error discovering websites: {e}")
            return []
    
    def _filter_financial_sites(self, urls: List[str]) -> List[str]:
        """Filter URLs to focus on financial/relevant sites"""
        financial_keywords = [
            'finance', 'financial', 'investing', 'investment', 'stock', 'market',
            'trading', 'portfolio', 'wealth', 'money', 'business', 'economy',
            'earnings', 'revenue', 'profit', 'growth', 'analysis', 'research',
            'news', 'media', 'press', 'announcement', 'report', 'filing',
            'sec.gov', 'yahoo.com/finance', 'marketwatch.com', 'bloomberg.com',
            'reuters.com', 'cnbc.com', 'wsj.com', 'ft.com', 'economist.com',
            'forbes.com', 'fortune.com', 'businessinsider.com', 'seekingalpha.com',
            'motleyfool.com', 'fool.com', 'investopedia.com', 'marketbeat.com',
            'zacks.com', 'tipranks.com', 'finviz.com', 'stocktwits.com'
        ]
        
        filtered_urls = []
        
        for url in urls:
            url_lower = url.lower()
            
            # Check if URL contains financial keywords
            is_financial = any(keyword in url_lower for keyword in financial_keywords)
            
            # Check if it's a news/media site
            is_news = any(domain in url_lower for domain in [
                'news', 'media', 'press', 'reuters', 'bloomberg', 'cnbc', 'wsj'
            ])
            
            # Check if it's a business site
            is_business = any(domain in url_lower for domain in [
                'business', 'company', 'corporate', 'investor', 'ir.'
            ])
            
            if is_financial or is_news or is_business:
                filtered_urls.append(url)
        
        print(f"✅ Filtered to {len(filtered_urls)} financial/relevant sites")
        return filtered_urls
    
    def _scrape_discovered_sites(self, urls: List[str], query: str) -> List[Dict[str, Any]]:
        """Scrape content from discovered websites"""
        scraped_content = []
        
        for url in urls[:10]:  # Limit to top 10 sites
            try:
                print(f"🕷️ Scraping: {url}")
                
                # Use Crawl4AI for scraping
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    result = loop.run_until_complete(self.crawler.arun(url))
                    loop.close()
                    
                    if result and result.get('markdown'):
                        content = result['markdown']
                        
                        # Check if content is relevant to the query
                        if self._is_content_relevant(content, query):
                            scraped_content.append({
                                'url': url,
                                'content': content[:5000],  # Limit content size
                                'relevance_score': self._calculate_relevance(content, query)
                            })
                            print(f"✅ Relevant content found: {len(content)} characters")
                        else:
                            print(f"⚠️ Content not relevant to query")
                    
                except Exception as e:
                    loop.close()
                    print(f"⚠️ Crawl4AI failed for {url}: {e}")
                    
                    # Fallback to simple requests
                    try:
                        response = self.session.get(url, timeout=10)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, 'html.parser')
                            
                            # Extract text content
                            text_content = soup.get_text()
                            
                            if self._is_content_relevant(text_content, query):
                                scraped_content.append({
                                    'url': url,
                                    'content': text_content[:5000],
                                    'relevance_score': self._calculate_relevance(text_content, query)
                                })
                                print(f"✅ Fallback content found: {len(text_content)} characters")
                    
                    except Exception as fallback_error:
                        print(f"❌ Fallback also failed for {url}: {fallback_error}")
                
                time.sleep(1)  # Be respectful to websites
                
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")
                continue
        
        # Sort by relevance score
        scraped_content.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        print(f"✅ Successfully scraped {len(scraped_content)} relevant sources")
        return scraped_content
    
    def _is_content_relevant(self, content: str, query: str) -> bool:
        """Check if content is relevant to the search query"""
        content_lower = content.lower()
        query_lower = query.lower()
        
        # Extract key terms from query
        query_terms = query_lower.split()
        
        # Check if content contains query terms
        term_matches = sum(1 for term in query_terms if term in content_lower)
        
        # Content is relevant if it contains at least 50% of query terms
        relevance_threshold = len(query_terms) * 0.5
        return term_matches >= relevance_threshold
    
    def _calculate_relevance(self, content: str, query: str) -> float:
        """Calculate relevance score between content and query"""
        content_lower = content.lower()
        query_lower = query.lower()
        
        # Extract key terms from query
        query_terms = query_lower.split()
        
        # Count term occurrences
        term_counts = {}
        for term in query_terms:
            term_counts[term] = content_lower.count(term)
        
        # Calculate relevance score
        total_occurrences = sum(term_counts.values())
        content_length = len(content_lower.split())
        
        if content_length == 0:
            return 0.0
        
        # Normalize by content length
        relevance_score = total_occurrences / content_length
        
        return relevance_score
    
    def _format_results(self, scraped_content: List[Dict[str, Any]], query: str) -> str:
        """Format scraped content into readable results"""
        if not scraped_content:
            return "❌ No relevant content found"
        
        result = f"""
🔄 Dynamic Web Search Results for: "{query}"

📊 Summary:
- Sources Discovered: {len(scraped_content)}
- Total Content: {sum(len(item['content']) for item in scraped_content)} characters
- Average Relevance Score: {sum(item['relevance_score'] for item in scraped_content) / len(scraped_content):.4f}

📰 Top Sources:
"""
        
        for i, item in enumerate(scraped_content[:5], 1):
            result += f"""
{i}. {item['url']}
   Relevance Score: {item['relevance_score']:.4f}
   Content Preview: {item['content'][:200]}...
"""
        
        result += f"""

📋 Full Content Summary:
{chr(10).join([f"• {item['content'][:500]}..." for item in scraped_content[:3]])}

✅ Dynamic search completed successfully
"""
        
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
            
            # Search queries for institutional data
            institutional_queries = [
                f"{company_name} FII holdings foreign institutional investors",
                f"{company_name} major shareholders ownership data",
                f"{company_name} institutional ownership mutual funds",
                f"{company_name} options flow institutional activity",
                f"{company_name} insider trading institutional investors",
                f"{company_name} shareholder structure ownership breakdown"
            ]
            
            institutional_data = {}
            
            for query in institutional_queries:
                print(f"🔍 Searching: {query}")
                result = self.search_tool._run(query)
                
                if result and "✅" in result:
                    institutional_data[query] = result
                else:
                    institutional_data[query] = f"❌ No data found for: {query}"
            
            # Format results
            return self._format_institutional_results(institutional_data, company_name)
            
        except Exception as e:
            return f"❌ Error in institutional data search: {str(e)}"
    
    def _format_institutional_results(self, data: Dict[str, str], company_name: str) -> str:
        """Format institutional data results"""
        result = f"""
🏦 Institutional Data Analysis for {company_name}

📊 Data Sources Searched:
"""
        
        for query, content in data.items():
            status = "✅ Found" if "✅" in content else "❌ Not Found"
            result += f"• {query}: {status}\n"
        
        result += f"""

📋 Detailed Results:
"""
        
        for query, content in data.items():
            if "✅" in content:
                result += f"""
🔍 {query}:
{content[:1000]}...
"""
        
        result += f"""

✅ Institutional data search completed
"""
        
        return result

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
            
            # Search queries for crypto data
            crypto_queries = [
                f"{crypto_name} cryptocurrency price market cap",
                f"{crypto_name} crypto trading volume institutional adoption",
                f"{crypto_name} blockchain technology development updates",
                f"{crypto_name} crypto market sentiment analysis",
                f"{crypto_name} cryptocurrency news developments",
                f"{crypto_name} crypto institutional investment data"
            ]
            
            crypto_data = {}
            
            for query in crypto_queries:
                print(f"🔍 Searching: {query}")
                result = self.search_tool._run(query)
                
                if result and "✅" in result:
                    crypto_data[query] = result
                else:
                    crypto_data[query] = f"❌ No data found for: {query}"
            
            # Format results
            return self._format_crypto_results(crypto_data, crypto_name)
            
        except Exception as e:
            return f"❌ Error in crypto data search: {str(e)}"
    
    def _format_crypto_results(self, data: Dict[str, str], crypto_name: str) -> str:
        """Format cryptocurrency data results"""
        result = f"""
🪙 Cryptocurrency Data Analysis for {crypto_name}

📊 Data Sources Searched:
"""
        
        for query, content in data.items():
            status = "✅ Found" if "✅" in content else "❌ Not Found"
            result += f"• {query}: {status}\n"
        
        result += f"""

📋 Detailed Results:
"""
        
        for query, content in data.items():
            if "✅" in content:
                result += f"""
🔍 {query}:
{content[:1000]}...
"""
        
        result += f"""

✅ Cryptocurrency data search completed
"""
        
        return result

# Export all tools
__all__ = [
    'DynamicWebSearchTool',
    'InstitutionalDataTool', 
    'CryptoDataTool'
] 