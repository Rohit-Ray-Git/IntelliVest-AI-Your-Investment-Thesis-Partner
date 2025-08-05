#!/usr/bin/env python3
"""
Test script for the new Gemini 2.5 Flash based market scanner
"""

import os
import sys
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.market_scanner_tool import DynamicMarketScannerTool

def test_gemini_market_scanner():
    """Test the new Gemini 2.5 Flash based market scanner"""
    
    print("🧪 Testing Gemini 2.5 Flash Market Scanner")
    print("=" * 50)
    
    # Check if GOOGLE_API_KEY is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google API key:")
        print("export GOOGLE_API_KEY='your_api_key_here'")
        return False
    
    try:
        # Initialize the market scanner
        print("🔧 Initializing Dynamic Market Scanner...")
        scanner = DynamicMarketScannerTool(max_workers=5)
        
        if not scanner.llm:
            print("❌ Gemini 2.5 Flash not initialized properly")
            return False
        
        print("✅ Gemini 2.5 Flash initialized successfully")
        
        # Test the discovery methods
        print("\n🔍 Testing stock discovery...")
        discovered_stocks = scanner._discover_trending_stocks(days_back=5)
        print(f"📊 Discovered {len(discovered_stocks)} stocks")
        
        if discovered_stocks:
            print(f"🔍 Sample stocks: {discovered_stocks[:10]}")
        else:
            print("⚠️ No stocks discovered")
        
        # Test sector discovery
        print("\n🔍 Testing sector discovery...")
        discovered_sectors = scanner._discover_sector_indices()
        print(f"📊 Discovered {len(discovered_sectors)} sectors")
        
        if discovered_sectors:
            print(f"🔍 Sample sectors: {list(discovered_sectors.items())[:5]}")
        else:
            print("⚠️ No sectors discovered")
        
        # Test index discovery
        print("\n🔍 Testing index discovery...")
        discovered_indices = scanner._discover_market_indices()
        print(f"📊 Discovered {len(discovered_indices)} indices")
        
        if discovered_indices:
            print(f"🔍 Sample indices: {list(discovered_indices.items())[:5]}")
        else:
            print("⚠️ No indices discovered")
        
        # Test the full run
        print("\n🚀 Testing full market scan...")
        result = scanner._run(days_back=5)
        
        if "error" in result:
            print(f"❌ Market scan failed: {result['error']}")
            return False
        
        print("✅ Market scan completed successfully")
        print(f"📊 Scan date: {result.get('scan_date', 'N/A')}")
        print(f"📊 Discovery method: {result.get('discovery_method', 'N/A')}")
        print(f"📊 Market focus: {result.get('market_focus', 'N/A')}")
        
        # Check results
        top_stocks = result.get('top_performing_stocks', [])
        top_sectors = result.get('top_performing_sectors', [])
        
        print(f"📈 Top stocks found: {len(top_stocks)}")
        if top_stocks:
            print("🏆 Top 3 stocks:")
            for i, stock in enumerate(top_stocks[:3], 1):
                print(f"  {i}. {stock['symbol']} ({stock['name']}) - {stock['price_change_pct']:+.2f}%")
        
        print(f"📈 Top sectors found: {len(top_sectors)}")
        if top_sectors:
            print("🏆 Top 3 sectors:")
            for i, sector in enumerate(top_sectors[:3], 1):
                print(f"  {i}. {sector['symbol']} ({sector['name']}) - {sector['price_change_pct']:+.2f}%")
        
        # Check market insights
        insights = result.get('market_insights', {})
        print(f"🧠 Market sentiment: {insights.get('market_sentiment', 'N/A')}")
        print(f"🧠 Risk level: {insights.get('risk_level', 'N/A')}")
        
        # Check discovery stats
        stats = result.get('discovery_stats', {})
        print(f"📊 Stocks analyzed: {stats.get('stocks_analyzed', 0)}")
        print(f"📊 Sectors analyzed: {stats.get('sectors_analyzed', 0)}")
        print(f"📊 Indices analyzed: {stats.get('indices_analyzed', 0)}")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gemini_market_scanner()
    sys.exit(0 if success else 1) 