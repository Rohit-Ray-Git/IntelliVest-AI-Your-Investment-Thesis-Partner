#!/usr/bin/env python3
"""
🧪 Test Script for Google Gemini 2.5 Flash Integration
=====================================================

This script tests the LLM-based scraping functionality with Google Gemini.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_integration():
    """Test the Gemini integration and LLM-based scraping"""
    print("🧪 Testing Google Gemini 2.5 Flash Integration")
    print("=" * 60)
    
    # Check if Google API key is available
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("Please set GOOGLE_API_KEY in your .env file")
        return False
    
    print("✅ Google API key found")
    
    try:
        # Import the dynamic search tool
        from tools.dynamic_search_tools import DynamicWebSearchTool
        
        print("✅ Successfully imported DynamicWebSearchTool")
        
        # Initialize the tool
        print("\n🔧 Initializing DynamicWebSearchTool...")
        search_tool = DynamicWebSearchTool()
        
        # Test a simple financial query
        test_query = "Apple Inc. stock price and financial metrics"
        print(f"\n🔍 Testing with query: '{test_query}'")
        
        # Run the search
        print("⏳ Running LLM-based web search...")
        result = search_tool._run(test_query)
        
        print("\n📊 Search Results:")
        print("-" * 40)
        print(result)
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_gemini_api_directly():
    """Test Gemini API directly"""
    print("\n🧪 Testing Gemini API Directly")
    print("=" * 40)
    
    try:
        import google.generativeai as genai
        
        # Configure Gemini
        google_api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=google_api_key)
        
        # Create model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Test prompt
        test_prompt = """
        Extract financial metrics from this text:
        Apple Inc. reported revenue of $394.3 billion in 2023, with a market cap of $2.8 trillion and P/E ratio of 28.5.
        The company's stock price is $150.25 per share.
        """
        
        print("📝 Testing Gemini with financial data extraction...")
        response = model.generate_content(test_prompt)
        
        print("✅ Gemini API Response:")
        print("-" * 30)
        print(response.text)
        
        return True
        
    except Exception as e:
        print(f"❌ Direct Gemini API test failed: {e}")
        return False

def test_playwright_setup():
    """Test Playwright setup"""
    print("\n🧪 Testing Playwright Setup")
    print("=" * 30)
    
    try:
        from playwright.sync_api import sync_playwright
        
        print("✅ Playwright imported successfully")
        
        # Test browser launch
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            print("✅ Browser launched successfully")
            
            page = browser.new_page()
            print("✅ Page created successfully")
            
            # Test navigation
            page.goto("https://finance.yahoo.com/quote/AAPL", timeout=10000)
            title = page.title()
            print(f"✅ Navigation successful - Page title: {title}")
            
            page.close()
            browser.close()
            print("✅ Browser closed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Playwright test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Gemini Integration Tests")
    print("=" * 60)
    
    # Test 1: Direct Gemini API
    test1_success = test_gemini_api_directly()
    
    # Test 2: Playwright setup
    test2_success = test_playwright_setup()
    
    # Test 3: Full integration
    test3_success = test_gemini_integration()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 30)
    print(f"✅ Direct Gemini API: {'PASS' if test1_success else 'FAIL'}")
    print(f"✅ Playwright Setup: {'PASS' if test2_success else 'FAIL'}")
    print(f"✅ Full Integration: {'PASS' if test3_success else 'FAIL'}")
    
    if all([test1_success, test2_success, test3_success]):
        print("\n🎉 All tests passed! Gemini integration is working correctly.")
        return True
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 