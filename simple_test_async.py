#!/usr/bin/env python3
"""
🧪 Simple Async Test
==================
Very simple test to isolate the async issue.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def simple_test():
    """Simple test to check async functionality"""
    print("🧪 Simple Async Test")
    print("=" * 30)
    
    try:
        # Test 1: Basic import
        print("1. Testing import...")
        from tools.dynamic_search_tools import DynamicWebSearchTool
        print("✅ Import successful")
        
        # Test 2: Basic initialization
        print("2. Testing initialization...")
        tool = DynamicWebSearchTool()
        print("✅ Initialization successful")
        
        # Test 3: Basic async call
        print("3. Testing async call...")
        result = await tool._run("test query")
        print("✅ Async call successful")
        print(f"Result type: {type(result)}")
        print(f"Result length: {len(result)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    success = await simple_test()
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Tests failed!")
    return success

if __name__ == "__main__":
    asyncio.run(main()) 