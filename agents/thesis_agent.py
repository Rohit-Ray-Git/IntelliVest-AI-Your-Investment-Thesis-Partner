"""
📝 Thesis Agent - Investment Thesis Generation & Development
===========================================================

This agent generates comprehensive investment theses including:
- Investment recommendation and rationale
- Value proposition and investment case
- Risk-reward analysis and timeline
- Exit strategy and key catalysts
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools
from tools.investment_tools import ThesisGenerationTool
from tools.dynamic_search_tools import DynamicWebSearchTool
from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType

class ThesisAgent:
    """📝 Thesis Agent for investment thesis generation"""
    
    def __init__(self):
        self.name = "Investment Thesis Writer"
        self.role = "Investment thesis generation and recommendation"
        self.backstory = """
        You are an expert investment thesis writer with 20+ years of experience in institutional investing.
        You specialize in creating comprehensive investment theses that include:
        - Clear investment recommendations (Buy/Hold/Sell)
        - Compelling value propositions and investment cases
        - Comprehensive risk-reward analysis
        - Investment timeline and exit strategies
        - Professional formatting for institutional investors
        
        You integrate research, sentiment, and valuation data to create compelling
        investment narratives that drive investment decisions.
        """
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool(),
            ThesisGenerationTool()
        ]
        
        # Initialize advanced fallback system
        self.fallback_system = AdvancedFallbackSystem()
        
    async def generate_thesis(self, company_name: str, research_data: Dict[str, Any], 
                            sentiment_data: Dict[str, Any], valuation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive investment thesis
        
        Args:
            company_name: Name or symbol of the company
            research_data: Research analysis data
            sentiment_data: Sentiment analysis data
            valuation_data: Valuation analysis data
            
        Returns:
            Dictionary containing comprehensive investment thesis
        """
        print(f"📝 Thesis Agent: Starting thesis generation for {company_name}")
        
        thesis_data = {
            "company_name": company_name,
            "investment_recommendation": "",
            "value_proposition": "",
            "investment_case": "",
            "risk_reward_analysis": "",
            "investment_timeline": "",
            "exit_strategy": "",
            "key_risks": [],
            "catalysts": [],
            "thesis_strength": 0.0,
            "confidence_level": "",
            "thesis_summary": "",
            "data_sources": []
        }
        
        try:
            # 1. Analyze all data and generate investment recommendation
            print("🎯 Generating investment recommendation...")
            recommendation = await self._generate_recommendation(company_name, research_data, sentiment_data, valuation_data)
            thesis_data["investment_recommendation"] = recommendation
            
            # 2. Create compelling value proposition
            print("💎 Creating value proposition...")
            value_proposition = await self._create_value_proposition(company_name, research_data, sentiment_data, valuation_data)
            thesis_data["value_proposition"] = value_proposition
            
            # 3. Build comprehensive investment case
            print("📊 Building investment case...")
            investment_case = await self._build_investment_case(company_name, research_data, sentiment_data, valuation_data)
            thesis_data["investment_case"] = investment_case
            
            # 4. Perform risk-reward analysis
            print("⚖️ Performing risk-reward analysis...")
            risk_reward = await self._analyze_risk_reward(company_name, research_data, sentiment_data, valuation_data)
            thesis_data["risk_reward_analysis"] = risk_reward
            
            # 5. Define investment timeline
            print("⏰ Defining investment timeline...")
            timeline = await self._define_investment_timeline(company_name, research_data, sentiment_data, valuation_data)
            thesis_data["investment_timeline"] = timeline
            
            # 6. Develop exit strategy
            print("🚪 Developing exit strategy...")
            exit_strategy = await self._develop_exit_strategy(company_name, research_data, sentiment_data, valuation_data)
            thesis_data["exit_strategy"] = exit_strategy
            
            # 7. Identify key risks and catalysts
            print("⚠️ Identifying key risks and catalysts...")
            risks_and_catalysts = await self._identify_risks_and_catalysts(company_name, research_data, sentiment_data, valuation_data)
            thesis_data["key_risks"] = risks_and_catalysts["risks"]
            thesis_data["catalysts"] = risks_and_catalysts["catalysts"]
            
            # 8. Assess thesis strength and confidence
            print("📈 Assessing thesis strength and confidence...")
            strength_assessment = await self._assess_thesis_strength(thesis_data)
            thesis_data["thesis_strength"] = strength_assessment["strength"]
            thesis_data["confidence_level"] = strength_assessment["confidence"]
            
            # 9. Create executive summary
            print("📋 Creating executive summary...")
            summary = await self._create_executive_summary(thesis_data)
            thesis_data["thesis_summary"] = summary
            
            print(f"✅ Thesis Agent: Completed thesis generation for {company_name}")
            return thesis_data
            
        except Exception as e:
            print(f"❌ Thesis Agent: Error during thesis generation - {str(e)}")
            return thesis_data
    
    async def _generate_recommendation(self, company_name: str, research_data: Dict[str, Any], 
                                     sentiment_data: Dict[str, Any], valuation_data: Dict[str, Any]) -> str:
        """Generate investment recommendation (Buy/Hold/Sell)"""
        try:
            # Combine all analysis data
            combined_data = {
                "research": research_data,
                "sentiment": sentiment_data,
                "valuation": valuation_data
            }
            
            prompt = f"""
            Generate an investment recommendation for {company_name} based on comprehensive analysis:
            
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide a clear investment recommendation covering:
            
            RECOMMENDATION: [BUY/HOLD/SELL]
            - Clear recommendation with conviction level
            - Justification based on all analysis
            - Key factors driving the recommendation
            
            RECOMMENDATION RATIONALE:
            - Primary investment thesis
            - Key value drivers
            - Risk factors considered
            - Expected return potential
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else "Investment recommendation not available"
            
        except Exception as e:
            print(f"❌ Error generating recommendation: {e}")
            return "Investment recommendation failed"
    
    async def _create_value_proposition(self, company_name: str, research_data: Dict[str, Any], 
                                      sentiment_data: Dict[str, Any], valuation_data: Dict[str, Any]) -> str:
        """Create compelling value proposition"""
        try:
            prompt = f"""
            Create a compelling value proposition for {company_name} based on:
            
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide a compelling value proposition covering:
            
            VALUE PROPOSITION:
            - Unique value proposition
            - Competitive advantages
            - Market opportunities
            - Growth potential
            
            INVESTMENT ATTRACTIVENESS:
            - Why this investment is attractive
            - Key differentiators
            - Market positioning
            - Value creation potential
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else "Value proposition not available"
            
        except Exception as e:
            print(f"❌ Error creating value proposition: {e}")
            return "Value proposition failed"
    
    async def _build_investment_case(self, company_name: str, research_data: Dict[str, Any], 
                                   sentiment_data: Dict[str, Any], valuation_data: Dict[str, Any]) -> str:
        """Build comprehensive investment case"""
        try:
            prompt = f"""
            Build a comprehensive investment case for {company_name} based on:
            
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide a comprehensive investment case covering:
            
            INVESTMENT CASE:
            1. Business Model: How the company creates value
            2. Market Opportunity: Size and growth potential
            3. Competitive Position: Advantages and moats
            4. Financial Performance: Historical and projected
            5. Management Quality: Leadership and execution
            6. Growth Strategy: Plans and execution capability
            
            INVESTMENT DRIVERS:
            - Primary factors driving investment value
            - Key catalysts for value creation
            - Growth and expansion opportunities
            - Operational improvements potential
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else "Investment case not available"
            
        except Exception as e:
            print(f"❌ Error building investment case: {e}")
            return "Investment case failed"
    
    async def _analyze_risk_reward(self, company_name: str, research_data: Dict[str, Any], 
                                 sentiment_data: Dict[str, Any], valuation_data: Dict[str, Any]) -> str:
        """Perform comprehensive risk-reward analysis"""
        try:
            prompt = f"""
            Perform a comprehensive risk-reward analysis for {company_name} based on:
            
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide comprehensive risk-reward analysis covering:
            
            REWARD POTENTIAL:
            - Expected return scenarios
            - Upside potential
            - Value creation opportunities
            - Growth catalysts
            
            RISK FACTORS:
            - Key risks to the investment
            - Downside scenarios
            - Risk mitigation strategies
            - Risk monitoring points
            
            RISK-REWARD RATIO:
            - Expected return vs. risk
            - Probability-weighted scenarios
            - Risk-adjusted returns
            - Investment attractiveness
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else "Risk-reward analysis not available"
            
        except Exception as e:
            print(f"❌ Error analyzing risk-reward: {e}")
            return "Risk-reward analysis failed"
    
    async def _define_investment_timeline(self, company_name: str, research_data: Dict[str, Any], 
                                        sentiment_data: Dict[str, Any], valuation_data: Dict[str, Any]) -> str:
        """Define investment timeline and milestones"""
        try:
            prompt = f"""
            Define an investment timeline for {company_name} based on:
            
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide investment timeline covering:
            
            INVESTMENT TIMELINE:
            - Short-term milestones (3-6 months)
            - Medium-term objectives (6-18 months)
            - Long-term goals (18+ months)
            - Key performance indicators
            
            MILESTONES AND CATALYSTS:
            - Expected catalysts and events
            - Performance milestones
            - Market developments
            - Company-specific events
            
            TIMELINE RISKS:
            - Timeline risks and delays
            - Monitoring points
            - Adjustment triggers
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else "Investment timeline not available"
            
        except Exception as e:
            print(f"❌ Error defining investment timeline: {e}")
            return "Investment timeline failed"
    
    async def _develop_exit_strategy(self, company_name: str, research_data: Dict[str, Any], 
                                   sentiment_data: Dict[str, Any], valuation_data: Dict[str, Any]) -> str:
        """Develop comprehensive exit strategy"""
        try:
            prompt = f"""
            Develop an exit strategy for {company_name} based on:
            
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide exit strategy covering:
            
            EXIT STRATEGY:
            - Primary exit scenarios
            - Target exit valuations
            - Exit timing considerations
            - Exit method preferences
            
            EXIT TRIGGERS:
            - Positive exit triggers
            - Negative exit triggers
            - Performance-based exits
            - Market-based exits
            
            EXIT EXECUTION:
            - Exit execution plan
            - Liquidity considerations
            - Tax implications
            - Transaction costs
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else "Exit strategy not available"
            
        except Exception as e:
            print(f"❌ Error developing exit strategy: {e}")
            return "Exit strategy failed"
    
    async def _identify_risks_and_catalysts(self, company_name: str, research_data: Dict[str, Any], 
                                          sentiment_data: Dict[str, Any], valuation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify key risks and catalysts"""
        try:
            prompt = f"""
            Identify key risks and catalysts for {company_name} based on:
            
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide analysis covering:
            
            KEY RISKS:
            - Primary investment risks
            - Business model risks
            - Market and competitive risks
            - Financial and operational risks
            - Regulatory and compliance risks
            
            KEY CATALYSTS:
            - Positive catalysts
            - Growth catalysts
            - Market catalysts
            - Company-specific catalysts
            - Industry catalysts
            
            Format as lists for easy reference.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            content = result.content if result else "Risks and catalysts analysis not available"
            
            # Parse the result
            risks = []
            catalysts = []
            
            if "KEY RISKS:" in content:
                risks_section = content.split("KEY RISKS:")[1].split("KEY CATALYSTS:")[0]
                risks = [line.strip() for line in risks_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            if "KEY CATALYSTS:" in content:
                catalysts_section = content.split("KEY CATALYSTS:")[1]
                catalysts = [line.strip() for line in catalysts_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            return {
                "risks": risks,
                "catalysts": catalysts
            }
            
        except Exception as e:
            print(f"❌ Error identifying risks and catalysts: {e}")
            return {
                "risks": ["Risk identification failed"],
                "catalysts": ["Catalyst identification failed"]
            }
    
    async def _assess_thesis_strength(self, thesis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess thesis strength and confidence level"""
        try:
            prompt = f"""
            Assess the strength and confidence level of the investment thesis based on:
            
            Thesis Data: {thesis_data}
            
            Provide assessment covering:
            
            THESIS STRENGTH (0-10 scale):
            - Overall thesis strength
            - Data quality and completeness
            - Analysis depth and rigor
            - Recommendation conviction
            
            CONFIDENCE LEVEL:
            - High/Medium/Low confidence
            - Confidence factors
            - Uncertainty sources
            - Monitoring requirements
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            content = result.content if result else "Thesis strength assessment not available"
            
            # Parse the result
            strength = 5.0  # Default
            confidence = "Medium"
            
            # Extract strength score
            import re
            strength_match = re.search(r'strength[:\s]*(\d+(?:\.\d+)?)', content.lower())
            if strength_match:
                strength = float(strength_match.group(1))
            
            # Extract confidence level
            if "high confidence" in content.lower():
                confidence = "High"
            elif "low confidence" in content.lower():
                confidence = "Low"
            else:
                confidence = "Medium"
            
            return {
                "strength": strength,
                "confidence": confidence
            }
            
        except Exception as e:
            print(f"❌ Error assessing thesis strength: {e}")
            return {
                "strength": 5.0,
                "confidence": "Medium"
            }
    
    async def _create_executive_summary(self, thesis_data: Dict[str, Any]) -> str:
        """Create executive summary of the investment thesis"""
        try:
            prompt = f"""
            Create an executive summary of the investment thesis based on:
            
            Thesis Data: {thesis_data}
            
            Provide an executive summary covering:
            
            EXECUTIVE SUMMARY:
            - Investment recommendation and rationale
            - Key value proposition
            - Expected returns and timeline
            - Key risks and catalysts
            - Investment thesis strength
            
            Format as a concise executive summary for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else "Executive summary not available"
            
        except Exception as e:
            print(f"❌ Error creating executive summary: {e}")
            return "Executive summary failed"

# Export the agent
__all__ = ['ThesisAgent'] 