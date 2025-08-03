"""
📝 Thesis Agent - Investment Thesis Generation & Synthesis
=========================================================

This agent generates comprehensive investment theses including:
- Executive summary and investment case
- Investment thesis synthesis
- Risk-reward analysis
- Investment recommendation
- Thesis validation and confidence levels
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools and base agent
from tools.investment_tools import ThesisGenerationTool
from tools.dynamic_search_tools import DynamicWebSearchTool
from agents.base_agent import BaseAgent
from llm.advanced_fallback_system import TaskType

class ThesisAgent(BaseAgent):
    """📝 Thesis Agent for investment thesis generation"""
    
    def __init__(self):
        """Initialize the thesis agent"""
        super().__init__(
            name="Thesis Writer",
            role="Investment thesis generation and synthesis",
            backstory="""
            You are an expert investment thesis writer with 20+ years of experience in institutional investing.
            You specialize in creating comprehensive investment theses, including:
            - Executive summaries and investment cases
            - Investment thesis synthesis and narrative development
            - Risk-reward analysis and scenario planning
            - Investment recommendations with conviction levels
            - Thesis validation and confidence assessment
            - Professional presentation for institutional investors
            
            You synthesize complex financial analysis into compelling investment narratives
            that are both comprehensive and accessible to sophisticated investors.
            """
        )
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool(),
            ThesisGenerationTool()
        ]
        
    async def analyze(self, company_name: str, **kwargs) -> Dict[str, Any]:
        """
        Main analysis method - generates investment thesis
        
        Args:
            company_name: Name or symbol of the company to analyze
            **kwargs: Additional parameters including research_data, sentiment_data, valuation_data
            
        Returns:
            Dictionary containing comprehensive investment thesis
        """
        research_data = kwargs.get('research_data', {})
        sentiment_data = kwargs.get('sentiment_data', {})
        valuation_data = kwargs.get('valuation_data', {})
        return await self.generate_thesis(company_name, research_data, sentiment_data, valuation_data)
    
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide thesis data to other agents"""
        try:
            if request_type == "thesis_data":
                # Generate thesis and return data
                thesis_data = await self.generate_thesis(company_name)
                return {
                    "agent": self.name,
                    "data_type": request_type,
                    "company_name": company_name,
                    "data": thesis_data,
                    "message": f"Thesis data provided for {company_name}"
                }
            else:
                return await super().provide_data(request_type, company_name, specific_data)
                
        except Exception as e:
            return {
                "agent": self.name,
                "data_type": request_type,
                "company_name": company_name,
                "data": {},
                "error": f"Error providing thesis data: {str(e)}"
            }
    
    async def generate_thesis(self, company_name: str, research_data: Dict[str, Any] = None, 
                            sentiment_data: Dict[str, Any] = None, valuation_data: Dict[str, Any] = None) -> Dict[str, Any]:
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
            # 1. Generate investment recommendation
            print("🎯 Generating investment recommendation...")
            recommendation = await self._generate_recommendation(company_name, research_data, sentiment_data, valuation_data)
            thesis_data["investment_recommendation"] = recommendation
            
            # 2. Create value proposition
            print("💎 Creating value proposition...")
            value_proposition = await self._create_value_proposition(company_name, research_data, sentiment_data, valuation_data)
            thesis_data["value_proposition"] = value_proposition
            
            # 3. Build investment case
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
            return {
                "company_name": company_name,
                "thesis_content": f"Error generating thesis: {str(e)}",
                "status": "error",
                "recommendation": "Unable to generate recommendation"
            } 