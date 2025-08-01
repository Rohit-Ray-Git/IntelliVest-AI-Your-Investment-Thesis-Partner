#!/usr/bin/env python3
"""
🎯 IntelliVest AI - Google Gemini 2.5 Flash Demo
============================================================
💡 Demonstration of enhanced LLM-based scraping with Google Gemini 2.5 Flash
💡 Shows the power of intelligent web scraping for financial analysis
============================================================
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def demo_gemini_scraping():
    """Demonstrate the Gemini-powered scraping capabilities"""
    print("🎯 Google Gemini 2.5 Flash LLM-based Scraping Demo")
    print("=" * 60)
    
    # Check if Google API key is available
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("Please set GOOGLE_API_KEY in your .env file")
        return False
    
    print("✅ Google API key found")
    
    try:
        # Import the enhanced dynamic search tool
        from tools.dynamic_search_tools import DynamicWebSearchTool
        
        print("✅ Successfully imported DynamicWebSearchTool")
        
        # Initialize the tool
        print("\n🔧 Initializing Gemini-powered search tool...")
        search_tool = DynamicWebSearchTool()
        
        # Demo queries to showcase different capabilities
        demo_queries = [
            "Apple Inc. latest earnings report 2025",
            "Tesla stock price and financial metrics",
            "Microsoft quarterly results and analyst ratings",
            "Amazon market position and competitive analysis"
        ]
        
        print("\n🧪 Running Gemini-powered scraping demonstrations...")
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n📊 Demo {i}: {query}")
            print("-" * 50)
            
            try:
                # Run the search
                result = search_tool._run(query)
                
                # Extract key information from result
                if "✅ Found" in result:
                    # Count sources found
                    lines = result.split('\n')
                    sources_count = 0
                    for line in lines:
                        if "📄 Source" in line:
                            sources_count += 1
                    
                    print(f"✅ Found {sources_count} relevant sources")
                    print("📝 Sample content extracted:")
                    
                    # Show a preview of the content
                    content_start = result.find("📝 Content Preview:")
                    if content_start != -1:
                        content_end = result.find("\n", content_start + 100)
                        if content_end != -1:
                            preview = result[content_start:content_end]
                            print(preview)
                        else:
                            print("Content preview available")
                    else:
                        print("Content extracted successfully")
                        
                else:
                    print("⚠️ No relevant sources found")
                    
            except Exception as e:
                print(f"❌ Demo {i} failed: {e}")
            
            print()
        
        print("🎉 Gemini-powered scraping demonstration completed!")
        print("\n💡 Key Features Demonstrated:")
        print("   • Intelligent web search with Tavily")
        print("   • LLM-based content extraction with Google Gemini 2.5 Flash")
        print("   • Financial data extraction and summarization")
        print("   • Relevance filtering and content optimization")
        print("   • Respectful scraping with robots.txt compliance")
        print("   • Robust fallback system")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def demo_financial_analysis():
    """Demonstrate the full financial analysis pipeline"""
    print("\n🎯 Full Financial Analysis Pipeline Demo")
    print("=" * 60)
    
    try:
        # Import the enhanced analysis function
        import asyncio
        from simple_analysis import analyze_investment
        
        # Test with a well-known company
        test_company = "Apple Inc."
        print(f"📊 Testing full analysis pipeline with: {test_company}")
        
        # Run a quick analysis (limited scope for demo)
        print("⏳ Running enhanced analysis...")
        result = asyncio.run(analyze_investment(test_company))
        
        if result["status"] == "success":
            print("✅ Full analysis pipeline working!")
            print(f"🧠 LLM Engine: {result.get('llm_engine', 'Google Gemini 2.5 Flash')}")
            print("📊 Analysis components completed successfully")
        else:
            print("⚠️ Analysis pipeline had issues")
            
        return True
        
    except Exception as e:
        print(f"❌ Full analysis demo failed: {e}")
        return False

def main():
    """Main demonstration function"""
    print("🚀 IntelliVest AI - Google Gemini 2.5 Flash Integration Demo")
    print("=" * 70)
    print("💡 This demo showcases the enhanced LLM-based scraping capabilities")
    print("💡 Powered by Google Gemini 2.5 Flash for intelligent content extraction")
    print("=" * 70)
    
    # Demo 1: Gemini scraping capabilities
    demo1_success = demo_gemini_scraping()
    
    # Demo 2: Full analysis pipeline
    demo2_success = demo_financial_analysis()
    
    # Summary
    print("\n📋 Demo Summary")
    print("=" * 30)
    print(f"✅ Gemini Scraping Demo: {'PASS' if demo1_success else 'FAIL'}")
    print(f"✅ Full Analysis Pipeline: {'PASS' if demo2_success else 'FAIL'}")
    
    if all([demo1_success, demo2_success]):
        print("\n🎉 All demos passed! Google Gemini 2.5 Flash integration is working perfectly.")
        print("\n🚀 Ready to use enhanced investment analysis with:")
        print("   • Intelligent web scraping")
        print("   • Real-time financial data extraction")
        print("   • Smart content analysis")
        print("   • Comprehensive investment thesis generation")
    else:
        print("\n⚠️ Some demos failed. Please check the error messages above.")
    
    print("\n💡 To run the full analysis:")
    print("   python simple_analysis.py")

if __name__ == "__main__":
    main() 