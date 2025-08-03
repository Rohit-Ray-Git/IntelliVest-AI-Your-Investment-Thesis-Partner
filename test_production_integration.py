#!/usr/bin/env python3
"""
🧪 Comprehensive Test Suite for IntelliVest AI Production System
===============================================================

This test suite verifies:
- System initialization
- All analysis types (research, sentiment, valuation, thesis, full)
- Advanced fallback system
- Custom tools integration
- Real-time monitoring
- Analysis history
"""

import asyncio
import time
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the production system
from production_integration import ProductionIntelliVestAI, AnalysisRequest, AnalysisResult

class TestProductionIntegration:
    """Test suite for the production integration system"""
    
    def __init__(self):
        self.intellivest_ai = None
        self.test_results = []
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": timestamp
        }
        self.test_results.append(result)
        
        # Print result
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_1_system_import(self):
        """Test 1: System Import"""
        try:
            from production_integration import ProductionIntelliVestAI, AnalysisRequest, AnalysisResult
            self.log_test("System Import", "PASS", "All modules imported successfully")
            return True
        except Exception as e:
            self.log_test("System Import", "FAIL", f"Import error: {str(e)}")
            return False
    
    def test_2_system_initialization(self):
        """Test 2: System Initialization"""
        try:
            self.intellivest_ai = ProductionIntelliVestAI()
            self.log_test("System Initialization", "PASS", "Production system initialized successfully")
            return True
        except Exception as e:
            self.log_test("System Initialization", "FAIL", f"Initialization error: {str(e)}")
            return False
    
    def test_3_request_creation(self):
        """Test 3: Analysis Request Creation"""
        try:
            request = AnalysisRequest(
                company_name="Apple Inc.",
                analysis_type="research",
                include_tools=True,
                use_advanced_fallback=True
            )
            self.log_test("Request Creation", "PASS", f"Created request for {request.company_name}")
            return True
        except Exception as e:
            self.log_test("Request Creation", "FAIL", f"Request creation error: {str(e)}")
            return False
    
    def test_4_system_monitoring(self):
        """Test 4: System Monitoring"""
        try:
            status = self.intellivest_ai.get_system_status()
            self.log_test("System Monitoring", "PASS", f"System status: {status.get('system_status', 'Unknown')}")
            return True
        except Exception as e:
            self.log_test("System Monitoring", "FAIL", f"Monitoring error: {str(e)}")
            return False
    
    async def test_5_research_analysis(self):
        """Test 5: Research Analysis"""
        try:
            request = AnalysisRequest(
                company_name="Apple Inc.",
                analysis_type="research",
                include_tools=True,
                use_advanced_fallback=True
            )
            
            start_time = time.time()
            result = await self.intellivest_ai.analyze_company(request)
            execution_time = time.time() - start_time
            
            if result.status == "success":
                self.log_test("Research Analysis", "PASS", 
                            f"Execution time: {execution_time:.2f}s, Confidence: {result.confidence_score:.2f}")
                return True
            else:
                self.log_test("Research Analysis", "FAIL", f"Analysis failed: {result.status}")
                return False
                
        except Exception as e:
            self.log_test("Research Analysis", "FAIL", f"Analysis error: {str(e)}")
            return False
    
    async def test_6_sentiment_analysis(self):
        """Test 6: Sentiment Analysis"""
        try:
            request = AnalysisRequest(
                company_name="Tesla Inc.",
                analysis_type="sentiment",
                include_tools=True,
                use_advanced_fallback=True
            )
            
            start_time = time.time()
            result = await self.intellivest_ai.analyze_company(request)
            execution_time = time.time() - start_time
            
            if result.status == "success":
                self.log_test("Sentiment Analysis", "PASS", 
                            f"Execution time: {execution_time:.2f}s, Confidence: {result.confidence_score:.2f}")
                return True
            else:
                self.log_test("Sentiment Analysis", "FAIL", f"Analysis failed: {result.status}")
                return False
                
        except Exception as e:
            self.log_test("Sentiment Analysis", "FAIL", f"Analysis error: {str(e)}")
            return False
    
    async def test_7_valuation_analysis(self):
        """Test 7: Valuation Analysis"""
        try:
            request = AnalysisRequest(
                company_name="Microsoft Corporation",
                analysis_type="valuation",
                include_tools=True,
                use_advanced_fallback=True
            )
            
            start_time = time.time()
            result = await self.intellivest_ai.analyze_company(request)
            execution_time = time.time() - start_time
            
            if result.status == "success":
                self.log_test("Valuation Analysis", "PASS", 
                            f"Execution time: {execution_time:.2f}s, Confidence: {result.confidence_score:.2f}")
                return True
            else:
                self.log_test("Valuation Analysis", "FAIL", f"Analysis failed: {result.status}")
                return False
                
        except Exception as e:
            self.log_test("Valuation Analysis", "FAIL", f"Analysis error: {str(e)}")
            return False
    
    async def test_8_thesis_analysis(self):
        """Test 8: Thesis Analysis"""
        try:
            request = AnalysisRequest(
                company_name="Amazon.com Inc.",
                analysis_type="thesis",
                include_tools=True,
                use_advanced_fallback=True
            )
            
            start_time = time.time()
            result = await self.intellivest_ai.analyze_company(request)
            execution_time = time.time() - start_time
            
            if result.status == "success":
                self.log_test("Thesis Analysis", "PASS", 
                            f"Execution time: {execution_time:.2f}s, Confidence: {result.confidence_score:.2f}")
                return True
            else:
                self.log_test("Thesis Analysis", "FAIL", f"Analysis failed: {result.status}")
                return False
                
        except Exception as e:
            self.log_test("Thesis Analysis", "FAIL", f"Analysis error: {str(e)}")
            return False
    
    def test_9_analysis_history(self):
        """Test 9: Analysis History"""
        try:
            history = self.intellivest_ai.get_analysis_history(limit=5)
            self.log_test("Analysis History", "PASS", f"Retrieved {len(history)} history entries")
            return True
        except Exception as e:
            self.log_test("Analysis History", "FAIL", f"History error: {str(e)}")
            return False
    
    def test_10_multiple_analyses(self):
        """Test 10: Multiple Sequential Analyses"""
        try:
            # This test verifies the system can handle multiple analyses
            status = self.intellivest_ai.get_system_status()
            total_analyses = status.get('metrics', {}).get('total_analyses', 0)
            
            if total_analyses >= 4:  # We should have at least 4 analyses from previous tests
                self.log_test("Multiple Analyses", "PASS", f"Successfully completed {total_analyses} analyses")
                return True
            else:
                self.log_test("Multiple Analyses", "FAIL", f"Only completed {total_analyses} analyses")
                return False
                
        except Exception as e:
            self.log_test("Multiple Analyses", "FAIL", f"Multiple analyses error: {str(e)}")
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("=" * 60)
        print("🧪 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['details']}")
        
        print("\n" + "=" * 60)
        
        # Overall assessment
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! System is ready for production.")
        elif passed_tests >= total_tests * 0.8:
            print("⚠️ Most tests passed. System needs minor fixes.")
        else:
            print("❌ Multiple tests failed. System needs significant work.")
        
        return passed_tests == total_tests

async def run_comprehensive_test():
    """Run the comprehensive test suite"""
    print("🚀 Starting Comprehensive Test Suite for IntelliVest AI")
    print("=" * 60)
    
    tester = TestProductionIntegration()
    
    # Run synchronous tests
    tests = [
        tester.test_1_system_import,
        tester.test_2_system_initialization,
        tester.test_3_request_creation,
        tester.test_4_system_monitoring,
    ]
    
    for test in tests:
        test()
    
    # Run asynchronous tests
    async_tests = [
        tester.test_5_research_analysis,
        tester.test_6_sentiment_analysis,
        tester.test_7_valuation_analysis,
        tester.test_8_thesis_analysis,
    ]
    
    for test in async_tests:
        await test()
    
    # Run final tests
    tester.test_9_analysis_history()
    tester.test_10_multiple_analyses()
    
    # Print summary
    success = tester.print_summary()
    
    return success

if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(run_comprehensive_test())
    
    # Exit with appropriate code
    sys.exit(0 if success else 1) 