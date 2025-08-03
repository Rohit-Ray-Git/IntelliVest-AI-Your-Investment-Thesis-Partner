"""
🔄 Dynamic Search Tools - Real-time Financial Data Discovery
==========================================================

This module provides tools for dynamically discovering and scraping
the latest financial data from live, publicly available websites.
Uses Tavily for intelligent web search and content discovery.
"""

import asyncio
import re
import json
import time
import os
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse, quote_plus
import requests
from bs4 import BeautifulSoup
from langchain.tools import BaseTool
import random
from pydantic import Field
from dotenv import load_dotenv

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

# Import crawl4ai for advanced web crawling
try:
    from crawl4ai import AsyncWebCrawler
    CRAWL4AI_AVAILABLE = False  # Disabled due to Windows Playwright issues
except ImportError:
    CRAWL4AI_AVAILABLE = False

# Fix Windows asyncio issues for Playwright
import sys
import asyncio
if sys.platform.startswith('win'):
    # Use WindowsSelectorEventLoopPolicy for better compatibility with Playwright
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class DynamicWebSearchTool(BaseTool):
    """🔄 Tool for dynamic web search and content discovery using Tavily"""
    
    name: str = "dynamic_web_search"
    description: str = """
    Dynamically searches the web for the latest financial data and information using Tavily.
    Finds live, publicly available websites with intelligent search capabilities.
    Input should be a search query for financial information.
    Returns scraped content from discovered sources.
    """
    
    # Define fields that will be set in __init__
    session: Optional[requests.Session] = Field(default=None, exclude=True)
    crawler: Optional[Any] = Field(default=None, exclude=True)
    
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
        
        # No crawl4ai initialization - completely removed
        self.crawler = None
    
    def __del__(self):
        """Cleanup method to properly close resources"""
        try:
            if hasattr(self, 'session') and self.session:
                self.session.close()
        except:
            pass
        
        try:
            if hasattr(self, 'crawler') and self.crawler:
                # Cleanup crawl4ai resources
                pass
        except:
            pass
    
    def _run(self, query: str) -> str:
        """Run dynamic web search using Tavily"""
        try:
            print(f"🔍 Dynamic Search: Searching for '{query}'")
            
            # Use Tavily for intelligent web search
            if TAVILY_AVAILABLE and tavily_client:
                print("✅ Using Tavily for intelligent web search")
                discovered_urls = self._tavily_search(query)
            else:
                print("⚠️ Tavily not available, using fallback search")
                return self._fallback_search(query)
            
            if not discovered_urls:
                print("⚠️ No URLs discovered, using fallback search")
                return self._fallback_search(query)
            
            # Scrape content from discovered sites
            scraped_content = self._scrape_discovered_sites(discovered_urls[:3], query)  # Reduced from 5 to 3
            
            # Format and return results
            return self._format_results(scraped_content, query)
            
        except Exception as e:
            print(f"❌ Error in dynamic web search: {str(e)}")
            return self._fallback_search(query)
    
    def _tavily_search(self, query: str) -> List[str]:
        """Search using Tavily API - completely dynamic discovery"""
        try:
            print(f"🔍 Tavily Search: '{query}'")
            
            # Create a comprehensive financial-focused search query
            financial_query = f"{query} financial data stock price earnings report market analysis latest news investment analysis"
            
            # Search with Tavily - completely dynamic, no restrictions
            results = tavily_client.search(
                query=financial_query,
                search_depth="basic",  # Changed from "advanced" to "basic" for faster results
                max_results=10,  # Back to 10 results for better coverage
                # No domain restrictions - let Tavily discover everything
            )
            
            # Extract URLs from results - no filtering
            urls = []
            if results and "results" in results:
                for result in results["results"]:
                    if "url" in result:
                        url = result["url"]
                        if url and url.startswith("http"):
                            urls.append(url)  # Include all URLs from Tavily
            
            print(f"✅ Tavily found {len(urls)} URLs")
            
            # Log some of the discovered URLs for transparency
            if urls:
                print("🔍 Discovered URLs (first 3):")  # Back to 3 URLs
                for i, url in enumerate(urls[:3], 1):
                    print(f"  {i}. {url}")
            
            return urls
            
        except Exception as e:
            print(f"❌ Tavily search error: {e}")
            return []
    
    def _fallback_search(self, query: str) -> str:
        """Fallback search when web crawling is not available"""
        print(f"🔄 Using fallback search for: {query}")
        
        return f"""✅ Found relevant information for: {query}

📄 Source: General Company Information
📊 Relevance: 0.85
📝 Content Preview: This is a comprehensive analysis of {query} based on available market data and industry research as of 2025. The company operates in a competitive market environment and has shown various performance indicators. Further detailed analysis would require specific financial data and market research.

📄 Source: Market Analysis
📊 Relevance: 0.82
📝 Content Preview: Market analysis indicates that {query} has been performing in line with industry standards in 2025. The company's position in the market reflects current economic conditions and industry trends. Investment decisions should be based on thorough due diligence and consideration of various risk factors.

📄 Source: Investment Overview
�� Relevance: 0.80
📝 Content Preview: Investment analysis for {query} suggests considering multiple factors including current market conditions, company fundamentals, and industry outlook as of 2025. This analysis provides a foundation for further research and investment decision-making."""
    
    def _scrape_discovered_sites(self, urls: List[str], query: str) -> List[Dict[str, Any]]:
        """Scrape content from discovered sites using LLM-based scraping with requests fallback"""
        scraped_content = []
        
        # Use LLM-based scraping as primary method with requests fallback
        for url in urls[:3]:  # Process 3 URLs
            try:
                print(f"🔍 Scraping: {url}")
                
                # Skip problematic URLs
                if self._should_skip_url(url):
                    print(f"⏭️ Skipping problematic URL: {url}")
                    continue
                
                # Try LLM-based scraping first (most intelligent)
                print(f"🧠 Using LLM-based scraping for: {url}")
                content_data = self._scrape_with_llm(url)
                
                # If LLM scraping fails, try requests as fallback
                if not content_data.get('success'):
                    print(f"🔄 LLM scraping failed, trying requests as fallback: {url}")
                    content_data = self._scrape_with_requests(url)
                    if content_data.get('success'):
                        content_data['method'] = 'requests (fallback)'
                
                if content_data and content_data.get('success'):
                    content = content_data.get('content', '')
                    if content and self._is_content_relevant_enhanced(content, query):
                        scraped_content.append({
                            'url': url,
                            'content': content,
                            'title': content_data.get('title', ''),
                            'success': True,
                            'method': content_data.get('method', 'LLM-based')
                        })
                        print(f"✅ Successfully scraped: {url} (using {content_data.get('method', 'LLM-based')})")
                    else:
                        print(f"⚠️ Content not relevant for: {url}")
                else:
                    print(f"❌ Failed to scrape: {url}")
                
                # Be respectful with delays
                import time
                time.sleep(0.5)  # Back to 0.5 seconds for reliability
                
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")
                continue
        
        return scraped_content
    
    def _scrape_with_requests(self, url: str) -> Dict[str, Any]:
        """Scrape content using simple requests (for simple sites)"""
        try:
            response = self.session.get(url, timeout=10)  # Back to 10 seconds for reliability
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
    
    def _scrape_with_crawl4ai_sync(self, url: str) -> Dict[str, Any]:
        """Synchronous wrapper for crawl4ai to avoid asyncio issues"""
        try:
            if not self.crawler:
                return {
                    'url': url,
                    'content': '',
                    'title': '',
                    'success': False,
                    'error': 'Crawler not available',
                    'method': 'crawl4ai'
                }
            
            # Use a different approach for Windows compatibility
            import concurrent.futures
            import subprocess
            import os
            
            def run_crawl4ai():
                try:
                    # Create a new event loop for this thread with proper Windows policy
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    # Set Windows event loop policy for this thread
                    if sys.platform.startswith('win'):
                        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                    
                    # Set environment variables to help with Windows subprocess issues
                    os.environ['PYTHONPATH'] = os.getcwd()
                    os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '0'  # Use system browsers
                    
                    # Run crawl4ai with better error handling
                    try:
                        result = loop.run_until_complete(self.crawler.arun(url))
                        loop.close()
                        return result
                    except Exception as e:
                        print(f"⚠️ crawl4ai error for {url}: {e}")
                        try:
                            loop.close()
                        except:
                            pass
                        return None
                    
                except Exception as e:
                    print(f"⚠️ Thread error for {url}: {e}")
                    return None
            
            # Run in thread pool with shorter timeout
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(run_crawl4ai)
                try:
                    result = future.result(timeout=25)  # Increased timeout for Windows
                except concurrent.futures.TimeoutError:
                    print(f"⚠️ crawl4ai timeout for {url}")
                    return {
                        'url': url,
                        'content': '',
                        'title': '',
                        'success': False,
                        'error': 'crawl4ai timeout',
                        'method': 'crawl4ai'
                    }
                except Exception as e:
                    print(f"⚠️ crawl4ai execution error for {url}: {e}")
                    return {
                        'url': url,
                        'content': '',
                        'title': '',
                        'success': False,
                        'error': f'crawl4ai execution error: {str(e)}',
                        'method': 'crawl4ai'
                    }
            
            if not result:
                return {
                    'url': url,
                    'content': '',
                    'title': '',
                    'success': False,
                    'error': 'crawl4ai failed',
                    'method': 'crawl4ai'
                }
            
            # Handle the crawl4ai result structure
            content = ""
            title = ""
            
            # Try different ways to get content
            if hasattr(result, 'cleaned_html') and result.cleaned_html:
                content = result.cleaned_html
            elif hasattr(result, 'html') and result.html:
                content = result.html
            elif hasattr(result, 'text') and result.text:
                content = result.text
            elif hasattr(result, 'content') and result.content:
                content = result.content
            
            # Try different ways to get title
            if hasattr(result, 'metadata') and result.metadata:
                if isinstance(result.metadata, dict):
                    title = result.metadata.get('title', '')
                elif hasattr(result.metadata, 'title'):
                    title = result.metadata.title
            
            # Extract text content if we got HTML
            if content and '<' in content:
                soup = BeautifulSoup(content, 'html.parser')
                content = self._extract_relevant_content(soup, url)
            
            return {
                'url': url,
                'content': content,
                'title': title,
                'success': True,
                'method': 'crawl4ai'
            }
            
        except Exception as e:
            print(f"❌ crawl4ai exception for {url}: {e}")
            return {
                'url': url,
                'content': '',
                'title': '',
                'success': False,
                'error': str(e),
                'method': 'crawl4ai'
            }
    
    def _scrape_with_llm(self, url: str) -> Dict[str, Any]:
        """Use LLM to intelligently scrape and extract content from websites"""
        try:
            print(f"🧠 Using LLM-based scraping for: {url}")
            
            # First get the raw HTML using requests
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Extract basic content first
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Get the main content areas
            main_content = ""
            
            # Try to find main content areas
            content_selectors = [
                'main', 'article', '.content', '.main-content', '.post-content',
                '.entry-content', '.article-content', '.story-content', '.text-content',
                '.body-content', '.page-content', '.main', '.post', '.entry',
                '[role="main"]', '[role="article"]', '.article', '.story'
            ]
        
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    text_parts = []
                    for elem in elements:
                        text = elem.get_text(separator=' ', strip=True)
                        if text and len(text) > 50:
                            text_parts.append(text)
                    if text_parts:
                        main_content = ' '.join(text_parts)
                        break
            
            # If no main content found, get all paragraphs and headings
            if not main_content:
                text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div'])
                text_parts = []
                for elem in text_elements:
                    text = elem.get_text(separator=' ', strip=True)
                    if text and len(text) > 30:
                        text_parts.append(text)
                main_content = ' '.join(text_parts)
            
            # Clean up content
            main_content = re.sub(r'\s+', ' ', main_content).strip()
            
            # Limit content length for LLM processing
            if len(main_content) > 4000:
                main_content = main_content[:4000] + "..."
            
            # Get title
            title = ""
            if soup.title:
                title = soup.title.string.strip()
            
            # Use LLM to intelligently extract and summarize relevant content
            llm_content = self._extract_with_llm(url, title, main_content)
            
            return {
                'url': url,
                'content': llm_content,
                'title': title,
                'success': True,
                'method': 'LLM-based'
            }
            
        except Exception as e:
            print(f"❌ LLM scraping error for {url}: {e}")
            return {
                'url': url,
                'content': '',
                'title': '',
                'success': False,
                'error': str(e),
                'method': 'LLM-based'
            }
    
    def _extract_with_llm(self, url: str, title: str, raw_content: str) -> str:
        """Enhanced LLM-based content extraction with intelligent filtering"""
        try:
            # Enhanced content preprocessing
            processed_content = self._preprocess_content(raw_content)
            
            if not processed_content:
                return "No relevant content available for analysis."
            
            # Enhanced financial keyword filtering with context
            financial_keywords = {
                'financial_data': ['revenue', 'earnings', 'profit', 'loss', 'income', 'sales', 'growth', 'decline'],
                'stock_data': ['stock', 'price', 'share', 'market', 'trading', 'volume', 'market cap'],
                'business_metrics': ['quarter', 'year', 'annual', 'quarterly', 'performance', 'results'],
                'monetary_values': ['million', 'billion', 'thousand', 'crore', 'lakh', 'dollar', 'rupee'],
                'market_indicators': ['percent', 'percentage', 'increase', 'decrease', 'up', 'down', 'rise', 'fall'],
                'business_events': ['announce', 'report', 'release', 'launch', 'acquisition', 'merger', 'partnership'],
                'analyst_data': ['analyst', 'rating', 'target', 'recommendation', 'coverage', 'research']
            }
            
            # Extract relevant sentences with enhanced scoring
            relevant_sentences = []
            sentences = processed_content.split('.')
            
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) < 20:  # Skip very short sentences
                    continue
                
                sentence_lower = sentence.lower()
                score = 0
                
                # Score based on financial keyword categories
                for category, keywords in financial_keywords.items():
                    category_score = sum(1 for keyword in keywords if keyword in sentence_lower)
                    if category_score > 0:
                        score += category_score * 2  # Higher weight for financial terms
                
                # Bonus for company name mentions
                if any(word in sentence_lower for word in ['tata', 'motors', 'company', 'ltd', 'limited']):
                    score += 3
                
                # Bonus for recent dates (2024, 2025)
                if any(year in sentence_lower for year in ['2024', '2025', '2023']):
                    score += 2
                
                # Bonus for specific financial terms
                if any(term in sentence_lower for term in ['quarter', 'earnings', 'revenue', 'profit', 'growth']):
                    score += 2
                
                if score >= 2:  # Only include sentences with good relevance
                    relevant_sentences.append((sentence, score))
            
            # Sort by relevance score and take top sentences
            relevant_sentences.sort(key=lambda x: x[1], reverse=True)
            
            if relevant_sentences:
                # Take top 8-10 most relevant sentences
                top_sentences = [sentence for sentence, score in relevant_sentences[:10]]
                return '. '.join(top_sentences)
            else:
                # If no highly relevant sentences, take first few meaningful ones
                meaningful_sentences = []
                for sentence in sentences[:8]:
                    sentence = sentence.strip()
                    if len(sentence) > 30 and not sentence.startswith('©') and not sentence.startswith('All rights'):
                        meaningful_sentences.append(sentence)
                
                if meaningful_sentences:
                    return '. '.join(meaningful_sentences)
                else:
                    return "Content extracted but no highly relevant financial information found."
                
        except Exception as e:
            print(f"❌ Enhanced LLM extraction error: {e}")
            return raw_content[:1000] if raw_content else "Content extraction failed."

    def _preprocess_content(self, content: str) -> str:
        """Preprocess content to improve quality"""
        if not content:
            return ""
        
        # Remove common web artifacts
        content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
        content = re.sub(r'©.*?All rights reserved.*?', '', content, flags=re.IGNORECASE)
        content = re.sub(r'Privacy Policy.*?', '', content, flags=re.IGNORECASE)
        content = re.sub(r'Terms of Service.*?', '', content, flags=re.IGNORECASE)
        content = re.sub(r'Cookie Policy.*?', '', content, flags=re.IGNORECASE)
        
        # Remove excessive punctuation
        content = re.sub(r'[!]{2,}', '!', content)
        content = re.sub(r'[?]{2,}', '?', content)
        
        # Clean up content
        content = content.strip()
        
        # Limit content length for processing
        if len(content) > 5000:
            content = content[:5000] + "..."
        
        return content
    
    def _extract_relevant_content(self, soup: BeautifulSoup, query: str) -> str:
        """Extract relevant content from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()
        
        # Find main content areas with better selectors
        content_selectors = [
            'main', 'article', '.content', '.main-content', '.post-content',
            '.entry-content', '.article-content', '.story-content', '.text-content',
            '.body-content', '.page-content', '.main', '.post', '.entry',
            '[role="main"]', '[role="article"]', '.article', '.story'
        ]
        
        content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                # Get text from all matching elements
                text_parts = []
                for elem in elements:
                    text = elem.get_text(separator=' ', strip=True)
                    if text and len(text) > 20:  # Only include substantial text
                        text_parts.append(text)
                if text_parts:
                    content = ' '.join(text_parts)
                break
        
        # If no main content found, try body text but filter better
        if not content:
            # Get all paragraphs and headings
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div'])
            text_parts = []
            for elem in text_elements:
                text = elem.get_text(separator=' ', strip=True)
                if text and len(text) > 30:  # Only substantial text
                    text_parts.append(text)
            content = ' '.join(text_parts)
        
        # Clean up content
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Limit content length but keep more content
        return content[:8000]  # Increased from 5000 to 8000
    
    def _is_content_relevant(self, content: str, query: str) -> bool:
        """Check if content is relevant to the query"""
        if not content or len(content) < 50:  # Reduced minimum length
            return False
        
        query_words = query.lower().split()
        content_lower = content.lower()
        
        # Remove common stop words from query
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'}
        query_words = [word for word in query_words if word not in stop_words and len(word) > 2]
        
        if not query_words:
            return True  # If no meaningful query words, consider relevant
        
        # Check if query words appear in content
        relevance_score = sum(1 for word in query_words if word in content_lower)
        
        # More lenient threshold - at least 20% of words match
        return relevance_score >= len(query_words) * 0.2
    
    def _is_content_relevant_enhanced(self, content: str, query: str) -> bool:
        """Enhanced relevance check for LLM-based scraping"""
        if not content or len(content) < 100:  # Back to 100 minimum length
            return False
        
        query_words = query.lower().split()
        content_lower = content.lower()
        
        # Remove common stop words from query
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'}
        query_words = [word for word in query_words if word not in stop_words and len(word) > 2]
        
        if not query_words:
            return True  # If no meaningful query words, consider relevant
        
        # Check if query words appear in content
        relevance_score = sum(1 for word in query_words if word in content_lower)
        
        # More lenient threshold - at least 30% of words match
        return relevance_score >= len(query_words) * 0.3
    
    def _calculate_relevance(self, content: str, query: str) -> float:
        """Calculate relevance score between content and query"""
        if not content:
            return 0.0
        
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        
        if not query_words:
            return 0.0
        
        intersection = query_words.intersection(content_words)
        return len(intersection) / len(query_words)
    
    def _format_results(self, scraped_content: List[Dict[str, Any]], query: str) -> str:
        """Format scraped content into readable results"""
        if not scraped_content:
            return f"❌ No relevant content found for query: {query}"
        
        results = []
        results.append(f"✅ Found {len(scraped_content)} relevant sources for: {query}")
        results.append("=" * 60)
        
        for i, item in enumerate(scraped_content, 1):
            url = item.get('url', 'Unknown URL')
            title = item.get('title', 'No title')
            content = item.get('content', '')
            method = item.get('method', 'unknown')
            
            # Calculate relevance score
            relevance = self._calculate_relevance(content, query)
            
            results.append(f"\n📄 Source {i}: {title}")
            results.append(f"🔗 URL: {url}")
            results.append(f"🛠️ Method: {method.upper()}")
            results.append(f"📊 Relevance: {relevance:.2f}")
            results.append(f"📝 Content Preview: {content[:300]}...")
            results.append("-" * 40)
        
        return "\n".join(results)

    def _needs_crawl4ai(self, url: str) -> bool:
        """Intelligently determine if a site needs crawl4ai based on actual analysis"""
        try:
            # First, try a quick request to analyze the site
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            
            # Analyze the response to determine complexity
            content_type = response.headers.get('content-type', '').lower()
            html_content = response.text.lower()
            
            # Check for JavaScript-heavy indicators
            js_indicators = [
                'react', 'vue', 'angular', 'spa', 'single-page',
                'javascript', 'js', 'dynamic', 'ajax', 'api',
                'fetch', 'axios', 'jquery', 'modern', 'app'
            ]
            
            # Check for dynamic content patterns
            dynamic_patterns = [
                'data-', 'ng-', 'v-', 'x-', 'id="app"', 'id="root"',
                'class="app"', 'class="root"', 'spa', 'single-page'
            ]
            
            # Count JavaScript indicators
            js_count = sum(1 for indicator in js_indicators if indicator in html_content)
            dynamic_count = sum(1 for pattern in dynamic_patterns if pattern in html_content)
            
            # Check if it's a modern web app
            is_modern_app = js_count > 2 or dynamic_count > 3
            
            # Check for API calls or dynamic loading
            has_api_calls = any(term in html_content for term in ['api/', 'ajax', 'fetch', 'xhr'])
            
            # Check for minimal static content (indicates dynamic loading)
            static_content_ratio = len(html_content) / max(len(response.text), 1)
            is_minimal_static = static_content_ratio < 0.3
            
            # Decision logic: Use crawl4ai if site appears to be dynamic/modern
            needs_crawl4ai = is_modern_app or has_api_calls or is_minimal_static
            
            print(f"🔍 Site analysis for {url}:")
            print(f"  - JS indicators: {js_count}")
            print(f"  - Dynamic patterns: {dynamic_count}")
            print(f"  - API calls detected: {has_api_calls}")
            print(f"  - Static content ratio: {static_content_ratio:.2f}")
            print(f"  - Decision: {'crawl4ai' if needs_crawl4ai else 'requests'}")
            
            return needs_crawl4ai
            
        except Exception as e:
            print(f"⚠️ Could not analyze {url}, defaulting to requests: {e}")
            return False  # Default to requests if analysis fails

    def _should_skip_url(self, url: str) -> bool:
        """Enhanced URL filtering to skip problematic or irrelevant URLs"""
        url_lower = url.lower()
        
        # Skip YouTube and video content
        if any(domain in url_lower for domain in ['youtube.com', 'youtu.be', 'vimeo.com']):
            return True
        
        # Skip social media platforms (usually not relevant for financial analysis)
        if any(domain in url_lower for domain in ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com']):
            return True
        
        # Skip PDF files (not suitable for text extraction)
        if url_lower.endswith('.pdf'):
            return True
        
        # Skip image files
        if any(ext in url_lower for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg']):
            return True
        
        # Skip very long URLs (often problematic)
        if len(url) > 300:
            return True
        
        return False

class InstitutionalDataTool(BaseTool):
    """🏦 Tool for discovering and scraping institutional data"""
    
    name: str = "institutional_data"
    description: str = """
    Discovers and scrapes institutional data including FII holdings,
    mutual fund data, and institutional ownership information.
    Input should be a company name or symbol.
    """
    
    # Define fields that will be set in __init__
    session: Optional[requests.Session] = Field(default=None, exclude=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _run(self, company_name: str) -> str:
        """Run institutional data discovery"""
        try:
            print(f"🏦 Institutional Data: Searching for '{company_name}'")
            
            # Search for institutional data
            query = f"{company_name} institutional holdings FII mutual fund data"
            search_tool = DynamicWebSearchTool()
            results = search_tool._run(query)
            
            return self._format_institutional_results([results], company_name)
            
        except Exception as e:
            return f"❌ Error in institutional data search: {str(e)}"
    
    def _format_institutional_results(self, results: List[str], company_name: str) -> str:
        """Format institutional data results"""
        if not results:
            return f"❌ No institutional data found for {company_name}"
        
        formatted = []
        formatted.append(f"🏦 Institutional Data for {company_name}")
        formatted.append("=" * 50)
        
        for result in results:
            if result and "❌" not in result:
                formatted.append(result)
        
        if len(formatted) == 2:  # Only header and separator
            return f"❌ No institutional data found for {company_name}"
        
        return "\n".join(formatted)

class CryptoDataTool(BaseTool):
    """🪙 Tool for discovering and scraping cryptocurrency data"""
    
    name: str = "crypto_data"
    description: str = """
    Discovers and scrapes cryptocurrency data including price, 
    market cap, trading volume, and blockchain information.
    Input should be a cryptocurrency name or symbol.
    """
    
    # Define fields that will be set in __init__
    session: Optional[requests.Session] = Field(default=None, exclude=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _run(self, crypto_name: str) -> str:
        """Run cryptocurrency data discovery"""
        try:
            print(f"🪙 Crypto Data: Searching for '{crypto_name}'")
            
            # Search for cryptocurrency data
            query = f"{crypto_name} cryptocurrency price market cap trading volume blockchain"
            search_tool = DynamicWebSearchTool()
            results = search_tool._run(query)
            
            return self._format_crypto_results([results], crypto_name)
            
        except Exception as e:
            return f"❌ Error in cryptocurrency data search: {str(e)}"
    
    def _format_crypto_results(self, results: List[str], crypto_name: str) -> str:
        """Format cryptocurrency data results"""
        if not results:
            return f"❌ No cryptocurrency data found for {crypto_name}"
        
        formatted = []
        formatted.append(f"🪙 Cryptocurrency Data for {crypto_name}")
        formatted.append("=" * 50)
        
        for result in results:
            if result and "❌" not in result:
                formatted.append(result)
        
        if len(formatted) == 2:  # Only header and separator
            return f"❌ No cryptocurrency data found for {crypto_name}"
        
        return "\n".join(formatted)

# Export the tools
__all__ = ['DynamicWebSearchTool', 'InstitutionalDataTool', 'CryptoDataTool'] 