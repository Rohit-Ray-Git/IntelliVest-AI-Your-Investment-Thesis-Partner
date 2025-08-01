#!/usr/bin/env python3
"""
Test Tavily Integration
This script tests the Tavily integration to ensure it's working correctly.
"""

import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append('.')

async def test_tavily_integration():
    """Test the Tavily integration"""
    print("🔍 Testing Tavily Integration")
    print("=" * 50)
    
    try:
        from tools.dynamic_search_tools import DynamicWebSearchTool
        
        print("✅ DynamicWebSearchTool imported successfully")
        
        # Check if Tavily is available
        from tools.dynamic_search_tools import TAVILY_AVAILABLE, tavily_client
        print(f"✅ Tavily Available: {TAVILY_AVAILABLE}")
        print(f"✅ Tavily Client: {tavily_client is not None}")
        
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
            
            try:
                # Test Tavily search directly
                if TAVILY_AVAILABLE and tavily_client:
                    print("🔍 Testing Tavily search...")
                    urls = search_tool._tavily_search(query)
                    
                    if urls:
                        print(f"✅ Tavily found {len(urls)} URLs")
                        for i, url in enumerate(urls[:5], 1):
                            print(f"  {i}. {url}")
                            
                            # Check if URL is relevant
                            if any(keyword in url.lower() for keyword in ['finance', 'stock', 'market', 'investing', 'yahoo', 'bloomberg', 'reuters']):
                                print("     ✅ Relevant financial URL")
                            elif any(keyword in url.lower() for keyword in ['microsoft', 'google', 'yahoo.com']):
                                print("     ⚠️ Potentially irrelevant URL")
                            else:
                                print("     ℹ️ Neutral URL")
                    else:
                        print("❌ No URLs found from Tavily")
                else:
                    print("❌ Tavily not available")
                
                # Test the full search process
                print(f"\n🔍 Testing full search process...")
                result = search_tool._run(query)
                
                print(f"✅ Search completed")
                print(f"📝 Result preview: {result[:300]}...")
                
                # Check if result contains relevant information
                if "✅ Found" in result and "❌ No relevant content" not in result:
                    print("✅ Search returned relevant content")
                else:
                    print("⚠️ Search may not have returned relevant content")
                    
            except Exception as e:
                print(f"❌ Error testing query '{query}': {e}")
                import traceback
                traceback.print_exc()
        
        # Test Tavily API directly
        print(f"\n🔍 Testing Tavily API Directly")
        print("-" * 40)
        
        if TAVILY_AVAILABLE and tavily_client:
            try:
                test_query = "Tesla stock price financial data"
                print(f"Testing direct Tavily API with: '{test_query}'")
                
                results = tavily_client.search(
                    query=test_query,
                    search_depth="advanced",
                    max_results=5,
                    include_domains=[
                        "finance.yahoo.com", "marketwatch.com", "investing.com", 
                        "seekingalpha.com", "bloomberg.com", "reuters.com"
                    ]
                )
                
                print(f"✅ Direct Tavily API call successful")
                print(f"📊 Results structure: {list(results.keys()) if results else 'No results'}")
                
                if results and "results" in results:
                    print(f"📄 Found {len(results['results'])} results")
                    for i, result in enumerate(results['results'][:3], 1):
                        print(f"  {i}. {result.get('url', 'No URL')}")
                        print(f"     Title: {result.get('title', 'No title')[:50]}...")
                else:
                    print("❌ No results from direct Tavily API call")
                    
            except Exception as e:
                print(f"❌ Error with direct Tavily API: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ Tavily not available for direct API test")
            
    except Exception as e:
        print(f"❌ Error in Tavily integration test: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function"""
    print("🚀 Tavily Integration Test")
    print("=" * 60)
    
    # Test Tavily integration
    await test_tavily_integration()
    
    print("\n" + "=" * 60)
    print("📊 TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 