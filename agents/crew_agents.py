"""
🤖 CrewAI Agent Definitions for IntelliVest AI
==============================================

This module defines specialized CrewAI agents for investment analysis:
- Research Agent: Gathers financial data and news
- Sentiment Agent: Analyzes market sentiment
- Valuation Agent: Performs financial valuation
- Thesis Writer Agent: Creates investment theses
- Critic Agent: Reviews and improves theses

All agents use Gemini 2.5 Flash as the primary LLM with fallback support.
"""

import os
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import CrewAI components
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Import our custom tools (will be created next)
from tools.investment_tools import (
    WebCrawlerTool,
    FinancialDataTool,
    SentimentAnalysisTool,
    ValuationTool,
    ThesisGenerationTool,
    CritiqueTool
)

class InvestmentAnalysisCrew:
    """
    🚀 Main CrewAI orchestration class for investment analysis
    """
    
    def __init__(self):
        """Initialize the investment analysis crew with LLM and tools"""
        self.setup_llm()
        self.setup_tools()
        self.create_agents()
        
    def setup_llm(self):
        """Setup LLM with fallback support"""
        try:
            # Primary LLM: Gemini 2.5 Flash
            self.primary_llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.7,
                max_output_tokens=8192
            )
            print("✅ Primary LLM: Gemini 2.5 Flash configured")
            
        except Exception as e:
            print(f"⚠️ Gemini 2.5 Flash failed: {e}")
            # Fallback to OpenAI/Groq
            self.primary_llm = ChatOpenAI(
                model="gpt-4",
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE"),
                temperature=0.7
            )
            print("✅ Fallback LLM: OpenAI/Groq configured")
    
    def setup_tools(self):
        """Initialize all custom tools"""
        self.tools = {
            'web_crawler': WebCrawlerTool(),
            'financial_data': FinancialDataTool(),
            'sentiment_analysis': SentimentAnalysisTool(),
            'valuation': ValuationTool(),
            'thesis_generation': ThesisGenerationTool(),
            'critique': CritiqueTool()
        }
        print("✅ All tools initialized")
    
    def create_agents(self):
        """Create specialized CrewAI agents"""
        
        # 🤖 Research Agent
        self.researcher = Agent(
            role="Financial Research Analyst",
            goal="Gather comprehensive financial data, news, and market information about the target company",
            backstory="""You are an expert financial research analyst with 15+ years of experience. 
            You specialize in gathering and analyzing financial data, market news, and company information. 
            You have access to web crawling tools and financial data APIs to collect comprehensive information.""",
            tools=[self.tools['web_crawler'], self.tools['financial_data']],
            llm=self.primary_llm,
            verbose=True,
            allow_delegation=False
        )
        
        # 🧠 Sentiment Agent
        self.sentiment_analyst = Agent(
            role="Market Sentiment Analyst",
            goal="Analyze market sentiment, investor mood, and public perception of the company",
            backstory="""You are a market psychology expert with deep understanding of investor behavior. 
            You analyze news sentiment, social media trends, and market reactions to understand 
            how investors feel about a company. You can identify bullish and bearish signals.""",
            tools=[self.tools['sentiment_analysis']],
            llm=self.primary_llm,
            verbose=True,
            allow_delegation=False
        )
        
        # 📊 Valuation Agent
        self.valuation_analyst = Agent(
            role="Financial Valuation Expert",
            goal="Perform comprehensive financial valuation using multiple methodologies",
            backstory="""You are a senior financial analyst specializing in company valuation. 
            You use DCF, comparable analysis, asset-based valuation, and other methodologies. 
            You have expertise in analyzing financial statements, ratios, and market metrics.""",
            tools=[self.tools['valuation'], self.tools['financial_data']],
            llm=self.primary_llm,
            verbose=True,
            allow_delegation=False
        )
        
        # ✍️ Thesis Writer Agent
        self.thesis_writer = Agent(
            role="Investment Thesis Writer",
            goal="Create professional, well-structured investment theses based on research and analysis",
            backstory="""You are an experienced investment analyst and writer. You create compelling 
            investment theses that clearly articulate investment opportunities, risks, and recommendations. 
            Your writing is professional, data-driven, and persuasive to institutional investors.""",
            tools=[self.tools['thesis_generation']],
            llm=self.primary_llm,
            verbose=True,
            allow_delegation=False
        )
        
        # 🔍 Critic Agent
        self.critic = Agent(
            role="Investment Thesis Critic",
            goal="Review investment theses for biases, gaps, and areas of improvement",
            backstory="""You are a senior investment analyst known for your critical thinking and 
            ability to identify weaknesses in investment arguments. You help improve theses by 
            pointing out biases, missing data, and logical flaws. You ensure theses are balanced and thorough.""",
            tools=[self.tools['critique']],
            llm=self.primary_llm,
            verbose=True,
            allow_delegation=False
        )
        
        print("✅ All agents created successfully")
    
    def create_tasks(self, company_name: str, urls: List[str] = None) -> List[Task]:
        """Create tasks for the investment analysis workflow"""
        
        tasks = [
            # Task 1: Research
            Task(
                description=f"""
                Research {company_name} thoroughly:
                1. Gather financial data (revenue, earnings, growth rates)
                2. Collect recent news and market updates
                3. Analyze competitive landscape
                4. Review management team and strategy
                5. Identify key risks and opportunities
                
                Use web crawling for news and financial data tools for company metrics.
                Provide comprehensive, well-organized research findings.
                """,
                agent=self.researcher,
                expected_output="Comprehensive research report with financial data, news analysis, and market insights"
            ),
            
            # Task 2: Sentiment Analysis
            Task(
                description=f"""
                Analyze market sentiment for {company_name}:
                1. Evaluate news sentiment (positive/negative/neutral)
                2. Assess social media and investor sentiment
                3. Analyze market reactions to recent events
                4. Identify sentiment trends and patterns
                5. Consider impact on stock price
                
                Use sentiment analysis tools to quantify market mood.
                Provide detailed sentiment analysis with supporting evidence.
                """,
                agent=self.sentiment_analyst,
                expected_output="Detailed sentiment analysis report with quantified sentiment scores and trend analysis"
            ),
            
            # Task 3: Valuation
            Task(
                description=f"""
                Perform comprehensive valuation of {company_name}:
                1. Calculate key financial ratios (P/E, P/B, ROE, etc.)
                2. Perform DCF analysis with reasonable assumptions
                3. Compare with industry peers
                4. Assess intrinsic value vs market price
                5. Identify valuation drivers and risks
                
                Use financial data tools and valuation methodologies.
                Provide detailed valuation analysis with price targets.
                """,
                agent=self.valuation_analyst,
                expected_output="Comprehensive valuation report with multiple methodologies and price targets"
            ),
            
            # Task 4: Thesis Generation
            Task(
                description=f"""
                Create an investment thesis for {company_name}:
                1. Synthesize research, sentiment, and valuation findings
                2. Articulate clear investment opportunity
                3. Identify key investment drivers
                4. Assess risks and mitigation strategies
                5. Provide actionable recommendations
                
                Structure the thesis professionally with clear sections.
                Make it compelling for institutional investors.
                """,
                agent=self.thesis_writer,
                expected_output="Professional investment thesis with clear structure, analysis, and recommendations"
            ),
            
            # Task 5: Critique and Improvement
            Task(
                description=f"""
                Review and improve the investment thesis for {company_name}:
                1. Identify potential biases and assumptions
                2. Check for missing data or analysis gaps
                3. Assess logical consistency and reasoning
                4. Suggest improvements and additional analysis
                5. Ensure balanced risk-reward assessment
                
                Provide constructive feedback to improve the thesis quality.
                """,
                agent=self.critic,
                expected_output="Detailed critique with specific improvements and enhanced thesis version"
            )
        ]
        
        return tasks
    
    def run_analysis(self, company_name: str, urls: List[str] = None) -> Dict[str, Any]:
        """
        🚀 Run the complete investment analysis using CrewAI
        
        Args:
            company_name: Name of the company to analyze
            urls: Optional list of URLs to crawl for research
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            print(f"🚀 Starting agentic analysis for: {company_name}")
            
            # Create tasks
            tasks = self.create_tasks(company_name, urls)
            
            # Create crew
            crew = Crew(
                agents=[
                    self.researcher,
                    self.sentiment_analyst,
                    self.valuation_analyst,
                    self.thesis_writer,
                    self.critic
                ],
                tasks=tasks,
                process=Process.sequential,  # Run tasks sequentially for investment analysis
                verbose=True
            )
            
            # Execute the crew
            print("🤖 Executing CrewAI workflow...")
            result = crew.kickoff()
            
            return {
                "company_name": company_name,
                "status": "success",
                "result": result,
                "agents_used": [
                    "Financial Research Analyst",
                    "Market Sentiment Analyst", 
                    "Financial Valuation Expert",
                    "Investment Thesis Writer",
                    "Investment Thesis Critic"
                ]
            }
            
        except Exception as e:
            print(f"❌ Error in agentic analysis: {e}")
            return {
                "company_name": company_name,
                "status": "error",
                "error": str(e),
                "result": None
            }

# Example usage
if __name__ == "__main__":
    # Test the crew
    crew = InvestmentAnalysisCrew()
    result = crew.run_analysis("Apple Inc.")
    print("Analysis completed!")
    print(result) 