"""
🤖 Intelligent Agent Communication Example
=========================================

This example demonstrates how agents can communicate intelligently with each other
to enhance the investment thesis generation process.
"""

import asyncio
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our enhanced agents and communication system
from agents.agent_communication_system import communication_system, CommunicatingAgent
from agents.enhanced_thesis_rewrite_agent import EnhancedThesisRewriteAgent

# Example enhanced agents that can communicate
class EnhancedResearchAgent(CommunicatingAgent):
    """Enhanced Research Agent with communication capabilities"""
    
    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            capabilities=["company_research", "financial_data", "market_analysis", "collaboration"]
        )
    
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide research data to other agents"""
        if request_type == "company_research":
            return {
                "company_overview": f"Comprehensive overview of {company_name}",
                "business_model": f"Business model analysis for {company_name}",
                "market_position": f"Market position analysis for {company_name}",
                "financial_metrics": f"Key financial metrics for {company_name}",
                "growth_prospects": f"Growth prospects for {company_name}"
            }
        else:
            return {"error": f"Cannot provide {request_type} data"}
    
    async def collaborate(self, collaboration_type: str, shared_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other agents"""
        if collaboration_type == "data_validation":
            return {
                "validation_result": "Data validated successfully",
                "confidence_score": 0.85,
                "validation_notes": "All data points verified and consistent"
            }
        else:
            return {"error": f"Cannot collaborate on {collaboration_type}"}

class EnhancedSentimentAgent(CommunicatingAgent):
    """Enhanced Sentiment Agent with communication capabilities"""
    
    def __init__(self):
        super().__init__(
            name="SentimentAgent",
            capabilities=["sentiment_analysis", "market_mood", "validation", "collaboration"]
        )
    
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide sentiment data to other agents"""
        if request_type == "sentiment_analysis":
            return {
                "news_sentiment": f"News sentiment analysis for {company_name}",
                "social_sentiment": f"Social media sentiment for {company_name}",
                "analyst_sentiment": f"Analyst sentiment for {company_name}",
                "market_mood": f"Overall market mood for {company_name}",
                "sentiment_score": 0.72
            }
        else:
            return {"error": f"Cannot provide {request_type} data"}
    
    async def collaborate(self, collaboration_type: str, shared_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other agents"""
        if collaboration_type == "sentiment_validation":
            return {
                "validation_result": "Sentiment analysis validated",
                "consistency_score": 0.88,
                "validation_notes": "Sentiment data is consistent across sources"
            }
        else:
            return {"error": f"Cannot collaborate on {collaboration_type}"}

class EnhancedValuationAgent(CommunicatingAgent):
    """Enhanced Valuation Agent with communication capabilities"""
    
    def __init__(self):
        super().__init__(
            name="ValuationAgent",
            capabilities=["financial_metrics", "valuation_analysis", "validation", "collaboration"]
        )
    
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide valuation data to other agents"""
        if request_type == "financial_metrics":
            return {
                "dcf_analysis": f"DCF analysis for {company_name}",
                "comparable_analysis": f"Comparable company analysis for {company_name}",
                "relative_valuation": f"Relative valuation metrics for {company_name}",
                "fair_value": f"Fair value estimate for {company_name}",
                "valuation_range": f"Valuation range for {company_name}"
            }
        else:
            return {"error": f"Cannot provide {request_type} data"}
    
    async def collaborate(self, collaboration_type: str, shared_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other agents"""
        if collaboration_type == "valuation_validation":
            return {
                "validation_result": "Valuation analysis validated",
                "consistency_score": 0.92,
                "validation_notes": "Valuation metrics are consistent and reliable"
            }
        else:
            return {"error": f"Cannot collaborate on {collaboration_type}"}

