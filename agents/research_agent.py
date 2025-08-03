"""
📚 Research Agent - Comprehensive Financial Research & Analysis
=============================================================

This agent conducts comprehensive financial research including:
- Company overview and business model analysis
- Financial performance and ratio analysis
- Market position and competitive analysis
- Risk assessment and industry trends
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools and base agent
from tools.investment_tools import WebCrawlerTool, FinancialDataTool
from tools.dynamic_search_tools import DynamicWebSearchTool, InstitutionalDataTool
from agents.base_agent import BaseAgent
from llm.advanced_fallback_system import TaskType

class ResearchAgent(BaseAgent):
    """🔍 Research Agent for comprehensive company analysis"""
    
    def __init__(self):
        """Initialize the research agent"""
        super().__init__(
            name="Research Analyst",
            role="Comprehensive company research and data gathering",
            backstory="""
            You are an expert research analyst with 15+ years of experience in financial markets.
            You specialize in gathering comprehensive information about companies, including:
            - Latest news and market developments
            - Business model and competitive analysis
            - Financial metrics and performance data
            - Market position and industry trends
            - Institutional holdings and FII data
            - Cryptocurrency market data (if applicable)
            
            You use dynamic web search to find the most recent and relevant information
            from live, publicly available sources. You never rely on outdated or hard-coded sources.
            """
        )
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool(),
            InstitutionalDataTool(),
            WebCrawlerTool(),
            FinancialDataTool()
        ]
        
    async def analyze(self, company_name: str, **kwargs) -> Dict[str, Any]:
        """
        Main analysis method - conducts comprehensive research
        
        Args:
            company_name: Name or symbol of the company to research
            **kwargs: Additional parameters (not used for research)
            
        Returns:
            Dictionary containing comprehensive research data
        """
        return await self.research_company(company_name)
    
    async def research_company(self, company_name: str) -> Dict[str, Any]:
        """
        Conduct comprehensive research on a company
        
        Args:
            company_name: Name or symbol of the company to research
            
        Returns:
            Dictionary containing comprehensive research data
        """
        print(f"🔍 Research Agent: Starting comprehensive research on {company_name}")
        
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
            "data_sources": []
        }
        
        try:
            # 1. Dynamic web search for latest news and developments
            print("📰 Searching for latest news and developments...")
            news_data = await self._search_latest_news(company_name)
            research_data["latest_news"] = news_data
            
            # 2. Get financial data and metrics
            print("📊 Gathering financial data and metrics...")
            financial_data = await self._get_financial_data(company_name)
            research_data["financial_data"] = financial_data
            
            # 3. Search for institutional data (FII, holdings, etc.)
            print("🏦 Searching for institutional data...")
            institutional_data = await self._get_institutional_data(company_name)
            research_data["institutional_data"] = institutional_data
            
            # 4. Analyze business model and market position
            print("🏢 Analyzing business model and market position...")
            business_analysis = await self._analyze_business_model(company_name, research_data)
            research_data["business_analysis"] = business_analysis
            
            # 5. Assess competitive landscape
            print("🎯 Assessing competitive landscape...")
            competitive_analysis = await self._analyze_competition(company_name, research_data)
            research_data["competitive_landscape"] = competitive_analysis
            
            # 6. Identify risk factors and growth prospects
            print("⚠️ Identifying risk factors and growth prospects...")
            risk_analysis = await self._analyze_risks_and_growth(company_name, research_data)
            research_data["risk_factors"] = risk_analysis["risks"]
            research_data["growth_prospects"] = risk_analysis["growth"]
            
            print(f"✅ Research Agent: Completed comprehensive research on {company_name}")
            return research_data
            
        except Exception as e:
            print(f"❌ Research Agent: Error during research - {str(e)}")
            return research_data
    
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide research data to other agents"""
        try:
            if request_type == "research_data":
                # Return existing research data if available, otherwise conduct new research
                research_data = await self.research_company(company_name)
                return {
                    "agent": self.name,
                    "data_type": request_type,
                    "company_name": company_name,
                    "data": research_data,
                    "message": f"Research data provided for {company_name}"
                }
            else:
                return await super().provide_data(request_type, company_name, specific_data)
                
        except Exception as e:
            return {
                "agent": self.name,
                "data_type": request_type,
                "company_name": company_name,
                "data": {},
                "error": f"Error providing research data: {str(e)}"
            }
    
    async def _search_latest_news(self, company_name: str) -> List[Dict[str, Any]]:
        """Search for latest news and developments"""
        try:
            # Use dynamic web search tool
            search_tool = DynamicWebSearchTool()
            
            # Search queries for latest news
            queries = [
                f"{company_name} latest news developments",
                f"{company_name} recent announcements earnings",
                f"{company_name} market updates stock price",
                f"{company_name} business developments strategy"
            ]
            
            news_results = []
            for query in queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    news_results.append({
                        "query": query,
                        "content": result,
                        "timestamp": asyncio.get_event_loop().time()
                    })
            
            return news_results
            
        except Exception as e:
            print(f"❌ Error searching latest news: {e}")
            return []
    
    async def _get_financial_data(self, company_name: str) -> Dict[str, Any]:
        """Get comprehensive financial data"""
        try:
            # Use financial data tool
            financial_tool = FinancialDataTool()
            financial_data = financial_tool._run(company_name)
            
            # Also search for additional financial metrics
            search_tool = DynamicWebSearchTool()
            additional_queries = [
                f"{company_name} financial ratios P/E P/B ROE",
                f"{company_name} revenue growth profit margin",
                f"{company_name} balance sheet cash flow"
            ]
            
            additional_data = {}
            for query in additional_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    additional_data[query] = result
            
            return {
                "financial_metrics": financial_data,
                "additional_financial_data": additional_data
            }
            
        except Exception as e:
            print(f"❌ Error getting financial data: {e}")
            return {}
    
    async def _get_institutional_data(self, company_name: str) -> Dict[str, Any]:
        """Get institutional data and holdings"""
        try:
            # Use institutional data tool
            institutional_tool = InstitutionalDataTool()
            institutional_data = institutional_tool._run(company_name)
            
            # Also search for FII and institutional holdings
            search_tool = DynamicWebSearchTool()
            queries = [
                f"{company_name} FII holdings institutional investors",
                f"{company_name} mutual fund holdings",
                f"{company_name} insider trading institutional ownership"
            ]
            
            additional_data = {}
            for query in queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    additional_data[query] = result
            
            return {
                "institutional_holdings": institutional_data,
                "additional_institutional_data": additional_data
            }
            
        except Exception as e:
            print(f"❌ Error getting institutional data: {e}")
            return {}
    
    async def _analyze_business_model(self, company_name: str, research_data: Dict) -> str:
        """Analyze business model and market position"""
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
            
            response = await llm.ainvoke([{"role": "user", "content": context}])
            return response.content
            
        except Exception as e:
            print(f"❌ Error analyzing business model: {e}")
            return f"Business model analysis for {company_name} could not be completed due to an error."
    
    async def _analyze_competition(self, company_name: str, research_data: Dict) -> str:
        """Analyze competitive landscape"""
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
            
            response = await llm.ainvoke([{"role": "user", "content": context}])
            return response.content
            
        except Exception as e:
            print(f"❌ Error analyzing competition: {e}")
            return f"Competitive analysis for {company_name} could not be completed due to an error."
    
    async def _analyze_risks_and_growth(self, company_name: str, research_data: Dict) -> Dict[str, Any]:
        """Analyze risks and growth prospects"""
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
            
            response = await llm.ainvoke([{"role": "user", "content": context}])
            
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
            print(f"❌ Error analyzing risks and growth: {e}")
            return {
                "risks": [f"Risk analysis for {company_name} could not be completed due to an error."],
                "growth": f"Growth analysis for {company_name} could not be completed due to an error."
            } 