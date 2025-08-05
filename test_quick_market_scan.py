#!/usr/bin/env python3
"""
Quick test for optimized market scanner - top 3 stocks and sectors only
"""
import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tools.market_scanner_tool import DynamicMarketScannerTool

def test_quick_market_scan():
    """Test the optimized market scanner for quick results"""
    print("⚡ Testing Quick Market Scanner (Top 3 Only)")
    print("=" * 50)
    
    # Check API keys
    groq_key = os.getenv("GROQ_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    print(f"🔑 Groq API Key: {'✅ Found' if groq_key else '❌ Not found'}")
    print(f"🔑 Google API Key: {'✅ Found' if google_key else '❌ Not found'}")
    
    if not groq_key:
        print("❌ GROQ_API_KEY not found. Please set it to test.")
        return False
    
    try:
        print("\n🔧 Initializing Quick Market Scanner...")
        scanner = DynamicMarketScannerTool(max_workers=3)
        
        # Check initialization
        print(f"🤖 Groq DeepSeek (Primary): {'✅ Available' if scanner.llm else '❌ Not available'}")
        print(f"🤖 Gemini 2.5 Flash (Fallback): {'✅ Available' if scanner.groq_llm else '❌ Not available'}")
        
        if not scanner.llm:
            print("❌ No LLM available for testing")
            return False
        
        print("\n🚀 Running quick market scan...")
        start_time = datetime.now()
        
        result = scanner._run(days_back=3)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        if "error" in result:
            print(f"❌ Market scan failed: {result['error']}")
            return False
        
        print(f"✅ Quick market scan completed in {duration:.2f} seconds!")
        print(f"📊 Scan date: {result.get('scan_date', 'N/A')}")
        
        top_stocks = result.get('top_performing_stocks', [])
        top_sectors = result.get('top_performing_sectors', [])
        
        print(f"\n📈 Top 3 Stocks Found: {len(top_stocks)}")
        if top_stocks:
            for i, stock in enumerate(top_stocks, 1):
                print(f"  {i}. {stock['symbol']} ({stock['name']}) - {stock['price_change_pct']:+.2f}% - Source: {stock['source']}")
        
        print(f"\n📈 Top 3 Sectors Found: {len(top_sectors)}")
        if top_sectors:
            for i, sector in enumerate(top_sectors, 1):
                print(f"  {i}. {sector['symbol']} ({sector['name']}) - {sector['price_change_pct']:+.2f}% - Source: {sector['source']}")
        
        # Check data sources
        groq_sources = [stock['source'] for stock in top_stocks if 'groq' in stock['source']]
        yfinance_sources = [stock['source'] for stock in top_stocks if 'yfinance' in stock['source']]
        
        print(f"\n📊 Data Source Summary:")
        print(f"   - Groq DeepSeek data: {len(groq_sources)} stocks")
        print(f"   - yfinance fallback: {len(yfinance_sources)} stocks")
        
        print(f"\n⚡ Performance: {duration:.2f} seconds for top 3 stocks and sectors")
        print("✅ Quick market scanner working efficiently!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_quick_market_scan()
    sys.exit(0 if success else 1) 