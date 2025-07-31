"""
🤖 Simplified CrewAI Agent Definitions for IntelliVest AI
========================================================

This module defines simplified CrewAI agents for investment analysis without custom tools.
We'll add tools in the next iteration once the basic agentic system is working.
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

class SimpleInvestmentAnalysisCrew:
    """
    🚀 Simplified CrewAI orchestration class for investment analysis
    """
    
    def __init__(self):
        """Initialize the investment analysis crew with LLM"""
        self.setup_llm()
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
    
    def create_agents(self):
        """Create specialized CrewAI agents without custom tools"""
        
        # 🤖 Research Agent
        self.researcher = Agent(
            role="Financial Research Analyst",
            goal="Gather comprehensive financial data, news, and market information about the target company",
            backstory="""You are an expert financial research analyst with 15+ years of experience. 
            You specialize in gathering and analyzing financial data, market news, and company information. 
            You have access to web crawling tools and financial data APIs to collect comprehensive information.
            You can provide detailed analysis of company financials, market position, and competitive landscape.""",
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
            You provide detailed sentiment analysis with quantified scores and trend analysis.""",
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
            You can calculate key ratios like P/E, P/B, ROE, and provide price targets.""",
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
            You structure theses with clear sections: Executive Summary, Investment Case, Risks, and Conclusion.""",
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
            You provide constructive feedback and suggest improvements.""",
            llm=self.primary_llm,
            verbose=True,
            allow_delegation=False
        )
        
        print("✅ All agents created successfully")
    
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
                
                Provide detailed, well-organized research findings with specific data points and insights.
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
                
                Provide quantified sentiment analysis with supporting evidence and trend analysis.
                """,
                agent=self.sentiment_analyst,
                expected_output="Detailed sentiment analysis report with quantified scores and trend analysis"
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
                   - Discounted Cash Flow (DCF) analysis
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
                expected_output="Comprehensive valuation report with multiple methodologies and price targets"
            ),
            
            # Task 4: Thesis Generation
            Task(
                description=f"""
                Create an investment thesis for {company_name}:
                
                1. Executive Summary:
                   - Investment recommendation (Buy/Hold/Sell)
                   - Key investment thesis in 2-3 sentences
                   - Expected return and time horizon
                
                2. Investment Case:
                   - Primary investment drivers
                   - Growth catalysts and opportunities
                   - Competitive advantages
                
                3. Financial Analysis:
                   - Key financial metrics and trends
                   - Valuation analysis and price targets
                   - Cash flow and capital allocation
                
                4. Risk Assessment:
                   - Key risks and mitigation strategies
                   - Downside scenarios
                   - Risk-reward analysis
                
                5. Conclusion:
                   - Investment recommendation
                   - Key factors to monitor
                   - Exit strategy considerations
                
                Structure the thesis professionally and make it compelling for institutional investors.
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
                
                2. Data Quality:
                   - Verify data sources and accuracy
                   - Check for missing or outdated information
                   - Assess completeness of analysis
                
                3. Logical Consistency:
                   - Review internal logic and reasoning
                   - Check for contradictions in the analysis
                   - Assess strength of conclusions
                
                4. Risk Assessment:
                   - Evaluate adequacy of risk analysis
                   - Identify additional risks not considered
                   - Assess risk mitigation strategies
                
                5. Improvements:
                   - Suggest specific improvements
                   - Recommend additional analysis needed
                   - Enhance the overall thesis quality
                
                Provide constructive feedback to improve the thesis quality and balance.
                """,
                agent=self.critic,
                expected_output="Detailed critique with specific improvements and enhanced thesis version"
            )
        ]
        
        return tasks
    
    def run_analysis(self, company_name: str) -> Dict[str, Any]:
        """
        🚀 Run the complete investment analysis using CrewAI
        
        Args:
            company_name: Name of the company to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            print(f"🚀 Starting agentic analysis for: {company_name}")
            
            # Create tasks
            tasks = self.create_tasks(company_name)
            
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
    crew = SimpleInvestmentAnalysisCrew()
    result = crew.run_analysis("Apple Inc.")
    print("Analysis completed!")
    print(result) 