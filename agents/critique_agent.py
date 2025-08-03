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
from tools.investment_tools import ValidationTool
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
            ValidationTool()
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