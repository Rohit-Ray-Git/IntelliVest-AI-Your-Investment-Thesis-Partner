"""
🧪 Simple CrewAI Test
====================

Test CrewAI with minimal setup to debug tool issues.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.investment_tools import FinancialDataTool

# Load environment variables
load_dotenv()

def test_simple_crew():
    """Test CrewAI with a simple agent and tool"""
    
    print("🧪 Testing simple CrewAI setup...")
    
    # Setup LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )
    
    # Create a simple tool
    tool = FinancialDataTool()
    
    # Create a simple agent
    agent = Agent(
        role="Financial Analyst",
        goal="Get financial data for companies",
        backstory="You are a financial analyst who gets company data.",
        tools=[tool],
        llm=llm,
        verbose=True
    )
    
    # Create a simple task
    task = Task(
        description="Get financial data for Apple Inc.",
        agent=agent,
        expected_output="Financial data for Apple"
    )
    
    # Create crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    
    # Run
    result = crew.kickoff()
    print("Result:", result)

if __name__ == "__main__":
    test_simple_crew() 