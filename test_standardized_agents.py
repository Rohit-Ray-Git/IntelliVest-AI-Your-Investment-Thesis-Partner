#!/usr/bin/env python3
"""
🧪 Test Standardized Agents
===========================

Simple test to verify that all standardized agents can be imported and initialized.
"""

import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_agent_imports():
    """Test that all agents can be imported successfully"""
    print("🧪 Testing Standardized Agent Imports...")
    
    try:
        # Test BaseAgent import
        from agents.base_agent import BaseAgent
        print("✅ BaseAgent imported successfully")
        
        # Test individual agent imports
        from agents.research_agent import ResearchAgent
        print("✅ ResearchAgent imported successfully")
        
        from agents.sentiment_agent import SentimentAgent
        print("✅ SentimentAgent imported successfully")
        
        from agents.valuation_agent import ValuationAgent
        print("✅ ValuationAgent imported successfully")
        
        from agents.thesis_agent import ThesisAgent
        print("✅ ThesisAgent imported successfully")
        
        from agents.critique_agent import CritiqueAgent
        print("✅ CritiqueAgent imported successfully")
        
        print("\n🎉 All agents imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_agent_initialization():
    """Test that all agents can be initialized successfully"""
    print("\n🧪 Testing Agent Initialization...")
    
    try:
        # Test agent initialization
        from agents.research_agent import ResearchAgent
        from agents.sentiment_agent import SentimentAgent
        from agents.valuation_agent import ValuationAgent
        from agents.thesis_agent import ThesisAgent
        from agents.critique_agent import CritiqueAgent
        
        # Initialize agents
        research_agent = ResearchAgent()
        print("✅ ResearchAgent initialized successfully")
        
        sentiment_agent = SentimentAgent()
        print("✅ SentimentAgent initialized successfully")
        
        valuation_agent = ValuationAgent()
        print("✅ ValuationAgent initialized successfully")
        
        thesis_agent = ThesisAgent()
        print("✅ ThesisAgent initialized successfully")
        
        critique_agent = CritiqueAgent()
        print("✅ CritiqueAgent initialized successfully")
        
        # Test agent info
        print(f"\n📊 Agent Information:")
        print(f"  - Research Agent: {research_agent.get_agent_info()}")
        print(f"  - Sentiment Agent: {sentiment_agent.get_agent_info()}")
        print(f"  - Valuation Agent: {valuation_agent.get_agent_info()}")
        print(f"  - Thesis Agent: {thesis_agent.get_agent_info()}")
        print(f"  - Critique Agent: {critique_agent.get_agent_info()}")
        
        print("\n🎉 All agents initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def test_standardized_interface():
    """Test that all agents have the standardized interface"""
    print("\n🧪 Testing Standardized Interface...")
    
    try:
        from agents.base_agent import BaseAgent
        from agents.research_agent import ResearchAgent
        from agents.sentiment_agent import SentimentAgent
        from agents.valuation_agent import ValuationAgent
        from agents.thesis_agent import ThesisAgent
        from agents.critique_agent import CritiqueAgent
        
        agents = [
            ResearchAgent(),
            SentimentAgent(),
            ValuationAgent(),
            ThesisAgent(),
            CritiqueAgent()
        ]
        
        # Test that all agents have required methods
        required_methods = ['analyze', 'handle_message', 'provide_data', 'get_agent_info']
        
        for i, agent in enumerate(agents):
            agent_name = agent.__class__.__name__
            print(f"  Testing {agent_name}...")
            
            for method in required_methods:
                if hasattr(agent, method):
                    print(f"    ✅ {method} method exists")
                else:
                    print(f"    ❌ {method} method missing")
                    return False
        
        print("\n🎉 All agents have standardized interface!")
        return True
        
    except Exception as e:
        print(f"❌ Interface test error: {e}")
        return False

async def test_agent_communication():
    """Test agent communication capabilities"""
    print("\n🧪 Testing Agent Communication...")
    
    try:
        from agents.research_agent import ResearchAgent
        from agents.sentiment_agent import SentimentAgent
        
        # Initialize agents
        research_agent = ResearchAgent()
        sentiment_agent = SentimentAgent()
        
        # Test message handling
        test_message = {
            "type": "data_request",
            "content": {
                "request_type": "research_data",
                "company_name": "AAPL"
            }
        }
        
        # Test research agent message handling
        response = await research_agent.handle_message(test_message)
        print(f"✅ Research agent message handling: {response.get('status', 'success')}")
        
        # Test sentiment agent message handling
        response = await sentiment_agent.handle_message(test_message)
        print(f"✅ Sentiment agent message handling: {response.get('status', 'success')}")
        
        print("\n🎉 Agent communication test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Communication test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Standardized Agent Tests")
    print("=" * 50)
    
    # Run tests
    tests = [
        ("Import Test", test_agent_imports),
        ("Initialization Test", test_agent_initialization),
        ("Interface Test", test_standardized_interface),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Run async test
    print(f"\n🧪 Running Communication Test...")
    try:
        result = asyncio.run(test_agent_communication())
        results.append(("Communication Test", result))
    except Exception as e:
        print(f"❌ Communication test error: {e}")
        results.append(("Communication Test", False))
    
    # Print results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Standardized agents are working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 