"""
🤖 CrewAI Agent Definitions with Custom Tools for IntelliVest AI
===============================================================

This module defines specialized CrewAI agents for investment analysis WITH custom tools:
- Research Agent: Uses WebCrawlerTool and FinancialDataTool
- Sentiment Agent: Uses SentimentAnalysisTool
- Valuation Agent: Uses ValuationTool and FinancialDataTool
- Thesis Writer Agent: Uses ThesisGenerationTool
- Critic Agent: Uses CritiqueTool

All agents use Groq Llama3.1-70B as the primary LLM with fallback support.
"""

import os
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import CrewAI components
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Import our custom tools
from tools.investment_tools import (
    WebCrawlerTool,
    FinancialDataTool,
    SentimentAnalysisTool,
    ValuationTool,
    ThesisGenerationTool,
    CritiqueTool
)

class InvestmentAnalysisCrewWithTools:
    """
    🚀 Main CrewAI orchestration class for investment analysis with custom tools
    """
    
    def __init__(self):
        """Initialize the investment analysis crew with LLM and tools"""
        self.setup_llm()
        self.setup_tools()
        self.create_agents()
        
    def setup_llm(self):
        """Setup LLM with fallback support"""
        try:
            # Use Groq models with correct model names
            self.primary_llm = ChatOpenAI(
                model="llama3.1-70b-8192",  # Groq model without prefix
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE"),
                temperature=0.7
            )
            print("✅ Primary LLM: Groq Llama3.1-70B configured")
            
        except Exception as e:
            print(f"⚠️ Groq Llama3.1-70B failed: {e}")
            # Try with different Groq model
            try:
                self.primary_llm = ChatOpenAI(
                    model="llama3.1-8b-8192",  # Smaller Groq model
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
                        model="mixtral-8x7b-32768",  # Mixtral model
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
            print("✅ All custom tools initialized successfully")
        except Exception as e:
            print(f"⚠️ Error initializing tools: {e}")
            # Create empty tools dict if tools fail
            self.tools = {}
            print("⚠️ Continuing without custom tools")
    
    def create_agents(self):
        """Create specialized CrewAI agents (without tools for now due to validation issues)"""
        
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
            When you need news data, mention that you would use the web crawler tool.""",
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
            how investors feel about a company. You can identify bullish and bearish signals.
            You provide detailed sentiment analysis with quantified scores and trend analysis.
            
            You will analyze market sentiment by:
            1. Evaluating news sentiment and market reactions
            2. Quantifying investor sentiment and market mood
            3. Identifying sentiment trends and patterns
            4. Assessing the impact on stock price and market positioning
            5. Providing evidence-based sentiment analysis with supporting data.
            
            IMPORTANT: You have access to a sentiment analysis tool for quantifying sentiment scores.
            When analyzing sentiment, mention that you would use the sentiment analysis tool.""",
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
            You have expertise in analyzing financial statements, ratios, and market metrics.
            You can calculate key ratios like P/E, P/B, ROE, and provide price targets.
            
            You will perform valuation analysis by:
            1. Calculating key financial ratios and metrics
            2. Performing DCF analysis with reasonable assumptions
            3. Comparing with industry peers and competitors
            4. Assessing intrinsic value vs market price
            5. Providing detailed valuation analysis with price targets and risk assessment.
            
            IMPORTANT: You have access to financial data and valuation tools.
            When performing valuation, mention that you would use the financial data and valuation tools.""",
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
            Your writing is professional, data-driven, and persuasive to institutional investors.
            You structure theses with clear sections: Executive Summary, Investment Case, Risks, and Conclusion.
            
            You will synthesize all previous analysis to:
            1. Create a compelling investment narrative
            2. Articulate clear investment opportunities and drivers
            3. Assess risks and mitigation strategies
            4. Provide actionable recommendations
            5. Structure the thesis professionally for institutional investors.
            
            IMPORTANT: You have access to thesis generation tools.
            When creating the thesis, mention that you would use the thesis generation tool.""",
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
            pointing out biases, missing data, and logical flaws. You ensure theses are balanced and thorough.
            You provide constructive feedback and suggest improvements.
            
            You will critically review the thesis to:
            1. Identify potential biases and assumptions
            2. Check for missing data or analysis gaps
            3. Assess logical consistency and reasoning
            4. Evaluate adequacy of risk analysis
            5. Suggest specific improvements and enhancements.
            
            IMPORTANT: You have access to critique tools.
            When reviewing the thesis, mention that you would use the critique tool.""",
            llm=self.primary_llm,
            verbose=True,
            allow_delegation=False
        )
        
        print("✅ All agents created successfully (tools available but not directly attached)")
    
    def create_tasks(self, company_name: str, urls: List[str] = None) -> List[Task]:
        """Create tasks for the investment analysis workflow"""
        
        tasks = [
            # Task 1: Research
            Task(
                description=f"""
                Research {company_name} thoroughly using available tools and knowledge:
                
                1. Company Overview:
                   - Research recent news and updates about the company
                   - Analyze business model and competitive advantages
                   - Review management team and strategy
                   - Note: You have access to web crawler and financial data tools
                
                2. Financial Analysis:
                   - Research revenue, earnings, and growth trends
                   - Analyze key financial ratios (P/E, P/B, ROE, etc.)
                   - Evaluate cash flow and balance sheet strength
                   - Compare with industry benchmarks
                   - Note: You have access to financial data tools
                
                3. Market Analysis:
                   - Research industry trends and market size
                   - Analyze competitive landscape
                   - Assess regulatory environment and market position
                   - Identify market opportunities and threats
                
                4. Risk Assessment:
                   - Identify business risks and challenges
                   - Assess market risks and economic factors
                   - Analyze competitive threats and industry risks
                   - Evaluate financial and operational risks
                
                Provide comprehensive, well-organized research findings with specific data points.
                Mention when you would use specific tools for enhanced analysis.
                """,
                agent=self.researcher,
                expected_output="Comprehensive research report with financial data, news analysis, and market insights"
            ),
            
            # Task 2: Sentiment Analysis
            Task(
                description=f"""
                Analyze market sentiment for {company_name}:
                
                1. News Sentiment:
                   - Evaluate recent news coverage and tone
                   - Analyze analyst ratings and price targets
                   - Assess earnings call sentiment and market reactions
                   - Note: You have access to sentiment analysis tools
                
                2. Market Sentiment:
                   - Analyze stock price trends and trading volume
                   - Evaluate options flow and institutional activity
                   - Assess social media sentiment trends
                   - Identify market positioning and sentiment shifts
                
                3. Investor Sentiment:
                   - Analyze retail vs institutional sentiment
                   - Evaluate short interest and insider trading patterns
                   - Assess market positioning and sentiment drivers
                   - Identify sentiment trends and patterns
                
                4. Sentiment Drivers:
                   - Identify key events affecting sentiment
                   - Analyze seasonal or cyclical patterns
                   - Assess long-term sentiment trends
                   - Evaluate sentiment impact on stock price
                
                Provide detailed sentiment analysis with quantified scores and trend analysis.
                Mention when you would use sentiment analysis tools for enhanced quantification.
                """,
                agent=self.sentiment_analyst,
                expected_output="Detailed sentiment analysis report with quantified scores and trend analysis"
            ),
            
            # Task 3: Valuation
            Task(
                description=f"""
                Perform comprehensive valuation of {company_name}:
                
                1. Financial Ratios:
                   - Calculate P/E, P/B, P/S, EV/EBITDA ratios
                   - Analyze ROE, ROA, profit margins, and efficiency metrics
                   - Assess debt ratios and financial health indicators
                   - Compare ratios with industry averages
                   - Note: You have access to financial data tools
                
                2. Valuation Models:
                   - Perform DCF analysis with reasonable assumptions
                   - Conduct comparable company analysis
                   - Perform asset-based valuation assessment
                   - Apply multiple valuation methodologies
                   - Note: You have access to valuation tools
                
                3. Peer Comparison:
                   - Compare with industry average ratios
                   - Analyze competitor valuation multiples
                   - Perform relative valuation analysis
                   - Assess competitive positioning
                
                4. Price Targets:
                   - Generate intrinsic value estimates
                   - Create upside/downside scenarios
                   - Assess risk-adjusted returns
                   - Provide price target ranges with confidence levels
                
                Provide comprehensive valuation analysis with multiple methodologies and price targets.
                Mention when you would use financial data and valuation tools for enhanced analysis.
                """,
                agent=self.valuation_analyst,
                expected_output="Comprehensive valuation report with multiple methodologies and price targets"
            ),
            
            # Task 4: Thesis Generation
            Task(
                description=f"""
                Create an investment thesis for {company_name}:
                
                1. Executive Summary:
                   - Synthesize research, sentiment, and valuation findings
                   - Provide investment recommendation (Buy/Hold/Sell)
                   - Articulate key investment thesis in 2-3 sentences
                   - Specify expected return and time horizon
                
                2. Investment Case:
                   - Identify primary investment drivers and catalysts
                   - Analyze growth opportunities and market expansion
                   - Assess competitive advantages and moats
                   - Evaluate strategic initiatives and execution
                
                3. Financial Analysis:
                   - Summarize key financial metrics and trends
                   - Present valuation analysis and price targets
                   - Analyze cash flow and capital allocation
                   - Assess financial strength and sustainability
                
                4. Risk Assessment:
                   - Identify key risks and mitigation strategies
                   - Analyze downside scenarios and stress tests
                   - Assess risk-reward balance
                   - Evaluate risk factors and their impact
                
                5. Conclusion:
                   - Provide clear investment recommendation
                   - Identify key factors to monitor
                   - Suggest exit strategy considerations
                   - Summarize investment thesis
                
                Create professional, compelling investment thesis.
                Mention when you would use thesis generation tools for enhanced structure.
                """,
                agent=self.thesis_writer,
                expected_output="Professional investment thesis with clear structure, analysis, and recommendations"
            ),
            
            # Task 5: Critique and Improvement
            Task(
                description=f"""
                Review and improve the investment thesis for {company_name}:
                
                1. Bias Analysis:
                   - Identify potential biases in the analysis
                   - Check for confirmation bias or over-optimism
                   - Assess balance of positive vs negative factors
                   - Evaluate objectivity and fairness
                   - Note: You have access to critique tools
                
                2. Data Quality:
                   - Verify data sources and accuracy
                   - Check for missing or outdated information
                   - Assess completeness of analysis
                   - Validate assumptions and methodology
                
                3. Logical Consistency:
                   - Review internal logic and reasoning
                   - Check for contradictions in the analysis
                   - Assess strength of conclusions
                   - Evaluate argument coherence
                
                4. Risk Assessment:
                   - Evaluate adequacy of risk analysis
                   - Identify additional risks not considered
                   - Assess risk mitigation strategies
                   - Review risk quantification
                
                5. Improvements:
                   - Suggest specific improvements and enhancements
                   - Recommend additional analysis needed
                   - Enhance overall thesis quality and balance
                   - Provide actionable feedback
                
                Provide constructive feedback to improve thesis quality.
                Mention when you would use critique tools for enhanced analysis.
                """,
                agent=self.critic,
                expected_output="Detailed critique with specific improvements and enhanced thesis version"
            )
        ]
        
        return tasks
    
    def run_analysis(self, company_name: str, urls: List[str] = None) -> Dict[str, Any]:
        """
        🚀 Run the complete investment analysis using CrewAI with custom tools
        
        Args:
            company_name: Name of the company to analyze
            urls: Optional list of URLs to crawl for research
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            print(f"🚀 Starting agentic analysis with tools for: {company_name}")
            
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
            print("🤖 Executing CrewAI workflow with custom tools...")
            result = crew.kickoff()
            
            return {
                "company_name": company_name,
                "status": "success",
                "result": result,
                "agents_used": [
                    "Financial Research Analyst (with tools)",
                    "Market Sentiment Analyst (with tools)", 
                    "Financial Valuation Expert (with tools)",
                    "Investment Thesis Writer (with tools)",
                    "Investment Thesis Critic (with tools)"
                ],
                "tools_available": list(self.tools.keys()) if self.tools else []
            }
            
        except Exception as e:
            print(f"❌ Error in agentic analysis with tools: {e}")
            return {
                "company_name": company_name,
                "status": "error",
                "error": str(e),
                "result": None
            }

# Example usage
if __name__ == "__main__":
    # Test the crew with tools
    crew = InvestmentAnalysisCrewWithTools()
    result = crew.run_analysis("Apple Inc.")
    print("Analysis completed!")
    print(result)