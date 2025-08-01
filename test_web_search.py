#!/usr/bin/env python3
"""
Test Web Search Functionality
This script tests the web search tools to identify why they're returning Microsoft links.
"""

import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append('.')

async def test_web_search():
    """Test the web search functionality"""
    print("🔍 Testing Web Search Functionality")
    print("=" * 50)
    
    try:
        # Import the search tool
        from tools.dynamic_search_tools import DynamicWebSearchTool
        
        print("✅ DynamicWebSearchTool imported successfully")
        
        # Test with different queries
        test_queries = [
            "Tesla stock price financial data",
            "Apple Inc earnings report",
            "Bitcoin cryptocurrency price",
            "TCS Tata Consultancy Services financials"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: '{query}'")
            print("-" * 40)
            
            # Create search tool instance
            search_tool = DynamicWebSearchTool()
            
            # Test the search
            try:
                result = search_tool._run(query)
                print(f"✅ Search completed for: {query}")
                print(f"📝 Result preview: {result[:500]}...")
                
                # Check if result contains Microsoft links
                if "microsoft" in result.lower():
                    print("⚠️ WARNING: Result contains Microsoft links!")
                else:
                    print("✅ Result appears to be relevant")
                    
            except Exception as e:
                print(f"❌ Error in search: {e}")
                import traceback
                traceback.print_exc()
        
        # Test the website discovery function specifically
        print(f"\n🔍 Testing website discovery function")
        print("-" * 40)
        
        search_tool = DynamicWebSearchTool()
        test_query = "Tesla stock price"
        
        try:
            discovered_urls = search_tool._discover_websites(test_query)
            print(f"✅ Discovered {len(discovered_urls)} URLs")
            
            for i, url in enumerate(discovered_urls[:5], 1):
                print(f"  {i}. {url}")
                if "microsoft" in url.lower():
                    print("     ⚠️ WARNING: Microsoft URL detected!")
                elif "tesla" in url.lower() or "finance" in url.lower() or "stock" in url.lower():
                    print("     ✅ Relevant URL detected")
                else:
                    print("     ℹ️ Neutral URL")
                    
        except Exception as e:
            print(f"❌ Error in website discovery: {e}")
            import traceback
            traceback.print_exc()
        
        # Test the filtering function
        print(f"\n🔍 Testing URL filtering function")
        print("-" * 40)
        
        try:
            # Create some test URLs
            test_urls = [
                "https://www.microsoft.com/privacy",
                "https://finance.yahoo.com/quote/TSLA",
                "https://www.tesla.com/investors",
                "https://www.microsoft.com/services",
                "https://www.marketwatch.com/investing/stock/tsla",
                "https://www.microsoft.com/help"
            ]
            
            filtered_urls = search_tool._filter_financial_sites(test_urls)
            print(f"✅ Filtered {len(test_urls)} URLs to {len(filtered_urls)} financial URLs")
            
            for i, url in enumerate(filtered_urls, 1):
                print(f"  {i}. {url}")
                
        except Exception as e:
            print(f"❌ Error in URL filtering: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Error importing or testing web search: {e}")
        import traceback
        traceback.print_exc()

async def test_search_engines():
    """Test search engine functionality"""
    print(f"\n🔍 Testing Search Engine Functionality")
    print("=" * 50)
    
    try:
        import requests
        from bs4 import BeautifulSoup
        import time
        
        # Test different search engines
        search_engines = [
            ("Google", "https://www.google.com/search"),
            ("Bing", "https://www.bing.com/search"),
            ("Yahoo", "https://search.yahoo.com/search")
        ]
        
        test_query = "Tesla stock price"
        
        for engine_name, engine_url in search_engines:
            print(f"\n🔍 Testing {engine_name}")
            print("-" * 30)
            
            try:
                # Create session
                session = requests.Session()
                session.headers.update({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                })
                
                # Make request
                params = {'q': test_query, 'num': 5}
                response = session.get(engine_url, params=params, timeout=10)
                response.raise_for_status()
                
                print(f"✅ {engine_name} response status: {response.status_code}")
                print(f"📄 Response length: {len(response.text)} characters")
                
                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for links
                links = soup.find_all('a', href=True)
                print(f"🔗 Found {len(links)} links")
                
                # Show first few links
                for i, link in enumerate(links[:5], 1):
                    href = link['href']
                    print(f"  {i}. {href}")
                    if "microsoft" in href.lower():
                        print("     ⚠️ WARNING: Microsoft link detected!")
                
                time.sleep(2)  # Be respectful
                
            except Exception as e:
                print(f"❌ Error with {engine_name}: {e}")
                
    except Exception as e:
        print(f"❌ Error in search engine test: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function"""
    print("🚀 Web Search Functionality Test")
    print("=" * 60)
    
    # Test web search tools
    await test_web_search()
    
    # Test search engines
    await test_search_engines()
    
    print("\n" + "=" * 60)
    print("📊 TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 