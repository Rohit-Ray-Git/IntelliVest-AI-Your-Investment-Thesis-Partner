"""
✏️ Enhanced Thesis Rewrite Agent - Intelligent Inter-Agent Communication
=======================================================================

This enhanced agent can intelligently communicate with other agents to:
- Request additional data when needed
- Collaborate with research, sentiment, and valuation agents
- Validate improvements with critique agent
- Dynamically adapt based on available information
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools and communication system
from tools.dynamic_search_tools import DynamicWebSearchTool
from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType
from agents.agent_communication_system import CommunicatingAgent, MessageType

class EnhancedThesisRewriteAgent(CommunicatingAgent):
    """✏️ Enhanced Thesis Rewrite Agent with intelligent inter-agent communication"""
    
    def __init__(self):
        # Initialize as a communicating agent
        super().__init__(
            name="Thesis Rewriter",
            capabilities=[
                "thesis_rewriting",
                "data_analysis", 
                "collaboration",
                "validation"
            ]
        )
        
        self.role = "Intelligent thesis improvement and enhancement"
        self.backstory = """
        You are an expert investment thesis rewriter with 15+ years of experience in 
        institutional investment writing and analysis. You can intelligently communicate
        with other agents to gather additional data, validate improvements, and ensure
        the highest quality thesis output.
        
        You specialize in:
        - Analyzing critique feedback and identifying actionable improvements
        - Requesting additional data from research, sentiment, and valuation agents
        - Collaborating with other agents for comprehensive analysis
        - Validating improvements with critique agent
        - Maintaining professional standards while improving content
        """
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool()
        ]
        
        # Initialize advanced fallback system
        self.fallback_system = AdvancedFallbackSystem()
        
    async def revise_thesis_intelligently(self, thesis_markdown: str, critique: str, 
                                        company_name: str, available_data: Dict[str, Any] = None) -> str:
        """
        Intelligently revise the investment thesis with inter-agent communication
        
        Args:
            thesis_markdown: Original investment thesis
            critique: Critique feedback and recommendations
            company_name: Name or symbol of the company
            available_data: Any existing data from previous analysis
            
        Returns:
            Revised and improved investment thesis
        """
        print(f"✏️ Enhanced Thesis Rewrite Agent: Starting intelligent thesis revision for {company_name}")
        
        try:
            # Step 1: Analyze critique feedback
            print("🔍 Analyzing critique feedback...")
            critique_analysis = await self._analyze_critique_feedback(thesis_markdown, critique, company_name)
            
            # Step 2: Identify specific improvements needed
            print("🎯 Identifying specific improvements...")
            improvements_needed = await self._identify_improvements_needed(critique_analysis)
            
            # Step 3: Intelligently gather additional data from other agents
            print("🤖 Intelligently gathering additional data from other agents...")
            additional_data = await self._gather_data_intelligently(company_name, improvements_needed, available_data)
            
            # Step 4: Collaborate with other agents for validation
            print("🤝 Collaborating with other agents for validation...")
            validation_results = await self._collaborate_for_validation(company_name, improvements_needed, additional_data)
            
            # Step 5: Rewrite thesis with all gathered information
            print("✏️ Rewriting thesis with comprehensive data...")
            revised_thesis = await self._rewrite_thesis_with_intelligence(
                thesis_markdown, critique_analysis, improvements_needed, 
                additional_data, validation_results, company_name
            )
            
            # Step 6: Validate improvements with critique agent
            print("✅ Validating improvements with critique agent...")
            final_thesis = await self._validate_improvements(revised_thesis, company_name)
            
            print(f"✅ Enhanced Thesis Rewrite Agent: Completed intelligent thesis revision for {company_name}")
            return final_thesis
            
        except Exception as e:
            print(f"❌ Enhanced Thesis Rewrite Agent: Error during intelligent thesis revision - {str(e)}")
            return f"❌ Intelligent thesis revision failed: {str(e)}"
    
    async def _gather_data_intelligently(self, company_name: str, improvements_needed: Dict[str, Any], 
                                       available_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Intelligently gather additional data from other agents"""
        try:
            additional_data = {}
            
            # Check what data we already have
            existing_data = available_data or {}
            
            # Identify what additional data we need
            data_requirements = self._identify_data_requirements(improvements_needed, existing_data)
            
            # Request data from appropriate agents
            for data_type, requirements in data_requirements.items():
                print(f"📊 Requesting {data_type} data from other agents...")
                
                if data_type == "financial_data":
                    # Request from valuation agent
                    response = await self.request_data(
                        recipient="ValuationAgent",
                        request_type="financial_metrics",
                        company_name=company_name,
                        specific_data=requirements
                    )
                    if "error" not in response:
                        additional_data["financial_data"] = response
                
                elif data_type == "sentiment_data":
                    # Request from sentiment agent
                    response = await self.request_data(
                        recipient="SentimentAgent", 
                        request_type="sentiment_analysis",
                        company_name=company_name,
                        specific_data=requirements
                    )
                    if "error" not in response:
                        additional_data["sentiment_data"] = response
                
                elif data_type == "research_data":
                    # Request from research agent
                    response = await self.request_data(
                        recipient="ResearchAgent",
                        request_type="company_research", 
                        company_name=company_name,
                        specific_data=requirements
                    )
                    if "error" not in response:
                        additional_data["research_data"] = response
                
                elif data_type == "market_data":
                    # Use dynamic search for market data
                    search_tool = DynamicWebSearchTool()
                    for requirement in requirements:
                        result = search_tool._run(f"{company_name} {requirement}")
                        if result and "✅" in result:
                            additional_data[f"market_data_{requirement}"] = result
            
            return additional_data
            
        except Exception as e:
            print(f"❌ Error gathering data intelligently: {e}")
            return {}
    
    async def _collaborate_for_validation(self, company_name: str, improvements_needed: Dict[str, Any], 
                                        additional_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other agents for validation"""
        try:
            validation_results = {}
            
            # Collaborate with research agent for data validation
            print("🔍 Collaborating with research agent for data validation...")
            research_validation = await self.request_collaboration(
                recipient="ResearchAgent",
                collaboration_type="data_validation",
                shared_data={
                    "company_name": company_name,
                    "improvements_needed": improvements_needed,
                    "additional_data": additional_data
                },
                params={"validation_type": "data_accuracy"}
            )
            if "error" not in research_validation:
                validation_results["research_validation"] = research_validation
            
            # Collaborate with sentiment agent for sentiment validation
            print("😊 Collaborating with sentiment agent for sentiment validation...")
            sentiment_validation = await self.request_collaboration(
                recipient="SentimentAgent",
                collaboration_type="sentiment_validation",
                shared_data={
                    "company_name": company_name,
                    "improvements_needed": improvements_needed,
                    "additional_data": additional_data
                },
                params={"validation_type": "sentiment_consistency"}
            )
            if "error" not in sentiment_validation:
                validation_results["sentiment_validation"] = sentiment_validation
            
            # Collaborate with valuation agent for valuation validation
            print("💰 Collaborating with valuation agent for valuation validation...")
            valuation_validation = await self.request_collaboration(
                recipient="ValuationAgent",
                collaboration_type="valuation_validation",
                shared_data={
                    "company_name": company_name,
                    "improvements_needed": improvements_needed,
                    "additional_data": additional_data
                },
                params={"validation_type": "valuation_consistency"}
            )
            if "error" not in valuation_validation:
                validation_results["valuation_validation"] = valuation_validation
            
            return validation_results
            
        except Exception as e:
            print(f"❌ Error collaborating for validation: {e}")
            return {}
    
    async def _rewrite_thesis_with_intelligence(self, thesis_markdown: str, critique_analysis: Dict[str, Any],
                                              improvements_needed: Dict[str, Any], additional_data: Dict[str, Any],
                                              validation_results: Dict[str, Any], company_name: str) -> str:
        """Rewrite the thesis using all intelligently gathered information"""
        try:
            prompt = f"""
            Rewrite the investment thesis for {company_name} using comprehensive intelligently gathered data:
            
            Original Thesis:
            {thesis_markdown}
            
            Critique Analysis:
            {critique_analysis}
            
            Improvements Needed:
            {improvements_needed}
            
            Additional Data from Other Agents:
            {additional_data}
            
            Validation Results from Collaboration:
            {validation_results}
            
            Rewrite the thesis addressing:
            
            1. CONTENT IMPROVEMENTS:
            - Add missing sections and analysis based on additional data
            - Strengthen weak arguments with validated information
            - Expand incomplete analysis with comprehensive data
            - Clarify unclear points with additional context
            
            2. STRUCTURAL IMPROVEMENTS:
            - Improve organization and flow based on validation feedback
            - Enhance logical structure with collaborative insights
            - Better presentation format incorporating agent feedback
            - Clearer executive summary with validated key points
            
            3. DATA ENHANCEMENTS:
            - Incorporate additional data from research, sentiment, and valuation agents
            - Add source citations and validation references
            - Strengthen evidence with collaborative validation
            - Validate key claims with multi-agent verification
            
            4. BIAS MITIGATION:
            - Address identified biases with collaborative feedback
            - Include alternative viewpoints from multiple agents
            - Provide balanced perspective with comprehensive data
            - Enhance objectivity through multi-agent validation
            
            Maintain professional institutional investor format while significantly improving quality
            through intelligent collaboration and comprehensive data integration.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else "Intelligent thesis rewriting failed"
            
        except Exception as e:
            print(f"❌ Error rewriting thesis with intelligence: {e}")
            return f"❌ Intelligent thesis rewriting failed: {str(e)}"
    
    async def _validate_improvements(self, revised_thesis: str, company_name: str) -> str:
        """Validate improvements with critique agent"""
        try:
            # Request validation from critique agent
            validation_response = await self.request_validation(
                recipient="CritiqueAgent",
                validation_type="improvement_validation",
                data={
                    "revised_thesis": revised_thesis,
                    "company_name": company_name
                },
                criteria={
                    "validation_type": "improvement_quality",
                    "quality_standards": "institutional_investor"
                }
            )
            
            if "error" not in validation_response:
                # If critique agent suggests further improvements, incorporate them
                if "suggestions" in validation_response:
                    print("🔄 Incorporating final validation suggestions...")
                    final_thesis = await self._incorporate_validation_suggestions(
                        revised_thesis, validation_response["suggestions"], company_name
                    )
                    return final_thesis
                else:
                    return revised_thesis
            else:
                print(f"⚠️ Validation failed: {validation_response['error']}")
                return revised_thesis
                
        except Exception as e:
            print(f"❌ Error validating improvements: {e}")
            return revised_thesis
    
    def _identify_data_requirements(self, improvements_needed: Dict[str, Any], existing_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Identify what additional data is needed"""
        data_requirements = {
            "financial_data": [],
            "sentiment_data": [],
            "research_data": [],
            "market_data": []
        }
        
        # Check content improvements
        for improvement in improvements_needed.get("content_improvements", []):
            if "financial" in improvement.lower() or "valuation" in improvement.lower():
                data_requirements["financial_data"].append(improvement)
            elif "sentiment" in improvement.lower() or "mood" in improvement.lower():
                data_requirements["sentiment_data"].append(improvement)
            elif "research" in improvement.lower() or "analysis" in improvement.lower():
                data_requirements["research_data"].append(improvement)
            else:
                data_requirements["market_data"].append(improvement)
        
        # Check data enhancements
        for enhancement in improvements_needed.get("data_enhancements", []):
            if "financial" in enhancement.lower():
                data_requirements["financial_data"].append(enhancement)
            elif "sentiment" in enhancement.lower():
                data_requirements["sentiment_data"].append(enhancement)
            elif "research" in enhancement.lower():
                data_requirements["research_data"].append(enhancement)
            else:
                data_requirements["market_data"].append(enhancement)
        
        # Remove duplicates and filter out existing data
        for data_type in data_requirements:
            data_requirements[data_type] = list(set(data_requirements[data_type]))
            # Filter out data we already have
            if data_type in existing_data:
                data_requirements[data_type] = [
                    req for req in data_requirements[data_type] 
                    if req not in str(existing_data[data_type])
                ]
        
        return data_requirements
    
    async def _incorporate_validation_suggestions(self, revised_thesis: str, suggestions: List[str], company_name: str) -> str:
        """Incorporate final validation suggestions"""
        try:
            prompt = f"""
            Incorporate the following validation suggestions into the revised thesis for {company_name}:
            
            Revised Thesis:
            {revised_thesis}
            
            Validation Suggestions:
            {suggestions}
            
            Please incorporate these final suggestions to ensure the thesis meets the highest
            institutional investor standards. Make only the necessary changes to address
            the validation feedback while maintaining the overall quality and structure.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else revised_thesis
            
        except Exception as e:
            print(f"❌ Error incorporating validation suggestions: {e}")
            return revised_thesis
    
    # Override base class methods to provide data to other agents
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide data to other agents"""
        try:
            if request_type == "thesis_data":
                # Provide thesis-related data
                return {
                    "thesis_components": ["executive_summary", "investment_case", "risk_analysis"],
                    "thesis_strength": "high",
                    "thesis_quality": "institutional_standard"
                }
            else:
                return {"error": f"Cannot provide {request_type} data"}
        except Exception as e:
            return {"error": f"Error providing data: {str(e)}"}
    
    async def collaborate(self, collaboration_type: str, shared_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other agents"""
        try:
            if collaboration_type == "thesis_improvement":
                # Collaborate on thesis improvement
                return {
                    "collaboration_result": "thesis_improvement_suggestions",
                    "improvement_areas": ["content", "structure", "data"],
                    "collaboration_quality": "high"
                }
            else:
                return {"error": f"Cannot collaborate on {collaboration_type}"}
        except Exception as e:
            return {"error": f"Error collaborating: {str(e)}"}

# Export the enhanced agent
__all__ = ['EnhancedThesisRewriteAgent'] 