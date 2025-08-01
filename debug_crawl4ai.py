#!/usr/bin/env python3
"""
Debug Crawl4AI Issue
This script debugs why crawl4ai is returning Microsoft links instead of discovered URLs.
"""

import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append('.')

async def debug_crawl4ai():
    """Debug the crawl4ai issue"""
    print("🔍 Debugging Crawl4AI Issue")
    print("=" * 50)
    
    try:
        from tools.dynamic_search_tools import DynamicWebSearchTool
        
        print("✅ DynamicWebSearchTool imported successfully")
        
        # Create search tool
        search_tool = DynamicWebSearchTool()
        
        # Test query
        test_query = "Tesla stock price"
        
        print(f"\n🔍 Testing with query: '{test_query}'")
        print("-" * 40)
        
        # Step 1: Discover websites
        print("📡 Step 1: Discovering websites...")
        discovered_urls = search_tool._discover_websites(test_query)
        print(f"✅ Discovered {len(discovered_urls)} URLs")
        
        for i, url in enumerate(discovered_urls[:5], 1):
            print(f"  {i}. {url}")
        
        # Step 2: Filter financial sites
        print(f"\n🔍 Step 2: Filtering financial sites...")
        filtered_urls = search_tool._filter_financial_sites(discovered_urls)
        print(f"✅ Filtered to {len(filtered_urls)} financial URLs")
        
        for i, url in enumerate(filtered_urls[:5], 1):
            print(f"  {i}. {url}")
        
        # Step 3: Test crawl4ai directly with discovered URLs
        print(f"\n🔍 Step 3: Testing crawl4ai with discovered URLs...")
        
        if filtered_urls:
            test_url = filtered_urls[0]
            print(f"Testing crawl4ai with URL: {test_url}")
            
            try:
                # Test crawl4ai directly
                if search_tool.crawler:
                    print("✅ Crawler is available")
                    
                    # Test the crawl4ai call
                    result = await search_tool._scrape_with_crawl4ai(test_url)
                    
                    print(f"✅ Crawl4AI result:")
                    print(f"  URL: {result.get('url')}")
                    print(f"  Success: {result.get('success')}")
                    print(f"  Title: {result.get('title', 'No title')[:100]}...")
                    print(f"  Content length: {len(result.get('content', ''))}")
                    
                    if result.get('content'):
                        content_preview = result.get('content', '')[:200]
                        print(f"  Content preview: {content_preview}...")
                        
                        # Check if content contains Microsoft
                        if "microsoft" in content_preview.lower():
                            print("⚠️ WARNING: Content contains Microsoft!")
                        else:
                            print("✅ Content appears relevant")
                    
                else:
                    print("❌ Crawler is not available")
                    
            except Exception as e:
                print(f"❌ Error testing crawl4ai: {e}")
                import traceback
                traceback.print_exc()
        
        # Step 4: Test the full scraping function
        print(f"\n🔍 Step 4: Testing full scraping function...")
        
        try:
            # Use only the first 3 URLs to avoid too many requests
            test_urls = filtered_urls[:3] if filtered_urls else []
            
            if test_urls:
                print(f"Testing with URLs: {test_urls}")
                
                # Test the scraping function
                scraped_content = search_tool._scrape_discovered_sites(test_urls, test_query)
                
                print(f"✅ Scraped {len(scraped_content)} content items")
                
                for i, item in enumerate(scraped_content, 1):
                    print(f"\n  Item {i}:")
                    print(f"    URL: {item.get('url')}")
                    print(f"    Success: {item.get('success')}")
                    print(f"    Title: {item.get('title', 'No title')[:50]}...")
                    
                    if item.get('content'):
                        content_preview = item.get('content', '')[:100]
                        print(f"    Content preview: {content_preview}...")
                        
                        if "microsoft" in content_preview.lower():
                            print("    ⚠️ WARNING: Content contains Microsoft!")
                        else:
                            print("    ✅ Content appears relevant")
            else:
                print("❌ No URLs to test")
                
        except Exception as e:
            print(f"❌ Error in full scraping test: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Error in debug: {e}")
        import traceback
        traceback.print_exc()

async def test_crawl4ai_directly():
    """Test crawl4ai directly without our wrapper"""
    print(f"\n🔍 Testing Crawl4AI Directly")
    print("=" * 50)
    
    try:
        from crawl4ai import AsyncWebCrawler
        
        print("✅ Crawl4AI imported successfully")
        
        # Create crawler
        crawler = AsyncWebCrawler()
        print("✅ Crawler created successfully")
        
        # Test with a known financial URL
        test_url = "https://finance.yahoo.com/quote/TSLA"
        print(f"Testing with URL: {test_url}")
        
        try:
            result = await crawler.arun(test_url)
            print(f"✅ Crawl4AI result:")
            print(f"  URL: {test_url}")
            print(f"  Raw HTML length: {len(result.raw_html) if result.raw_html else 0}")
            print(f"  Cleaned HTML length: {len(result.cleaned_html) if result.cleaned_html else 0}")
            print(f"  Metadata: {result.metadata}")
            
            if result.cleaned_html:
                content_preview = result.cleaned_html[:200]
                print(f"  Content preview: {content_preview}...")
                
                if "microsoft" in content_preview.lower():
                    print("⚠️ WARNING: Content contains Microsoft!")
                elif "tesla" in content_preview.lower() or "yahoo" in content_preview.lower():
                    print("✅ Content appears relevant")
                else:
                    print("ℹ️ Content appears neutral")
                    
        except Exception as e:
            print(f"❌ Error with crawl4ai: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Error importing crawl4ai: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main debug function"""
    print("🚀 Crawl4AI Debug Test")
    print("=" * 60)
    
    # Debug our tool
    await debug_crawl4ai()
    
    # Test crawl4ai directly
    await test_crawl4ai_directly()
    
    print("\n" + "=" * 60)
    print("📊 DEBUG COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 