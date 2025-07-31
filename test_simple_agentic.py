"""
🧪 Test Script for Simplified Agentic AI Setup
==============================================

This script tests the simplified CrewAI setup without custom tools.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_simple_agentic():
    """Test the simplified agentic system"""
    print("🚀 Testing Simplified Agentic AI Setup\n")
    print("=" * 50)
    
    try:
        from agents.crew_agents_simple import SimpleInvestmentAnalysisCrew
        
        print("✅ Simplified CrewAI agents imported successfully")
        
        # Create crew
        print("🤖 Creating simplified crew...")
        crew = SimpleInvestmentAnalysisCrew()
        print("✅ Simplified crew created successfully")
        
        # Test agent creation
        print("📋 Testing agent creation...")
        agents = [
            crew.researcher,
            crew.sentiment_analyst,
            crew.valuation_analyst,
            crew.thesis_writer,
            crew.critic
        ]
        print(f"✅ Successfully created {len(agents)} agents")
        
        # Test task creation
        print("📝 Testing task creation...")
        tasks = crew.create_tasks("Apple Inc.")
        print(f"✅ Successfully created {len(tasks)} tasks")
        
        print("\n🎉 Simplified agentic system setup is working!")
        print("\n📊 Summary:")
        print(f"   - LLM: {crew.primary_llm}")
        print(f"   - Agents: {len(agents)}")
        print(f"   - Tasks: {len(tasks)}")
        
        return True
            
    except Exception as e:
        print(f"❌ Error in simplified agentic test: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_agentic()
    sys.exit(0 if success else 1) 