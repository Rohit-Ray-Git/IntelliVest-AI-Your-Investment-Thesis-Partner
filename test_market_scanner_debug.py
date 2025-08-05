#!/usr/bin/env python3
"""
🔍 Market Scanner Debug Test
============================

Simple test to debug the Indian market scanner and see what's happening
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.market_scanner_tool import DynamicMarketScannerTool

def test_market_scanner():
    """Test the market scanner and show detailed output"""
    print("🔍 Testing Indian Market Scanner...")
    print("=" * 50)
    
    try:
        # Create scanner instance
        scanner = DynamicMarketScannerTool()
        
        # Test the discovery process
        print("📊 Running market scan...")
        result = scanner._run(days_back=5)
        
        print("\n📈 Scan Results:")
        print("=" * 30)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return
        
        # Show scan info
        print(f"📅 Scan Date: {result.get('scan_date', 'N/A')}")
        print(f"📊 Days Analyzed: {result.get('days_analyzed', 'N/A')}")
        print(f"🎯 Market Focus: {result.get('market_focus', 'N/A')}")
        
        # Show discovery stats
        stats = result.get('discovery_stats', {})
        print(f"\n📊 Discovery Statistics:")
        print(f"   - Stocks Analyzed: {stats.get('stocks_analyzed', 0)}")
        print(f"   - Sectors Analyzed: {stats.get('sectors_analyzed', 0)}")
        print(f"   - Indices Analyzed: {stats.get('indices_analyzed', 0)}")
        
        # Show top stocks
        top_stocks = result.get('top_performing_stocks', [])
        print(f"\n🥇 Top Performing Stocks ({len(top_stocks)} found):")
        for i, stock in enumerate(top_stocks[:5], 1):
            print(f"   {i}. {stock.get('symbol', 'N/A')} - {stock.get('name', 'N/A')} ({stock.get('price_change_pct', 0):+.2f}%)")
        
        # Show top sectors
        top_sectors = result.get('top_performing_sectors', [])
        print(f"\n🏆 Top Performing Sectors ({len(top_sectors)} found):")
        for i, sector in enumerate(top_sectors[:5], 1):
            print(f"   {i}. {sector.get('name', 'N/A')} ({sector.get('price_change_pct', 0):+.2f}%)")
        
        # Show market insights
        insights = result.get('market_insights', {})
        print(f"\n💡 Market Insights:")
        print(f"   - Sentiment: {insights.get('market_sentiment', 'N/A')}")
        print(f"   - Risk Level: {insights.get('risk_level', 'N/A')}")
        print(f"   - Indian Focus: {insights.get('indian_market_focus', 'N/A')}")
        
        # Show market summary
        summary = result.get('market_summary', '')
        if summary:
            print(f"\n📋 Market Summary:")
            print(summary)
        
        print("\n✅ Market scanner test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_market_scanner() 