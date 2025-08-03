#!/usr/bin/env python3
"""
🤖 Detailed Agent Testing Suite
===============================

This script performs comprehensive testing of each agent in the IntelliVest AI system.
It tests core functionality, error handling, and integration capabilities.
"""

import asyncio
import sys
import traceback
import time
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class TestResult:
    """Test result data structure"""
    agent_name: str
    test_name: str
    success: bool
    execution_time: float
    error_message: str = None
    details: Dict[str, Any] = None

class DetailedAgentTester:
    """Comprehensive agent testing suite"""
    
    def __init__(self):
        self.test_results = []
        self.test_company = "Apple Inc."
        self.test_crypto = "Bitcoin"
        
    async def run_all_tests(self):
        """Run all comprehensive agent tests"""
        print("🤖 IntelliVest AI - Detailed Agent Testing Suite")
        print("=" * 60)
        
        # Test individual agents
        await self.test_research_agent()
        await self.test_sentiment_agent()
        await self.test_valuation_agent()
        await self.test_thesis_agent()
        await self.test_critique_agent()
        await self.test_crypto_agent()
        await self.test_enhanced_thesis_rewrite_agent()
        await self.test_base_agent()
        await self.test_agent_communication_system()
        await self.test_crew_agents_with_tools()
        
        # Generate comprehensive report
        self.generate_test_report()
    
    async def test_research_agent(self):
        """Test Research Agent functionality"""
        print("\n🔍 Testing Research Agent...")
        
        try:
            from agents.research_agent import ResearchAgent
            
            # Test 1: Agent Initialization
            start_time = time.time()
            agent = ResearchAgent()
            init_time = time.time() - start_time
            
            self.test_results.append(TestResult(
                agent_name="Research Agent",
                test_name="Initialization",
                success=True,
                execution_time=init_time,
                details={"agent_type": type(agent).__name__}
            ))
            print("✅ Initialization: Success")
            
            # Test 2: Core Analysis Method
            start_time = time.time()
            analysis_result = await agent.analyze(self.test_company)
            analysis_time = time.time() - start_time
            
            success = isinstance(analysis_result, dict) and "company_name" in analysis_result
            self.test_results.append(TestResult(
                agent_name="Research Agent",
                test_name="Core Analysis",
                success=success,
                execution_time=analysis_time,
                details={"result_keys": list(analysis_result.keys()) if isinstance(analysis_result, dict) else None}
            ))
            print(f"✅ Core Analysis: {'Success' if success else 'Failed'}")
            
            # Test 3: Research Company Method
            start_time = time.time()
            research_result = await agent.research_company(self.test_company)
            research_time = time.time() - start_time
            
            success = isinstance(research_result, dict) and "latest_news" in research_result
            self.test_results.append(TestResult(
                agent_name="Research Agent",
                test_name="Research Company",
                success=success,
                execution_time=research_time,
                details={"has_news": "latest_news" in research_result if isinstance(research_result, dict) else False}
            ))
            print(f"✅ Research Company: {'Success' if success else 'Failed'}")
            
            # Test 4: Message Handling
            start_time = time.time()
            message = {
                "sender": "test_agent",
                "recipient": "research_agent",
                "message_type": "data_request",
                "content": {"request_type": "company_data", "company_name": self.test_company}
            }
            message_result = await agent.handle_message(message)
            message_time = time.time() - start_time
            
            success = isinstance(message_result, dict)
            self.test_results.append(TestResult(
                agent_name="Research Agent",
                test_name="Message Handling",
                success=success,
                execution_time=message_time,
                details={"response_type": type(message_result).__name__}
            ))
            print(f"✅ Message Handling: {'Success' if success else 'Failed'}")
            
        except Exception as e:
            self.test_results.append(TestResult(
                agent_name="Research Agent",
                test_name="General",
                success=False,
                execution_time=0,
                error_message=str(e)
            ))
            print(f"❌ Research Agent Test Failed: {e}")
    
    async def test_sentiment_agent(self):
        """Test Sentiment Agent functionality"""
        print("\n😊 Testing Sentiment Agent...")
        
        try:
            from agents.sentiment_agent import SentimentAgent
            
            # Test 1: Agent Initialization
            start_time = time.time()
            agent = SentimentAgent()
            init_time = time.time() - start_time
            
            self.test_results.append(TestResult(
                agent_name="Sentiment Agent",
                test_name="Initialization",
                success=True,
                execution_time=init_time,
                details={"agent_type": type(agent).__name__}
            ))
            print("✅ Initialization: Success")
            
            # Test 2: Core Analysis Method
            start_time = time.time()
            analysis_result = await agent.analyze(self.test_company)
            analysis_time = time.time() - start_time
            
            success = isinstance(analysis_result, dict)
            self.test_results.append(TestResult(
                agent_name="Sentiment Agent",
                test_name="Core Analysis",
                success=success,
                execution_time=analysis_time,
                details={"result_type": type(analysis_result).__name__}
            ))
            print(f"✅ Core Analysis: {'Success' if success else 'Failed'}")
            
            # Test 3: Sentiment Analysis Method
            start_time = time.time()
            sentiment_result = await agent.analyze_sentiment(self.test_company)
            sentiment_time = time.time() - start_time
            
            success = isinstance(sentiment_result, dict)
            self.test_results.append(TestResult(
                agent_name="Sentiment Agent",
                test_name="Sentiment Analysis",
                success=success,
                execution_time=sentiment_time,
                details={"has_sentiment_data": "news_sentiment" in sentiment_result if isinstance(sentiment_result, dict) else False}
            ))
            print(f"✅ Sentiment Analysis: {'Success' if success else 'Failed'}")
            
            # Test 4: Data Provision
            start_time = time.time()
            data_result = await agent.provide_data("sentiment_data", self.test_company, ["news_sentiment"])
            data_time = time.time() - start_time
            
            success = isinstance(data_result, dict) and "agent" in data_result
            self.test_results.append(TestResult(
                agent_name="Sentiment Agent",
                test_name="Data Provision",
                success=success,
                execution_time=data_time,
                details={"response_keys": list(data_result.keys()) if isinstance(data_result, dict) else None}
            ))
            print(f"✅ Data Provision: {'Success' if success else 'Failed'}")
            
        except Exception as e:
            self.test_results.append(TestResult(
                agent_name="Sentiment Agent",
                test_name="General",
                success=False,
                execution_time=0,
                error_message=str(e)
            ))
            print(f"❌ Sentiment Agent Test Failed: {e}")
    
    async def test_valuation_agent(self):
        """Test Valuation Agent functionality"""
        print("\n💰 Testing Valuation Agent...")
        
        try:
            from agents.valuation_agent import ValuationAgent
            
            # Test 1: Agent Initialization
            start_time = time.time()
            agent = ValuationAgent()
            init_time = time.time() - start_time
            
            self.test_results.append(TestResult(
                agent_name="Valuation Agent",
                test_name="Initialization",
                success=True,
                execution_time=init_time,
                details={"agent_type": type(agent).__name__}
            ))
            print("✅ Initialization: Success")
            
            # Test 2: Core Analysis Method
            start_time = time.time()
            analysis_result = await agent.analyze(self.test_company)
            analysis_time = time.time() - start_time
            
            success = isinstance(analysis_result, dict)
            self.test_results.append(TestResult(
                agent_name="Valuation Agent",
                test_name="Core Analysis",
                success=success,
                execution_time=analysis_time,
                details={"result_type": type(analysis_result).__name__}
            ))
            print(f"✅ Core Analysis: {'Success' if success else 'Failed'}")
            
            # Test 3: Valuation Analysis Method
            start_time = time.time()
            valuation_result = await agent.analyze_valuation(self.test_company)
            valuation_time = time.time() - start_time
            
            success = isinstance(valuation_result, dict)
            self.test_results.append(TestResult(
                agent_name="Valuation Agent",
                test_name="Valuation Analysis",
                success=success,
                execution_time=valuation_time,
                details={"has_valuation_data": "financial_ratios" in valuation_result if isinstance(valuation_result, dict) else False}
            ))
            print(f"✅ Valuation Analysis: {'Success' if success else 'Failed'}")
            
        except Exception as e:
            self.test_results.append(TestResult(
                agent_name="Valuation Agent",
                test_name="General",
                success=False,
                execution_time=0,
                error_message=str(e)
            ))
            print(f"❌ Valuation Agent Test Failed: {e}")
    
    async def test_thesis_agent(self):
        """Test Thesis Agent functionality"""
        print("\n📝 Testing Thesis Agent...")
        
        try:
            from agents.thesis_agent import ThesisAgent
            
            # Test 1: Agent Initialization
            start_time = time.time()
            agent = ThesisAgent()
            init_time = time.time() - start_time
            
            self.test_results.append(TestResult(
                agent_name="Thesis Agent",
                test_name="Initialization",
                success=True,
                execution_time=init_time,
                details={"agent_type": type(agent).__name__}
            ))
            print("✅ Initialization: Success")
            
            # Test 2: Core Analysis Method
            start_time = time.time()
            analysis_result = await agent.analyze(self.test_company)
            analysis_time = time.time() - start_time
            
            success = isinstance(analysis_result, dict)
            self.test_results.append(TestResult(
                agent_name="Thesis Agent",
                test_name="Core Analysis",
                success=success,
                execution_time=analysis_time,
                details={"result_type": type(analysis_result).__name__}
            ))
            print(f"✅ Core Analysis: {'Success' if success else 'Failed'}")
            
            # Test 3: Thesis Generation Method
            start_time = time.time()
            thesis_result = await agent.generate_thesis(self.test_company, {})
            thesis_time = time.time() - start_time
            
            success = isinstance(thesis_result, dict)
            self.test_results.append(TestResult(
                agent_name="Thesis Agent",
                test_name="Thesis Generation",
                success=success,
                execution_time=thesis_time,
                details={"has_thesis": "investment_thesis" in thesis_result if isinstance(thesis_result, dict) else False}
            ))
            print(f"✅ Thesis Generation: {'Success' if success else 'Failed'}")
            
        except Exception as e:
            self.test_results.append(TestResult(
                agent_name="Thesis Agent",
                test_name="General",
                success=False,
                execution_time=0,
                error_message=str(e)
            ))
            print(f"❌ Thesis Agent Test Failed: {e}")
    
    async def test_critique_agent(self):
        """Test Critique Agent functionality"""
        print("\n🔍 Testing Critique Agent...")
        
        try:
            from agents.critique_agent import CritiqueAgent
            
            # Test 1: Agent Initialization
            start_time = time.time()
            agent = CritiqueAgent()
            init_time = time.time() - start_time
            
            self.test_results.append(TestResult(
                agent_name="Critique Agent",
                test_name="Initialization",
                success=True,
                execution_time=init_time,
                details={"agent_type": type(agent).__name__}
            ))
            print("✅ Initialization: Success")
            
            # Test 2: Core Analysis Method
            start_time = time.time()
            analysis_result = await agent.analyze(self.test_company)
            analysis_time = time.time() - start_time
            
            success = isinstance(analysis_result, dict)
            self.test_results.append(TestResult(
                agent_name="Critique Agent",
                test_name="Core Analysis",
                success=success,
                execution_time=analysis_time,
                details={"result_type": type(analysis_result).__name__}
            ))
            print(f"✅ Core Analysis: {'Success' if success else 'Failed'}")
            
            # Test 3: Critique Method
            start_time = time.time()
            critique_result = await agent.critique_thesis(self.test_company, {"investment_thesis": "Test thesis"})
            critique_time = time.time() - start_time
            
            success = isinstance(critique_result, dict)
            self.test_results.append(TestResult(
                agent_name="Critique Agent",
                test_name="Thesis Critique",
                success=success,
                execution_time=critique_time,
                details={"has_critique": "critique" in critique_result if isinstance(critique_result, dict) else False}
            ))
            print(f"✅ Thesis Critique: {'Success' if success else 'Failed'}")
            
        except Exception as e:
            self.test_results.append(TestResult(
                agent_name="Critique Agent",
                test_name="General",
                success=False,
                execution_time=0,
                error_message=str(e)
            ))
            print(f"❌ Critique Agent Test Failed: {e}")
    
    async def test_crypto_agent(self):
        """Test Crypto Agent functionality"""
        print("\n🪙 Testing Crypto Agent...")
        
        try:
            from agents.crypto_agent import CryptoAgent
            
            # Test 1: Agent Initialization
            start_time = time.time()
            agent = CryptoAgent()
            init_time = time.time() - start_time
            
            self.test_results.append(TestResult(
                agent_name="Crypto Agent",
                test_name="Initialization",
                success=True,
                execution_time=init_time,
                details={"agent_type": type(agent).__name__}
            ))
            print("✅ Initialization: Success")
            
            # Test 2: Cryptocurrency Analysis Method
            start_time = time.time()
            crypto_result = await agent.analyze_cryptocurrency(self.test_crypto)
            crypto_time = time.time() - start_time
            
            success = isinstance(crypto_result, dict) and "crypto_name" in crypto_result
            self.test_results.append(TestResult(
                agent_name="Crypto Agent",
                test_name="Cryptocurrency Analysis",
                success=success,
                execution_time=crypto_time,
                details={"has_market_data": "market_analysis" in crypto_result if isinstance(crypto_result, dict) else False}
            ))
            print(f"✅ Cryptocurrency Analysis: {'Success' if success else 'Failed'}")
            
        except Exception as e:
            self.test_results.append(TestResult(
                agent_name="Crypto Agent",
                test_name="General",
                success=False,
                execution_time=0,
                error_message=str(e)
            ))
            print(f"❌ Crypto Agent Test Failed: {e}")
    
    async def test_enhanced_thesis_rewrite_agent(self):
        """Test Enhanced Thesis Rewrite Agent functionality"""
        print("\n✏️ Testing Enhanced Thesis Rewrite Agent...")
        
        try:
            from agents.enhanced_thesis_rewrite_agent import EnhancedThesisRewriteAgent
            
            # Test 1: Agent Initialization
            start_time = time.time()
            agent = EnhancedThesisRewriteAgent()
            init_time = time.time() - start_time
            
            self.test_results.append(TestResult(
                agent_name="Enhanced Thesis Rewrite Agent",
                test_name="Initialization",
                success=True,
                execution_time=init_time,
                details={"agent_type": type(agent).__name__}
            ))
            print("✅ Initialization: Success")
            
            # Test 2: Thesis Rewrite Method
            start_time = time.time()
            rewrite_result = await agent.rewrite_thesis(self.test_company, {"investment_thesis": "Test thesis"})
            rewrite_time = time.time() - start_time
            
            success = isinstance(rewrite_result, dict)
            self.test_results.append(TestResult(
                agent_name="Enhanced Thesis Rewrite Agent",
                test_name="Thesis Rewrite",
                success=success,
                execution_time=rewrite_time,
                details={"has_rewritten_thesis": "rewritten_thesis" in rewrite_result if isinstance(rewrite_result, dict) else False}
            ))
            print(f"✅ Thesis Rewrite: {'Success' if success else 'Failed'}")
            
        except Exception as e:
            self.test_results.append(TestResult(
                agent_name="Enhanced Thesis Rewrite Agent",
                test_name="General",
                success=False,
                execution_time=0,
                error_message=str(e)
            ))
            print(f"❌ Enhanced Thesis Rewrite Agent Test Failed: {e}")
    
    async def test_base_agent(self):
        """Test Base Agent functionality"""
        print("\n🤖 Testing Base Agent...")
        
        try:
            from agents.base_agent import BaseAgent
            
            # Test 1: Base Agent Import
            start_time = time.time()
            # Note: BaseAgent is abstract, so we can't instantiate it directly
            init_time = time.time() - start_time
            
            self.test_results.append(TestResult(
                agent_name="Base Agent",
                test_name="Import",
                success=True,
                execution_time=init_time,
                details={"agent_type": "Abstract Base Class"}
            ))
            print("✅ Import: Success")
            
        except Exception as e:
            self.test_results.append(TestResult(
                agent_name="Base Agent",
                test_name="General",
                success=False,
                execution_time=0,
                error_message=str(e)
            ))
            print(f"❌ Base Agent Test Failed: {e}")
    
    async def test_agent_communication_system(self):
        """Test Agent Communication System functionality"""
        print("\n📡 Testing Agent Communication System...")
        
        try:
            from agents.agent_communication_system import AgentCommunicationSystem, AgentMessage, MessageType
            
            # Test 1: System Initialization
            start_time = time.time()
            comm_system = AgentCommunicationSystem()
            init_time = time.time() - start_time
            
            self.test_results.append(TestResult(
                agent_name="Agent Communication System",
                test_name="Initialization",
                success=True,
                execution_time=init_time,
                details={"system_type": type(comm_system).__name__}
            ))
            print("✅ Initialization: Success")
            
            # Test 2: Agent Registration
            start_time = time.time()
            comm_system.register_agent("test_agent", None, ["data_analysis"])
            reg_time = time.time() - start_time
            
            success = "test_agent" in comm_system.agents
            self.test_results.append(TestResult(
                agent_name="Agent Communication System",
                test_name="Agent Registration",
                success=success,
                execution_time=reg_time,
                details={"registered_agents": list(comm_system.agents.keys())}
            ))
            print(f"✅ Agent Registration: {'Success' if success else 'Failed'}")
            
        except Exception as e:
            self.test_results.append(TestResult(
                agent_name="Agent Communication System",
                test_name="General",
                success=False,
                execution_time=0,
                error_message=str(e)
            ))
            print(f"❌ Agent Communication System Test Failed: {e}")
    
    async def test_crew_agents_with_tools(self):
        """Test Crew Agents with Tools functionality"""
        print("\n🚀 Testing Crew Agents with Tools...")
        
        try:
            from agents.crew_agents_with_tools import InvestmentAnalysisCrewWithTools
            
            # Test 1: Crew Initialization
            start_time = time.time()
            crew = InvestmentAnalysisCrewWithTools()
            init_time = time.time() - start_time
            
            self.test_results.append(TestResult(
                agent_name="Crew Agents with Tools",
                test_name="Initialization",
                success=True,
                execution_time=init_time,
                details={"crew_type": type(crew).__name__}
            ))
            print("✅ Initialization: Success")
            
            # Test 2: Agent Availability
            start_time = time.time()
            expected_agents = ['researcher', 'sentiment_analyst', 'valuation_analyst', 'thesis_writer', 'critic']
            available_agents = [agent for agent in expected_agents if hasattr(crew, agent)]
            agent_check_time = time.time() - start_time
            
            success = len(available_agents) == len(expected_agents)
            self.test_results.append(TestResult(
                agent_name="Crew Agents with Tools",
                test_name="Agent Availability",
                success=success,
                execution_time=agent_check_time,
                details={"available_agents": available_agents, "expected_agents": expected_agents}
            ))
            print(f"✅ Agent Availability: {'Success' if success else 'Failed'}")
            
            # Test 3: Task Creation
            start_time = time.time()
            tasks = crew.create_tasks(self.test_company)
            task_creation_time = time.time() - start_time
            
            success = isinstance(tasks, list) and len(tasks) > 0
            self.test_results.append(TestResult(
                agent_name="Crew Agents with Tools",
                test_name="Task Creation",
                success=success,
                execution_time=task_creation_time,
                details={"task_count": len(tasks) if isinstance(tasks, list) else 0}
            ))
            print(f"✅ Task Creation: {'Success' if success else 'Failed'}")
            
        except Exception as e:
            self.test_results.append(TestResult(
                agent_name="Crew Agents with Tools",
                test_name="General",
                success=False,
                execution_time=0,
                error_message=str(e)
            ))
            print(f"❌ Crew Agents with Tools Test Failed: {e}")
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        # Group results by agent
        agent_results = {}
        for result in self.test_results:
            if result.agent_name not in agent_results:
                agent_results[result.agent_name] = []
            agent_results[result.agent_name].append(result)
        
        # Calculate statistics
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r.success)
        failed_tests = total_tests - successful_tests
        
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful: {successful_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        # Detailed agent results
        print(f"\n🤖 AGENT-BY-AGENT RESULTS:")
        for agent_name, results in agent_results.items():
            agent_success = sum(1 for r in results if r.success)
            agent_total = len(results)
            agent_success_rate = (agent_success/agent_total)*100 if agent_total > 0 else 0
            
            print(f"\n   {agent_name}:")
            print(f"     Tests: {agent_success}/{agent_total} ({agent_success_rate:.1f}%)")
            
            for result in results:
                status = "✅" if result.success else "❌"
                print(f"       {status} {result.test_name}: {result.execution_time:.2f}s")
                if result.error_message:
                    print(f"         Error: {result.error_message}")
                if result.details:
                    print(f"         Details: {result.details}")
        
        # Performance analysis
        print(f"\n⚡ PERFORMANCE ANALYSIS:")
        successful_results = [r for r in self.test_results if r.success]
        if successful_results:
            avg_time = sum(r.execution_time for r in successful_results) / len(successful_results)
            max_time = max(r.execution_time for r in successful_results)
            min_time = min(r.execution_time for r in successful_results)
            
            print(f"   Average Execution Time: {avg_time:.2f}s")
            print(f"   Fastest Test: {min_time:.2f}s")
            print(f"   Slowest Test: {max_time:.2f}s")
        
        # Final verdict
        print(f"\n🎯 FINAL VERDICT:")
        if successful_tests == total_tests:
            print("   🎉 ALL TESTS PASSED! The agent system is fully functional.")
        elif successful_tests >= total_tests * 0.8:
            print("   ✅ MOSTLY SUCCESSFUL! The agent system is working with minor issues.")
        elif successful_tests >= total_tests * 0.5:
            print("   ⚠️ PARTIALLY SUCCESSFUL! The agent system has significant issues.")
        else:
            print("   ❌ MOSTLY FAILED! The agent system has major issues.")
        
        print("\n" + "=" * 60)

async def main():
    """Main test execution"""
    tester = DetailedAgentTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 