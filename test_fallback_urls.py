#!/usr/bin/env python3
"""
Test Fallback URLs
This script tests the fallback financial URLs to ensure they work correctly.
"""

import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append('.')

async def test_fallback_urls():
    """Test the fallback financial URLs"""
    print("🔍 Testing Fallback Financial URLs")
    print("=" * 50)
    
    try:
        from tools.dynamic_search_tools import DynamicWebSearchTool
        
        print("✅ DynamicWebSearchTool imported successfully")
        
        # Create search tool
        search_tool = DynamicWebSearchTool()
        
        # Test different queries
        test_queries = [
            "Tesla stock price",
            "Apple Inc earnings",
            "Bitcoin cryptocurrency",
            "TCS Tata Consultancy"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: '{query}'")
            print("-" * 40)
            
            # Get fallback URLs
            fallback_urls = search_tool._get_fallback_financial_sites(query)
            print(f"✅ Found {len(fallback_urls)} fallback URLs")
            
            for i, url in enumerate(fallback_urls[:3], 1):  # Test first 3 URLs
                print(f"  {i}. {url}")
                
                try:
                    # Test if URL is accessible
                    response = search_tool.session.get(url, timeout=10)
                    if response.status_code == 200:
                        print(f"     ✅ Accessible (Status: {response.status_code})")
                        
                        # Check if content is relevant
                        soup = BeautifulSoup(response.text, 'html.parser')
                        content = search_tool._extract_relevant_content(soup, query)
                        
                        if content:
                            print(f"     ✅ Content extracted ({len(content)} chars)")
                            if search_tool._is_content_relevant(content, query):
                                print(f"     ✅ Content is relevant")
                            else:
                                print(f"     ⚠️ Content not relevant")
                        else:
                            print(f"     ⚠️ No content extracted")
                    else:
                        print(f"     ❌ Not accessible (Status: {response.status_code})")
                        
                except Exception as e:
                    print(f"     ❌ Error accessing: {e}")
                
                # Be respectful with delays
                import time
                time.sleep(1)
        
        # Test the full discovery process
        print(f"\n🔍 Testing Full Discovery Process")
        print("-" * 40)
        
        test_query = "Tesla stock price"
        discovered_urls = search_tool._discover_websites(test_query)
        print(f"✅ Discovered {len(discovered_urls)} URLs")
        
        for i, url in enumerate(discovered_urls[:5], 1):
            print(f"  {i}. {url}")
        
        # Test filtering
        filtered_urls = search_tool._filter_financial_sites(discovered_urls)
        print(f"✅ Filtered to {len(filtered_urls)} financial URLs")
        
        for i, url in enumerate(filtered_urls[:5], 1):
            print(f"  {i}. {url}")
            
    except Exception as e:
        print(f"❌ Error in test: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function"""
    print("🚀 Fallback URLs Test")
    print("=" * 60)
    
    # Test fallback URLs
    await test_fallback_urls()
    
    print("\n" + "=" * 60)
    print("📊 TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 