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