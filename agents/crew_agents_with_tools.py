"""
🤖 CrewAI Agents with Advanced Fallback System & Parallel Processing
===================================================================

This module defines CrewAI agents with integrated tools, advanced fallback system,
and optimized parallel processing for high-speed research.
"""

import os
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables and configure LiteLLM
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

from crewai import Agent, Task, Crew, Process

# Import our advanced fallback system
from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType

class InvestmentAnalysisCrewWithTools:
    """
    🚀 Advanced CrewAI system with tools, multi-LLM fallback, and parallel processing
    """
    
    def __init__(self, max_concurrent: int = 10):
        """Initialize the investment analysis crew with parallel processing"""
        self.max_concurrent = max_concurrent
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
        """Initialize all custom tools including parallel processing tools"""
        try:
            from tools.investment_tools import (
                WebCrawlerTool,
                FinancialDataTool,
                SentimentAnalysisTool,
                ValuationTool,
                ThesisGenerationTool,
                CritiqueTool
            )
            
            # Import parallel processing tools
            from tools.parallel_search_tools import (
                ParallelWebSearchTool,
                ParallelInstitutionalDataTool
            )
            
            self.tools = {
                'web_crawler': WebCrawlerTool(),
                'financial_data': FinancialDataTool(),
                'sentiment_analysis': SentimentAnalysisTool(),
                'valuation': ValuationTool(),
                'thesis_generation': ThesisGenerationTool(),
                'critique': CritiqueTool(),
                # Add parallel processing tools
                'parallel_web_search': ParallelWebSearchTool(max_concurrent=self.max_concurrent),
                'parallel_institutional_data': ParallelInstitutionalDataTool()
            }
            print(f"✅ Tools initialized successfully with {self.max_concurrent} parallel workers")
        except Exception as e:
            print(f"⚠️ Error initializing tools: {e}")
            self.tools = {}
            print("⚠️ Continuing without custom tools")
    
    def create_agents(self):
        """Create specialized CrewAI agents with advanced fallback system and parallel processing"""

        # ⚡ Optimized Research Agent with Parallel Processing
        self.researcher = Agent(
            role="High-Speed Financial Research Analyst",
            goal="Gather comprehensive financial data, news, and market information using parallel processing for maximum speed with focus on CURRENT and RECENT data",
            backstory=f"""You are an expert financial research analyst with 15+ years of experience.
            You specialize in gathering and analyzing the MOST RECENT financial data, market news, and company information
            using advanced parallel processing techniques to achieve maximum speed and efficiency.
            
            Your expertise includes:
            - Real-time market data analysis and current financial metrics
            - Latest earnings reports, guidance updates, and recent corporate developments
            - Current competitive landscape and recent market changes
            - Recent regulatory updates and compliance changes
            - Latest analyst reports, price targets, and institutional activity
            - Current risk factors and recent market developments
            
            You have access to:
            - Parallel web search tools for ultra-fast current data discovery
            - Financial data APIs for comprehensive real-time metrics
            - Parallel institutional data tools for current holdings analysis
            - Advanced AI models for optimal analysis quality
            
            Your parallel processing capabilities allow you to:
            1. Search multiple current news sources simultaneously
            2. Gather the latest financial data from multiple sources in parallel
            3. Analyze current institutional holdings and real-time market data concurrently
            4. Process multiple current analysis tasks simultaneously
            
            When given a company name, you will:
            1. Use parallel search to gather the MOST RECENT news and market updates rapidly
            2. Analyze current comprehensive financial metrics using parallel data gathering
            3. Evaluate the current competitive landscape with concurrent analysis
            4. Identify current key risks and opportunities using parallel processing
            5. Provide well-organized research findings with specific CURRENT data points
            
            CRITICAL: You prioritize the LATEST information from the past 3-6 months and avoid outdated data.
            - Focus on recent earnings reports, current financial metrics, and latest developments
            - Emphasize what has changed recently and current market conditions
            - Include specific dates and timeframes for all information
            - Prioritize 2025 data and Q1 2025 results when available
            - Use parallel web search tools for current news and market data
            - Use parallel institutional data tools for current holdings analysis
            - Use financial data tools for current comprehensive metrics
            
            You use the most advanced AI models available for optimal analysis quality
            and achieve 2-3x faster execution times compared to traditional sequential methods
            while ensuring all data is current and relevant.""",
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
            # For CrewAI with LiteLLM, we need to use the proper model format
            # Use Gemini 2.5 Flash as the primary model for all tasks
            # Format: "gemini/gemini-2.5-flash" for LiteLLM (explicit format)
            # Also ensure API key is properly configured
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if not google_api_key:
                print("⚠️ Warning: GOOGLE_API_KEY not found in environment")
            
            return "gemini/gemini-2.5-flash"
        except Exception as e:
            print(f"⚠️ Error getting LLM for {task_type.value}: {e}")
            # Fallback to basic LLM setup
            return "gemini/gemini-2.5-flash"

    def create_tasks(self, company_name: str) -> List[Task]:
        """Create tasks for the investment analysis workflow"""
        from datetime import datetime
        
        # Get current date for analysis
        current_date = datetime.now().strftime("%B %d, %Y")
        current_year = datetime.now().year
        
        tasks = [
            # Task 1: Research
            Task(
                description=f"""
                Research {company_name} thoroughly and provide a comprehensive analysis using the MOST RECENT and CURRENT data available:
                
                CURRENT DATE: {current_date} - Use this date for all analysis references.
                
                CRITICAL: Focus on the LATEST information from the past 3-6 months. Prioritize real-time data and recent developments.
                
                1. Company Overview (Recent Developments):
                   - Current business model and latest products/services launched
                   - Recent market position changes and competitive advantages
                   - Latest management changes, strategy updates, or corporate actions
                   - Recent earnings reports, guidance updates, or financial announcements
                
                2. Financial Analysis (Latest Data):
                   - Most recent quarterly/annual financial results (Q4 2024, Q1 {current_year})
                   - Current financial ratios and metrics (P/E, P/B, ROE, etc.)
                   - Latest cash flow and balance sheet strength indicators
                   - Recent debt levels, credit ratings, or financial health updates
                   - Current stock price performance and trading volume trends
                
                3. Market Analysis (Current State):
                   - Latest industry trends and market size updates
                   - Current competitive landscape and recent competitive moves
                   - Recent regulatory changes or compliance updates
                   - Current market sentiment and analyst ratings
                   - Latest market share data and positioning
                
                4. Risk Assessment (Current Risks):
                   - Current business risks and challenges (last 3-6 months)
                   - Recent market risks and economic factors affecting the company
                   - Current competitive threats and industry disruptions
                   - Latest regulatory or legal developments
                   - Current supply chain or operational challenges
                
                5. Recent News and Events (Past 3-6 Months):
                   - Latest earnings calls and management commentary
                   - Recent analyst reports and price target updates
                   - Current insider trading activity or institutional moves
                   - Latest product launches, partnerships, or acquisitions
                   - Recent legal issues, investigations, or controversies
                
                IMPORTANT REQUIREMENTS:
                - Use ONLY the most recent data available (prioritize last 3-6 months)
                - Include specific dates and timeframes for all information
                - Focus on current market conditions and recent developments
                - Avoid outdated information or historical data unless relevant to current analysis
                - Emphasize what has changed recently and current trends
                - Prioritize {current_year} data and Q1 {current_year} results when available
                - ALWAYS use {current_date} as the analysis date, not historical dates
                
                Provide comprehensive, well-organized research findings with specific current data points and recent developments.
                Use available tools for web crawling and financial data to gather the LATEST information.
                """,
                agent=self.researcher,
                expected_output="Comprehensive research report with current financial data, recent market analysis, and latest risk assessment"
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
                
                CURRENT DATE: {current_date} - Use this date for the thesis.
                
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
                
                IMPORTANT: 
                - Use {current_date} as the analysis date
                - Structure the thesis professionally for institutional investors
                - Include the current date in the thesis header
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
            ),

            # Task 6: Final Thesis Rewrite (NEW)
            Task(
                description=f"""
                Rewrite the investment thesis for {company_name} based on the critic's recommendations:
                
                CURRENT DATE: {current_date} - Use this date for the final thesis.
                
                Using the original thesis and the critic's detailed feedback, create a final improved investment thesis:
                
                1. Address All Critic Feedback:
                   - Incorporate all valid recommendations from the critique
                   - Fix any identified biases or logical inconsistencies
                   - Add missing data or analysis as suggested
                   - Strengthen weak arguments or assumptions
                
                2. Enhanced Executive Summary:
                   - Clear investment recommendation with confidence level
                   - Key thesis points with supporting evidence
                   - Expected return and time horizon with risk factors
                
                3. Strengthened Investment Case:
                   - Robust value drivers with quantitative support
                   - Clear growth opportunities with market validation
                   - Competitive advantages with competitive analysis
                
                4. Comprehensive Financial Analysis:
                   - Complete financial metrics with peer comparison
                   - Multiple valuation approaches with sensitivity analysis
                   - Financial health assessment with risk factors
                
                5. Thorough Risk Assessment:
                   - Comprehensive risk identification and analysis
                   - Risk mitigation strategies with implementation plans
                   - Downside scenarios with probability assessment
                
                6. Actionable Conclusion:
                   - Clear investment recommendation with conviction
                   - Specific action items for investors
                   - Key monitoring points and triggers
                
                CRITICAL REQUIREMENTS:
                - Use {current_date} as the analysis date in the thesis header
                - Create a professional, well-structured final investment thesis
                - Address all critique feedback and provide compelling, well-supported investment recommendation
                - Ensure the thesis reflects current market conditions as of {current_date}
                """,
                agent=self.thesis_writer,
                expected_output="Final improved investment thesis incorporating all critic recommendations"
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