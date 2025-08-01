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

# Import our custom tools
from tools.investment_tools import WebCrawlerTool, FinancialDataTool
from tools.dynamic_search_tools import DynamicWebSearchTool, InstitutionalDataTool
from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType

class ResearchAgent:
    """🔍 Research Agent for comprehensive company analysis"""
    
    def __init__(self):
        self.name = "Research Analyst"
        self.role = "Comprehensive company research and data gathering"
        self.backstory = """
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
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool(),
            InstitutionalDataTool(),
            WebCrawlerTool(),
            FinancialDataTool()
        ]
        
        # Initialize advanced fallback system
        self.fallback_system = AdvancedFallbackSystem()
        
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
                f"{company_name} financial ratios metrics",
                f"{company_name} balance sheet income statement",
                f"{company_name} cash flow analysis"
            ]
            
            additional_data = {}
            for query in additional_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    additional_data[query] = result
            
            return {
                "basic_data": financial_data,
                "additional_metrics": additional_data
            }
            
        except Exception as e:
            print(f"❌ Error getting financial data: {e}")
            return {}
    
    async def _get_institutional_data(self, company_name: str) -> Dict[str, Any]:
        """Get institutional data including FII holdings"""
        try:
            # Use institutional data tool
            institutional_tool = InstitutionalDataTool()
            institutional_data = institutional_tool._run(company_name)
            
            # Search for additional institutional information
            search_tool = DynamicWebSearchTool()
            additional_queries = [
                f"{company_name} FII holdings foreign institutional investors",
                f"{company_name} major shareholders ownership",
                f"{company_name} institutional ownership data",
                f"{company_name} mutual fund holdings",
                f"{company_name} options flow institutional activity"
            ]
            
            additional_data = {}
            for query in additional_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    additional_data[query] = result
            
            return {
                "institutional_data": institutional_data,
                "additional_institutional_info": additional_data
            }
            
        except Exception as e:
            print(f"❌ Error getting institutional data: {e}")
            return {}
    
    async def _analyze_business_model(self, company_name: str, research_data: Dict) -> str:
        """Analyze business model and market position"""
        try:
            # Use advanced fallback system for analysis
            prompt = f"""
            Analyze the business model and market position of {company_name} based on the following research data:
            
            Latest News: {research_data.get('latest_news', [])}
            Financial Data: {research_data.get('financial_data', {})}
            Institutional Data: {research_data.get('institutional_data', {})}
            
            Provide a comprehensive analysis covering:
            1. Business Model: How the company makes money
            2. Market Position: Competitive advantages and market share
            3. Revenue Streams: Primary and secondary revenue sources
            4. Growth Strategy: How the company plans to grow
            5. Market Trends: Industry trends affecting the company
            
            Format the analysis professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.RESEARCH,
                max_fallbacks=3
            )
            
            return result.content if result else "Business model analysis not available"
            
        except Exception as e:
            print(f"❌ Error analyzing business model: {e}")
            return "Business model analysis failed"
    
    async def _analyze_competition(self, company_name: str, research_data: Dict) -> str:
        """Analyze competitive landscape"""
        try:
            # Search for competitive information
            search_tool = DynamicWebSearchTool()
            competitive_queries = [
                f"{company_name} competitors competitive analysis",
                f"{company_name} market share industry position",
                f"{company_name} competitive advantages moat",
                f"{company_name} industry competitors comparison"
            ]
            
            competitive_data = []
            for query in competitive_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    competitive_data.append(result)
            
            # Analyze competitive landscape
            prompt = f"""
            Analyze the competitive landscape for {company_name} based on the following data:
            
            Competitive Data: {competitive_data}
            Financial Data: {research_data.get('financial_data', {})}
            
            Provide analysis covering:
            1. Main Competitors: Key competitors in the market
            2. Competitive Advantages: What makes this company unique
            3. Market Share: Company's position relative to competitors
            4. Competitive Threats: Potential challenges from competitors
            5. Industry Dynamics: How competition affects the business
            
            Format professionally for investment analysis.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.RESEARCH,
                max_fallbacks=3
            )
            
            return result.content if result else "Competitive analysis not available"
            
        except Exception as e:
            print(f"❌ Error analyzing competition: {e}")
            return "Competitive analysis failed"
    
    async def _analyze_risks_and_growth(self, company_name: str, research_data: Dict) -> Dict[str, Any]:
        """Analyze risk factors and growth prospects"""
        try:
            # Search for risk and growth information
            search_tool = DynamicWebSearchTool()
            risk_queries = [
                f"{company_name} risk factors challenges",
                f"{company_name} growth prospects opportunities",
                f"{company_name} regulatory risks compliance",
                f"{company_name} market risks volatility"
            ]
            
            risk_data = []
            for query in risk_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    risk_data.append(result)
            
            # Analyze risks and growth
            prompt = f"""
            Analyze risk factors and growth prospects for {company_name} based on:
            
            Risk Data: {risk_data}
            Financial Data: {research_data.get('financial_data', {})}
            News Data: {research_data.get('latest_news', [])}
            
            Provide analysis covering:
            
            RISK FACTORS:
            1. Market Risks: Industry and market-related risks
            2. Financial Risks: Debt, liquidity, and financial risks
            3. Operational Risks: Business and operational challenges
            4. Regulatory Risks: Compliance and regulatory issues
            5. Competitive Risks: Threats from competitors
            
            GROWTH PROSPECTS:
            1. Market Opportunities: Potential growth areas
            2. Strategic Initiatives: Company's growth strategies
            3. Industry Trends: Favorable industry developments
            4. Innovation Potential: R&D and innovation opportunities
            5. Geographic Expansion: International growth potential
            
            Format professionally for investment analysis.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.RESEARCH,
                max_fallbacks=3
            )
            
            # Parse the result to separate risks and growth
            content = result.content if result else "Risk and growth analysis not available"
            
            # Simple parsing - in production, you'd want more sophisticated parsing
            risks = []
            growth = ""
            
            if "RISK FACTORS:" in content:
                risk_section = content.split("RISK FACTORS:")[1].split("GROWTH PROSPECTS:")[0]
                risks = [line.strip() for line in risk_section.split('\n') if line.strip() and line.strip()[0].isdigit()]
            
            if "GROWTH PROSPECTS:" in content:
                growth_section = content.split("GROWTH PROSPECTS:")[1]
                growth = growth_section.strip()
            
            return {
                "risks": risks,
                "growth": growth
            }
            
        except Exception as e:
            print(f"❌ Error analyzing risks and growth: {e}")
            return {
                "risks": ["Risk analysis failed"],
                "growth": "Growth analysis failed"
            }
    
    async def handle_message(self, message):
        """
        Handle incoming messages from other agents
        
        Args:
            message: AgentMessage object containing the message
            
        Returns:
            Response dictionary
        """
        try:
            if message.message_type.value == "data_request":
                return await self._handle_data_request(message)
            elif message.message_type.value == "collaboration_request":
                return await self._handle_collaboration_request(message)
            elif message.message_type.value == "analysis_request":
                return await self._handle_analysis_request(message)
            elif message.message_type.value == "validation_request":
                return await self._handle_validation_request(message)
            else:
                return {
                    "status": "success",
                    "agent": self.name,
                    "message_type": message.message_type.value,
                    "response": f"Processed {message.message_type.value} from {message.sender}"
                }
        except Exception as e:
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e)
            }
    
    async def _handle_data_request(self, message):
        """Handle data requests from other agents"""
        company_name = message.content.get("company_name", "")
        request_type = message.content.get("request_type", "")
        
        if request_type == "company_research":
            research_data = await self.research_company(company_name)
            return {
                "status": "success",
                "agent": self.name,
                "data": research_data,
                "data_type": "company_research"
            }
        elif request_type == "financial_data":
            financial_data = await self._get_financial_data(company_name)
            return {
                "status": "success",
                "agent": self.name,
                "data": financial_data,
                "data_type": "financial_data"
            }
        else:
            return {
                "status": "success",
                "agent": self.name,
                "response": f"Provided {request_type} data for {company_name}"
            }
    
    async def _handle_collaboration_request(self, message):
        """Handle collaboration requests from other agents"""
        collaboration_type = message.content.get("collaboration_type", "")
        shared_data = message.content.get("shared_data", {})
        
        return {
            "status": "success",
            "agent": self.name,
            "collaboration_type": collaboration_type,
            "response": f"Collaborating on {collaboration_type}"
        }
    
    async def _handle_analysis_request(self, message):
        """Handle analysis requests from other agents"""
        analysis_type = message.content.get("analysis_type", "")
        data = message.content.get("data", {})
        
        return {
            "status": "success",
            "agent": self.name,
            "analysis_type": analysis_type,
            "response": f"Performed {analysis_type} analysis"
        }
    
    async def _handle_validation_request(self, message):
        """Handle validation requests from other agents"""
        validation_type = message.content.get("validation_type", "")
        data = message.content.get("data", {})
        
        return {
            "status": "success",
            "agent": self.name,
            "validation_type": validation_type,
            "response": f"Validated {validation_type}"
        }

# Export the agent
__all__ = ['ResearchAgent'] 