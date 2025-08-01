"""
🧪 Test New Agent System - Comprehensive Testing
==============================================

This script tests the new separate agent files and dynamic web search capabilities
to ensure all components are working correctly.
"""

import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path for imports
sys.path.append('.')

def test_imports():
    """Test that all modules can be imported successfully"""
    print("🔍 Testing module imports...")
    
    try:
        # Test agent imports
        from agents.research_agent import ResearchAgent
        from agents.sentiment_agent import SentimentAgent
        from agents.valuation_agent import ValuationAgent
        from agents.thesis_agent import ThesisAgent
        from agents.critique_agent import CritiqueAgent
        from agents.crypto_agent import CryptoAgent
        from agents.crew_orchestrator import CrewOrchestrator
        
        # Test tool imports
        from tools.dynamic_search_tools import DynamicWebSearchTool, InstitutionalDataTool, CryptoDataTool
        from tools.investment_tools import WebCrawlerTool, FinancialDataTool, SentimentAnalysisTool, ValuationTool, ThesisGenerationTool, CritiqueTool
        
        # Test LLM imports
        from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType
        
        print("✅ All modules imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_agent_initialization():
    """Test that all agents can be initialized"""
    print("🚀 Testing agent initialization...")
    
    try:
        # Initialize all agents
        research_agent = ResearchAgent()
        sentiment_agent = SentimentAgent()
        valuation_agent = ValuationAgent()
        thesis_agent = ThesisAgent()
        critique_agent = CritiqueAgent()
        crypto_agent = CryptoAgent()
        crew_orchestrator = CrewOrchestrator()
        
        print("✅ All agents initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization error: {e}")
        return False

def test_tool_initialization():
    """Test that all tools can be initialized"""
    print("🛠️ Testing tool initialization...")
    
    try:
        # Initialize all tools
        dynamic_search_tool = DynamicWebSearchTool()
        institutional_data_tool = InstitutionalDataTool()
        crypto_data_tool = CryptoDataTool()
        web_crawler_tool = WebCrawlerTool()
        financial_data_tool = FinancialDataTool()
        sentiment_analysis_tool = SentimentAnalysisTool()
        valuation_tool = ValuationTool()
        thesis_generation_tool = ThesisGenerationTool()
        critique_tool = CritiqueTool()
        
        print("✅ All tools initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Tool initialization error: {e}")
        return False

def test_llm_system():
    """Test the advanced fallback system"""
    print("🧠 Testing LLM system...")
    
    try:
        # Initialize advanced fallback system
        fallback_system = AdvancedFallbackSystem()
        
        # Test system status
        status = fallback_system.get_system_status()
        print(f"✅ LLM system status: {status['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM system error: {e}")
        return False

async def test_dynamic_search():
    """Test dynamic web search functionality"""
    print("🔍 Testing dynamic web search...")
    
    try:
        from tools.dynamic_search_tools import DynamicWebSearchTool
        
        search_tool = DynamicWebSearchTool()
        
        # Test a simple search
        test_query = "Apple Inc latest news financial"
        print(f"🔍 Testing search: {test_query}")
        
        result = search_tool._run(test_query)
        
        if result and "✅" in result:
            print("✅ Dynamic search working successfully")
            print(f"📊 Result preview: {result[:200]}...")
            return True
        else:
            print("⚠️ Dynamic search returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Dynamic search error: {e}")
        return False

async def test_research_agent():
    """Test research agent functionality"""
    print("🔍 Testing research agent...")
    
    try:
        from agents.research_agent import ResearchAgent
        
        research_agent = ResearchAgent()
        
        # Test research on a well-known company
        test_company = "Apple"
        print(f"🔍 Testing research on: {test_company}")
        
        research_data = await research_agent.research_company(test_company)
        
        if research_data and research_data.get("company_name"):
            print("✅ Research agent working successfully")
            print(f"📊 Research data keys: {list(research_data.keys())}")
            return True
        else:
            print("⚠️ Research agent returned no data")
            return False
            
    except Exception as e:
        print(f"❌ Research agent error: {e}")
        return False

async def test_sentiment_agent():
    """Test sentiment agent functionality"""
    print("🧠 Testing sentiment agent...")
    
    try:
        from agents.sentiment_agent import SentimentAgent
        
        sentiment_agent = SentimentAgent()
        
        # Test sentiment analysis
        test_company = "Tesla"
        print(f"🧠 Testing sentiment analysis on: {test_company}")
        
        sentiment_data = await sentiment_agent.analyze_sentiment(test_company)
        
        if sentiment_data and sentiment_data.get("company_name"):
            print("✅ Sentiment agent working successfully")
            print(f"📊 Sentiment data keys: {list(sentiment_data.keys())}")
            return True
        else:
            print("⚠️ Sentiment agent returned no data")
            return False
            
    except Exception as e:
        print(f"❌ Sentiment agent error: {e}")
        return False

async def test_crew_orchestrator():
    """Test crew orchestrator functionality"""
    print("🚀 Testing crew orchestrator...")
    
    try:
        from agents.crew_orchestrator import CrewOrchestrator
        
        crew_orchestrator = CrewOrchestrator()
        
        # Test agent status
        status = crew_orchestrator.get_agent_status()
        print(f"✅ Crew orchestrator status: {status['system_status']}")
        
        # Test a simple analysis
        test_company = "Microsoft"
        print(f"🚀 Testing crew analysis on: {test_company}")
        
        # Run a research-only analysis for speed
        analysis_result = await crew_orchestrator.run_comprehensive_analysis(test_company, "research")
        
        if analysis_result and analysis_result.get("status") == "completed":
            print("✅ Crew orchestrator working successfully")
            print(f"📊 Analysis type: {analysis_result.get('analysis_type')}")
            print(f"⏱️ Execution time: {analysis_result.get('execution_time')} seconds")
            return True
        else:
            print("⚠️ Crew orchestrator analysis failed")
            return False
            
    except Exception as e:
        print(f"❌ Crew orchestrator error: {e}")
        return False

async def test_crypto_agent():
    """Test crypto agent functionality"""
    print("🪙 Testing crypto agent...")
    
    try:
        from agents.crypto_agent import CryptoAgent
        
        crypto_agent = CryptoAgent()
        
        # Test crypto analysis
        test_crypto = "Bitcoin"
        print(f"🪙 Testing crypto analysis on: {test_crypto}")
        
        crypto_data = await crypto_agent.analyze_cryptocurrency(test_crypto)
        
        if crypto_data and crypto_data.get("crypto_name"):
            print("✅ Crypto agent working successfully")
            print(f"📊 Crypto data keys: {list(crypto_data.keys())}")
            return True
        else:
            print("⚠️ Crypto agent returned no data")
            return False
            
    except Exception as e:
        print(f"❌ Crypto agent error: {e}")
        return False

async def run_comprehensive_test():
    """Run comprehensive test of the new agent system"""
    print("🧪 Starting comprehensive test of new agent system...")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Module imports
    test_results.append(("Module Imports", test_imports()))
    
    # Test 2: Agent initialization
    test_results.append(("Agent Initialization", test_agent_initialization()))
    
    # Test 3: Tool initialization
    test_results.append(("Tool Initialization", test_tool_initialization()))
    
    # Test 4: LLM system
    test_results.append(("LLM System", test_llm_system()))
    
    # Test 5: Dynamic search
    test_results.append(("Dynamic Search", await test_dynamic_search()))
    
    # Test 6: Research agent
    test_results.append(("Research Agent", await test_research_agent()))
    
    # Test 7: Sentiment agent
    test_results.append(("Sentiment Agent", await test_sentiment_agent()))
    
    # Test 8: Crypto agent
    test_results.append(("Crypto Agent", await test_crypto_agent()))
    
    # Test 9: Crew orchestrator
    test_results.append(("Crew Orchestrator", await test_crew_orchestrator()))
    
    # Print results
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"📈 Overall Result: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! New agent system is ready for use.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

def main():
    """Main function to run the test"""
    print("🚀 IntelliVest AI - New Agent System Test")
    print("=" * 60)
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run the comprehensive test
    success = asyncio.run(run_comprehensive_test())
    
    print()
    print("=" * 60)
    if success:
        print("🎉 Test completed successfully!")
    else:
        print("⚠️ Test completed with some failures.")
    
    return success

if __name__ == "__main__":
    main() 