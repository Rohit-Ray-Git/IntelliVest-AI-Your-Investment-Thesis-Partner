"""
🔄 LangGraph Investment Analysis Workflow
========================================

This module defines a sophisticated LangGraph workflow for investment analysis with:
- State management and persistence
- Conditional logic and decision trees
- Parallel and sequential execution
- Error handling and recovery
- Dynamic task routing
"""

import os
import asyncio
from typing import Dict, List, Any, TypedDict, Annotated
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import LangGraph components
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# Import LangChain components
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

# Import our custom tools and agents
from tools.investment_tools import (
    WebCrawlerTool,
    FinancialDataTool,
    SentimentAnalysisTool,
    ValuationTool,
    ThesisGenerationTool,
    CritiqueTool
)

# Define the state structure
class InvestmentState(TypedDict):
    """State for the investment analysis workflow"""
    company_name: str
    messages: Annotated[List, add_messages]
    research_data: Dict[str, Any]
    sentiment_analysis: Dict[str, Any]
    valuation_data: Dict[str, Any]
    investment_thesis: Dict[str, Any]
    critique: Dict[str, Any]
    current_step: str
    errors: List[str]
    tools_used: List[str]
    confidence_score: float
    recommendation: str

class InvestmentWorkflow:
    """
    🚀 Advanced LangGraph workflow for investment analysis
    """
    
    def __init__(self):
        """Initialize the investment workflow"""
        self.setup_llm()
        self.setup_tools()
        self.create_workflow()
        
    def setup_llm(self):
        """Setup LLM with fallback support"""
        try:
            # Use Groq models with correct model names
            self.primary_llm = ChatOpenAI(
                model="groq/llama3.1-70b-8192",  # Use groq/ prefix
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE"),
                temperature=0.7
            )
            print("✅ LangGraph LLM: Groq Llama3.1-70B configured")
            
        except Exception as e:
            print(f"⚠️ Groq Llama3.1-70B failed: {e}")
            # Try with different Groq model
            try:
                self.primary_llm = ChatOpenAI(
                    model="groq/llama3.1-8b-8192",  # Smaller Groq model
                    api_key=os.getenv("OPENAI_API_KEY"),
                    base_url=os.getenv("OPENAI_API_BASE"),
                    temperature=0.7
                )
                print("✅ Fallback LLM: Groq Llama3.1-8B configured")
            except Exception as e2:
                print(f"⚠️ Groq Llama3.1-8B failed: {e2}")
                # Try with Mixtral
                try:
                    self.primary_llm = ChatOpenAI(
                        model="groq/mixtral-8x7b-32768",  # Mixtral model
                        api_key=os.getenv("OPENAI_API_KEY"),
                        base_url=os.getenv("OPENAI_API_BASE"),
                        temperature=0.7
                    )
                    print("✅ Final Fallback LLM: Groq Mixtral configured")
                except Exception as e3:
                    print(f"❌ All LLM options failed: {e3}")
                    raise e3
    
    def setup_tools(self):
        """Initialize all custom tools"""
        try:
            self.tools = {
                'web_crawler': WebCrawlerTool(),
                'financial_data': FinancialDataTool(),
                'sentiment_analysis': SentimentAnalysisTool(),
                'valuation': ValuationTool(),
                'thesis_generation': ThesisGenerationTool(),
                'critique': CritiqueTool()
            }
            print("✅ LangGraph tools initialized successfully")
        except Exception as e:
            print(f"⚠️ Error initializing tools: {e}")
            self.tools = {}
            print("⚠️ Continuing without custom tools")
    
    def research_agent(self, state: InvestmentState) -> InvestmentState:
        """Research agent node"""
        try:
            company_name = state["company_name"]
            
            # Create research prompt
            research_prompt = f"""
            You are a Financial Research Analyst. Research {company_name} thoroughly:
            
            1. Company Overview:
               - Business model and main products/services
               - Market position and competitive advantages
               - Management team and strategy
            
            2. Financial Analysis:
               - Revenue, earnings, and growth trends
               - Key financial ratios (P/E, P/B, ROE, etc.)
               - Cash flow and balance sheet strength
            
            3. Market Analysis:
               - Industry trends and market size
               - Competitive landscape
               - Regulatory environment
            
            4. Risk Assessment:
               - Business risks and challenges
               - Market risks and economic factors
               - Competitive threats
            
            Provide comprehensive, well-organized research findings with specific data points.
            """
            
            # Get LLM response
            messages = [HumanMessage(content=research_prompt)]
            response = self.primary_llm.invoke(messages)
            
            # Update state
            state["research_data"] = {
                "analysis": response.content,
                "company_name": company_name,
                "timestamp": asyncio.get_event_loop().time()
            }
            state["current_step"] = "research_completed"
            state["tools_used"].append("research_analysis")
            
            print(f"✅ Research completed for {company_name}")
            
        except Exception as e:
            state["errors"].append(f"Research error: {str(e)}")
            print(f"❌ Research error: {e}")
        
        return state
    
    def sentiment_agent(self, state: InvestmentState) -> InvestmentState:
        """Sentiment analysis agent node"""
        try:
            company_name = state["company_name"]
            
            # Create sentiment analysis prompt
            sentiment_prompt = f"""
            You are a Market Sentiment Analyst. Analyze market sentiment for {company_name}:
            
            1. News Sentiment:
               - Recent news coverage and tone
               - Analyst ratings and price targets
               - Earnings call sentiment
            
            2. Market Sentiment:
               - Stock price trends and volume
               - Options flow and institutional activity
               - Social media sentiment trends
            
            3. Investor Sentiment:
               - Retail vs institutional sentiment
               - Short interest and insider trading
               - Market positioning
            
            4. Sentiment Drivers:
               - Key events affecting sentiment
               - Seasonal or cyclical patterns
               - Long-term sentiment trends
            
            Provide detailed sentiment analysis with quantified scores and trend analysis.
            """
            
            # Get LLM response
            messages = [HumanMessage(content=sentiment_prompt)]
            response = self.primary_llm.invoke(messages)
            
            # Update state
            state["sentiment_analysis"] = {
                "analysis": response.content,
                "company_name": company_name,
                "timestamp": asyncio.get_event_loop().time()
            }
            state["current_step"] = "sentiment_completed"
            state["tools_used"].append("sentiment_analysis")
            
            print(f"✅ Sentiment analysis completed for {company_name}")
            
        except Exception as e:
            state["errors"].append(f"Sentiment error: {str(e)}")
            print(f"❌ Sentiment error: {e}")
        
        return state
    
    def valuation_agent(self, state: InvestmentState) -> InvestmentState:
        """Valuation agent node"""
        try:
            company_name = state["company_name"]
            
            # Create valuation prompt
            valuation_prompt = f"""
            You are a Financial Valuation Expert. Perform comprehensive valuation of {company_name}:
            
            1. Financial Ratios:
               - P/E, P/B, P/S, EV/EBITDA ratios
               - ROE, ROA, profit margins
               - Debt ratios and financial health
            
            2. Valuation Models:
               - DCF analysis with reasonable assumptions
               - Comparable company analysis
               - Asset-based valuation
            
            3. Peer Comparison:
               - Industry average ratios
               - Competitor valuation multiples
               - Relative valuation analysis
            
            4. Price Targets:
               - Intrinsic value estimates
               - Upside/downside scenarios
               - Risk-adjusted returns
            
            Provide detailed valuation analysis with multiple methodologies and price targets.
            """
            
            # Get LLM response
            messages = [HumanMessage(content=valuation_prompt)]
            response = self.primary_llm.invoke(messages)
            
            # Update state
            state["valuation_data"] = {
                "analysis": response.content,
                "company_name": company_name,
                "timestamp": asyncio.get_event_loop().time()
            }
            state["current_step"] = "valuation_completed"
            state["tools_used"].append("valuation_analysis")
            
            print(f"✅ Valuation completed for {company_name}")
            
        except Exception as e:
            state["errors"].append(f"Valuation error: {str(e)}")
            print(f"❌ Valuation error: {e}")
        
        return state
    
    def thesis_writer_agent(self, state: InvestmentState) -> InvestmentState:
        """Thesis writer agent node"""
        try:
            company_name = state["company_name"]
            
            # Gather previous analysis
            research = state.get("research_data", {}).get("analysis", "")
            sentiment = state.get("sentiment_analysis", {}).get("analysis", "")
            valuation = state.get("valuation_data", {}).get("analysis", "")
            
            # Create thesis generation prompt
            thesis_prompt = f"""
            You are an Investment Thesis Writer. Create an investment thesis for {company_name}:
            
            Previous Analysis:
            - Research: {research[:500]}...
            - Sentiment: {sentiment[:500]}...
            - Valuation: {valuation[:500]}...
            
            Create a professional investment thesis with:
            1. Executive Summary with investment recommendation
            2. Investment Case with key drivers
            3. Financial Analysis summary
            4. Risk Assessment
            5. Conclusion with actionable recommendations
            
            Structure the thesis professionally for institutional investors.
            """
            
            # Get LLM response
            messages = [HumanMessage(content=thesis_prompt)]
            response = self.primary_llm.invoke(messages)
            
            # Update state
            state["investment_thesis"] = {
                "thesis": response.content,
                "company_name": company_name,
                "timestamp": asyncio.get_event_loop().time()
            }
            state["current_step"] = "thesis_completed"
            state["tools_used"].append("thesis_generation")
            
            print(f"✅ Investment thesis completed for {company_name}")
            
        except Exception as e:
            state["errors"].append(f"Thesis error: {str(e)}")
            print(f"❌ Thesis error: {e}")
        
        return state
    
    def critic_agent(self, state: InvestmentState) -> InvestmentState:
        """Critic agent node"""
        try:
            company_name = state["company_name"]
            thesis = state.get("investment_thesis", {}).get("thesis", "")
            
            # Create critique prompt
            critique_prompt = f"""
            You are an Investment Thesis Critic. Review and improve the investment thesis for {company_name}:
            
            Thesis to Review:
            {thesis[:1000]}...
            
            Provide a detailed critique covering:
            1. Bias Analysis - identify potential biases
            2. Data Quality - check for missing information
            3. Logical Consistency - review reasoning
            4. Risk Assessment - evaluate risk analysis
            5. Improvements - suggest specific enhancements
            
            Provide constructive feedback to improve thesis quality.
            """
            
            # Get LLM response
            messages = [HumanMessage(content=critique_prompt)]
            response = self.primary_llm.invoke(messages)
            
            # Update state
            state["critique"] = {
                "critique": response.content,
                "company_name": company_name,
                "timestamp": asyncio.get_event_loop().time()
            }
            state["current_step"] = "critique_completed"
            state["tools_used"].append("critique_analysis")
            
            print(f"✅ Critique completed for {company_name}")
            
        except Exception as e:
            state["errors"].append(f"Critique error: {str(e)}")
            print(f"❌ Critique error: {e}")
        
        return state
    
    def decision_router(self, state: InvestmentState) -> str:
        """Route to next step based on current state"""
        current_step = state.get("current_step", "start")
        
        # Define the workflow sequence
        workflow_steps = [
            "start",
            "research_completed", 
            "sentiment_completed",
            "valuation_completed",
            "thesis_completed",
            "critique_completed"
        ]
        
        try:
            current_index = workflow_steps.index(current_step)
            if current_index < len(workflow_steps) - 1:
                next_step = workflow_steps[current_index + 1]
                return next_step
            else:
                return "end"
        except ValueError:
            return "research"  # Default to research if step not found
    
    def create_workflow(self):
        """Create the LangGraph workflow"""
        
        # Create the workflow graph
        workflow = StateGraph(InvestmentState)
        
        # Add nodes
        workflow.add_node("research", self.research_agent)
        workflow.add_node("sentiment", self.sentiment_agent)
        workflow.add_node("valuation", self.valuation_agent)
        workflow.add_node("thesis", self.thesis_writer_agent)
        workflow.add_node("critique", self.critic_agent)
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "research",
            self.decision_router,
            {
                "sentiment": "sentiment",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "sentiment",
            self.decision_router,
            {
                "valuation": "valuation",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "valuation",
            self.decision_router,
            {
                "thesis": "thesis",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "thesis",
            self.decision_router,
            {
                "critique": "critique",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "critique",
            self.decision_router,
            {
                "end": END
            }
        )
        
        # Set entry point
        workflow.set_entry_point("research")
        
        # Compile the workflow
        self.app = workflow.compile(checkpointer=MemorySaver())
        
        print("✅ LangGraph workflow created successfully")
    
    def run_analysis(self, company_name: str) -> Dict[str, Any]:
        """
        🚀 Run the complete investment analysis using LangGraph
        
        Args:
            company_name: Name of the company to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            print(f"🚀 Starting LangGraph analysis for: {company_name}")
            
            # Initialize state
            initial_state = InvestmentState(
                company_name=company_name,
                messages=[],
                research_data={},
                sentiment_analysis={},
                valuation_data={},
                investment_thesis={},
                critique={},
                current_step="start",
                errors=[],
                tools_used=[],
                confidence_score=0.0,
                recommendation=""
            )
            
            # Run the workflow
            print("🔄 Executing LangGraph workflow...")
            result = self.app.invoke(initial_state)
            
            # Calculate confidence score based on completion
            completed_steps = len([k for k, v in result.items() if isinstance(v, dict) and v])
            total_steps = 5
            confidence_score = (completed_steps / total_steps) * 100
            
            # Generate final recommendation
            recommendation = self._generate_recommendation(result, confidence_score)
            
            return {
                "company_name": company_name,
                "status": "success",
                "result": result,
                "confidence_score": confidence_score,
                "recommendation": recommendation,
                "steps_completed": completed_steps,
                "total_steps": total_steps,
                "tools_used": result.get("tools_used", []),
                "errors": result.get("errors", [])
            }
            
        except Exception as e:
            print(f"❌ Error in LangGraph analysis: {e}")
            return {
                "company_name": company_name,
                "status": "error",
                "error": str(e),
                "result": None
            }
    
    def _generate_recommendation(self, result: Dict, confidence_score: float) -> str:
        """Generate final investment recommendation"""
        try:
            # Create recommendation prompt
            recommendation_prompt = f"""
            Based on the investment analysis with {confidence_score:.1f}% confidence score:
            
            Research: {result.get('research_data', {}).get('analysis', '')[:300]}...
            Sentiment: {result.get('sentiment_analysis', {}).get('analysis', '')[:300]}...
            Valuation: {result.get('valuation_data', {}).get('analysis', '')[:300]}...
            Thesis: {result.get('investment_thesis', {}).get('thesis', '')[:300]}...
            Critique: {result.get('critique', {}).get('critique', '')[:300]}...
            
            Provide a clear, actionable investment recommendation (Buy/Hold/Sell) 
            with brief reasoning and confidence level.
            """
            
            messages = [HumanMessage(content=recommendation_prompt)]
            response = self.primary_llm.invoke(messages)
            
            return response.content
            
        except Exception as e:
            return f"Recommendation generation failed: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Test the LangGraph workflow
    workflow = InvestmentWorkflow()
    result = workflow.run_analysis("Apple Inc.")
    print("LangGraph analysis completed!")
    print(result) 