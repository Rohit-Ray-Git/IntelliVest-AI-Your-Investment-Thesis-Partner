"""
💰 Valuation Agent - Financial Valuation & Analysis
==================================================

This agent performs comprehensive financial valuation including:
- DCF (Discounted Cash Flow) analysis
- Comparable company analysis
- Financial ratio analysis
- Intrinsic value calculations
- Risk-adjusted valuations
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools and base agent
from tools.investment_tools import FinancialDataTool, ValuationTool
from tools.dynamic_search_tools import DynamicWebSearchTool
from agents.base_agent import BaseAgent
from llm.advanced_fallback_system import TaskType

class ValuationAgent(BaseAgent):
    """💰 Valuation Agent for financial analysis and valuation"""
    
    def __init__(self):
        """Initialize the valuation agent"""
        super().__init__(
            name="Valuation Analyst",
            role="Financial valuation and intrinsic value analysis",
            backstory="""
            You are an expert valuation analyst with 15+ years of experience in financial modeling.
            You specialize in comprehensive financial valuation, including:
            - DCF (Discounted Cash Flow) analysis and modeling
            - Comparable company analysis and peer benchmarking
            - Financial ratio analysis and trend assessment
            - Intrinsic value calculations and fair value estimates
            - Risk-adjusted valuations and scenario analysis
            - Industry-specific valuation methodologies
            
            You use dynamic web search to find the most recent financial data
            and market information for accurate valuations.
            """
        )
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool(),
            FinancialDataTool(),
            ValuationTool()
        ]
        
    async def analyze(self, company_name: str, **kwargs) -> Dict[str, Any]:
        """
        Main analysis method - conducts comprehensive valuation
        
        Args:
            company_name: Name or symbol of the company to analyze
            **kwargs: Additional parameters including research_data and sentiment_data
            
        Returns:
            Dictionary containing comprehensive valuation analysis
        """
        research_data = kwargs.get('research_data', {})
        sentiment_data = kwargs.get('sentiment_data', {})
        return await self.conduct_valuation(company_name, research_data, sentiment_data)
    
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide valuation data to other agents"""
        try:
            if request_type == "valuation_data":
                # Conduct valuation analysis and return data
                valuation_data = await self.conduct_valuation(company_name)
                return {
                    "agent": self.name,
                    "data_type": request_type,
                    "company_name": company_name,
                    "data": valuation_data,
                    "message": f"Valuation data provided for {company_name}"
                }
            elif request_type == "financial_metrics":
                # Return financial metrics
                financial_metrics = await self._gather_financial_metrics(company_name)
                return {
                    "agent": self.name,
                    "data_type": request_type,
                    "company_name": company_name,
                    "data": financial_metrics,
                    "message": f"Financial metrics provided for {company_name}"
                }
            else:
                return await super().provide_data(request_type, company_name, specific_data)
                
        except Exception as e:
            return {
                "agent": self.name,
                "data_type": request_type,
                "company_name": company_name,
                "data": {},
                "error": f"Error providing valuation data: {str(e)}"
            }
    
    async def conduct_valuation(self, company_name: str, research_data: Dict[str, Any] = None, sentiment_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Conduct comprehensive financial valuation
        
        Args:
            company_name: Name or symbol of the company to value
            research_data: Optional research data from previous analysis
            sentiment_data: Optional sentiment data from previous analysis
            
        Returns:
            Dictionary containing comprehensive valuation analysis
        """
        print(f"💰 Valuation Agent: Starting valuation analysis for {company_name}")
        
        valuation_data = {
            "company_name": company_name,
            "financial_metrics": {},
            "dcf_analysis": {},
            "comparable_analysis": {},
            "relative_valuation": {},
            "asset_based_valuation": {},
            "growth_assessment": "",
            "risk_assessment": "",
            "fair_value_estimate": "",
            "valuation_range": "",
            "key_drivers": [],
            "valuation_risks": [],
            "data_sources": []
        }
        
        try:
            # 1. Gather comprehensive financial metrics
            print("📊 Gathering financial metrics...")
            financial_metrics = await self._gather_financial_metrics(company_name)
            valuation_data["financial_metrics"] = financial_metrics
            
            # 2. Perform DCF analysis
            print("💵 Performing DCF analysis...")
            dcf_analysis = await self._perform_dcf_analysis(company_name, financial_metrics)
            valuation_data["dcf_analysis"] = dcf_analysis
            
            # 3. Perform comparable company analysis
            print("🏢 Performing comparable company analysis...")
            comparable_analysis = await self._perform_comparable_analysis(company_name, financial_metrics)
            valuation_data["comparable_analysis"] = comparable_analysis
            
            # 4. Perform relative valuation
            print("📈 Performing relative valuation...")
            relative_valuation = await self._perform_relative_valuation(company_name, financial_metrics)
            valuation_data["relative_valuation"] = relative_valuation
            
            # 5. Perform asset-based valuation
            print("🏗️ Performing asset-based valuation...")
            asset_valuation = await self._perform_asset_based_valuation(company_name, financial_metrics)
            valuation_data["asset_based_valuation"] = asset_valuation
            
            # 6. Assess growth prospects
            print("📈 Assessing growth prospects...")
            growth_assessment = await self._assess_growth_prospects(company_name, valuation_data)
            valuation_data["growth_assessment"] = growth_assessment
            
            # 7. Assess valuation risks
            print("⚠️ Assessing valuation risks...")
            risk_assessment = await self._assess_valuation_risks(company_name, valuation_data)
            valuation_data["risk_assessment"] = risk_assessment
            
            # 8. Calculate fair value estimate
            print("🎯 Calculating fair value estimate...")
            fair_value = await self._calculate_fair_value(valuation_data)
            valuation_data["fair_value_estimate"] = fair_value["estimate"]
            valuation_data["valuation_range"] = fair_value["range"]
            valuation_data["key_drivers"] = fair_value["drivers"]
            valuation_data["valuation_risks"] = fair_value["risks"]
            
            print(f"✅ Valuation Agent: Completed valuation analysis for {company_name}")
            return valuation_data
            
        except Exception as e:
            print(f"❌ Valuation Agent: Error during valuation analysis - {str(e)}")
            return valuation_data 