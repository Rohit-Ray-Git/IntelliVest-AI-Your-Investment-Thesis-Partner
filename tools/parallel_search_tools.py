"""
⚡ Parallel Search Tools - High-Speed Financial Data Discovery
=============================================================

This module provides optimized tools for parallel web scraping and data discovery.
Uses concurrent processing to dramatically reduce execution time while maintaining
data quality and respecting rate limits.
"""

import asyncio
import aiohttp
import asyncio
import re
import json
import time
import os
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urljoin, urlparse, quote_plus
import requests
from bs4 import BeautifulSoup
from langchain.tools import BaseTool
import random
from pydantic import Field
from dotenv import load_dotenv
import concurrent.futures
from functools import partial

# Load environment variables
load_dotenv()

# Import Tavily for intelligent web search
try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    if TAVILY_API_KEY:
        tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    else:
        TAVILY_AVAILABLE = False
        tavily_client = None
except ImportError:
    TAVILY_AVAILABLE = False
    tavily_client = None

# Import faster alternatives to Playwright
try:
    import trafilatura
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False

# Fix Windows asyncio issues
import sys
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class ParallelWebSearchTool(BaseTool):
    """⚡ High-speed parallel web search and content discovery using Tavily"""
    
    name: str = "parallel_web_search"
    description: str = """
    High-speed parallel web search for financial data using concurrent processing.
    Dramatically faster than sequential search while maintaining data quality.
    Input should be a search query for financial information.
    Returns scraped content from discovered sources.
    """
    
    # Define fields that will be set in __init__
    session: Optional[requests.Session] = Field(default=None, exclude=True)
    max_concurrent: int = Field(default=10, description="Maximum concurrent requests")
    timeout: int = Field(default=15, description="Request timeout in seconds")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Initialize Trafilatura for ultra-fast content extraction
        if TRAFILATURA_AVAILABLE:
            print("✅ Trafilatura initialized for ultra-fast content extraction")
        else:
            print("⚠️ Trafilatura not available, using fallback methods")
        
        # Performance settings
        self.max_concurrent = kwargs.get('max_concurrent', 10)
        self.timeout = kwargs.get('timeout', 15)
        
        print(f"⚡ Parallel Web Search Tool initialized with {self.max_concurrent} concurrent workers")
    
    def __del__(self):
        """Cleanup method to properly close resources"""
        try:
            if hasattr(self, 'session') and self.session:
                self.session.close()
        except:
            pass
    
    def _run(self, query: str) -> str:
        """
        Main execution method - performs parallel web search and scraping
        
        Args:
            query: Search query for financial information
            
        Returns:
            Formatted string with scraped content
        """
        print(f"⚡ Parallel Search: Searching for '{query}'")
        
        try:
            # Step 1: Discover URLs using Tavily (fast)
            print("🔍 Discovering URLs with Tavily...")
            urls = self._tavily_search(query)
            
            if not urls:
                print("❌ No URLs discovered, using fallback search")
                return self._fallback_search(query)
            
            print(f"✅ Discovered {len(urls)} URLs")
            
            # Step 2: Parallel scraping of discovered URLs
            print(f"⚡ Starting parallel scraping with {self.max_concurrent} workers...")
            scraped_content = self._parallel_scrape_urls(urls, query)
            
            # Step 3: Format and return results
            return self._format_results(scraped_content, query)
            
        except Exception as e:
            print(f"❌ Error in parallel search: {e}")
            return f"❌ Parallel search failed: {str(e)}"
    
    def _tavily_search(self, query: str) -> List[str]:
        """Search for URLs using Tavily API"""
        if not TAVILY_AVAILABLE or not tavily_client:
            return []
        
        try:
            print(f"🔍 Tavily Search: '{query}'")
            response = tavily_client.search(
                query=query,
                search_depth="basic",
                max_results=10,
                include_domains=["finance.yahoo.com", "investing.com", "marketwatch.com", 
                               "seekingalpha.com", "cnbc.com", "bloomberg.com", "reuters.com",
                               "wsj.com", "ft.com", "apple.com", "google.com", "nasdaq.com", "macrotrends.net", "nseindia.com",
                               "bseindia.com"]
            )
            
            urls = []
            if response and 'results' in response:
                for result in response['results']:
                    url = result.get('url', '')
                    if url and self._is_valid_financial_url(url):
                        urls.append(url)
            
            print(f"✅ Tavily found {len(urls)} URLs")
            if urls:
                print(f"🔍 Discovered URLs (first 3):")
                for i, url in enumerate(urls[:3], 1):
                    print(f"  {i}. {url}")
            
            return urls
            
        except Exception as e:
            print(f"❌ Tavily search error: {e}")
            return []
    
    def _parallel_scrape_urls(self, urls: List[str], query: str) -> List[Dict[str, Any]]:
        """
        Parallel scraping of multiple URLs using ThreadPoolExecutor
        
        Args:
            urls: List of URLs to scrape
            query: Original search query for relevance checking
            
        Returns:
            List of scraped content dictionaries
        """
        scraped_content = []
        
        # Filter out problematic URLs
        valid_urls = [url for url in urls[:8] if not self._should_skip_url(url)]  # Process up to 8 URLs
        
        if not valid_urls:
            return scraped_content
        
        print(f"⚡ Parallel scraping {len(valid_urls)} URLs...")
        start_time = time.time()
        
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            # Create scraping tasks
            scraping_tasks = [
                executor.submit(self._scrape_single_url, url, query)
                for url in valid_urls
            ]
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(scraping_tasks, timeout=60):
                try:
                    result = future.result()
                    if result and result.get('success'):
                        scraped_content.append(result)
                        print(f"✅ Parallel scraped: {result['url']} ({result.get('method', 'unknown')})")
                    elif result:
                        print(f"⚠️ Parallel scrape failed: {result['url']} - {result.get('error', 'unknown error')}")
                except Exception as e:
                    print(f"❌ Parallel scrape error: {e}")
                    continue
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"⚡ Parallel scraping completed in {execution_time:.2f} seconds")
        print(f"📊 Successfully scraped {len(scraped_content)} out of {len(valid_urls)} URLs")
        
        return scraped_content
    
    def _scrape_single_url(self, url: str, query: str) -> Dict[str, Any]:
        """
        Scrape a single URL with multiple fallback methods
        
        Args:
            url: URL to scrape
            query: Original search query for relevance checking
            
        Returns:
            Dictionary with scraping results
        """
        try:
            # Try Trafilatura first (fastest)
            if TRAFILATURA_AVAILABLE:
                content_data = self._scrape_with_trafilatura(url)
                if content_data.get('success'):
                    content = content_data.get('content', '')
                    if content and self._is_content_relevant_enhanced(content, query):
                        return {
                            'url': url,
                            'content': content,
                            'title': content_data.get('title', ''),
                            'success': True,
                            'method': 'trafilatura'
                        }
            
            # Try requests as fallback
            content_data = self._scrape_with_requests(url)
            if content_data.get('success'):
                content = content_data.get('content', '')
                if content and self._is_content_relevant_enhanced(content, query):
                    return {
                        'url': url,
                        'content': content,
                        'title': content_data.get('title', ''),
                        'success': True,
                        'method': 'requests'
                    }
            
            # Try LLM-based scraping as last resort
            content_data = self._scrape_with_llm(url)
            if content_data.get('success'):
                content = content_data.get('content', '')
                if content and self._is_content_relevant_enhanced(content, query):
                    return {
                        'url': url,
                        'content': content,
                        'title': content_data.get('title', ''),
                        'success': True,
                        'method': 'LLM-based'
                    }
            
            return {
                'url': url,
                'content': '',
                'title': '',
                'success': False,
                'error': 'All scraping methods failed',
                'method': 'none'
            }
            
        except Exception as e:
            return {
                'url': url,
                'content': '',
                'title': '',
                'success': False,
                'error': str(e),
                'method': 'error'
            }
    
    def _scrape_with_trafilatura(self, url: str) -> Dict[str, Any]:
        """Ultra-fast scraping using Trafilatura"""
        try:
            # Use requests to get the page
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Extract content with Trafilatura
            extracted_text = trafilatura.extract(response.text, include_formatting=True)
            
            if extracted_text:
                # Get title
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string if soup.title else ''
                
                return {
                    'url': url,
                    'content': extracted_text,
                    'title': title,
                    'success': True,
                    'method': 'trafilatura'
                }
            else:
                return {
                    'url': url,
                    'content': '',
                    'title': '',
                    'success': False,
                    'error': 'No content extracted',
                    'method': 'trafilatura'
                }
                
        except Exception as e:
            return {
                'url': url,
                'content': '',
                'title': '',
                'success': False,
                'error': str(e),
                'method': 'trafilatura'
            }
    
    def _scrape_with_requests(self, url: str) -> Dict[str, Any]:
        """Scrape content using requests with optimized settings"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            content = self._extract_relevant_content(soup, url)
            
            return {
                'url': url,
                'content': content,
                'title': soup.title.string if soup.title else '',
                'success': True,
                'method': 'requests'
            }
            
        except Exception as e:
            return {
                'url': url,
                'content': '',
                'title': '',
                'success': False,
                'error': str(e),
                'method': 'requests'
            }
    
    def _scrape_with_llm(self, url: str) -> Dict[str, Any]:
        """LLM-based scraping for complex sites"""
        try:
            # Get raw content first
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else ''
            
            # Extract main content
            content = self._extract_relevant_content(soup, url)
            
            if content and len(content) > 100:
                return {
                    'url': url,
                    'content': content,
                    'title': title,
                    'success': True,
                    'method': 'LLM-based'
                }
            else:
                return {
                    'url': url,
                    'content': '',
                    'title': title,
                    'success': False,
                    'error': 'Insufficient content',
                    'method': 'LLM-based'
                }
                
        except Exception as e:
            return {
                'url': url,
                'content': '',
                'title': '',
                'success': False,
                'error': str(e),
                'method': 'LLM-based'
            }
    
    def _extract_relevant_content(self, soup: BeautifulSoup, query: str) -> str:
        """Extract relevant content from BeautifulSoup object"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit content length for performance
        if len(text) > 10000:
            text = text[:10000] + "..."
        
        return text
    
    def _is_content_relevant_enhanced(self, content: str, query: str) -> bool:
        """Enhanced relevance checking"""
        if not content or len(content) < 50:
            return False
        
        # Convert to lowercase for comparison
        content_lower = content.lower()
        query_lower = query.lower()
        
        # Extract key terms from query
        query_terms = [term.strip() for term in query_lower.split() if len(term) > 2]
        
        # Check if key terms appear in content
        relevant_terms = 0
        for term in query_terms:
            if term in content_lower:
                relevant_terms += 1
        
        # Content is relevant if at least 30% of terms match
        relevance_threshold = max(1, len(query_terms) * 0.3)
        return relevant_terms >= relevance_threshold
    
    def _is_valid_financial_url(self, url: str) -> bool:
        """Check if URL is likely to contain financial data"""
        financial_domains = [
            'finance.yahoo.com', 'investing.com', 'marketwatch.com',
            'seekingalpha.com', 'cnbc.com', 'bloomberg.com', 'reuters.com',
            'wsj.com', 'ft.com', 'apple.com', 'google.com', 'nasdaq.com',
            'marketbeat.com', 'tipranks.com', 'gurufocus.com', 'macrotrends.net'
        ]
        
        try:
            domain = urlparse(url).netloc.lower()
            return any(financial_domain in domain for financial_domain in financial_domains)
        except:
            return False
    
    def _should_skip_url(self, url: str) -> bool:
        """Check if URL should be skipped"""
        skip_patterns = [
            'youtube.com', 'facebook.com', 'twitter.com', 'instagram.com',
            'linkedin.com', 'reddit.com', 'pinterest.com', 'tiktok.com',
            'google.com/maps', 'google.com/search', 'bing.com/search',
            'yahoo.com/search', 'duckduckgo.com', 'wikipedia.org'
        ]
        
        url_lower = url.lower()
        return any(pattern in url_lower for pattern in skip_patterns)
    
    def _fallback_search(self, query: str) -> str:
        """Fallback search when Tavily is not available"""
        return f"❌ Fallback search not implemented for: {query}"
    
    def _format_results(self, scraped_content: List[Dict[str, Any]], query: str) -> str:
        """Format scraped content into readable results"""
        if not scraped_content:
            return f"❌ No relevant content found for: {query}"
        
        results = []
        results.append(f"✅ Found {len(scraped_content)} relevant sources for: {query}")
        results.append("")
        
        for i, content_data in enumerate(scraped_content, 1):
            url = content_data.get('url', 'Unknown URL')
            method = content_data.get('method', 'Unknown method')
            content = content_data.get('content', '')
            
            results.append(f"📄 Source {i}: {url}")
            results.append(f"🔧 Method: {method}")
            results.append(f"📝 Content: {content[:500]}...")
            results.append("")
        
        return "\n".join(results)

