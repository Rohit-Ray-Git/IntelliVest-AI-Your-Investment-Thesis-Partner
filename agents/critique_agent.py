"""
🔍 Critique Agent - Investment Thesis Critique & Validation
==========================================================

This agent handles investment thesis critique and validation including:
- Thesis validation and verification
- Bias detection and mitigation
- Alternative scenario analysis
- Risk assessment validation
- Quality assurance and peer review
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools
from tools.investment_tools import CritiqueTool
from tools.dynamic_search_tools import DynamicWebSearchTool
from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType

class CritiqueAgent:
    """🔍 Critique Agent for investment thesis critique and validation"""
    
    def __init__(self):
        self.name = "Investment Thesis Critic"
        self.role = "Thesis critique, validation, and quality assurance"
        self.backstory = """
        You are an expert investment thesis critic with 18+ years of experience in institutional investing.
        You specialize in critically evaluating investment theses and providing:
        - Objective thesis validation and verification
        - Bias detection and mitigation strategies
        - Alternative scenario analysis and stress testing
        - Risk assessment validation and enhancement
        - Quality assurance and peer review processes
        
        You act as a devil's advocate to ensure investment theses are robust,
        well-reasoned, and consider all potential scenarios and risks.
        """
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool(),
            CritiqueTool()
        ]
        
        # Initialize advanced fallback system
        self.fallback_system = AdvancedFallbackSystem()
        
    async def critique_thesis(self, company_name: str, thesis_data: Dict[str, Any], 
                            research_data: Dict[str, Any], sentiment_data: Dict[str, Any], 
                            valuation_data: Dict[str, Any]) -> Dict[str, Any]:
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
        
        if request_type == "critique_data":
            critique_data = await self.critique_thesis({}, {})
            return {
                "status": "success",
                "agent": self.name,
                "data": critique_data,
                "data_type": "critique_data"
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
    
    async def _validate_thesis(self, company_name: str, thesis_data: Dict[str, Any], 
                             research_data: Dict[str, Any], sentiment_data: Dict[str, Any], 
                             valuation_data: Dict[str, Any]) -> str:
        """Validate the investment thesis against all available data"""
        try:
            # Combine all data for validation
            combined_data = {
                "thesis": thesis_data,
                "research": research_data,
                "sentiment": sentiment_data,
                "valuation": valuation_data
            }
            
            prompt = f"""
            Validate the investment thesis for {company_name} against all available data:
            
            Thesis Data: {thesis_data}
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide comprehensive validation covering:
            
            THESIS VALIDATION:
            - Consistency with research findings
            - Alignment with sentiment analysis
            - Support from valuation analysis
            - Logical coherence and reasoning
            
            DATA CONSISTENCY:
            - Cross-validation of key assumptions
            - Consistency across different analyses
            - Data quality and reliability
            - Source credibility assessment
            
            LOGICAL VALIDATION:
            - Soundness of investment logic
            - Completeness of analysis
            - Reasonableness of conclusions
            - Strength of supporting evidence
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.CRITIQUE,
                max_fallbacks=3
            )
            
            return result.content if result else "Thesis validation not available"
            
        except Exception as e:
            print(f"❌ Error validating thesis: {e}")
            return "Thesis validation failed"
    
    async def _analyze_biases(self, company_name: str, thesis_data: Dict[str, Any], 
                            research_data: Dict[str, Any], sentiment_data: Dict[str, Any], 
                            valuation_data: Dict[str, Any]) -> str:
        """Analyze for biases and assumptions in the thesis"""
        try:
            prompt = f"""
            Analyze the investment thesis for {company_name} to identify biases and assumptions:
            
            Thesis Data: {thesis_data}
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide bias analysis covering:
            
            COGNITIVE BIASES:
            - Confirmation bias detection
            - Anchoring bias identification
            - Overconfidence assessment
            - Availability bias analysis
            
            ANALYTICAL ASSUMPTIONS:
            - Key assumptions identification
            - Assumption validity assessment
            - Sensitivity to assumption changes
            - Alternative assumption scenarios
            
            DATA BIASES:
            - Sample bias detection
            - Selection bias identification
            - Reporting bias assessment
            - Survivorship bias analysis
            
            MITIGATION STRATEGIES:
            - Bias mitigation approaches
            - Alternative perspectives
            - Robustness testing
            - Validation methods
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.CRITIQUE,
                max_fallbacks=3
            )
            
            return result.content if result else "Bias analysis not available"
            
        except Exception as e:
            print(f"❌ Error analyzing biases: {e}")
            return "Bias analysis failed"
    
    async def _develop_alternative_scenarios(self, company_name: str, thesis_data: Dict[str, Any], 
                                           research_data: Dict[str, Any], sentiment_data: Dict[str, Any], 
                                           valuation_data: Dict[str, Any]) -> str:
        """Develop alternative scenarios and stress testing"""
        try:
            prompt = f"""
            Develop alternative scenarios and stress testing for {company_name} investment thesis:
            
            Thesis Data: {thesis_data}
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide alternative scenario analysis covering:
            
            BULL SCENARIO:
            - Optimistic assumptions
            - Best-case outcomes
            - Upside catalysts
            - Maximum value potential
            
            BEAR SCENARIO:
            - Pessimistic assumptions
            - Worst-case outcomes
            - Downside risks
            - Minimum value potential
            
            BASE SCENARIO:
            - Realistic assumptions
            - Expected outcomes
            - Balanced view
            - Most likely value
            
            STRESS TESTING:
            - Key variable sensitivity
            - Break-even analysis
            - Scenario probability assessment
            - Risk-adjusted scenarios
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.CRITIQUE,
                max_fallbacks=3
            )
            
            return result.content if result else "Alternative scenarios not available"
            
        except Exception as e:
            print(f"❌ Error developing alternative scenarios: {e}")
            return "Alternative scenarios failed"
    
    async def _validate_risks(self, company_name: str, thesis_data: Dict[str, Any], 
                            research_data: Dict[str, Any], sentiment_data: Dict[str, Any], 
                            valuation_data: Dict[str, Any]) -> str:
        """Validate and enhance risk assessments"""
        try:
            prompt = f"""
            Validate and enhance risk assessments for {company_name} investment thesis:
            
            Thesis Data: {thesis_data}
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide risk validation covering:
            
            RISK COMPREHENSIVENESS:
            - Completeness of risk identification
            - Risk categorization and prioritization
            - Risk quantification assessment
            - Risk mitigation evaluation
            
            RISK VALIDATION:
            - Risk probability assessment
            - Risk impact evaluation
            - Risk correlation analysis
            - Risk interdependencies
            
            MISSING RISKS:
            - Additional risks not considered
            - Emerging risk factors
            - Systemic risk assessment
            - Black swan event consideration
            
            RISK MONITORING:
            - Risk monitoring framework
            - Early warning indicators
            - Risk escalation triggers
            - Risk management protocols
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.CRITIQUE,
                max_fallbacks=3
            )
            
            return result.content if result else "Risk validation not available"
            
        except Exception as e:
            print(f"❌ Error validating risks: {e}")
            return "Risk validation failed"
    
    async def _assess_quality(self, company_name: str, thesis_data: Dict[str, Any], 
                            research_data: Dict[str, Any], sentiment_data: Dict[str, Any], 
                            valuation_data: Dict[str, Any]) -> str:
        """Assess overall quality of the investment thesis"""
        try:
            prompt = f"""
            Assess the overall quality of the investment thesis for {company_name}:
            
            Thesis Data: {thesis_data}
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide quality assessment covering:
            
            ANALYSIS QUALITY:
            - Depth and rigor of analysis
            - Data quality and reliability
            - Methodology appropriateness
            - Analytical framework strength
            
            LOGICAL QUALITY:
            - Logical coherence and flow
            - Argument strength and validity
            - Evidence quality and relevance
            - Conclusion support
            
            PRESENTATION QUALITY:
            - Clarity and organization
            - Professional formatting
            - Executive summary quality
            - Supporting documentation
            
            COMPREHENSIVENESS:
            - Coverage completeness
            - Alternative view consideration
            - Risk assessment thoroughness
            - Implementation feasibility
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.CRITIQUE,
                max_fallbacks=3
            )
            
            return result.content if result else "Quality assessment not available"
            
        except Exception as e:
            print(f"❌ Error assessing quality: {e}")
            return "Quality assessment failed"
    
    async def _conduct_peer_review(self, company_name: str, thesis_data: Dict[str, Any], 
                                 research_data: Dict[str, Any], sentiment_data: Dict[str, Any], 
                                 valuation_data: Dict[str, Any]) -> str:
        """Conduct peer review of the investment thesis"""
        try:
            prompt = f"""
            Conduct a peer review of the investment thesis for {company_name}:
            
            Thesis Data: {thesis_data}
            Research Data: {research_data}
            Sentiment Data: {sentiment_data}
            Valuation Data: {valuation_data}
            
            Provide peer review covering:
            
            PEER REVIEW ASSESSMENT:
            - Independent evaluation perspective
            - Expert opinion and insights
            - Industry benchmark comparison
            - Best practices assessment
            
            VALIDATION POINTS:
            - Strong points and strengths
            - Areas of agreement
            - Supporting evidence validation
            - Credible analysis elements
            
            CHALLENGE POINTS:
            - Areas of disagreement
            - Alternative interpretations
            - Weaknesses and gaps
            - Questionable assumptions
            
            RECOMMENDATIONS:
            - Improvement suggestions
            - Additional analysis needs
            - Risk mitigation strategies
            - Implementation guidance
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.CRITIQUE,
                max_fallbacks=3
            )
            
            return result.content if result else "Peer review not available"
            
        except Exception as e:
            print(f"❌ Error conducting peer review: {e}")
            return "Peer review failed"
    
    async def _calculate_critique_score(self, critique_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate critique score and validation status"""
        try:
            prompt = f"""
            Calculate a critique score and validation status based on:
            
            Critique Data: {critique_data}
            
            Provide assessment covering:
            
            CRITIQUE SCORE (0-10 scale):
            - Overall thesis quality score
            - Validation strength assessment
            - Risk assessment quality
            - Bias mitigation effectiveness
            
            VALIDATION STATUS:
            - Validated/Partially Validated/Not Validated
            - Confidence level assessment
            - Key validation factors
            - Remaining concerns
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.CRITIQUE,
                max_fallbacks=3
            )
            
            content = result.content if result else "Critique score calculation not available"
            
            # Parse the result
            score = 5.0  # Default
            status = "Partially Validated"
            
            # Extract score
            import re
            score_match = re.search(r'score[:\s]*(\d+(?:\.\d+)?)', content.lower())
            if score_match:
                score = float(score_match.group(1))
            
            # Extract status
            if "validated" in content.lower():
                if "not validated" in content.lower():
                    status = "Not Validated"
                elif "partially validated" in content.lower():
                    status = "Partially Validated"
                else:
                    status = "Validated"
            
            return {
                "score": score,
                "status": status
            }
            
        except Exception as e:
            print(f"❌ Error calculating critique score: {e}")
            return {
                "score": 5.0,
                "status": "Partially Validated"
            }
    
    async def _identify_improvements_and_issues(self, critique_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify improvements and critical issues"""
        try:
            prompt = f"""
            Identify improvements and critical issues based on:
            
            Critique Data: {critique_data}
            
            Provide analysis covering:
            
            IMPROVEMENT RECOMMENDATIONS:
            - Specific improvement suggestions
            - Enhanced analysis needs
            - Additional data requirements
            - Methodology improvements
            
            CRITICAL ISSUES:
            - Major concerns and issues
            - Deal-breaker problems
            - Significant risks not addressed
            - Fundamental flaws
            
            STRENGTHS:
            - Strong points and positives
            - Well-executed elements
            - Credible analysis aspects
            - Valid assumptions
            
            WEAKNESSES:
            - Areas needing improvement
            - Weak analysis elements
            - Questionable assumptions
            - Missing components
            
            Format as lists for easy reference.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.CRITIQUE,
                max_fallbacks=3
            )
            
            content = result.content if result else "Improvements and issues analysis not available"
            
            # Parse the result
            improvements = []
            issues = []
            strengths = []
            weaknesses = []
            
            if "IMPROVEMENT RECOMMENDATIONS:" in content:
                improvements_section = content.split("IMPROVEMENT RECOMMENDATIONS:")[1].split("CRITICAL ISSUES:")[0]
                improvements = [line.strip() for line in improvements_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            if "CRITICAL ISSUES:" in content:
                issues_section = content.split("CRITICAL ISSUES:")[1].split("STRENGTHS:")[0]
                issues = [line.strip() for line in issues_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            if "STRENGTHS:" in content:
                strengths_section = content.split("STRENGTHS:")[1].split("WEAKNESSES:")[0]
                strengths = [line.strip() for line in strengths_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            if "WEAKNESSES:" in content:
                weaknesses_section = content.split("WEAKNESSES:")[1]
                weaknesses = [line.strip() for line in weaknesses_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            return {
                "improvements": improvements,
                "issues": issues,
                "strengths": strengths,
                "weaknesses": weaknesses
            }
            
        except Exception as e:
            print(f"❌ Error identifying improvements and issues: {e}")
            return {
                "improvements": ["Improvement identification failed"],
                "issues": ["Issue identification failed"],
                "strengths": ["Strength identification failed"],
                "weaknesses": ["Weakness identification failed"]
            }

# Export the agent
__all__ = ['CritiqueAgent'] 