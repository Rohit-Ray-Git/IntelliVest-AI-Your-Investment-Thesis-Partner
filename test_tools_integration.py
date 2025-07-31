"""
🧪 Test Custom Tools Integration
================================

This script tests the custom tools before integrating them with CrewAI.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_tools_import():
    """Test if custom tools can be imported"""
    print("🔍 Testing tools import...")
    
    try:
        from tools.investment_tools import (
            WebCrawlerTool,
            FinancialDataTool,
            SentimentAnalysisTool,
            ValuationTool,
            ThesisGenerationTool,
            CritiqueTool
        )
        print("✅ All custom tools imported successfully")
        return True
    except Exception as e:
        print(f"❌ Tools import failed: {e}")
        return False

def test_financial_data_tool():
    """Test the financial data tool"""
    print("\n📊 Testing Financial Data Tool...")
    
    try:
        from tools.investment_tools import FinancialDataTool
        
        tool = FinancialDataTool()
        result = tool._run("AAPL")
        
        if "Financial Data Summary" in result:
            print("✅ Financial data tool working correctly")
            print(f"📝 Result length: {len(result)} characters")
            return True
        else:
            print(f"❌ Financial data tool returned unexpected result: {result[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ Financial data tool test failed: {e}")
        return False

def test_web_crawler_tool():
    """Test the web crawler tool"""
    print("\n🕷️ Testing Web Crawler Tool...")
    
    try:
        from tools.investment_tools import WebCrawlerTool
        
        tool = WebCrawlerTool()
        # Test with a simple company name
        result = tool._run("Apple")
        
        if "crawled" in result.lower() or "content" in result.lower():
            print("✅ Web crawler tool working correctly")
            print(f"📝 Result length: {len(result)} characters")
            return True
        else:
            print(f"❌ Web crawler tool returned unexpected result: {result[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ Web crawler tool test failed: {e}")
        return False

def test_sentiment_analysis_tool():
    """Test the sentiment analysis tool"""
    print("\n🧠 Testing Sentiment Analysis Tool...")
    
    try:
        from tools.investment_tools import SentimentAnalysisTool
        
        tool = SentimentAnalysisTool()
        # Test with sample text
        test_text = "Apple Inc. reported strong quarterly earnings with revenue growth of 15%. The company's new products are performing well in the market."
        result = tool._run(test_text)
        
        if "Sentiment Analysis Results" in result:
            print("✅ Sentiment analysis tool working correctly")
            print(f"📝 Result length: {len(result)} characters")
            return True
        else:
            print(f"❌ Sentiment analysis tool returned unexpected result: {result[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ Sentiment analysis tool test failed: {e}")
        return False

def test_crew_with_tools():
    """Test CrewAI with tools"""
    print("\n🤖 Testing CrewAI with Tools...")
    
    try:
        from agents.crew_agents_with_tools import InvestmentAnalysisCrewWithTools
        
        # Create crew with tools
        crew = InvestmentAnalysisCrewWithTools()
        print("✅ CrewAI with tools created successfully")
        
        # Test agent creation
        agents = [
            crew.researcher,
            crew.sentiment_analyst,
            crew.valuation_analyst,
            crew.thesis_writer,
            crew.critic
        ]
        print(f"✅ Successfully created {len(agents)} agents with tools")
        
        # Test task creation
        tasks = crew.create_tasks("Apple Inc.")
        print(f"✅ Successfully created {len(tasks)} tasks")
        
        # Check if tools are available
        tools_count = len(crew.tools) if crew.tools else 0
        print(f"✅ Tools available: {tools_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ CrewAI with tools test failed: {e}")
        return False

def main():
    """Run all tool tests"""
    print("🚀 Testing Custom Tools Integration\n")
    print("=" * 50)
    
    tests = [
        ("Tools Import Test", test_tools_import),
        ("Financial Data Tool Test", test_financial_data_tool),
        ("Web Crawler Tool Test", test_web_crawler_tool),
        ("Sentiment Analysis Tool Test", test_sentiment_analysis_tool),
        ("CrewAI with Tools Test", test_crew_with_tools)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tool tests passed! Ready for full integration.")
        print("\n🚀 Next steps:")
        print("1. Test full agentic analysis with tools")
        print("2. Create LangGraph workflows")
        print("3. Build fallback systems")
    else:
        print("⚠️ Some tool tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 