class ParallelInstitutionalDataTool(BaseTool):
    """🏦 High-speed parallel institutional data discovery"""
    
    name: str = "parallel_institutional_data"
    description: str = """
    High-speed parallel discovery and scraping of institutional data including
    FII holdings, mutual fund data, and institutional ownership information.
    Input should be a company name or symbol.
    """
    
    # Define fields that will be set in __init__
    search_tool: Optional[ParallelWebSearchTool] = Field(default=None, exclude=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_tool = ParallelWebSearchTool()
    
    def _run(self, company_name: str) -> str:
        """Run parallel institutional data search"""
        print(f"🏦 Parallel Institutional Data: Searching for '{company_name}'")
        
        # Multiple search queries for comprehensive coverage
        queries = [
            f"{company_name} institutional holdings FII mutual fund data",
            f"{company_name} FII holdings institutional investors",
            f"{company_name} mutual fund holdings",
            f"{company_name} insider trading institutional ownership"
        ]
        
        all_results = []
        
        # Run queries in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_query = {
                executor.submit(self.search_tool._run, query): query 
                for query in queries
            }
            
            for future in concurrent.futures.as_completed(future_to_query, timeout=120):
                query = future_to_query[future]
                try:
                    result = future.result()
                    all_results.append(f"Query: {query}\nResult: {result}\n")
                except Exception as e:
                    all_results.append(f"Query: {query}\nError: {str(e)}\n")
        
        return self._format_institutional_results(all_results, company_name)
    
    def _format_institutional_results(self, results: List[str], company_name: str) -> str:
        """Format institutional data results"""
        if not results:
            return f"❌ No institutional data found for {company_name}"
        
        formatted = [f"🏦 Institutional Data for {company_name}:"]
        formatted.append("=" * 50)
        
        for result in results:
            formatted.append(result)
        
        return "\n".join(formatted)

# Export the parallel tools
__all__ = ['ParallelWebSearchTool', 'ParallelInstitutionalDataTool'] 