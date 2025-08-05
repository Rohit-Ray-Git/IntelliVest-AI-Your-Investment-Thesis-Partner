#!/usr/bin/env python3
"""
Test script for the LLM fallback system (Gemini -> Groq -> yfinance)
"""
import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tools.market_scanner_tool import DynamicMarketScannerTool

def test_llm_fallback_system():
    """Test the LLM fallback system"""
    print("🧪 Testing LLM Fallback System")
    print("=" * 50)
    
    # Check API keys
    google_key = os.getenv("GOOGLE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    
    print(f"🔑 Google API Key: {'✅ Found' if google_key else '❌ Not found'}")
    print(f"🔑 Groq API Key: {'✅ Found' if groq_key else '❌ Not found'}")
    
    if not google_key and not groq_key:
        print("❌ No API keys found. Please set either GOOGLE_API_KEY or GROQ_API_KEY")
        return False
    
    try:
        print("\n🔧 Initializing Dynamic Market Scanner with LLM fallback...")
        scanner = DynamicMarketScannerTool(max_workers=3)
        
        # Check LLM initialization
        print(f"🤖 Gemini 2.5 Flash: {'✅ Available' if scanner.llm else '❌ Not available'}")
        print(f"🤖 Groq DeepSeek: {'✅ Available' if scanner.groq_llm else '❌ Not available'}")
        
        if not scanner.llm and not scanner.groq_llm:
            print("❌ No LLM available for testing")
            return False
        
        print("\n🔍 Testing LLM fallback system...")
        
        # Test stock discovery
        print("\n📊 Testing stock discovery with fallback...")
        discovered_stocks = scanner._discover_trending_stocks(days_back=3)
        print(f"📈 Discovered {len(discovered_stocks)} stocks")
        if discovered_stocks:
            print(f"🔍 Sample stocks: {discovered_stocks[:5]}")
        
        # Test sector discovery
        print("\n📊 Testing sector discovery with fallback...")
        discovered_sectors = scanner._discover_sector_indices()
        print(f"📈 Discovered {len(discovered_sectors)} sectors")
        if discovered_sectors:
            print(f"🔍 Sample sectors: {list(discovered_sectors.items())[:3]}")
        
        # Test index discovery
        print("\n📊 Testing index discovery with fallback...")
        discovered_indices = scanner._discover_market_indices()
        print(f"📈 Discovered {len(discovered_indices)} indices")
        if discovered_indices:
            print(f"🔍 Sample indices: {list(discovered_indices.items())[:3]}")
        
        # Test data fetching with fallback
        if discovered_stocks:
            print(f"\n📊 Testing data fetching with fallback for {discovered_stocks[0]}...")
            stock_data = scanner._get_stock_data_from_multiple_sources(discovered_stocks[0])
            if stock_data:
                print(f"✅ Data fetched successfully: {stock_data['name']} - {stock_data['price_change_pct']:+.2f}%")
                print(f"   Source: {stock_data['source']}")
            else:
                print("❌ Data fetching failed")
        
        # Test full market scan
        print("\n🚀 Testing full market scan with LLM fallback...")
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
        
        # Check fallback usage
        llm_sources = [stock['source'] for stock in top_stocks if 'llm' in stock['source']]
        yfinance_sources = [stock['source'] for stock in top_stocks if 'yfinance' in stock['source']]
        
        print(f"\n📊 Fallback Analysis:")
        print(f"   - LLM-based data: {len(llm_sources)} stocks")
        print(f"   - yfinance fallback: {len(yfinance_sources)} stocks")
        
        if llm_sources:
            print("✅ LLM fallback system working correctly!")
        else:
            print("⚠️ All data came from yfinance fallback - LLM may have failed")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_llm_fallback_system()
    sys.exit(0 if success else 1) 