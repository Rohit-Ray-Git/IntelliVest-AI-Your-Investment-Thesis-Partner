#!/usr/bin/env python3
"""
Test script for Tavily integration in the market scanner
"""
import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tools.market_scanner_tool import DynamicMarketScannerTool

def test_tavily_integration():
    """Test the Tavily integration in the market scanner"""
    print("🌐 Testing Tavily Integration in Market Scanner")
    print("=" * 60)
    
    # Check API keys
    google_key = os.getenv("GOOGLE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    print(f"🔑 Google API Key: {'✅ Found' if google_key else '❌ Not found'}")
    print(f"🔑 Groq API Key: {'✅ Found' if groq_key else '❌ Not found'}")
    print(f"🔑 Tavily API Key: {'✅ Found' if tavily_key else '❌ Not found'}")
    
    if not tavily_key:
        print("❌ TAVILY_API_KEY not found. Please set it to test real web search.")
        return False
    
    try:
        print("\n🔧 Initializing Dynamic Market Scanner with Tavily...")
        scanner = DynamicMarketScannerTool(max_workers=3)
        
        # Check initialization
        print(f"🤖 Groq DeepSeek (Primary): {'✅ Available' if scanner.llm else '❌ Not available'}")
        print(f"🤖 Gemini 2.5 Flash (Fallback): {'✅ Available' if scanner.groq_llm else '❌ Not available'}")
        print(f"🌐 Tavily Client: {'✅ Available' if scanner.tavily_client else '❌ Not available'}")
        
        if not scanner.tavily_client:
            print("❌ Tavily client not available for testing")
            return False
        
        print("\n🔍 Testing Tavily web search functionality...")
        
        # Test direct Tavily search
        print("\n📊 Testing direct Tavily search...")
        web_results = scanner._tavily_web_search("trending Indian stocks today NSE BSE top gainers")
        print(f"🌐 Tavily returned {len(web_results)} web results")
        
        if web_results:
            print("📝 Sample web results:")
            for i, result in enumerate(web_results[:3], 1):
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                print(f"  {i}. {title}")
                print(f"     URL: {url}")
        
        # Test stock extraction from web content
        print("\n📊 Testing stock extraction from web content...")
        web_stocks = scanner._extract_stocks_from_web_content(web_results)
        print(f"📈 Extracted {len(web_stocks)} stocks from web content")
        if web_stocks:
            print(f"🔍 Sample stocks: {web_stocks[:10]}")
        
        # Test sector extraction from web content
        print("\n📊 Testing sector extraction from web content...")
        web_sectors = scanner._extract_sectors_from_web_content(web_results)
        print(f"📈 Extracted {len(web_sectors)} sectors from web content")
        if web_sectors:
            print("🔍 Sample sectors:")
            for symbol, name in list(web_sectors.items())[:5]:
                print(f"  - {symbol}: {name}")
        
        # Test integrated discovery
        print("\n🚀 Testing integrated discovery with Tavily and Groq DeepSeek...")
        
        # Test stock discovery
        print("\n📊 Testing stock discovery with Tavily and Groq DeepSeek...")
        discovered_stocks = scanner._discover_trending_stocks(days_back=3)
        print(f"📈 Discovered {len(discovered_stocks)} stocks")
        if discovered_stocks:
            print(f"🔍 Sample stocks: {discovered_stocks[:5]}")
        
        # Test sector discovery
        print("\n📊 Testing sector discovery with Tavily and Groq DeepSeek...")
        discovered_sectors = scanner._discover_sector_indices()
        print(f"📈 Discovered {len(discovered_sectors)} sectors")
        if discovered_sectors:
            print("🔍 Sample sectors:")
            for symbol, name in list(discovered_sectors.items())[:5]:
                print(f"  - {symbol}: {name}")
        
        # Test index discovery
        print("\n📊 Testing index discovery with Tavily and Groq DeepSeek...")
        discovered_indices = scanner._discover_market_indices()
        print(f"📈 Discovered {len(discovered_indices)} indices")
        if discovered_indices:
            print("🔍 Sample indices:")
            for symbol, name in list(discovered_indices.items())[:5]:
                print(f"  - {symbol}: {name}")
        
        # Test full market scan
        print("\n🚀 Testing full market scan with Tavily and Groq DeepSeek integration...")
        result = scanner._run(days_back=3)
        
        if "error" in result:
            print(f"❌ Market scan failed: {result['error']}")
            return False
        
        print("✅ Market scan completed successfully")
        print(f"📊 Scan date: {result.get('scan_date', 'N/A')}")
        print(f"📊 Discovery method: {result.get('discovery_method', 'N/A')}")
        
        top_stocks = result.get('top_performing_stocks', [])
        top_sectors = result.get('top_performing_sectors', [])
        
        print(f"📈 Top stocks found: {len(top_stocks)}")
        if top_stocks:
            print("🏆 Top 3 stocks:")
            for i, stock in enumerate(top_stocks[:3], 1):
                print(f"  {i}. {stock['symbol']} ({stock['name']}) - {stock['price_change_pct']:+.2f}% - Source: {stock['source']}")
        
        print(f"📈 Top sectors found: {len(top_sectors)}")
        if top_sectors:
            print("🏆 Top 3 sectors:")
            for i, sector in enumerate(top_sectors[:3], 1):
                print(f"  {i}. {sector['symbol']} ({sector['name']}) - {sector['price_change_pct']:+.2f}% - Source: {sector['source']}")
        
        # Check data sources
        groq_sources = [stock['source'] for stock in top_stocks if 'groq' in stock['source']]
        yfinance_sources = [stock['source'] for stock in top_stocks if 'yfinance' in stock['source']]
        
        print(f"\n📊 Data Source Analysis:")
        print(f"   - Groq DeepSeek-based data: {len(groq_sources)} stocks")
        print(f"   - yfinance fallback: {len(yfinance_sources)} stocks")
        print(f"   - Web search results: {len(web_results)} pages analyzed")
        
        if web_results:
            print("✅ Tavily integration working correctly!")
        else:
            print("⚠️ No web results found - check Tavily API key and quota")
        
        print("\n✅ All Tavily and Groq DeepSeek integration tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tavily_integration()
    sys.exit(0 if success else 1) 