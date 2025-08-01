"""
💰 Valuation Agent - Financial Valuation Analysis
===============================================

This agent handles comprehensive financial valuation including:
- DCF (Discounted Cash Flow) analysis
- Comparable company analysis
- Relative valuation metrics
- Asset-based valuation
- Growth and risk assessment
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools
from tools.investment_tools import ValuationTool, FinancialDataTool
from tools.dynamic_search_tools import DynamicWebSearchTool
from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType

class ValuationAgent:
    """💰 Valuation Agent for financial valuation analysis"""
    
    def __init__(self):
        self.name = "Valuation Expert"
        self.role = "Financial valuation and metrics analysis"
        self.backstory = """
        You are an expert valuation analyst with 15+ years of experience in financial modeling.
        You specialize in comprehensive company valuation using multiple methodologies:
        - DCF (Discounted Cash Flow) analysis
        - Comparable company analysis and peer benchmarking
        - Relative valuation metrics (P/E, P/B, EV/EBITDA, etc.)
        - Asset-based valuation approaches
        - Growth and risk-adjusted valuation models
        
        You use dynamic web search to find the latest financial data and market information
        from live, publicly available sources. You understand that valuation is both art and science.
        """
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool(),
            ValuationTool(),
            FinancialDataTool()
        ]
        
        # Initialize advanced fallback system
        self.fallback_system = AdvancedFallbackSystem()
        
    async def perform_valuation(self, company_name: str, research_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform comprehensive financial valuation
        
        Args:
            company_name: Name or symbol of the company to value
            research_data: Optional research data from previous analysis
            
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
    
    async def _gather_financial_metrics(self, company_name: str) -> Dict[str, Any]:
        """Gather comprehensive financial metrics"""
        try:
            # Use financial data tool
            financial_tool = FinancialDataTool()
            basic_financial_data = financial_tool._run(company_name)
            
            # Use dynamic search for additional metrics
            search_tool = DynamicWebSearchTool()
            additional_queries = [
                f"{company_name} financial ratios metrics analysis",
                f"{company_name} balance sheet income statement cash flow",
                f"{company_name} earnings growth revenue growth",
                f"{company_name} debt ratios financial health",
                f"{company_name} return on equity return on assets",
                f"{company_name} free cash flow operating cash flow"
            ]
            
            additional_metrics = {}
            for query in additional_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    additional_metrics[query] = result
            
            return {
                "basic_data": basic_financial_data,
                "additional_metrics": additional_metrics
            }
            
        except Exception as e:
            print(f"❌ Error gathering financial metrics: {e}")
            return {}
    
    async def _perform_dcf_analysis(self, company_name: str, financial_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Perform DCF (Discounted Cash Flow) analysis"""
        try:
            # Search for DCF-related data
            search_tool = DynamicWebSearchTool()
            dcf_queries = [
                f"{company_name} DCF analysis discounted cash flow",
                f"{company_name} free cash flow projections",
                f"{company_name} growth rate terminal value",
                f"{company_name} discount rate WACC analysis"
            ]
            
            dcf_data = {}
            for query in dcf_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    dcf_data[query] = result
            
            # Use AI to perform DCF analysis
            prompt = f"""
            Perform a DCF (Discounted Cash Flow) analysis for {company_name} based on:
            
            Financial Metrics: {financial_metrics}
            DCF Data: {dcf_data}
            
            Provide analysis covering:
            1. Free Cash Flow Projections: 5-year forecast
            2. Growth Rate Assumptions: Revenue and FCF growth
            3. Terminal Value Calculation: Perpetuity growth method
            4. Discount Rate: WACC calculation and assumptions
            5. Present Value Calculation: DCF value per share
            6. Sensitivity Analysis: Key value drivers
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.VALUATION,
                max_fallbacks=3
            )
            
            return {
                "dcf_analysis": result.content if result else "DCF analysis not available",
                "dcf_data": dcf_data
            }
            
        except Exception as e:
            print(f"❌ Error performing DCF analysis: {e}")
            return {"dcf_analysis": "DCF analysis failed", "dcf_data": {}}
    
    async def _perform_comparable_analysis(self, company_name: str, financial_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comparable company analysis"""
        try:
            # Search for comparable companies
            search_tool = DynamicWebSearchTool()
            comparable_queries = [
                f"{company_name} comparable companies peer analysis",
                f"{company_name} industry competitors valuation",
                f"{company_name} sector peers financial comparison",
                f"{company_name} similar companies market cap"
            ]
            
            comparable_data = {}
            for query in comparable_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    comparable_data[query] = result
            
            # Use AI to perform comparable analysis
            prompt = f"""
            Perform a comparable company analysis for {company_name} based on:
            
            Financial Metrics: {financial_metrics}
            Comparable Data: {comparable_data}
            
            Provide analysis covering:
            1. Peer Group Selection: Comparable companies
            2. Valuation Multiples: P/E, P/B, EV/EBITDA, EV/Sales
            3. Peer Benchmarking: How company compares to peers
            4. Multiple Analysis: Justification for premium/discount
            5. Implied Valuation: Value based on peer multiples
            6. Peer Comparison: Strengths and weaknesses vs peers
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.VALUATION,
                max_fallbacks=3
            )
            
            return {
                "comparable_analysis": result.content if result else "Comparable analysis not available",
                "comparable_data": comparable_data
            }
            
        except Exception as e:
            print(f"❌ Error performing comparable analysis: {e}")
            return {"comparable_analysis": "Comparable analysis failed", "comparable_data": {}}
    
    async def _perform_relative_valuation(self, company_name: str, financial_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Perform relative valuation analysis"""
        try:
            # Use valuation tool
            valuation_tool = ValuationTool()
            basic_valuation = valuation_tool._run(company_name)
            
            # Search for additional valuation metrics
            search_tool = DynamicWebSearchTool()
            valuation_queries = [
                f"{company_name} P/E ratio analysis",
                f"{company_name} price to book value analysis",
                f"{company_name} EV/EBITDA analysis",
                f"{company_name} PEG ratio analysis"
            ]
            
            additional_valuation = {}
            for query in valuation_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    additional_valuation[query] = result
            
            return {
                "basic_valuation": basic_valuation,
                "additional_valuation": additional_valuation
            }
            
        except Exception as e:
            print(f"❌ Error performing relative valuation: {e}")
            return {}
    
    async def _perform_asset_based_valuation(self, company_name: str, financial_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Perform asset-based valuation"""
        try:
            # Search for asset-based valuation data
            search_tool = DynamicWebSearchTool()
            asset_queries = [
                f"{company_name} book value per share",
                f"{company_name} tangible book value",
                f"{company_name} asset value liquidation value",
                f"{company_name} net asset value NAV"
            ]
            
            asset_data = {}
            for query in asset_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    asset_data[query] = result
            
            # Use AI to perform asset-based analysis
            prompt = f"""
            Perform an asset-based valuation for {company_name} based on:
            
            Financial Metrics: {financial_metrics}
            Asset Data: {asset_data}
            
            Provide analysis covering:
            1. Book Value Analysis: Book value per share
            2. Tangible Book Value: Adjusted for intangibles
            3. Asset Quality: Quality of assets on balance sheet
            4. Liquidation Value: Estimated liquidation value
            5. Asset Utilization: How efficiently assets are used
            6. Asset-Based Valuation: Value based on assets
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.VALUATION,
                max_fallbacks=3
            )
            
            return {
                "asset_analysis": result.content if result else "Asset-based analysis not available",
                "asset_data": asset_data
            }
            
        except Exception as e:
            print(f"❌ Error performing asset-based valuation: {e}")
            return {"asset_analysis": "Asset-based analysis failed", "asset_data": {}}
    
    async def _assess_growth_prospects(self, company_name: str, valuation_data: Dict[str, Any]) -> str:
        """Assess growth prospects for valuation"""
        try:
            # Search for growth-related data
            search_tool = DynamicWebSearchTool()
            growth_queries = [
                f"{company_name} growth prospects opportunities",
                f"{company_name} revenue growth earnings growth",
                f"{company_name} market expansion new markets",
                f"{company_name} innovation R&D growth drivers"
            ]
            
            growth_data = []
            for query in growth_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    growth_data.append(result)
            
            # Use AI to assess growth prospects
            prompt = f"""
            Assess growth prospects for {company_name} based on:
            
            Valuation Data: {valuation_data}
            Growth Data: {growth_data}
            
            Provide analysis covering:
            1. Historical Growth: Past revenue and earnings growth
            2. Growth Drivers: Key factors driving growth
            3. Market Opportunities: New markets and expansion potential
            4. Innovation Pipeline: R&D and new product development
            5. Growth Sustainability: Long-term growth prospects
            6. Growth Risks: Factors that could limit growth
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.VALUATION,
                max_fallbacks=3
            )
            
            return result.content if result else "Growth assessment not available"
            
        except Exception as e:
            print(f"❌ Error assessing growth prospects: {e}")
            return "Growth assessment failed"
    
    async def _assess_valuation_risks(self, company_name: str, valuation_data: Dict[str, Any]) -> str:
        """Assess valuation risks"""
        try:
            # Search for risk-related data
            search_tool = DynamicWebSearchTool()
            risk_queries = [
                f"{company_name} valuation risks challenges",
                f"{company_name} financial risks debt risks",
                f"{company_name} market risks competitive risks",
                f"{company_name} regulatory risks compliance risks"
            ]
            
            risk_data = []
            for query in risk_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    risk_data.append(result)
            
            # Use AI to assess valuation risks
            prompt = f"""
            Assess valuation risks for {company_name} based on:
            
            Valuation Data: {valuation_data}
            Risk Data: {risk_data}
            
            Provide analysis covering:
            1. Financial Risks: Debt, liquidity, and financial health risks
            2. Market Risks: Industry and market-related risks
            3. Competitive Risks: Threats from competitors
            4. Regulatory Risks: Compliance and regulatory issues
            5. Valuation Model Risks: Risks in valuation assumptions
            6. Downside Scenarios: Potential downside risks
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.VALUATION,
                max_fallbacks=3
            )
            
            return result.content if result else "Risk assessment not available"
            
        except Exception as e:
            print(f"❌ Error assessing valuation risks: {e}")
            return "Risk assessment failed"
    
    async def _calculate_fair_value(self, valuation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate fair value estimate based on all valuation methods"""
        try:
            # Combine all valuation data
            combined_data = {
                "dcf_analysis": valuation_data.get("dcf_analysis", {}),
                "comparable_analysis": valuation_data.get("comparable_analysis", {}),
                "relative_valuation": valuation_data.get("relative_valuation", {}),
                "asset_based_valuation": valuation_data.get("asset_based_valuation", {}),
                "growth_assessment": valuation_data.get("growth_assessment", ""),
                "risk_assessment": valuation_data.get("risk_assessment", "")
            }
            
            # Use AI to calculate fair value
            prompt = f"""
            Calculate a fair value estimate based on all valuation methods for the company:
            
            DCF Analysis: {combined_data['dcf_analysis']}
            Comparable Analysis: {combined_data['comparable_analysis']}
            Relative Valuation: {combined_data['relative_valuation']}
            Asset-Based Valuation: {combined_data['asset_based_valuation']}
            Growth Assessment: {combined_data['growth_assessment']}
            Risk Assessment: {combined_data['risk_assessment']}
            
            Provide analysis covering:
            
            FAIR VALUE ESTIMATE:
            - Weighted average of all valuation methods
            - Justification for weightings
            - Fair value per share estimate
            
            VALUATION RANGE:
            - Bull case scenario
            - Base case scenario
            - Bear case scenario
            - Confidence interval
            
            KEY DRIVERS:
            - Primary factors affecting valuation
            - Value creation opportunities
            - Value destruction risks
            
            VALUATION RISKS:
            - Key risks to valuation
            - Downside scenarios
            - Monitoring points
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.VALUATION,
                max_fallbacks=3
            )
            
            content = result.content if result else "Fair value calculation not available"
            
            # Parse the result
            fair_value = ""
            valuation_range = ""
            drivers = []
            risks = []
            
            if "FAIR VALUE ESTIMATE:" in content:
                fair_value_section = content.split("FAIR VALUE ESTIMATE:")[1].split("VALUATION RANGE:")[0]
                fair_value = fair_value_section.strip()
            
            if "VALUATION RANGE:" in content:
                range_section = content.split("VALUATION RANGE:")[1].split("KEY DRIVERS:")[0]
                valuation_range = range_section.strip()
            
            if "KEY DRIVERS:" in content:
                drivers_section = content.split("KEY DRIVERS:")[1].split("VALUATION RISKS:")[0]
                drivers = [line.strip() for line in drivers_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            if "VALUATION RISKS:" in content:
                risks_section = content.split("VALUATION RISKS:")[1]
                risks = [line.strip() for line in risks_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            return {
                "estimate": fair_value,
                "range": valuation_range,
                "drivers": drivers,
                "risks": risks
            }
            
        except Exception as e:
            print(f"❌ Error calculating fair value: {e}")
            return {
                "estimate": "Fair value calculation failed",
                "range": "Valuation range not available",
                "drivers": [],
                "risks": []
            }

# Export the agent
__all__ = ['ValuationAgent'] 