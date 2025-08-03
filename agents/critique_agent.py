"""
🔍 Critique Agent - Investment Thesis Validation & Critique
==========================================================

This agent validates and critiques investment theses including:
- Thesis validation and fact-checking
- Logical consistency analysis
- Risk assessment validation
- Alternative scenario analysis
- Confidence level assessment
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools and base agent
from tools.investment_tools import SentimentAnalysisTool
from tools.dynamic_search_tools import DynamicWebSearchTool
from agents.base_agent import BaseAgent
from llm.advanced_fallback_system import TaskType

class CritiqueAgent(BaseAgent):
    """🔍 Critique Agent for investment thesis validation"""
    
    def __init__(self):
        """Initialize the critique agent"""
        super().__init__(
            name="Thesis Critic",
            role="Investment thesis validation and critique",
            backstory="""
            You are an expert investment thesis critic with 18+ years of experience in risk management.
            You specialize in validating and critiquing investment theses, including:
            - Thesis validation and fact-checking
            - Logical consistency and reasoning analysis
            - Risk assessment validation and stress testing
            - Alternative scenario analysis and contrarian views
            - Confidence level assessment and uncertainty quantification
            - Quality assurance for institutional investment decisions
            
            You provide objective, critical analysis to ensure investment theses are robust
            and can withstand scrutiny from sophisticated investors.
            """
        )
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool(),
            SentimentAnalysisTool()
        ]
        
    async def analyze(self, company_name: str, **kwargs) -> Dict[str, Any]:
        """
        Main analysis method - validates and critiques investment thesis
        
        Args:
            company_name: Name or symbol of the company to analyze
            **kwargs: Additional parameters including thesis_data, research_data, etc.
            
        Returns:
            Dictionary containing comprehensive critique and validation
        """
        thesis_data = kwargs.get('thesis_data', {})
        research_data = kwargs.get('research_data', {})
        sentiment_data = kwargs.get('sentiment_data', {})
        valuation_data = kwargs.get('valuation_data', {})
        return await self.critique_thesis(company_name, thesis_data, research_data, sentiment_data, valuation_data)
    
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide critique data to other agents"""
        try:
            if request_type == "critique_data":
                # Conduct critique analysis and return data
                critique_data = await self.critique_thesis(company_name)
                return {
                    "agent": self.name,
                    "data_type": request_type,
                    "company_name": company_name,
                    "data": critique_data,
                    "message": f"Critique data provided for {company_name}"
                }
            else:
                return await super().provide_data(request_type, company_name, specific_data)
                
        except Exception as e:
            return {
                "agent": self.name,
                "data_type": request_type,
                "company_name": company_name,
                "data": {},
                "error": f"Error providing critique data: {str(e)}"
            }
    
    async def critique_thesis(self, company_name: str, thesis_data: Dict[str, Any] = None, 
                            research_data: Dict[str, Any] = None, sentiment_data: Dict[str, Any] = None, 
                            valuation_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform comprehensive thesis critique and validation
        
        Args:
            company_name: Name or symbol of the company
            thesis_data: Investment thesis data
            research_data: Research analysis data
            sentiment_data: Sentiment analysis data
            valuation_data: Valuation analysis data
            
        Returns:
            Dictionary containing comprehensive critique analysis
        """
        print(f"🔍 Critique Agent: Starting thesis critique for {company_name}")
        
        critique_data = {
            "company_name": company_name,
            "thesis_validation": "",
            "bias_analysis": "",
            "alternative_scenarios": "",
            "risk_validation": "",
            "quality_assessment": "",
            "peer_review": "",
            "critique_score": 0.0,
            "validation_status": "",
            "improvement_recommendations": [],
            "critical_issues": [],
            "strengths": [],
            "weaknesses": [],
            "data_sources": []
        }
        
        try:
            # 1. Validate the investment thesis
            print("✅ Validating investment thesis...")
            validation = await self._validate_thesis(company_name, thesis_data, research_data, sentiment_data, valuation_data)
            critique_data["thesis_validation"] = validation
            
            # 2. Analyze for biases and assumptions
            print("🎭 Analyzing biases and assumptions...")
            bias_analysis = await self._analyze_biases(company_name, thesis_data, research_data, sentiment_data, valuation_data)
            critique_data["bias_analysis"] = bias_analysis
            
            # 3. Develop alternative scenarios
            print("🔄 Developing alternative scenarios...")
            alternative_scenarios = await self._develop_alternative_scenarios(company_name, thesis_data, research_data, sentiment_data, valuation_data)
            critique_data["alternative_scenarios"] = alternative_scenarios
            
            # 4. Validate risk assessments
            print("⚠️ Validating risk assessments...")
            risk_validation = await self._validate_risks(company_name, thesis_data, research_data, sentiment_data, valuation_data)
            critique_data["risk_validation"] = risk_validation
            
            # 5. Perform quality assessment
            print("📊 Performing quality assessment...")
            quality_assessment = await self._assess_quality(company_name, thesis_data, research_data, sentiment_data, valuation_data)
            critique_data["quality_assessment"] = quality_assessment
            
            # 6. Conduct peer review
            print("👥 Conducting peer review...")
            peer_review = await self._conduct_peer_review(company_name, thesis_data, research_data, sentiment_data, valuation_data)
            critique_data["peer_review"] = peer_review
            
            # 7. Calculate critique score and status
            print("📈 Calculating critique score...")
            score_and_status = await self._calculate_critique_score(critique_data)
            critique_data["critique_score"] = score_and_status["score"]
            critique_data["validation_status"] = score_and_status["status"]
            
            # 8. Identify improvements and issues
            print("🔧 Identifying improvements and issues...")
            improvements_and_issues = await self._identify_improvements_and_issues(critique_data)
            critique_data["improvement_recommendations"] = improvements_and_issues["improvements"]
            critique_data["critical_issues"] = improvements_and_issues["issues"]
            critique_data["strengths"] = improvements_and_issues["strengths"]
            critique_data["weaknesses"] = improvements_and_issues["weaknesses"]
            
            print(f"✅ Critique Agent: Completed thesis critique for {company_name}")
            return critique_data
            
        except Exception as e:
            print(f"❌ Critique Agent: Error during thesis critique - {str(e)}")
            return {
                "company_name": company_name,
                "critique_content": f"Error critiquing thesis: {str(e)}",
                "status": "error",
                "improvement_suggestions": []
            } 