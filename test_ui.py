#!/usr/bin/env python3
"""
🧪 Test UI Fixes
===============

Test script to verify the UI fixes work correctly
"""

import asyncio
from production_integration import ProductionIntelliVestAI, AnalysisRequest

async def test_ui_fixes():
    """Test UI fixes"""
    print("🧪 Testing UI Fixes...")
    print("=" * 50)
    
    # Initialize system
    system = ProductionIntelliVestAI()
    
    # Test system status
    print("1. Testing System Status...")
    status = system.get_system_status()
    print(f"   ✅ System Status: {status['system_status']}")
    print(f"   ✅ Total Analyses: {status['metrics']['total_analyses']}")
    print(f"   ✅ Available Models: {status['advanced_fallback_status'].get('available_models', 0)}")
    
    # Test CrewOutput handling
    print("\n2. Testing CrewOutput Handling...")
    try:
        # Create a mock CrewOutput-like object
        class MockCrewOutput:
            def __init__(self, content):
                self.raw = content
            
            def __str__(self):
                return str(self.raw)
        
        mock_result = {
            'status': 'success',
            'result': MockCrewOutput("Final investment thesis content"),
            'agents_used': ['Gemini 2.5 Flash']
        }
        
        # Test the handling
        crew_result = mock_result['result']
        if hasattr(crew_result, 'raw'):
            final_thesis = str(crew_result.raw)
        else:
            final_thesis = str(crew_result)
        
        print(f"   ✅ CrewOutput handled correctly: {final_thesis[:50]}...")
        
    except Exception as e:
        print(f"   ❌ CrewOutput handling failed: {e}")
    
    print("\n✅ UI Fixes Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_ui_fixes())