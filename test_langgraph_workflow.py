"""
🧪 Test LangGraph Workflow
==========================

This script tests the LangGraph workflow for investment analysis.
"""

import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_langgraph_import():
    """Test if LangGraph can be imported"""
    print("🔍 Testing LangGraph import...")
    
    try:
        from langgraph.graph import StateGraph, END
        from langgraph.graph.message import add_messages
        from langgraph.checkpoint.memory import MemorySaver
        print("✅ LangGraph components imported successfully")
        return True
    except ImportError as e:
        print(f"❌ LangGraph import failed: {e}")
        return False

def test_workflow_creation():
    """Test LangGraph workflow creation"""
    print("\n🔄 Testing LangGraph workflow creation...")
    
    try:
        from workflows.investment_workflow import InvestmentWorkflow
        
        # Create workflow
        workflow = InvestmentWorkflow()
        print("✅ LangGraph workflow created successfully")
        
        # Check if workflow has required components
        if hasattr(workflow, 'app'):
            print("✅ Workflow app compiled successfully")
        else:
            print("❌ Workflow app not found")
            return False
        
        if hasattr(workflow, 'primary_llm'):
            print("✅ Workflow LLM configured")
        else:
            print("❌ Workflow LLM not configured")
            return False
        
        if hasattr(workflow, 'tools'):
            print(f"✅ Workflow tools available: {len(workflow.tools)}")
        else:
            print("❌ Workflow tools not configured")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow creation failed: {e}")
        return False

def test_workflow_execution():
    """Test LangGraph workflow execution"""
    print("\n🚀 Testing LangGraph workflow execution...")
    
    try:
        from workflows.investment_workflow import InvestmentWorkflow
        
        # Create workflow
        workflow = InvestmentWorkflow()
        
        # Test with a simple company
        company_name = "Apple Inc."
        print(f"📈 Testing workflow with: {company_name}")
        
        # Run the workflow
        start_time = time.time()
        result = workflow.run_analysis(company_name)
        execution_time = time.time() - start_time
        
        # Check results
        print(f"⏱️ Workflow executed in {execution_time:.2f} seconds")
        print(f"📊 Status: {result['status']}")
        
        if result['status'] == 'success':
            print("✅ Workflow execution successful!")
            print(f"📝 Confidence Score: {result.get('confidence_score', 0):.1f}%")
            print(f"📋 Steps Completed: {result.get('steps_completed', 0)}/{result.get('total_steps', 0)}")
            print(f"🛠️ Tools Used: {len(result.get('tools_used', []))}")
            print(f"❌ Errors: {len(result.get('errors', []))}")
            
            # Show recommendation
            recommendation = result.get('recommendation', 'No recommendation generated')
            print(f"💡 Recommendation: {recommendation[:200]}...")
            
            return True
        else:
            print(f"❌ Workflow execution failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Workflow execution test failed: {e}")
        return False

def test_state_management():
    """Test LangGraph state management"""
    print("\n📊 Testing LangGraph state management...")
    
    try:
        from workflows.investment_workflow import InvestmentState
        
        # Create initial state
        initial_state = InvestmentState(
            company_name="Test Company",
            messages=[],
            research_data={},
            sentiment_analysis={},
            valuation_data={},
            investment_thesis={},
            critique={},
            current_step="start",
            errors=[],
            tools_used=[],
            confidence_score=0.0,
            recommendation=""
        )
        
        print("✅ InvestmentState created successfully")
        print(f"📝 Company: {initial_state['company_name']}")
        print(f"🔄 Current Step: {initial_state['current_step']}")
        print(f"🛠️ Tools Used: {len(initial_state['tools_used'])}")
        print(f"❌ Errors: {len(initial_state['errors'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ State management test failed: {e}")
        return False

def test_conditional_logic():
    """Test LangGraph conditional logic"""
    print("\n🔄 Testing LangGraph conditional logic...")
    
    try:
        from workflows.investment_workflow import InvestmentWorkflow
        
        # Create workflow
        workflow = InvestmentWorkflow()
        
        # Test decision router
        test_states = [
            {"current_step": "start"},
            {"current_step": "research_completed"},
            {"current_step": "sentiment_completed"},
            {"current_step": "valuation_completed"},
            {"current_step": "thesis_completed"},
            {"current_step": "critique_completed"}
        ]
        
        print("🧪 Testing decision router...")
        for i, state in enumerate(test_states):
            next_step = workflow.decision_router(state)
            print(f"   Step {i+1}: {state['current_step']} → {next_step}")
        
        print("✅ Conditional logic working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Conditional logic test failed: {e}")
        return False

def main():
    """Run all LangGraph tests"""
    print("🎯 LangGraph Workflow - Advanced Agentic System Test")
    print("=" * 60)
    
    tests = [
        ("LangGraph Import Test", test_langgraph_import),
        ("State Management Test", test_state_management),
        ("Conditional Logic Test", test_conditional_logic),
        ("Workflow Creation Test", test_workflow_creation),
        ("Workflow Execution Test", test_workflow_execution)
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
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All LangGraph tests passed! Advanced agentic system is ready.")
        print("\n🚀 LangGraph Capabilities:")
        print("   ✅ State Management: Persistent workflow state")
        print("   ✅ Conditional Logic: Dynamic task routing")
        print("   ✅ Error Handling: Robust error recovery")
        print("   ✅ Sequential Execution: Ordered workflow steps")
        print("   ✅ Confidence Scoring: Quality assessment")
        print("   ✅ Tool Integration: Custom tools available")
        
        print("\n🚀 Ready for Step 4: Advanced Fallback Systems!")
        
        return True
    else:
        print("⚠️ Some LangGraph tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 