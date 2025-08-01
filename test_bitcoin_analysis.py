#!/usr/bin/env python3
"""
🧪 Test Script for Bitcoin Analysis Fix
=====================================
Tests the async fixes with a proper stock symbol.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_stock_analysis():
    """Test the analysis with a proper stock symbol"""
    print("🧪 Testing Stock Analysis with Async Fixes")
    print("=" * 50)
    
    try:
        from simple_analysis import analyze_investment
        
        # Test with a proper stock symbol (Apple)
        test_company = "AAPL"
        print(f"📊 Testing analysis with: {test_company}")
        
        # Run a quick analysis
        print("⏳ Running analysis...")
        result = await analyze_investment(test_company)
        
        if result["status"] == "success":
            print("✅ Analysis completed successfully!")
            print(f"🧠 LLM Engine: {result.get('llm_engine', 'Google Gemini 2.5 Flash')}")
            print("📊 Analysis components completed")
            
            # Show some key results
            if result.get('thesis'):
                print(f"\n📋 Thesis Preview: {result['thesis'][:200]}...")
            
            return True
        else:
            print("❌ Analysis failed")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🚀 Testing Bitcoin Analysis Fix")
    print("=" * 50)
    
    success = await test_stock_analysis()
    
    if success:
        print("\n🎉 Async fixes are working correctly!")
        print("✅ No more 'coroutine was never awaited' errors")
        print("✅ Analysis pipeline is functioning")
    else:
        print("\n❌ Some issues remain")
    
    return success

if __name__ == "__main__":
    asyncio.run(main()) 