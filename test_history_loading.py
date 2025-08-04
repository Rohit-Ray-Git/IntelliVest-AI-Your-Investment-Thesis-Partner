#!/usr/bin/env python3
"""
Test history loading
"""

from production_integration import ProductionIntelliVestAI

def test_history_loading():
    """Test history loading"""
    print("🧪 Testing History Loading...")
    
    # Initialize system
    system = ProductionIntelliVestAI()
    
    # Get history
    history = system.get_analysis_history()
    
    print(f"📊 History count: {len(history)}")
    
    if history:
        print("📝 History entries:")
        for i, entry in enumerate(history):
            print(f"   {i+1}. {entry['company_name']} - {entry['analysis_type']} - {entry['status']}")
    else:
        print("⚠️ No history found")
    
    print("✅ History loading test completed!")

if __name__ == "__main__":
    test_history_loading() 