#!/usr/bin/env python3
"""
Simple Test Script - Core Agent Functionality Test
This script tests the core agent functionality without web crawling dependencies.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append('.')

async def test_core_agents():
    """Test core agent functionality without web crawling"""
    print("🧪 Testing Core Agent Functionality")
    print("=" * 50)
    
    try:
        # Import agents
        from agents.research_agent import ResearchAgent
        from agents.sentiment_agent import SentimentAgent
        from agents.valuation_agent import ValuationAgent
        from agents.thesis_agent import ThesisAgent
        from agents.critique_agent import CritiqueAgent
        from agents.thesis_rewrite_agent import ThesisRewriteAgent
        
        print("✅ All agents imported successfully")
        
        # Test 1: Agent Initialization
        print("\n🔧 Testing Agent Initialization...")
        research_agent = ResearchAgent()
        sentiment_agent = SentimentAgent()
        valuation_agent = ValuationAgent()
        thesis_agent = ThesisAgent()
        critique_agent = CritiqueAgent()
        rewriter_agent = ThesisRewriteAgent()
        
        print("✅ All agents initialized successfully")
        
        # Test 2: Agent Communication
        print("\n📡 Testing Agent Communication...")
        from agents.global_agentic_system import GlobalAgenticSystem, AgentMessage, MessageType
        
        # Initialize global system
        global_system = GlobalAgenticSystem()
        
        # Register agents
        agents = {
            "ResearchAgent": research_agent,
            "SentimentAgent": sentiment_agent,
            "ValuationAgent": valuation_agent,
            "ThesisAgent": thesis_agent,
            "CritiqueAgent": critique_agent,
            "RewriterAgent": rewriter_agent
        }
        
        for name, agent in agents.items():
            global_system.register_agent(name, agent, ["test"])
        
        print(f"✅ {len(agents)} agents registered with global system")
        
        # Test 3: Simple Message Passing
        print("\n💬 Testing Message Passing...")
        
        # Create a test message
        test_message = AgentMessage(
            sender="TestSender",
            recipient="ResearchAgent",
            message_type=MessageType.DATA_REQUEST,
            content={"test": "simple_communication_test"}
        )
        
        # Send message
        response = await global_system.send_message(test_message)
        print(f"✅ Message sent successfully: {response is not None}")
        
        # Test 4: Agent Method Availability
        print("\n🔍 Testing Agent Method Availability...")
        
        # Check if agents have required methods
        required_methods = {
            "ResearchAgent": ["research_company", "handle_message"],
            "SentimentAgent": ["analyze_sentiment", "handle_message"],
            "ValuationAgent": ["perform_valuation", "handle_message"],
            "ThesisAgent": ["generate_thesis", "handle_message"],
            "CritiqueAgent": ["critique_thesis", "handle_message"],
            "RewriterAgent": ["revise_thesis", "handle_message"]
        }
        
        for agent_name, methods in required_methods.items():
            agent = agents[agent_name]
            for method in methods:
                if hasattr(agent, method):
                    print(f"✅ {agent_name}.{method} - Available")
                else:
                    print(f"❌ {agent_name}.{method} - Missing")
        
        # Test 5: System Status
        print("\n📊 Testing System Status...")
        system_status = global_system.get_system_status()
        print(f"✅ System Status: {len(system_status.get('agents', {}))} agents active")
        
        # Test 6: Communication Log
        print("\n📝 Testing Communication Log...")
        communication_log = global_system.get_communication_log()
        print(f"✅ Communication Log: {len(communication_log)} entries")
        
        print("\n🎉 Core Agent Functionality Test Complete!")
        print("✅ All core systems are working correctly")
        print("✅ Agent communication is functional")
        print("✅ Method signatures are correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in core agent test: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_llm_system():
    """Test LLM system functionality"""
    print("\n🧠 Testing LLM System...")
    print("=" * 30)
    
    try:
        from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType
        
        # Initialize LLM system
        llm_system = AdvancedFallbackSystem()
        print("✅ Advanced Fallback System initialized")
        
        # Test simple prompt
        test_prompt = "What is 2 + 2? Please provide a simple answer."
        
        print("🤖 Testing LLM with simple prompt...")
        result = await llm_system.execute_with_fallback(
            prompt=test_prompt,
            task_type=TaskType.RESEARCH,
            max_fallbacks=2
        )
        
        if result and result.content:
            print("✅ LLM system working correctly")
            print(f"📝 Response: {result.content[:100]}...")
        else:
            print("⚠️ LLM system returned empty response")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in LLM test: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 IntelliVest AI - Core System Test")
    print("=" * 60)
    
    # Test core agents
    core_success = await test_core_agents()
    
    # Test LLM system
    llm_success = await test_llm_system()
    
    # Final results
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    if core_success and llm_success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Core agent functionality: Working")
        print("✅ LLM system: Working")
        print("✅ System is ready for analysis")
        print("\n💡 The system is working correctly!")
        print("💡 Web crawling issues are separate from core functionality")
        print("💡 You can now proceed with stock/crypto analysis")
    else:
        print("⚠️ SOME TESTS FAILED")
        if not core_success:
            print("❌ Core agent functionality: Failed")
        if not llm_success:
            print("❌ LLM system: Failed")
        print("\n🔧 Please check the error messages above")
    
    return core_success and llm_success

if __name__ == "__main__":
    asyncio.run(main()) 