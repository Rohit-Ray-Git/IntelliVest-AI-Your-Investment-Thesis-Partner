#!/usr/bin/env python3
"""
Test UI integration with optimized market scanner
"""
import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from production_integration import ProductionIntelliVestAI

def test_ui_integration():
    """Test the UI integration with the optimized market scanner"""
    print("🧪 Testing UI Integration with Optimized Market Scanner")
    print("=" * 60)
    
    try:
        print("\n🔧 Initializing Production System...")
        system = ProductionIntelliVestAI()
        
        print("\n📊 Testing Market Insights Integration...")
        start_time = datetime.now()
        
        # Test market insights (this is what the UI calls)
        market_data = system.get_market_insights(days_back=3)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        if "error" in market_data:
            print(f"❌ Market insights failed: {market_data['error']}")
            return False
        
        print(f"✅ Market insights loaded in {duration:.2f} seconds")
        print(f"📊 Scan date: {market_data.get('scan_date', 'N/A')}")
        
        # Check the structure that the UI expects
        top_stocks = market_data.get('top_performing_stocks', [])
        top_sectors = market_data.get('top_performing_sectors', [])
        market_insights = market_data.get('market_insights', {})
        
        print(f"\n📈 UI Data Structure Check:")
        print(f"   - Top stocks: {len(top_stocks)} found")
        print(f"   - Top sectors: {len(top_sectors)} found")
        print(f"   - Market insights: {'✅' if market_insights else '❌'}")
        
        # Display sample data for UI verification
        if top_stocks:
            print(f"\n🥇 Sample Top Stocks (UI will display):")
            for i, stock in enumerate(top_stocks[:3], 1):
                print(f"   {i}. {stock['symbol']} ({stock['name']}) - {stock['price_change_pct']:+.2f}% - Source: {stock.get('source', 'unknown')}")
        
        if top_sectors:
            print(f"\n🏆 Sample Top Sectors (UI will display):")
            for i, sector in enumerate(top_sectors[:3], 1):
                print(f"   {i}. {sector['symbol']} ({sector['name']}) - {sector['price_change_pct']:+.2f}% - Source: {sector.get('source', 'unknown')}")
        
        if market_insights:
            print(f"\n💡 Market Insights (UI will display):")
            print(f"   - Sentiment: {market_insights.get('market_sentiment', 'N/A')}")
            print(f"   - Risk Level: {market_insights.get('risk_level', 'N/A')}")
            print(f"   - Key Observations: {len(market_insights.get('key_observations', []))}")
        
        # Performance check
        if duration < 60:  # Should be under 60 seconds
            print(f"\n⚡ Performance: {duration:.2f}s (✅ Good - under 60s)")
        else:
            print(f"\n⚠️ Performance: {duration:.2f}s (Slow - over 60s)")
        
        print(f"\n✅ UI Integration Test Complete!")
        print(f"🚀 The Streamlit app should now display:")
        print(f"   - Top 3 stocks with performance cards")
        print(f"   - Top 3 sectors with performance cards")
        print(f"   - Market insights and sentiment")
        print(f"   - Performance metrics")
        print(f"   - Refresh button for updates")
        
        return True
        
    except Exception as e:
        print(f"❌ UI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ui_integration()
    sys.exit(0 if success else 1) 