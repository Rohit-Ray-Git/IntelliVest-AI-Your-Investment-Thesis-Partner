"""
✏️ Thesis Rewrite Agent - Investment Thesis Improvement & Enhancement
====================================================================

This agent analyzes critique feedback and automatically rewrites the investment thesis
based on the recommendations from the critique agent. It implements improvements,
addresses identified issues, and enhances the overall quality of the thesis.
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools
from tools.dynamic_search_tools import DynamicWebSearchTool
from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType

class ThesisRewriteAgent:
    """✏️ Thesis Rewrite Agent for investment thesis improvement and enhancement"""
    
    def __init__(self):
        self.name = "Investment Thesis Rewriter"
        self.role = "Thesis improvement, enhancement, and rewriting based on critique"
        self.backstory = """
        You are an expert investment thesis rewriter with 15+ years of experience in 
        institutional investment writing and analysis. You specialize in:
        - Analyzing critique feedback and identifying actionable improvements
        - Rewriting investment theses to address identified issues
        - Enhancing thesis quality, clarity, and persuasiveness
        - Incorporating missing components and strengthening weak areas
        - Maintaining professional standards while improving content
        
        You take critique feedback and transform it into concrete improvements
        that enhance the thesis's credibility, completeness, and effectiveness.
        """
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool()
        ]
        
        # Initialize advanced fallback system
        self.fallback_system = AdvancedFallbackSystem()
        
    async def revise_thesis(self, thesis_markdown: str, critique: str, company_name: str) -> str:
        """
        Revise the investment thesis based on critique feedback
        
        Args:
            thesis_markdown: Original investment thesis
            critique: Critique feedback and recommendations
            company_name: Name or symbol of the company
            
        Returns:
            Revised and improved investment thesis
        """
        print(f"✏️ Thesis Rewrite Agent: Starting thesis revision for {company_name}")
        
        try:
            # Step 1: Analyze critique feedback
            print("🔍 Analyzing critique feedback...")
            critique_analysis = await self._analyze_critique_feedback(thesis_markdown, critique, company_name)
            
            # Step 2: Identify specific improvements needed
            print("🎯 Identifying specific improvements...")
            improvements_needed = await self._identify_improvements_needed(critique_analysis)
            
            # Step 3: Research additional data if needed
            print("📚 Researching additional data...")
            additional_data = await self._research_additional_data(company_name, improvements_needed)
            
            # Step 4: Rewrite thesis with improvements
            print("✏️ Rewriting thesis with improvements...")
            revised_thesis = await self._rewrite_thesis_with_improvements(
                thesis_markdown, critique_analysis, improvements_needed, additional_data, company_name
            )
            
            # Step 5: Quality check and final polish
            print("✨ Final quality check and polish...")
            final_thesis = await self._final_quality_check(revised_thesis, company_name)
            
            print(f"✅ Thesis Rewrite Agent: Completed thesis revision for {company_name}")
            return final_thesis
            
        except Exception as e:
            print(f"❌ Thesis Rewrite Agent: Error during thesis revision - {str(e)}")
            return f"❌ Thesis revision failed: {str(e)}"
    
    async def rewrite_thesis(self, thesis_data: Dict[str, Any], critique_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Rewrite thesis based on critique data (alias for revise_thesis)
        
        Args:
            thesis_data: Original thesis data
            critique_data: Critique feedback and recommendations
            
        Returns:
            Dictionary containing rewritten thesis
        """
        try:
            thesis_markdown = thesis_data.get("thesis_content", "")
            critique = critique_data.get("critique_content", "")
            company_name = thesis_data.get("company_name", "Unknown Company")
            
            revised_thesis = await self.revise_thesis(thesis_markdown, critique, company_name)
            
            return {
                "company_name": company_name,
                "rewritten_thesis": revised_thesis,
                "status": "completed",
                "improvements_made": True
            }
        except Exception as e:
            return {
                "company_name": thesis_data.get("company_name", "Unknown Company"),
                "rewritten_thesis": f"Error rewriting thesis: {str(e)}",
                "status": "error",
                "improvements_made": False
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
    
    async def _analyze_critique_feedback(self, thesis_markdown: str, critique: str, company_name: str) -> Dict[str, Any]:
        """Analyze critique feedback to extract actionable insights"""
        try:
            prompt = f"""
            Analyze the critique feedback for {company_name} investment thesis:
            
            Original Thesis:
            {thesis_markdown[:2000]}...
            
            Critique Feedback:
            {critique}
            
            Provide detailed analysis covering:
            
            CRITIQUE SUMMARY:
            - Main issues identified
            - Key improvement areas
            - Critical concerns raised
            - Strengths to maintain
            
            ACTIONABLE INSIGHTS:
            - Specific changes needed
            - Missing components to add
            - Weak areas to strengthen
            - Bias issues to address
            
            PRIORITY IMPROVEMENTS:
            - High priority fixes
            - Medium priority enhancements
            - Low priority suggestions
            - Deal-breaker issues
            
            DATA REQUIREMENTS:
            - Additional data needed
            - Research gaps to fill
            - Sources to verify
            - Information to validate
            
            Format as structured analysis for thesis rewriting.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            content = result.content if result else "Critique analysis not available"
            
            # Parse the analysis
            analysis = {
                "critique_summary": "",
                "actionable_insights": [],
                "priority_improvements": [],
                "data_requirements": []
            }
            
            # Extract sections
            if "CRITIQUE SUMMARY:" in content:
                analysis["critique_summary"] = content.split("CRITIQUE SUMMARY:")[1].split("ACTIONABLE INSIGHTS:")[0].strip()
            
            if "ACTIONABLE INSIGHTS:" in content:
                insights_section = content.split("ACTIONABLE INSIGHTS:")[1].split("PRIORITY IMPROVEMENTS:")[0]
                analysis["actionable_insights"] = [line.strip() for line in insights_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            if "PRIORITY IMPROVEMENTS:" in content:
                priority_section = content.split("PRIORITY IMPROVEMENTS:")[1].split("DATA REQUIREMENTS:")[0]
                analysis["priority_improvements"] = [line.strip() for line in priority_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            if "DATA REQUIREMENTS:" in content:
                data_section = content.split("DATA REQUIREMENTS:")[1]
                analysis["data_requirements"] = [line.strip() for line in data_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error analyzing critique feedback: {e}")
            return {
                "critique_summary": "Critique analysis failed",
                "actionable_insights": [],
                "priority_improvements": [],
                "data_requirements": []
            }
    
    async def _identify_improvements_needed(self, critique_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Identify specific improvements needed based on critique analysis"""
        try:
            prompt = f"""
            Based on the critique analysis, identify specific improvements needed:
            
            Critique Analysis: {critique_analysis}
            
            Provide specific improvement plan covering:
            
            CONTENT IMPROVEMENTS:
            - Missing sections to add
            - Weak arguments to strengthen
            - Incomplete analysis to expand
            - Unclear points to clarify
            
            STRUCTURAL IMPROVEMENTS:
            - Organization improvements
            - Flow enhancements
            - Logical structure fixes
            - Presentation improvements
            
            DATA ENHANCEMENTS:
            - Additional data points needed
            - Source citations to add
            - Evidence to strengthen
            - Validation requirements
            
            BIAS MITIGATION:
            - Bias issues to address
            - Alternative viewpoints to include
            - Balanced perspective improvements
            - Objectivity enhancements
            
            Format as specific action items for thesis rewriting.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            content = result.content if result else "Improvements identification not available"
            
            # Parse improvements
            improvements = {
                "content_improvements": [],
                "structural_improvements": [],
                "data_enhancements": [],
                "bias_mitigation": []
            }
            
            # Extract sections
            if "CONTENT IMPROVEMENTS:" in content:
                content_section = content.split("CONTENT IMPROVEMENTS:")[1].split("STRUCTURAL IMPROVEMENTS:")[0]
                improvements["content_improvements"] = [line.strip() for line in content_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            if "STRUCTURAL IMPROVEMENTS:" in content:
                structural_section = content.split("STRUCTURAL IMPROVEMENTS:")[1].split("DATA ENHANCEMENTS:")[0]
                improvements["structural_improvements"] = [line.strip() for line in structural_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            if "DATA ENHANCEMENTS:" in content:
                data_section = content.split("DATA ENHANCEMENTS:")[1].split("BIAS MITIGATION:")[0]
                improvements["data_enhancements"] = [line.strip() for line in data_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            if "BIAS MITIGATION:" in content:
                bias_section = content.split("BIAS MITIGATION:")[1]
                improvements["bias_mitigation"] = [line.strip() for line in bias_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            return improvements
            
        except Exception as e:
            print(f"❌ Error identifying improvements: {e}")
            return {
                "content_improvements": [],
                "structural_improvements": [],
                "data_enhancements": [],
                "bias_mitigation": []
            }
    
    async def _research_additional_data(self, company_name: str, improvements_needed: Dict[str, Any]) -> Dict[str, Any]:
        """Research additional data based on identified improvements"""
        try:
            additional_data = {}
            
            # Research based on data enhancements needed
            data_enhancements = improvements_needed.get("data_enhancements", [])
            
            for enhancement in data_enhancements[:3]:  # Limit to top 3 enhancements
                try:
                    # Create search query based on enhancement
                    search_query = f"{company_name} {enhancement.lower().replace('-', ' ')}"
                    
                    # Use dynamic search tool
                    search_tool = DynamicWebSearchTool()
                    search_result = search_tool._run(search_query)
                    
                    additional_data[enhancement] = search_result
                    
                except Exception as e:
                    print(f"Warning: Error researching {enhancement}: {e}")
                    continue
            
            return additional_data
            
        except Exception as e:
            print(f"❌ Error researching additional data: {e}")
            return {}
    
    async def _rewrite_thesis_with_improvements(self, thesis_markdown: str, critique_analysis: Dict[str, Any], 
                                              improvements_needed: Dict[str, Any], additional_data: Dict[str, Any], 
                                              company_name: str) -> str:
        """Rewrite the thesis incorporating all improvements"""
        try:
            prompt = f"""
            Rewrite the investment thesis for {company_name} incorporating all improvements:
            
            Original Thesis:
            {thesis_markdown}
            
            Critique Analysis:
            {critique_analysis}
            
            Improvements Needed:
            {improvements_needed}
            
            Additional Data:
            {additional_data}
            
            Rewrite the thesis addressing:
            
            1. CONTENT IMPROVEMENTS:
            - Add missing sections and analysis
            - Strengthen weak arguments
            - Expand incomplete analysis
            - Clarify unclear points
            
            2. STRUCTURAL IMPROVEMENTS:
            - Improve organization and flow
            - Enhance logical structure
            - Better presentation format
            - Clearer executive summary
            
            3. DATA ENHANCEMENTS:
            - Incorporate additional data
            - Add source citations
            - Strengthen evidence
            - Validate key claims
            
            4. BIAS MITIGATION:
            - Address identified biases
            - Include alternative viewpoints
            - Provide balanced perspective
            - Enhance objectivity
            
            Maintain professional institutional investor format while significantly improving quality.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else "Thesis rewriting failed"
            
        except Exception as e:
            print(f"❌ Error rewriting thesis: {e}")
            return f"❌ Thesis rewriting failed: {str(e)}"
    
    async def _final_quality_check(self, revised_thesis: str, company_name: str) -> str:
        """Perform final quality check and polish"""
        try:
            prompt = f"""
            Perform final quality check on the revised investment thesis for {company_name}:
            
            Revised Thesis:
            {revised_thesis}
            
            Quality Check Requirements:
            
            1. CONTENT QUALITY:
            - Completeness of analysis
            - Accuracy of information
            - Logical consistency
            - Professional tone
            
            2. STRUCTURE QUALITY:
            - Clear organization
            - Logical flow
            - Executive summary quality
            - Supporting evidence
            
            3. PRESENTATION QUALITY:
            - Professional formatting
            - Clear language
            - Appropriate length
            - Actionable insights
            
            4. FINAL POLISH:
            - Grammar and spelling
            - Consistent formatting
            - Professional appearance
            - Institutional standards
            
            Return the final polished thesis ready for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else revised_thesis
            
        except Exception as e:
            print(f"❌ Error in final quality check: {e}")
            return revised_thesis

# Export the agent
__all__ = ['ThesisRewriteAgent'] 