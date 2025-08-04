#!/usr/bin/env python3
"""
Test enhanced history system with full content storage and retrieval
"""

import asyncio
from production_integration import ProductionIntelliVestAI, AnalysisRequest

async def test_enhanced_history():
    """Test the enhanced history system"""
    print("🧪 Testing Enhanced History System...")
    
    # Initialize the system
    system = ProductionIntelliVestAI()
    
    # Check initial history
    print(f"📊 Initial history count: {len(system.analysis_history)}")
    
    # Create test requests
    test_requests = [
        AnalysisRequest("Apple Inc.", "research", include_tools=True, use_advanced_fallback=True),
        AnalysisRequest("Tesla Inc.", "sentiment", include_tools=True, use_advanced_fallback=True)
    ]
    
    for i, request in enumerate(test_requests):
        print(f"🚀 Running test analysis {i+1} for: {request.company_name}")
        
        try:
            # Run analysis
            result = await system.analyze_company(request)
            
            print(f"✅ Analysis {i+1} completed with status: {result.status}")
            print(f"📊 History count after analysis {i+1}: {len(system.analysis_history)}")
            
        except Exception as e:
            print(f"❌ Analysis {i+1} failed: {e}")
    
    # Test history retrieval
    print("\n📋 Testing History Retrieval...")
    
    # Get history
    history = system.get_analysis_history(limit=10)
    print(f"📊 Retrieved {len(history)} history entries")
    
    if history:
        print("📝 History entries:")
        for i, entry in enumerate(history):
            print(f"   {i+1}. {entry['company_name']} - {entry['analysis_type']} - {entry['status']}")
        
        # Test getting specific analysis
        print("\n🎯 Testing Specific Analysis Retrieval...")
        analysis_0 = system.get_analysis_by_id(0)
        if analysis_0:
            print(f"✅ Retrieved analysis 0: {analysis_0['company_name']} - {analysis_0['analysis_type']}")
            print(f"   Content keys: {list(analysis_0.get('content', {}).keys())}")
        else:
            print("❌ Could not retrieve analysis 0")
        
        # Test company search
        print("\n🏢 Testing Company Search...")
        apple_analyses = system.get_analysis_by_company("Apple")
        print(f"📊 Found {len(apple_analyses)} analyses for Apple")
        
        tesla_analyses = system.get_analysis_by_company("Tesla")
        print(f"📊 Found {len(tesla_analyses)} analyses for Tesla")
        
    else:
        print("⚠️ No history entries found")
    
    print("\n✅ Enhanced history system test completed!")

if __name__ == "__main__":
    asyncio.run(test_enhanced_history()) 