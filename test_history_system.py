#!/usr/bin/env python3
"""
Test script to verify the history system works correctly
"""

import asyncio
from production_integration import ProductionIntelliVestAI, AnalysisRequest

async def test_history_system():
    """Test the history system"""
    print("🧪 Testing History System...")
    
    # Initialize the system
    system = ProductionIntelliVestAI()
    
    # Check initial history
    print(f"📊 Initial history count: {len(system.analysis_history)}")
    
    # Create a test request
    test_request = AnalysisRequest(
        company_name="Test Company",
        analysis_type="research",
        include_tools=True,
        use_advanced_fallback=True
    )
    
    print(f"🚀 Running test analysis for: {test_request.company_name}")
    
    try:
        # Run a quick analysis
        result = await system.analyze_company(test_request)
        
        print(f"✅ Analysis completed with status: {result.status}")
        print(f"📊 History count after analysis: {len(system.analysis_history)}")
        
        # Get history
        history = system.get_analysis_history(limit=10)
        print(f"📋 Retrieved {len(history)} history entries")
        
        if history:
            print("📝 History entries:")
            for i, entry in enumerate(history):
                print(f"   {i+1}. {entry['company_name']} - {entry['analysis_type']} - {entry['status']}")
        else:
            print("⚠️ No history entries found")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("\n✅ History system test completed!")

if __name__ == "__main__":
    asyncio.run(test_history_system()) 