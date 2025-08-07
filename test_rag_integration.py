"""
🧪 RAG Integration Test Script
=============================

This script tests the RAG system integration to ensure it's working properly.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_rag_system():
    """Test the RAG system functionality"""
    print("🧪 Testing RAG System Integration...")
    
    try:
        # Import the RAG system
        from tools.rag_system import RAGSystem
        
        # Initialize RAG system
        print("📝 Initializing RAG system...")
        rag_system = RAGSystem()
        
        # Test data
        test_company = "Test Company"
        test_content = """
        === FULL ANALYSIS ===
        
        COMPANY OVERVIEW:
        Test Company is a technology company focused on AI and machine learning.
        
        FINANCIAL METRICS:
        - Revenue: $100M
        - Growth Rate: 25%
        - Profit Margin: 15%
        
        RISK ASSESSMENT:
        - Market competition is high
        - Regulatory changes could impact business
        - Technology obsolescence risk
        
        INVESTMENT THESIS:
        Test Company shows strong growth potential with solid financials.
        However, risks should be carefully considered.
        """
        
        test_metadata = {
            'analysis_type': 'full',
            'timestamp': datetime.now().isoformat(),
            'source': 'test',
            'company_name': test_company
        }
        
        # Test storing report
        print("📝 Testing report storage...")
        report_id = rag_system.store_report(test_company, test_content, test_metadata)
        
        if report_id:
            print(f"✅ Report stored successfully with ID: {report_id}")
        else:
            print("❌ Failed to store report")
            return False
        
        # Test searching
        print("🔍 Testing search functionality...")
        search_results = rag_system.search_reports("financial metrics", test_company)
        
        if search_results:
            print(f"✅ Search returned {len(search_results)} results")
        else:
            print("⚠️ No search results found")
        
        # Test suggested questions
        print("❓ Testing suggested questions...")
        suggestions = rag_system.get_suggested_questions()
        
        if suggestions:
            print(f"✅ Generated {len(suggestions)} suggested questions")
            for i, suggestion in enumerate(suggestions[:3]):
                print(f"   {i+1}. {suggestion}")
        else:
            print("⚠️ No suggested questions generated")
        
        # Test system stats
        print("📊 Testing system statistics...")
        stats = rag_system.get_system_stats()
        
        if stats:
            print(f"✅ System stats: {stats}")
        else:
            print("⚠️ Could not get system stats")
        
        print("🎉 RAG system test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ RAG system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_streamlit_integration():
    """Test the Streamlit app RAG integration"""
    print("🧪 Testing Streamlit RAG Integration...")
    
    try:
        # Import the Streamlit app
        from streamlit_app import IntelliVestStreamlitApp
        
        # Initialize the app
        print("📝 Initializing Streamlit app...")
        app = IntelliVestStreamlitApp()
        
        # Test RAG system initialization
        if app.rag_system:
            print("✅ RAG system initialized in Streamlit app")
        else:
            print("❌ RAG system not initialized in Streamlit app")
            return False
        
        # Test store_analysis_in_rag method
        print("📝 Testing store_analysis_in_rag method...")
        
        # Create a mock result
        from production_integration import AnalysisRequest, AnalysisResult
        
        mock_request = AnalysisRequest(
            company_name="Test Company",
            analysis_type="full"
        )
        
        mock_content = {
            'summary': 'Test company analysis summary',
            'detailed_analysis': 'Detailed analysis of test company',
            'investment_thesis': 'Investment thesis for test company'
        }
        
        mock_result = AnalysisResult(
            request=mock_request,
            status="success",
            content=mock_content,
            metadata={},
            execution_time=10.0,
            models_used=["Test Model"],
            fallback_count=0,
            confidence_score=0.8,
            timestamp=datetime.now()
        )
        
        # Test storing in RAG
        success = app.store_analysis_in_rag(mock_result)
        
        if success:
            print("✅ Successfully stored mock analysis in RAG")
        else:
            print("❌ Failed to store mock analysis in RAG")
            return False
        
        print("🎉 Streamlit RAG integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit RAG integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting RAG Integration Tests...")
    print("=" * 50)
    
    # Test RAG system
    rag_test_passed = test_rag_system()
    
    print("\n" + "=" * 50)
    
    # Test Streamlit integration
    streamlit_test_passed = test_streamlit_integration()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"RAG System Test: {'✅ PASSED' if rag_test_passed else '❌ FAILED'}")
    print(f"Streamlit Integration Test: {'✅ PASSED' if streamlit_test_passed else '❌ FAILED'}")
    
    if rag_test_passed and streamlit_test_passed:
        print("🎉 All tests passed! RAG integration is working properly.")
    else:
        print("⚠️ Some tests failed. Please check the implementation.") 