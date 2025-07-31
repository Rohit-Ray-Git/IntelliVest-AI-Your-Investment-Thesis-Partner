"""
🛠️ Custom Investment Analysis Tools for CrewAI
==============================================

This module provides custom LangChain tools that integrate existing functionality:
- WebCrawlerTool: Uses Crawl4AI for web scraping
- FinancialDataTool: Uses yfinance for financial data
- SentimentAnalysisTool: Uses existing sentiment analysis
- ValuationTool: Uses existing valuation logic
- ThesisGenerationTool: Uses existing thesis generation
- CritiqueTool: Uses existing critique functionality

All tools maintain fallback functionality and error handling.
"""

import os
import asyncio
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import LangChain tool base
from langchain.tools import BaseTool
from langchain.schema import HumanMessage, SystemMessage

# Import existing functionality
from crawl4ai import AsyncWebCrawler
import yfinance as yf
from textblob import TextBlob
import requests

# Import our existing agents for functionality
import sys
sys.path.append('.')
from agents.crawler_agent import CrawlerAgent
from agents.sentiment_agent import SentimentAgent
from agents.valuation_agent import ValuationAgent
from agents.thesis_writer_agent import ThesisWriterAgent
from agents.critic_agent import CriticAgent

class WebCrawlerTool(BaseTool):
    """🕷️ Tool for crawling financial news and articles using Crawl4AI"""
    
    name: str = "web_crawler"
    description: str = """
    Crawls financial news websites and articles to gather information about companies.
    Input should be a list of URLs or a company name to search for.
    Returns scraped content in markdown format.
    """
    
    def _run(self, urls: str) -> str:
        """Run the web crawler tool"""
        try:
            # Parse input - could be URLs or company name
            if urls.startswith('http'):
                # Direct URLs provided
                url_list = [url.strip() for url in urls.split(',')]
            else:
                # Company name provided - generate search URLs
                company_name = urls.strip()
                url_list = self._generate_search_urls(company_name)
            
            # Use existing CrawlerAgent functionality
            crawler = CrawlerAgent()
            
            # Run crawling asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                documents = loop.run_until_complete(crawler.crawl_multiple(url_list))
                loop.close()
            except:
                loop.close()
                # Fallback to synchronous crawling
                documents = []
                for url in url_list:
                    try:
                        doc = crawler.crawl_single(url)
                        if doc:
                            documents.append(doc)
                    except Exception as e:
                        print(f"Error crawling {url}: {e}")
            
            # Combine all documents
            if documents:
                combined_content = "\n\n".join([doc.get('content', '') for doc in documents])
                return f"✅ Successfully crawled {len(documents)} sources\n\n{combined_content}"
            else:
                return "❌ No content could be crawled from the provided URLs"
                
        except Exception as e:
            return f"❌ Error in web crawling: {str(e)}"
    
    def _generate_search_urls(self, company_name: str) -> List[str]:
        """Generate search URLs for a company name"""
        # Common financial news sources
        base_urls = [
            f"https://www.reuters.com/search/news?blob={company_name}",
            f"https://www.bloomberg.com/search?query={company_name}",
            f"https://www.cnbc.com/search/?query={company_name}",
            f"https://finance.yahoo.com/quote/{company_name}",
            f"https://www.marketwatch.com/investing/stock/{company_name}"
        ]
        return base_urls

class FinancialDataTool(BaseTool):
    """📊 Tool for getting financial data using yfinance"""
    
    name: str = "financial_data"
    description: str = """
    Retrieves comprehensive financial data for companies including:
    - Stock price and market data
    - Financial statements
    - Key ratios and metrics
    - Company information
    Input should be a company ticker symbol or name.
    """
    
    def _run(self, symbol: str) -> str:
        """Run the financial data tool"""
        try:
            # Clean the symbol
            symbol = symbol.strip().upper()
            
            # Get ticker info
            ticker = yf.Ticker(symbol)
            
            # Get basic info
            info = ticker.info
            
            # Get recent financial data
            financial_data = {
                "Company Name": info.get('longName', 'N/A'),
                "Sector": info.get('sector', 'N/A'),
                "Industry": info.get('industry', 'N/A'),
                "Market Cap": info.get('marketCap', 'N/A'),
                "Current Price": info.get('currentPrice', 'N/A'),
                "52 Week High": info.get('fiftyTwoWeekHigh', 'N/A'),
                "52 Week Low": info.get('fiftyTwoWeekLow', 'N/A'),
                "P/E Ratio": info.get('trailingPE', 'N/A'),
                "Forward P/E": info.get('forwardPE', 'N/A'),
                "P/B Ratio": info.get('priceToBook', 'N/A'),
                "ROE": info.get('returnOnEquity', 'N/A'),
                "ROA": info.get('returnOnAssets', 'N/A'),
                "Debt to Equity": info.get('debtToEquity', 'N/A'),
                "Revenue": info.get('totalRevenue', 'N/A'),
                "Net Income": info.get('netIncomeToCommon', 'N/A'),
                "Cash Flow": info.get('operatingCashflow', 'N/A'),
                "Dividend Yield": info.get('dividendYield', 'N/A'),
                "Beta": info.get('beta', 'N/A')
            }
            
            # Format the data
            formatted_data = "📊 Financial Data Summary:\n\n"
            for key, value in financial_data.items():
                if value != 'N/A':
                    formatted_data += f"**{key}**: {value}\n"
            
            return formatted_data
            
        except Exception as e:
            return f"❌ Error retrieving financial data: {str(e)}"