class EnhancedCritiqueAgent(CommunicatingAgent):
    """Enhanced Critique Agent with communication capabilities"""
    
    def __init__(self):
        super().__init__(
            name="CritiqueAgent",
            capabilities=["thesis_critique", "validation", "quality_assessment", "collaboration"]
        )
    
    async def validate(self, validation_type: str, data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Validate thesis improvements"""
        if validation_type == "improvement_validation":
            thesis = data.get("revised_thesis", "")
            company_name = data.get("company_name", "")
            
            # Perform validation logic
            validation_score = 0.89
            suggestions = [
                "Consider adding more quantitative analysis",
                "Include additional risk factors",
                "Strengthen the competitive analysis section"
            ]
            
            return {
                "validation_score": validation_score,
                "quality_assessment": "High quality thesis",
                "suggestions": suggestions,
                "validation_notes": f"Thesis for {company_name} meets institutional standards"
            }
        else:
            return {"error": f"Cannot validate {validation_type}"}

async def demonstrate_intelligent_communication():
    """Demonstrate intelligent inter-agent communication"""
    
    print("🚀 Starting Intelligent Agent Communication Demo")
    print("=" * 60)
    
    # Initialize enhanced agents
    research_agent = EnhancedResearchAgent()
    sentiment_agent = EnhancedSentimentAgent()
    valuation_agent = EnhancedValuationAgent()
    critique_agent = EnhancedCritiqueAgent()
    thesis_rewrite_agent = EnhancedThesisRewriteAgent()
    
    # Wait for agents to register
    await asyncio.sleep(1)
    
    print("\n📊 Agent Registration Status:")
    print(f"Registered Agents: {list(communication_system.agents.keys())}")
    print(f"Agent Capabilities: {communication_system.agent_capabilities}")
    
    # Example scenario: Thesis rewrite agent needs additional data
    print("\n🤖 Scenario: Thesis Rewrite Agent needs additional data")
    print("-" * 50)
    
    # Simulate thesis rewrite process
    company_name = "Apple Inc."
    original_thesis = """
    # Investment Thesis: Apple Inc.
    
    ## Executive Summary
    Apple Inc. represents a compelling investment opportunity based on its strong brand, 
    innovative product ecosystem, and robust financial performance.
    
    ## Investment Case
    Apple's iPhone business continues to drive revenue growth, while services segment 
    provides recurring revenue streams and higher margins.
    
    ## Risk Analysis
    Key risks include supply chain disruptions and regulatory challenges.
    """
    
    critique_feedback = """
    The thesis lacks detailed financial analysis and quantitative metrics. 
    Need more comprehensive risk assessment and competitive analysis.
    """
    
    print(f"📝 Original Thesis Length: {len(original_thesis)} characters")
    print(f"🔍 Critique Feedback: {critique_feedback[:100]}...")
    
    # Demonstrate intelligent data gathering
    print("\n🤖 Step 1: Intelligent Data Gathering")
    print("-" * 40)
    
    # Thesis rewrite agent requests data from other agents
    print("📤 Thesis Rewrite Agent → Research Agent: Requesting company research data...")
    research_data = await thesis_rewrite_agent.request_data(
        recipient="ResearchAgent",
        request_type="company_research",
        company_name=company_name,
        specific_data=["financial_metrics", "growth_prospects"]
    )
    print(f"📥 Research Agent Response: {len(str(research_data))} characters")
    
    print("\n📤 Thesis Rewrite Agent → Sentiment Agent: Requesting sentiment analysis...")
    sentiment_data = await thesis_rewrite_agent.request_data(
        recipient="SentimentAgent",
        request_type="sentiment_analysis",
        company_name=company_name,
        specific_data=["news_sentiment", "analyst_sentiment"]
    )
    print(f"📥 Sentiment Agent Response: {len(str(sentiment_data))} characters")
    
    print("\n📤 Thesis Rewrite Agent → Valuation Agent: Requesting financial metrics...")
    valuation_data = await thesis_rewrite_agent.request_data(
        recipient="ValuationAgent",
        request_type="financial_metrics",
        company_name=company_name,
        specific_data=["dcf_analysis", "fair_value"]
    )
    print(f"📥 Valuation Agent Response: {len(str(valuation_data))} characters")
    
    # Demonstrate collaboration
    print("\n🤝 Step 2: Inter-Agent Collaboration")
    print("-" * 40)
    
    print("🤝 Thesis Rewrite Agent → Research Agent: Collaborating for data validation...")
    research_validation = await thesis_rewrite_agent.request_collaboration(
        recipient="ResearchAgent",
        collaboration_type="data_validation",
        shared_data={
            "company_name": company_name,
            "research_data": research_data
        },
        params={"validation_type": "data_accuracy"}
    )
    print(f"🤝 Research Validation Result: {research_validation}")
    
    print("\n🤝 Thesis Rewrite Agent → Sentiment Agent: Collaborating for sentiment validation...")
    sentiment_validation = await thesis_rewrite_agent.request_collaboration(
        recipient="SentimentAgent",
        collaboration_type="sentiment_validation",
        shared_data={
            "company_name": company_name,
            "sentiment_data": sentiment_data
        },
        params={"validation_type": "sentiment_consistency"}
    )
    print(f"🤝 Sentiment Validation Result: {sentiment_validation}")
    
    # Demonstrate final validation
    print("\n✅ Step 3: Final Validation with Critique Agent")
    print("-" * 50)
    
    # Simulate revised thesis
    revised_thesis = original_thesis + "\n\n## Enhanced Financial Analysis\n[Additional financial data would be here]"
    
    print("✅ Thesis Rewrite Agent → Critique Agent: Requesting improvement validation...")
    final_validation = await thesis_rewrite_agent.request_validation(
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
    print(f"✅ Final Validation Result: {final_validation}")
    
    # Show communication log
    print("\n📋 Communication Log Summary")
    print("-" * 40)
    communication_log = communication_system.get_communication_log()
    for i, log_entry in enumerate(communication_log[-5:], 1):  # Show last 5 entries
        print(f"{i}. {log_entry['sender']} → {log_entry['recipient']}: {log_entry['type']}")
    
    print(f"\n📊 Total Communications: {len(communication_log)}")
    print(f"🤖 Active Agents: {len(communication_system.agents)}")
    
    print("\n✅ Intelligent Agent Communication Demo Completed!")
    print("=" * 60)

if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(demonstrate_intelligent_communication()) 