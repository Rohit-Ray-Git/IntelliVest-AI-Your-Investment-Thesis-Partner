"""
🧪 Test Script for Agentic AI Setup
===================================

This script tests the CrewAI setup with custom tools and Gemini 2.5 Flash.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from crewai import Agent, Task, Crew, Process
        print("✅ CrewAI imported successfully")
    except ImportError as e:
        print(f"❌ CrewAI import failed: {e}")
        return False
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ LangChain Google GenAI imported successfully")
    except ImportError as e:
        print(f"❌ LangChain Google GenAI import failed: {e}")
        return False
    
    try:
        from tools.investment_tools import WebCrawlerTool, FinancialDataTool
        print("✅ Custom tools imported successfully")
    except ImportError as e:
        print(f"❌ Custom tools import failed: {e}")
        return False
    
    try:
        from agents.crew_agents import InvestmentAnalysisCrew
        print("✅ CrewAI agents imported successfully")
    except ImportError as e:
        print(f"❌ CrewAI agents import failed: {e}")
        return False
    
    return True

def test_llm_setup():
    """Test LLM setup with Gemini 2.5 Flash"""
    print("\n🧠 Testing LLM setup...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            max_output_tokens=8192
        )
        
        # Test a simple completion
        response = llm.invoke("Say 'Hello from Gemini 2.5 Flash!'")
        print(f"✅ LLM test successful: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False

def test_tools():
    """Test custom tools"""
    print("\n🛠️ Testing custom tools...")
    
    try:
        from tools.investment_tools import FinancialDataTool
        
        # Test financial data tool
        tool = FinancialDataTool()
        result = tool._run("AAPL")
        print(f"✅ Financial data tool test successful: {len(result)} characters")
        return True
        
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        return False

def test_crew_creation():
    """Test CrewAI crew creation"""
    print("\n🤖 Testing CrewAI crew creation...")
    
    try:
        from agents.crew_agents import InvestmentAnalysisCrew
        
        # Create crew (this will test all components)
        crew = InvestmentAnalysisCrew()
        print("✅ CrewAI crew created successfully")
        print(f"✅ Agents created: {len([crew.researcher, crew.sentiment_analyst, crew.valuation_analyst, crew.thesis_writer, crew.critic])}")
        return True
        
    except Exception as e:
        print(f"❌ CrewAI crew creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Agentic AI Setup Tests\n")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("LLM Setup Test", test_llm_setup),
        ("Tools Test", test_tools),
        ("CrewAI Creation Test", test_crew_creation)
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
        print("🎉 All tests passed! Agentic AI setup is ready.")
        print("\n🚀 Next steps:")
        print("1. Create LangGraph workflows")
        print("2. Build fallback systems")
        print("3. Integrate with main application")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 