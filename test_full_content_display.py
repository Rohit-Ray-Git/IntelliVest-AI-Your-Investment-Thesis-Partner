#!/usr/bin/env python3
"""
Test to verify full analysis content is being stored and displayed correctly
"""

from production_integration import ProductionIntelliVestAI

def test_full_content_display():
    """Test full content storage and retrieval"""
    print("🧪 Testing Full Content Display...")
    
    # Initialize system
    system = ProductionIntelliVestAI()
    
    # Get history
    history = system.get_analysis_history(limit=10)
    print(f"📊 Retrieved {len(history)} history entries")
    
    if history:
        print("📝 Testing content retrieval for each analysis:")
        
        for i, entry in enumerate(history):
            print(f"\n   {i+1}. {entry['company_name']} - {entry['analysis_type']}")
            
            # Get full analysis details
            full_analysis = system.get_analysis_by_id(i)
            
            if full_analysis:
                print(f"      ✅ Retrieved full analysis")
                print(f"      📋 Content keys: {list(full_analysis.get('content', {}).keys())}")
                
                # Check if content has actual data
                content = full_analysis.get('content', {})
                if isinstance(content, dict):
                    for key, value in content.items():
                        if isinstance(value, str):
                            print(f"      📄 {key}: {len(value)} characters")
                        else:
                            print(f"      📄 {key}: {type(value)}")
                else:
                    print(f"      📄 Content type: {type(content)}")
            else:
                print(f"      ❌ Could not retrieve full analysis")
        
        # Test company search
        print(f"\n🏢 Testing company search:")
        companies = ["Apple", "Tesla", "NESCO"]
        
        for company in companies:
            analyses = system.get_analysis_by_company(company)
            print(f"   {company}: {len(analyses)} analyses found")
            
            for analysis in analyses:
                content_keys = list(analysis.get('content', {}).keys())
                print(f"      📋 Content keys: {content_keys}")
    
    else:
        print("⚠️ No history entries found")
    
    print("\n✅ Full content display test completed!")
    print("🎯 The system should now show complete analysis results when selected from dropdown.")

if __name__ == "__main__":
    test_full_content_display() 