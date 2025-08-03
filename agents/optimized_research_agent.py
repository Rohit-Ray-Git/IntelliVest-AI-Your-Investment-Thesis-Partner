"""
⚡ Optimized Research Agent - High-Speed Financial Research & Analysis
=====================================================================

This agent conducts comprehensive financial research using parallel processing
to dramatically reduce execution time while maintaining data quality.
"""

import asyncio
import os
import time
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import concurrent.futures

# Load environment variables
load_dotenv()

# Import our optimized tools and base agent
from tools.parallel_search_tools import ParallelWebSearchTool, ParallelInstitutionalDataTool
from tools.investment_tools import WebCrawlerTool, FinancialDataTool
from agents.base_agent import BaseAgent
from llm.advanced_fallback_system import TaskType

class OptimizedResearchAgent(BaseAgent):
    """⚡ Optimized Research Agent for high-speed company analysis"""
    
    def __init__(self, max_concurrent: int = 10):
        """Initialize the optimized research agent"""
        super().__init__(
            name="Optimized Research Analyst",
            role="High-speed comprehensive company research and data gathering",
            backstory="""
            You are an expert research analyst with 15+ years of experience in financial markets.
            You specialize in gathering comprehensive information about companies using parallel
            processing techniques to achieve maximum speed and efficiency.
            
            You use parallel web search to find the most recent and relevant information
            from live, publicly available sources with dramatically reduced execution time.
            """
        )
        
        # Initialize optimized tools with parallel processing
        self.tools = [
            ParallelWebSearchTool(max_concurrent=max_concurrent),
            ParallelInstitutionalDataTool(),
            WebCrawlerTool(),
            FinancialDataTool()
        ]
        
        # Performance settings
        self.max_concurrent = max_concurrent
        print(f"⚡ Optimized Research Agent initialized with {max_concurrent} concurrent workers")
        
    async def analyze(self, company_name: str, **kwargs) -> Dict[str, Any]:
        """
        Main analysis method - conducts comprehensive research with parallel processing
        
        Args:
            company_name: Name or symbol of the company to research
            **kwargs: Additional parameters (not used for research)
            
        Returns:
            Dictionary containing comprehensive research data
        """
        return await self.research_company_parallel(company_name)
    
    async def research_company_parallel(self, company_name: str) -> Dict[str, Any]:
        """
        Conduct comprehensive research on a company using parallel processing
        
        Args:
            company_name: Name or symbol of the company to research
            
        Returns:
            Dictionary containing comprehensive research data
        """
        print(f"⚡ Optimized Research Agent: Starting parallel research on {company_name}")
        start_time = time.time()
        
        research_data = {
            "company_name": company_name,
            "latest_news": [],
            "financial_data": {},
            "institutional_data": {},
            "business_analysis": "",
            "market_position": "",
            "competitive_landscape": "",
            "risk_factors": [],
            "growth_prospects": "",
            "data_sources": [],
            "execution_time": 0,
            "parallel_workers_used": self.max_concurrent
        }
        
        try:
            # Step 1: Parallel data gathering
            print("⚡ Starting parallel data gathering...")
            parallel_results = await self._gather_data_parallel(company_name)
            
            # Step 2: Parallel analysis
            print("🧠 Starting parallel analysis...")
            analysis_results = await self._analyze_data_parallel(company_name, parallel_results)
            
            # Step 3: Combine results
            research_data.update(parallel_results)
            research_data.update(analysis_results)
            
            end_time = time.time()
            execution_time = end_time - start_time
            research_data["execution_time"] = execution_time
            
            print(f"✅ Optimized Research Agent: Completed parallel research on {company_name}")
            print(f"⚡ Total execution time: {execution_time:.2f} seconds")
            print(f"📊 Parallel workers used: {self.max_concurrent}")
            
            return research_data
            
        except Exception as e:
            print(f"❌ Optimized Research Agent: Error during parallel research - {str(e)}")
            research_data["execution_time"] = time.time() - start_time
            return research_data
    
    async def _gather_data_parallel(self, company_name: str) -> Dict[str, Any]:
        """Gather all data in parallel using ThreadPoolExecutor"""
        
        # Define all data gathering tasks
        tasks = {
            "latest_news": self._search_latest_news_parallel,
            "financial_data": self._get_financial_data_parallel,
            "institutional_data": self._get_institutional_data_parallel
        }
        
        results = {}
        
        # Execute all tasks in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(task, company_name): task_name
                for task_name, task in tasks.items()
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_task, timeout=120):
                task_name = future_to_task[future]
                try:
                    result = future.result()
                    results[task_name] = result
                    print(f"✅ Parallel {task_name} completed")
                except Exception as e:
                    print(f"❌ Parallel {task_name} failed: {e}")
                    results[task_name] = {}
        
        return results
    
    async def _analyze_data_parallel(self, company_name: str, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze gathered data in parallel"""
        
        # Define all analysis tasks
        tasks = {
            "business_analysis": self._analyze_business_model_parallel,
            "competitive_landscape": self._analyze_competition_parallel,
            "risk_growth": self._analyze_risks_and_growth_parallel
        }
        
        results = {}
        
        # Execute all analysis tasks in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(task, company_name, research_data): task_name
                for task_name, task in tasks.items()
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_task, timeout=60):
                task_name = future_to_task[future]
                try:
                    result = future.result()
                    if task_name == "risk_growth":
                        results["risk_factors"] = result.get("risks", [])
                        results["growth_prospects"] = result.get("growth", "")
                    else:
                        results[task_name] = result
                    print(f"✅ Parallel {task_name} analysis completed")
                except Exception as e:
                    print(f"❌ Parallel {task_name} analysis failed: {e}")
                    if task_name == "risk_growth":
                        results["risk_factors"] = []
                        results["growth_prospects"] = ""
                    else:
                        results[task_name] = ""
        
        return results
    
    def _search_latest_news_parallel(self, company_name: str) -> List[Dict[str, Any]]:
        """Search for latest news using parallel processing"""
        try:
            # Use parallel search tool
            search_tool = ParallelWebSearchTool(max_concurrent=self.max_concurrent)
            
            # Multiple search queries for comprehensive coverage
            queries = [
                f"{company_name} latest news developments",
                f"{company_name} recent announcements earnings",
                f"{company_name} market updates stock price",
                f"{company_name} business developments strategy"
            ]
            
            news_results = []
            
            # Execute queries in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                future_to_query = {
                    executor.submit(search_tool._run, query): query
                    for query in queries
                }
                
                for future in concurrent.futures.as_completed(future_to_query, timeout=60):
                    query = future_to_query[future]
                    try:
                        result = future.result()
                        if result and "✅" in result:
                            news_results.append({
                                "query": query,
                                "content": result,
                                "timestamp": time.time()
                            })
                    except Exception as e:
                        print(f"❌ News query failed for {query}: {e}")
            
            return news_results
            
        except Exception as e:
            print(f"❌ Error in parallel news search: {e}")
            return []
    
    def _get_financial_data_parallel(self, company_name: str) -> Dict[str, Any]:
        """Get comprehensive financial data using parallel processing"""
        try:
            # Use financial data tool
            financial_tool = FinancialDataTool()
            financial_data = financial_tool._run(company_name)
            
            # Use parallel search for additional financial metrics
            search_tool = ParallelWebSearchTool(max_concurrent=self.max_concurrent)
            additional_queries = [
                f"{company_name} financial ratios P/E P/B ROE",
                f"{company_name} revenue growth profit margin",
                f"{company_name} balance sheet cash flow"
            ]
            
            additional_data = {}
            
            # Execute additional queries in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                future_to_query = {
                    executor.submit(search_tool._run, query): query
                    for query in additional_queries
                }
                
                for future in concurrent.futures.as_completed(future_to_query, timeout=60):
                    query = future_to_query[future]
                    try:
                        result = future.result()
                        if result and "✅" in result:
                            additional_data[query] = result
                    except Exception as e:
                        print(f"❌ Financial query failed for {query}: {e}")
            
            return {
                "financial_metrics": financial_data,
                "additional_financial_data": additional_data
            }
            
        except Exception as e:
            print(f"❌ Error in parallel financial data gathering: {e}")
            return {}
    
    def _get_institutional_data_parallel(self, company_name: str) -> Dict[str, Any]:
        """Get institutional data using parallel processing"""
        try:
            # Use parallel institutional data tool
            institutional_tool = ParallelInstitutionalDataTool()
            institutional_data = institutional_tool._run(company_name)
            
            return {
                "institutional_holdings": institutional_data,
                "additional_institutional_data": {}
            }
            
        except Exception as e:
            print(f"❌ Error in parallel institutional data gathering: {e}")
            return {}
    
    def _analyze_business_model_parallel(self, company_name: str, research_data: Dict[str, Any]) -> str:
        """Analyze business model using LLM in parallel"""
        try:
            # Use LLM to analyze business model
            llm = self._get_llm_for_task(TaskType.RESEARCH)
            
            # Prepare context from research data
            context = f"""
            Company: {company_name}
            
            Latest News: {research_data.get('latest_news', [])}
            Financial Data: {research_data.get('financial_data', {})}
            Institutional Data: {research_data.get('institutional_data', {})}
            
            Please analyze the business model and market position of {company_name} based on the available data.
            Focus on:
            1. Core business model and revenue streams
            2. Market position and competitive advantages
            3. Industry trends and market dynamics
            4. Growth strategy and future prospects
            """
            
            response = llm.invoke([{"role": "user", "content": context}])
            return response.content
            
        except Exception as e:
            print(f"❌ Error in parallel business model analysis: {e}")
            return f"Business model analysis for {company_name} could not be completed due to an error."
    
    def _analyze_competition_parallel(self, company_name: str, research_data: Dict[str, Any]) -> str:
        """Analyze competitive landscape using LLM in parallel"""
        try:
            # Use LLM to analyze competition
            llm = self._get_llm_for_task(TaskType.RESEARCH)
            
            # Prepare context from research data
            context = f"""
            Company: {company_name}
            
            Research Data: {research_data}
            
            Please analyze the competitive landscape for {company_name} based on the available data.
            Focus on:
            1. Direct competitors and their market positions
            2. Competitive advantages and disadvantages
            3. Market share and competitive dynamics
            4. Barriers to entry and competitive moats
            5. Competitive threats and opportunities
            """
            
            response = llm.invoke([{"role": "user", "content": context}])
            return response.content
            
        except Exception as e:
            print(f"❌ Error in parallel competition analysis: {e}")
            return f"Competitive analysis for {company_name} could not be completed due to an error."
    
    def _analyze_risks_and_growth_parallel(self, company_name: str, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risks and growth prospects using LLM in parallel"""
        try:
            # Use LLM to analyze risks and growth
            llm = self._get_llm_for_task(TaskType.RESEARCH)
            
            # Prepare context from research data
            context = f"""
            Company: {company_name}
            
            Research Data: {research_data}
            
            Please analyze the risks and growth prospects for {company_name} based on the available data.
            
            For Risks, identify:
            1. Business risks and operational challenges
            2. Financial risks and liquidity concerns
            3. Market risks and competitive threats
            4. Regulatory risks and compliance issues
            5. Technology risks and disruption potential
            
            For Growth Prospects, identify:
            1. Market expansion opportunities
            2. Product development potential
            3. Strategic initiatives and partnerships
            4. Industry trends favoring growth
            5. Competitive advantages supporting growth
            """
            
            response = llm.invoke([{"role": "user", "content": context}])
            
            # Parse the response to extract risks and growth
            content = response.content
            
            # Simple parsing - in a real implementation, you might use more sophisticated parsing
            risks = []
            growth = ""
            
            if "risks" in content.lower():
                risks = [line.strip() for line in content.split('\n') if any(risk_word in line.lower() for risk_word in ['risk', 'threat', 'challenge', 'concern'])]
            
            if "growth" in content.lower():
                growth = content
            
            return {
                "risks": risks,
                "growth": growth
            }
            
        except Exception as e:
            print(f"❌ Error in parallel risks and growth analysis: {e}")
            return {
                "risks": [f"Risk analysis for {company_name} could not be completed due to an error."],
                "growth": f"Growth analysis for {company_name} could not be completed due to an error."
            }
    
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide research data to other agents"""
        try:
            if request_type == "research_data":
                # Return existing research data if available, otherwise conduct new research
                research_data = await self.research_company_parallel(company_name)
                return {
                    "agent": self.name,
                    "data_type": request_type,
                    "company_name": company_name,
                    "data": research_data,
                    "message": f"Parallel research data provided for {company_name}"
                }
            else:
                return await super().provide_data(request_type, company_name, specific_data)
                
        except Exception as e:
            return {
                "agent": self.name,
                "data_type": request_type,
                "company_name": company_name,
                "data": {},
                "error": f"Error providing parallel research data: {str(e)}"
            }

# Export the optimized agent
__all__ = ['OptimizedResearchAgent'] 