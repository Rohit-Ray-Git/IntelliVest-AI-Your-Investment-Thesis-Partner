"""
🤖 CrewAI Agents with Advanced Fallback System
==============================================

This module defines CrewAI agents with integrated tools and advanced fallback system.
"""

import os
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Import our advanced fallback system
from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType

class InvestmentAnalysisCrewWithTools:
    """
    🚀 Advanced CrewAI system with tools and multi-LLM fallback
    """
    
    def __init__(self):
        """Initialize the investment analysis crew"""
        self.setup_advanced_fallback()
        self.setup_tools()
        self.create_agents()
        
    def setup_advanced_fallback(self):
        """Setup advanced fallback system"""
        try:
            self.fallback_system = AdvancedFallbackSystem()
            print("✅ Advanced fallback system initialized")
        except Exception as e:
            print(f"❌ Error initializing fallback system: {e}")
            raise e
    
    def setup_tools(self):
        """Initialize all custom tools"""
        try:
            from tools.investment_tools import (
                WebCrawlerTool,
                FinancialDataTool,
                SentimentAnalysisTool,
                ValuationTool,
                ThesisGenerationTool,
                CritiqueTool
            )
            
            self.tools = {
                'web_crawler': WebCrawlerTool(),
                'financial_data': FinancialDataTool(),
                'sentiment_analysis': SentimentAnalysisTool(),
                'valuation': ValuationTool(),
                'thesis_generation': ThesisGenerationTool(),
                'critique': CritiqueTool()
            }
            print("✅ Tools initialized successfully")
        except Exception as e:
            print(f"⚠️ Error initializing tools: {e}")
            self.tools = {}
            print("⚠️ Continuing without custom tools")
    
    def create_agents(self):
        """Create specialized CrewAI agents with advanced fallback system"""

        # 🤖 Research Agent
        self.researcher = Agent(
            role="Financial Research Analyst",
            goal="Gather comprehensive financial data, news, and market information about the target company",
            backstory="""You are an expert financial research analyst with 15+ years of experience.
            You specialize in gathering and analyzing financial data, market news, and company information.
            You have access to web crawling tools and financial data APIs to collect comprehensive information.
            You can provide detailed analysis of company financials, market position, and competitive landscape.

            When given a company name, you will:
            1. Research recent news and market updates about the company
            2. Analyze comprehensive financial metrics and ratios
            3. Evaluate the competitive landscape and market position
            4. Identify key risks and opportunities
            5. Provide well-organized research findings with specific data points.

            IMPORTANT: You have access to custom tools for web crawling and financial data retrieval.
            When you need financial data, mention that you would use the financial data tool.
            When you need news data, mention that you would use the web crawler tool.
            
            You use the most advanced AI models available for optimal analysis quality.""",
            llm=self._get_llm_for_task(TaskType.RESEARCH),
            verbose=True,
            allow_delegation=False
        )

        # 🧠 Sentiment Agent
        self.sentiment_analyst = Agent(
            role="Market Sentiment Analyst",
            goal="Analyze market sentiment, investor psychology, and behavioral finance factors",
            backstory="""You are a market sentiment analyst specializing in behavioral finance and investor psychology.
            You analyze market sentiment through multiple lenses including news sentiment, social media trends,
            analyst ratings, and institutional behavior patterns.

            Your expertise includes:
            1. News sentiment analysis and media coverage trends
            2. Social media sentiment and retail investor behavior
            3. Analyst ratings and price target analysis
            4. Institutional investor sentiment and positioning
            5. Market psychology and behavioral finance patterns

            You provide quantified sentiment scores and trend analysis to help understand market psychology.
            
            You use advanced AI models to ensure the highest quality sentiment analysis.""",
            llm=self._get_llm_for_task(TaskType.SENTIMENT),
            verbose=True,
            allow_delegation=False
        )

        # 💰 Valuation Agent
        self.valuation_analyst = Agent(
            role="Financial Valuation Expert",
            goal="Perform comprehensive financial valuation using multiple methodologies",
            backstory="""You are a financial valuation expert with expertise in multiple valuation methodologies.
            You specialize in DCF analysis, comparable company analysis, and asset-based valuation.

            Your valuation approach includes:
            1. Discounted Cash Flow (DCF) analysis with sensitivity testing
            2. Comparable company and precedent transaction analysis
            3. Asset-based valuation and liquidation analysis
            4. Financial ratio analysis and benchmarking
            5. Risk-adjusted valuation and scenario analysis

            You provide detailed valuation models with clear assumptions and price targets.
            
            You use the most sophisticated AI models for complex financial calculations.""",
            llm=self._get_llm_for_task(TaskType.VALUATION),
            verbose=True,
            allow_delegation=False
        )

        # 📝 Thesis Writer
        self.thesis_writer = Agent(
            role="Investment Thesis Writer",
            goal="Create professional investment theses with clear investment cases and recommendations",
            backstory="""You are an investment thesis writer who creates professional-grade investment analysis.
            You synthesize research, sentiment, and valuation data into compelling investment theses.

            Your thesis structure includes:
            1. Executive summary with investment recommendation
            2. Investment case with key value drivers
            3. Financial analysis and valuation summary
            4. Risk assessment and mitigation strategies
            5. Actionable investment recommendations

            You write for institutional investors and provide clear, actionable insights.
            
            You use the highest quality AI models to ensure professional-grade analysis.""",
            llm=self._get_llm_for_task(TaskType.THESIS),
            verbose=True,
            allow_delegation=False
        )

        # 🔍 Critic Agent
        self.critic = Agent(
            role="Investment Thesis Critic",
            goal="Review and improve investment theses through critical analysis and quality assurance",
            backstory="""You are an investment thesis critic who ensures the highest quality of analysis.
            You review investment theses for bias, logical consistency, and completeness.

            Your critique process includes:
            1. Bias analysis and identification of potential conflicts
            2. Data quality assessment and completeness review
            3. Logical consistency and reasoning validation
            4. Risk assessment adequacy evaluation
            5. Specific improvement recommendations

            You provide constructive feedback to improve thesis quality and reliability.
            
            You use advanced AI models to ensure thorough and unbiased critique.""",
            llm=self._get_llm_for_task(TaskType.CRITIQUE),
            verbose=True,
            allow_delegation=False
        )

        print("✅ All agents created successfully with advanced fallback system")
    
    def _get_llm_for_task(self, task_type: TaskType):
        """Get LLM instance for a specific task type using advanced fallback system"""
        try:
            # Get the primary model for this task type
            primary_provider = self.fallback_system.fallback_chains[task_type][0]
            
            # For CrewAI, we need to use the correct model format
            if primary_provider.value.startswith("gemini"):
                # Use Google Generative AI for Gemini models
                return ChatGoogleGenerativeAI(
                    model=primary_provider.value,
                    google_api_key=os.getenv("GOOGLE_API_KEY"),
                    temperature=0.7
                )
            elif primary_provider.value.startswith("groq/"):
                # Use OpenAI format for Groq models
                return ChatOpenAI(
                    model=primary_provider.value,
                    api_key=os.getenv("OPENAI_API_KEY"),
                    base_url=os.getenv("OPENAI_API_BASE"),
                    temperature=0.7
                )
            else:
                # Fallback to Gemini 2.5 Flash
                return ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    google_api_key=os.getenv("GOOGLE_API_KEY"),
                    temperature=0.7
                )
        except Exception as e:
            print(f"⚠️ Error getting LLM for {task_type.value}: {e}")
            # Fallback to basic LLM setup - use direct model name without prefix
            return ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.7
            )

    def create_tasks(self, company_name: str) -> List[Task]:
        """Create tasks for the investment analysis workflow"""
        tasks = [
            # Task 1: Research
            Task(
                description=f"""
                Research {company_name} thoroughly and provide a comprehensive analysis:
                
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
                Use available tools for web crawling and financial data when needed.
                """,
                agent=self.researcher,
                expected_output="Comprehensive research report with financial data, market analysis, and risk assessment"
            ),

            # Task 2: Sentiment Analysis
            Task(
                description=f"""
                Analyze market sentiment for {company_name}:
                
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
                """,
                agent=self.sentiment_analyst,
                expected_output="Detailed sentiment analysis with quantified scores and market psychology insights"
            ),

            # Task 3: Valuation
            Task(
                description=f"""
                Perform comprehensive valuation of {company_name}:
                
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
                """,
                agent=self.valuation_analyst,
                expected_output="Comprehensive valuation analysis with multiple methodologies and price targets"
            ),

            # Task 4: Thesis Generation
            Task(
                description=f"""
                Create an investment thesis for {company_name}:
                
                Based on the research, sentiment, and valuation analysis, create a professional investment thesis:
                
                1. Executive Summary:
                   - Investment recommendation (Buy/Hold/Sell)
                   - Key investment thesis points
                   - Expected return and time horizon
                
                2. Investment Case:
                   - Primary value drivers
                   - Growth opportunities
                   - Competitive advantages
                
                3. Financial Analysis:
                   - Key financial metrics summary
                   - Valuation summary
                   - Financial health assessment
                
                4. Risk Assessment:
                   - Key risks and challenges
                   - Risk mitigation strategies
                   - Downside scenarios
                
                5. Conclusion:
                   - Investment recommendation
                   - Key action items
                   - Monitoring points
                
                Structure the thesis professionally for institutional investors.
                """,
                agent=self.thesis_writer,
                expected_output="Professional investment thesis with clear recommendation and supporting analysis"
            ),

            # Task 5: Critique
            Task(
                description=f"""
                Review and improve the investment thesis for {company_name}:
                
                Provide a detailed critique of the investment thesis covering:
                
                1. Bias Analysis:
                   - Identify potential biases in the analysis
                   - Check for balanced perspective
                   - Evaluate conflict of interest considerations
                
                2. Data Quality:
                   - Assess completeness of data used
                   - Check for missing information
                   - Validate data sources and reliability
                
                3. Logical Consistency:
                   - Review reasoning and logic flow
                   - Check for internal contradictions
                   - Validate assumptions and conclusions
                
                4. Risk Assessment:
                   - Evaluate adequacy of risk analysis
                   - Check for missing risk factors
                   - Assess risk quantification
                
                5. Improvements:
                   - Suggest specific enhancements
                   - Identify areas for deeper analysis
                   - Recommend additional research needs
                
                Provide constructive feedback to improve thesis quality and reliability.
                """,
                agent=self.critic,
                expected_output="Detailed critique with specific improvement recommendations"
            )
        ]
        return tasks

    async def run_analysis(self, company_name: str) -> Dict[str, Any]:
        """Run the complete investment analysis using CrewAI with advanced fallback"""
        try:
            print(f"🚀 Starting advanced agentic analysis for: {company_name}")
            print(f"🎯 Using Advanced Fallback System with Gemini 2.5 Flash as primary model")
            
            tasks = self.create_tasks(company_name)
            crew = Crew(
                agents=[
                    self.researcher, self.sentiment_analyst, self.valuation_analyst,
                    self.thesis_writer, self.critic
                ],
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            print("🤖 Executing CrewAI workflow with advanced fallback system...")
            result = crew.kickoff()
            
            return {
                "company_name": company_name,
                "status": "success",
                "result": result,
                "agents_used": [
                    "Research Agent (Gemini 2.5 Flash)",
                    "Sentiment Agent (Gemini 2.5 Flash)", 
                    "Valuation Agent (Gemini 2.5 Flash)",
                    "Thesis Writer (Gemini 2.5 Flash)",
                    "Critic Agent (Gemini 2.5 Flash)"
                ],
                "fallback_system": "Advanced Multi-LLM Orchestration",
                "primary_model": "Gemini 2.5 Flash",
                "fallback_models": [
                    "Groq DeepSeek R1 Distill Llama-70B",
                    "Groq Llama 3.3-70B Versatile"
                ]
            }
            
        except Exception as e:
            print(f"❌ Error in advanced agentic analysis: {e}")
            return {
                "company_name": company_name,
                "status": "error",
                "error": str(e),
                "result": None
            }

# Example usage
if __name__ == "__main__":
    # Test the advanced crew
    async def test_advanced_crew():
        crew = InvestmentAnalysisCrewWithTools()
        result = await crew.run_analysis("Apple Inc.")
        print("Advanced agentic analysis completed!")
        print(result)
    
    asyncio.run(test_advanced_crew())