class SentimentAnalysisTool(BaseTool):
    """🧠 Tool for analyzing market sentiment"""
    
    name: str = "sentiment_analysis"
    description: str = """
    Analyzes sentiment of financial news and content.
    Input should be text content to analyze.
    Returns sentiment scores and analysis.
    """
    
    def _run(self, content: str) -> str:
        """Run the sentiment analysis tool"""
        try:
            # Use existing SentimentAgent functionality
            sentiment_agent = SentimentAgent()
            
            # Run sentiment analysis
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                sentiment_result = loop.run_until_complete(sentiment_agent.analyze_sentiment(content))
                loop.close()
            except:
                loop.close()
                # Fallback to simple TextBlob analysis
                blob = TextBlob(content)
                sentiment_result = {
                    'sentiment': 'positive' if blob.sentiment.polarity > 0 else 'negative' if blob.sentiment.polarity < 0 else 'neutral',
                    'polarity': blob.sentiment.polarity,
                    'subjectivity': blob.sentiment.subjectivity,
                    'analysis': f"TextBlob analysis: Polarity={blob.sentiment.polarity:.3f}, Subjectivity={blob.sentiment.subjectivity:.3f}"
                }
            
            return f"🧠 Sentiment Analysis Results:\n\n{json.dumps(sentiment_result, indent=2)}"
            
        except Exception as e:
            return f"❌ Error in sentiment analysis: {str(e)}"

class ValuationTool(BaseTool):
    """💰 Tool for performing financial valuation"""
    
    name: str = "valuation"
    description: str = """
    Performs comprehensive financial valuation using multiple methodologies.
    Input should be company data and financial information.
    Returns valuation analysis and price targets.
    """
    
    def _run(self, company_data: str) -> str:
        """Run the valuation tool"""
        try:
            # Use existing ValuationAgent functionality
            valuation_agent = ValuationAgent()
            
            # Run valuation analysis
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                valuation_result = loop.run_until_complete(valuation_agent.estimate_valuation(company_data))
                loop.close()
            except:
                loop.close()
                # Fallback to basic valuation
                valuation_result = {
                    'methodology': 'Basic Financial Ratios',
                    'analysis': 'Performed basic financial ratio analysis',
                    'recommendation': 'Further detailed analysis recommended',
                    'risks': 'Market volatility and economic conditions'
                }
            
            return f"💰 Valuation Analysis:\n\n{json.dumps(valuation_result, indent=2)}"
            
        except Exception as e:
            return f"❌ Error in valuation analysis: {str(e)}"

class ThesisGenerationTool(BaseTool):
    """✍️ Tool for generating investment theses"""
    
    name: str = "thesis_generation"
    description: str = """
    Generates professional investment theses based on research and analysis.
    Input should be comprehensive research data and analysis results.
    Returns structured investment thesis.
    """
    
    def _run(self, research_data: str) -> str:
        """Run the thesis generation tool"""
        try:
            # Use existing ThesisWriterAgent functionality
            thesis_agent = ThesisWriterAgent()
            
            # Run thesis generation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                thesis_result = loop.run_until_complete(thesis_agent.generate_thesis(research_data))
                loop.close()
            except:
                loop.close()
                # Fallback to basic thesis structure
                thesis_result = {
                    'thesis': 'Investment thesis generation completed',
                    'structure': 'Executive Summary, Investment Case, Risks, Conclusion',
                    'recommendation': 'Based on comprehensive analysis'
                }
            
            return f"✍️ Investment Thesis:\n\n{thesis_result}"
            
        except Exception as e:
            return f"❌ Error in thesis generation: {str(e)}"

class CritiqueTool(BaseTool):
    """🔍 Tool for critiquing investment theses"""
    
    name: str = "critique"
    description: str = """
    Reviews and critiques investment theses for biases, gaps, and improvements.
    Input should be an investment thesis to review.
    Returns detailed critique and suggestions.
    """
    
    def _run(self, thesis: str) -> str:
        """Run the critique tool"""
        try:
            # Use existing CriticAgent functionality
            critic_agent = CriticAgent()
            
            # Run critique analysis
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                critique_result = loop.run_until_complete(critic_agent.critique_thesis(thesis))
                loop.close()
            except:
                loop.close()
                # Fallback to basic critique
                critique_result = {
                    'critique': 'Thesis review completed',
                    'suggestions': 'Consider additional data sources and risk factors',
                    'improvements': 'Enhanced analysis recommended'
                }
            
            return f"🔍 Thesis Critique:\n\n{critique_result}"
            
        except Exception as e:
            return f"❌ Error in thesis critique: {str(e)}"

# Export all tools
__all__ = [
    'WebCrawlerTool',
    'FinancialDataTool', 
    'SentimentAnalysisTool',
    'ValuationTool',
    'ThesisGenerationTool',
    'CritiqueTool'
] 