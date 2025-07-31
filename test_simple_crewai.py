"""
🧪 Simple CrewAI Test with Updated Model Configuration
=====================================================

This script tests CrewAI with the updated model configuration.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_simple_crewai():
    """Test simple CrewAI setup with updated models"""
    print("🔍 Testing Simple CrewAI Setup...")
    
    try:
        from crewai import Agent, Task, Crew, Process
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Create a simple agent with Gemini 2.5 Flash
        agent = Agent(
            role="Test Agent",
            goal="Test the model configuration",
            backstory="A simple test agent",
            llm=ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.7
            ),
            verbose=True
        )
        
        # Create a simple task
        task = Task(
            description="Provide a brief overview of Apple Inc.",
            agent=agent,
            expected_output="Brief company overview"
        )
        
        # Create crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        print("✅ Simple CrewAI setup created successfully")
        print("🤖 Agent LLM: Gemini 2.5 Flash")
        print("📋 Task: Company overview")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple CrewAI test failed: {e}")
        return False

async def test_simple_execution():
    """Test simple CrewAI execution"""
    print("\n🚀 Testing Simple CrewAI Execution...")
    
    try:
        from crewai import Agent, Task, Crew, Process
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Create a simple agent
        agent = Agent(
            role="Test Agent",
            goal="Test the model configuration",
            backstory="A simple test agent",
            llm=ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.7
            ),
            verbose=True
        )
        
        # Create a simple task
        task = Task(
            description="Provide a brief overview of Apple Inc.",
            agent=agent,
            expected_output="Brief company overview"
        )
        
        # Create crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute
        print("🤖 Executing simple CrewAI workflow...")
        result = crew.kickoff()
        
        print("✅ Simple CrewAI execution successful!")
        print(f"📝 Result: {result[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple CrewAI execution failed: {e}")
        return False

async def main():
    """Run simple CrewAI tests"""
    print("🎯 Simple CrewAI Test with Updated Model Configuration")
    print("=" * 60)
    
    tests = [
        ("Simple CrewAI Setup Test", test_simple_crewai),
        ("Simple CrewAI Execution Test", test_simple_execution)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All simple CrewAI tests passed!")
        print("✅ CrewAI works with Gemini 2.5 Flash model")
        return True
    else:
        print("⚠️ Some simple CrewAI tests failed.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 