#!/usr/bin/env python3
"""
🧪 Test Script for Async Playwright Fix
=====================================
Tests that the async Playwright integration is working correctly.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_async_playwright():
    """Test the async Playwright integration"""
    print("🧪 Testing Async Playwright Integration")
    print("=" * 50)
    
    try:
        from tools.dynamic_search_tools import DynamicWebSearchTool
        
        print("✅ Successfully imported DynamicWebSearchTool")
        
        # Initialize the tool
        print("🔧 Initializing tool...")
        search_tool = DynamicWebSearchTool()
        print("✅ Tool initialized successfully")
        
        # Test with a simple query
        test_query = "Apple Inc. stock price"
        print(f"🔍 Testing async search: '{test_query}'")
        
        result = await search_tool._run(test_query)
        
        print("✅ Async search completed successfully!")
        print(f"📊 Result length: {len(result)} characters")
        
        if "✅ Found" in result:
            print("✅ Found relevant sources!")
        else:
            print("⚠️ No sources found, but no errors occurred")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🚀 Testing Async Playwright Fix")
    print("=" * 50)
    
    success = await test_async_playwright()
    
    if success:
        print("\n🎉 Async Playwright fix is working correctly!")
        print("✅ No more 'Sync API inside asyncio loop' errors")
    else:
        print("\n❌ Async Playwright fix needs more work")
    
    return success

if __name__ == "__main__":
    asyncio.run(main()) 