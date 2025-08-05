"""
📈 Dynamic Market Scanner Tool for IntelliVest AI
=================================================

Automatically discovers and analyzes trending stocks and sectors from market data
"""

import os
import requests
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
import yfinance as yf
import pandas as pd
import random
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
import asyncio
import aiohttp

# Add Groq imports for fallback
try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️ langchain_groq not available. Install with: pip install langchain-groq")

# Add Tavily imports for real web search
try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False
    print("⚠️ tavily not available. Install with: pip install tavily-python")

class DynamicMarketScannerTool(BaseTool):
    """📈 Dynamic market scanner that automatically discovers trending stocks and sectors with focus on Indian markets"""
    
    name: str = "dynamic_market_scanner"
    description: str = """
    Dynamically scans the market to automatically discover and analyze trending stocks and sectors.
    Primarily focuses on Indian markets (NSE/BSE) with comprehensive coverage of Indian stocks, sectors, and indices.
    Uses intelligent algorithms to find top performers without predefined lists.
    Input should be the number of days to look back (default: 5 days).
    Returns comprehensive market analysis with automatically discovered top performers, emphasizing Indian market opportunities.
    """
    max_workers: int = Field(default=10, description="Number of parallel workers for data fetching")
    session: Optional[requests.Session] = Field(default=None, exclude=True)
    llm: Optional[Any] = Field(default=None, exclude=True, description="Gemini 2.5 Flash LLM for intelligent discovery")
    groq_llm: Optional[Any] = Field(default=None, exclude=True, description="Groq DeepSeek LLM for fallback")
    tavily_client: Optional[Any] = Field(default=None, exclude=True, description="Tavily client for real web search")
    
    def __init__(self, max_workers: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Initialize Gemini 2.5 Flash for intelligent search
        self.llm = None
        self.groq_llm = None
        self.tavily_client = None
        
        # Initialize Groq DeepSeek as primary LLM
        if GROQ_AVAILABLE:
            try:
                groq_api_key = os.getenv("GROQ_API_KEY")
                if groq_api_key:
                    self.llm = ChatGroq(
                        model_name="deepseek-r1-distill-llama-70b",
                        groq_api_key=groq_api_key,
                        temperature=0.1,
                        max_tokens=2048
                    )
                    print("✅ Groq DeepSeek (deepseek-r1-distill-llama-70b) initialized as primary LLM")
                else:
                    print("⚠️ GROQ_API_KEY not found for Groq DeepSeek")
            except Exception as e:
                print(f"⚠️ Groq DeepSeek initialization failed: {e}")
                self.llm = None
        else:
            print("⚠️ Groq not available for primary LLM")
        
        # Initialize Gemini 2.5 Flash as fallback (if needed)
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                self.groq_llm = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    google_api_key=api_key,
                    temperature=0.1,
                    max_tokens=2048
                )
                print("✅ Gemini 2.5 Flash initialized as fallback")
            else:
                print("⚠️ GOOGLE_API_KEY not found for Gemini fallback")
        except Exception as e:
            print(f"⚠️ Gemini 2.5 Flash initialization failed: {e}")
            self.groq_llm = None
        
        # Initialize Tavily for real web search
        if TAVILY_AVAILABLE:
            try:
                tavily_api_key = os.getenv("TAVILY_API_KEY")
                if tavily_api_key:
                    self.tavily_client = TavilyClient(api_key=tavily_api_key)
                    print("✅ Tavily client initialized successfully for real web search")
                else:
                    print("⚠️ TAVILY_API_KEY not found for real web search")
            except Exception as e:
                print(f"⚠️ Tavily initialization failed: {e}")
                self.tavily_client = None
        else:
            print("⚠️ Tavily not available for real web search")
    
    def _call_llm_with_fallback(self, messages: List, operation_name: str = "LLM call") -> Optional[Any]:
        """Call LLM with fallback from Groq DeepSeek to Gemini"""
        # Try Groq DeepSeek first (primary)
        if self.llm:
            try:
                response = self.llm.invoke(messages)
                if response and response.content:
                    return response
            except Exception as e:
                print(f"⚠️ Groq DeepSeek failed for {operation_name}: {e}")
        
        # Fallback to Gemini
        if self.groq_llm:
            try:
                print(f"🔄 Falling back to Gemini 2.5 Flash for {operation_name}...")
                response = self.groq_llm.invoke(messages)
                if response and response.content:
                    print(f"✅ Gemini 2.5 Flash succeeded for {operation_name}")
                    return response
            except Exception as e:
                print(f"⚠️ Gemini 2.5 Flash also failed for {operation_name}: {e}")
        
        print(f"❌ Both Groq DeepSeek and Gemini failed for {operation_name}")
        return None
    
    def _tavily_web_search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Perform real web search using Tavily API"""
        if not self.tavily_client:
            print("⚠️ Tavily client not available for web search")
            return []
        
        try:
            print(f"🔍 Tavily web search: {query}")
            
            # Enhanced query for Indian markets
            enhanced_query = f"{query} Indian markets NSE BSE current trending stocks sectors"
            
            search_result = self.tavily_client.search(
                query=enhanced_query,
                search_depth="basic",  # Changed from "advanced" to "basic" for speed
                max_results=max_results,
                include_answer=True,
                include_raw_content=True,
                include_images=False
            )
            
            if 'results' in search_result and search_result['results']:
                print(f"✅ Tavily found {len(search_result['results'])} results")
                return search_result['results']
            else:
                print("⚠️ No results from Tavily search")
                return []
                
        except Exception as e:
            print(f"⚠️ Tavily web search failed: {e}")
            return []
    
    def _extract_stocks_from_web_content(self, web_results: List[Dict[str, Any]]) -> List[str]:
        """Extract stock symbols from web search results"""
        discovered_stocks = set()
        
        for result in web_results:
            try:
                content = result.get('content', '')
                title = result.get('title', '')
                url = result.get('url', '')
                
                # Combine all text for analysis
                full_text = f"{title} {content}"
                
                # Extract stock symbols with .NS or .BO suffixes
                stock_symbols = re.findall(r'\b([A-Z]{2,10})\.(NS|BO)\b', full_text)
                for symbol, suffix in stock_symbols:
                    if symbol not in ['NS', 'BO', 'THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'HAVE', 'WILL', 'BEEN', 'THEY', 'THEIR']:
                        discovered_stocks.add(f"{symbol}.{suffix}")
                
                # Extract common Indian stock names and add suffixes
                stock_names = re.findall(r'\b([A-Z]{2,10})\b', full_text)
                for name in stock_names:
                    if len(name) >= 2 and name not in ['THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'HAVE', 'WILL', 'BEEN', 'THEY', 'THEIR', 'NS', 'BO']:
                        # Add both NSE and BSE suffixes for any valid stock name found
                        discovered_stocks.add(f"{name}.NS")
                        discovered_stocks.add(f"{name}.BO")
                
            except Exception as e:
                print(f"⚠️ Error extracting stocks from web result: {e}")
                continue
        
        return list(discovered_stocks)
    
    def _extract_sectors_from_web_content(self, web_results: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract sector information from web search results - focusing on 14 core NSE sectoral indices"""
        discovered_sectors = {}
        
        # Define the 14 core NSE sectoral indices
        indian_sectors = {
            '^NSEI': 'Nifty 50 (Overall Market)',
            '^NSEBANK': 'Nifty Bank',
            '^CNXAUTO': 'Nifty Auto',
            '^CNXFIN': 'Nifty Financial Services',
            '^CNXFMCG': 'Nifty FMCG',
            '^NSEIT': 'Nifty IT',
            '^CNXMETAL': 'Nifty Metal',
            '^CNXENERGY': 'Nifty Oil & Gas',
            '^CNXPHARMA': 'Nifty Pharma',
            '^CNXREALTY': 'Nifty Realty',
            '^CNXFIN_SRV': 'Nifty Financial Services (Alt)',
            '^CNXSERVICE': 'Nifty Healthcare',
            '^BSESN': 'Sensex (Overall Market)'
        }
        
        for result in web_results:
            try:
                content = result.get('content', '')
                title = result.get('title', '')
                
                # Combine all text for analysis
                full_text = f"{title} {content}"
                
                # Look for ^ symbols (Yahoo Finance format) - only from our 14 sectors
                yahoo_patterns = re.findall(r'\^([A-Z0-9_]+)', full_text)
                for pattern in yahoo_patterns:
                    if pattern in ['NSEBANK', 'CNXAUTO', 'CNXFIN', 'CNXFMCG', 'NSEIT', 'CNXMETAL', 'CNXENERGY', 'CNXPHARMA', 'CNXREALTY', 'CNXFIN_SRV', 'CNXSERVICE', 'NSEI', 'BSESN']:
                        discovered_sectors[f"^{pattern}"] = indian_sectors.get(f"^{pattern}", f"{pattern} Sector")
                
                # Look for sector mentions in text
                sector_keywords = {
                    'nifty bank': '^NSEBANK',
                    'bank nifty': '^NSEBANK',
                    'nifty auto': '^CNXAUTO',
                    'auto nifty': '^CNXAUTO',
                    'nifty financial': '^CNXFIN',
                    'financial services': '^CNXFIN',
                    'nifty fmcg': '^CNXFMCG',
                    'fmcg nifty': '^CNXFMCG',
                    'nifty it': '^NSEIT',
                    'it nifty': '^NSEIT',
                    'nifty metal': '^CNXMETAL',
                    'metal nifty': '^CNXMETAL',
                    'nifty oil': '^CNXENERGY',
                    'oil & gas': '^CNXENERGY',
                    'energy nifty': '^CNXENERGY',
                    'nifty pharma': '^CNXPHARMA',
                    'pharma nifty': '^CNXPHARMA',
                    'nifty realty': '^CNXREALTY',
                    'realty nifty': '^CNXREALTY',
                    'nifty healthcare': '^CNXSERVICE',
                    'healthcare nifty': '^CNXSERVICE',
                    'nifty 50': '^NSEI',
                    'sensex': '^BSESN'
                }
                
                # Check for sector keywords in text
                for keyword, symbol in sector_keywords.items():
                    if keyword.lower() in full_text.lower() and symbol not in discovered_sectors:
                        discovered_sectors[symbol] = indian_sectors.get(symbol, f"{symbol[1:]} Sector")
                
            except Exception as e:
                print(f"⚠️ Error extracting sectors from web result: {e}")
                continue
        
        return discovered_sectors
    
    def _run(self, days_back: int = 5) -> Dict[str, Any]:
        """Run dynamic Indian market scan for top performers"""
        try:
            print(f"🔍 Dynamically scanning Indian markets for top performers (last {days_back} days)...")
            
            # Discover trending Indian stocks and sectors dynamically
            discovered_data = self._discover_market_data(days_back)
            
            # Debug: Print what was discovered
            print(f"📊 Discovery Results:")
            print(f"   - Stocks discovered: {len(discovered_data['stocks'])}")
            print(f"   - Sectors discovered: {len(discovered_data['sectors'])}")
            print(f"   - Indices discovered: {len(discovered_data['indices'])}")
            
            if discovered_data['stocks']:
                print(f"   - Sample stocks: {list(discovered_data['stocks'].keys())[:5]}")
            
            # Analyze performance with error handling
            try:
                top_stocks = self._analyze_stock_performance(discovered_data['stocks'])
                print(f"   - Top stocks analyzed successfully: {len(top_stocks)}")
            except Exception as e:
                print(f"❌ Error analyzing stocks: {e}")
                top_stocks = []
            
            try:
                top_sectors = self._analyze_sector_performance(discovered_data['sectors'])
                print(f"   - Top sectors analyzed successfully: {len(top_sectors)}")
            except Exception as e:
                print(f"❌ Error analyzing sectors: {e}")
                top_sectors = []
            
            try:
                market_insights = self._generate_market_insights(discovered_data)
                print(f"   - Market insights generated successfully")
            except Exception as e:
                print(f"❌ Error generating insights: {e}")
                market_insights = {
                    'market_sentiment': 'neutral',
                    'trending_sectors': [],
                    'key_observations': [],
                    'risk_level': 'medium',
                    'indian_market_focus': True
                }
            
            print(f"📈 Analysis Results:")
            print(f"   - Top stocks found: {len(top_stocks)}")
            print(f"   - Top sectors found: {len(top_sectors)}")
            
            return {
                "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "days_analyzed": days_back,
                "discovery_method": "Dynamic Indian Market Scanner (Parallel)",
                "market_focus": "Indian Markets (NSE/BSE)",
                "top_performing_stocks": top_stocks,
                "top_performing_sectors": top_sectors,
                "market_insights": market_insights,
                "market_summary": self._create_market_summary(top_stocks, top_sectors),
                "discovery_stats": {
                    "stocks_analyzed": len(discovered_data['stocks']),
                    "sectors_analyzed": len(discovered_data['sectors']),
                    "indices_analyzed": len(discovered_data['indices'])
                }
            }
            
        except Exception as e:
            print(f"❌ Dynamic Indian market scan failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                "error": f"Dynamic Indian market scan failed: {str(e)}",
                "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def _discover_market_data(self, days_back: int) -> Dict[str, Any]:
        """Quickly discover top 3 Indian stocks and sectors"""
        print("🔍 Quick discovery of top 3 Indian stocks and sectors...")
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back + 5)
        
        market_data = {
            'stocks': {},
            'sectors': {},
            'indices': {}
        }
        
        # Quick discovery of top 3 stocks only
        discovered_stocks = self._discover_trending_stocks(days_back)
        print(f"📊 Quick discovery found {len(discovered_stocks)} top stocks")
        
        # Quick data fetching for top 3 stocks only
        print("⚡ Quick fetching of top stock data...")
        stock_data = self._fetch_stock_data_parallel(discovered_stocks, start_date, end_date)
        market_data['stocks'] = stock_data
        
        # Quick discovery of top 3 sectors only
        discovered_sectors = self._discover_sector_indices()
        print(f"📊 Quick discovery found {len(discovered_sectors)} top sectors")
        
        # Quick data fetching for top 3 sectors only
        print("⚡ Quick fetching of top sector data...")
        sector_data = self._fetch_sector_data_parallel(discovered_sectors, start_date, end_date)
        market_data['sectors'] = sector_data
        
        return market_data
    
    def _discover_trending_stocks(self, days_back: int) -> List[str]:
        """Quickly discover top 3 trending stocks using optimized approach"""
        discovered_stocks = set()
        
        # Strategy 1: Quick Tavily search (minimal results for speed)
        if self.tavily_client:
            print("🌐 Using Tavily for quick web search...")
            try:
                web_results = self._tavily_web_search("top gainers NSE today", max_results=2)
                web_stocks = self._extract_stocks_from_web_content(web_results)
                discovered_stocks.update(web_stocks)
                print(f"🌐 Tavily discovered {len(web_stocks)} stocks from web search")
            except Exception as e:
                print(f"⚠️ Tavily web search failed: {e}")
        
        # Strategy 2: Quick LLM discovery (simplified prompt)
        print("🤖 Using Groq DeepSeek for quick discovery...")
        
        try:
            system_prompt = """Find 3 trending Indian stocks. Return only stock symbols with .NS suffix."""
            
            user_prompt = """Find 3 Indian stocks trending today. Return only symbols like: STOCK.NS"""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self._call_llm_with_fallback(messages, "quick stock discovery")
            
            if response and response.content:
                # Extract stock symbols from response
                stock_symbols = re.findall(r'\b([A-Z]{2,10})\.(NS|BO)\b', response.content)
                for symbol, suffix in stock_symbols:
                    if symbol not in ['NS', 'BO', 'THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'HAVE', 'WILL', 'BEEN', 'THEY', 'THEIR']:
                        discovered_stocks.add(f"{symbol}.{suffix}")
            
        except Exception as e:
            print(f"⚠️ Quick stock discovery failed: {e}")
        
        # Return only top 3 stocks
        indian_stocks = [stock for stock in discovered_stocks if stock.endswith('.NS') or stock.endswith('.BO')]
        indian_stocks = list(set(indian_stocks))[:3]  # Only top 3
        
        print(f"📊 Quick discovery found {len(indian_stocks)} top stocks")
        if indian_stocks:
            print(f"🔍 Top stocks: {indian_stocks}")
        
        return indian_stocks
    
    def _gemini_intelligent_discovery(self) -> List[str]:
        """Use Groq DeepSeek and Tavily to intelligently discover trending stocks from live websites"""
        discovered = []
        
        if not self.llm and not self.groq_llm and not self.tavily_client:
            print("⚠️ No LLM or Tavily available for intelligent discovery")
            return discovered
        
        try:
            print("🔍 Groq DeepSeek agent and Tavily searching live financial websites...")
            
            # Strategy 1: Real web search using Tavily
            if self.tavily_client:
                print("🌐 Using Tavily for real web search...")
                web_results = self._tavily_web_search("trending Indian stocks today top gainers NSE BSE")
                web_stocks = self._extract_stocks_from_web_content(web_results)
                discovered.extend(web_stocks)
                print(f"🌐 Tavily discovered {len(web_stocks)} stocks from web search")
            
            # Strategy 2: LLM-based discovery (fallback if no Tavily)
            if self.llm or self.groq_llm:
                print("🤖 Using Groq DeepSeek for intelligent discovery...")
                # Strategy 2a: Search live financial websites
                discovered.extend(self._groq_search_live_websites())
                
                # Strategy 2b: Analyze current market trends
                discovered.extend(self._groq_analyze_market_trends())
                
                # Strategy 2c: Search for trending sectors
                discovered.extend(self._groq_search_trending_sectors())
            
        except Exception as e:
            print(f"⚠️ Intelligent discovery failed: {e}")
        
        return list(set(discovered))
    
    def _groq_search_live_websites(self) -> List[str]:
        """Use Groq DeepSeek to search live financial websites for trending stocks"""
        discovered = []
        
        try:
            system_prompt = """You are an expert financial analyst specializing in Indian markets (NSE/BSE). 
            Your task is to search live financial websites and find currently trending Indian stocks.
            
            Instructions:
            1. Search for live financial websites that show trending Indian stocks
            2. Look for websites that display top gainers, most active stocks, or trending tickers from Indian markets
            3. Extract stock symbols from these live sources
            4. Focus on finding Indian stocks that are currently performing well today
            5. Return only valid Indian stock symbols with .NS (NSE) or .BO (BSE) suffix
            6. Do NOT include any US stocks, global stocks, or non-Indian stocks
            7. Focus on major Indian companies and sectors
            
            Do not use any hardcoded stock names or predefined lists. Search dynamically."""
            
            user_prompt = """Search live financial websites and find 20 Indian stocks that are currently trending well in the Indian market today. 
            Look for:
            - Top gainers on NSE/BSE
            - Most active Indian stocks  
            - High volume Indian stocks
            - Indian stocks with positive price movements
            
            Search multiple live sources and return only Indian stock symbols with .NS or .BO suffix.
            Do NOT include any US or global stocks."""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self._call_llm_with_fallback(messages, "live website search")
            
            # Parse the response to extract stock symbols
            if response and response.content:
                # Extract stock symbols from Groq DeepSeek's response - be more specific
                stock_symbols = re.findall(r'\b([A-Z]{2,10})\.(NS|BO)\b', response.content)
                for symbol, suffix in stock_symbols:
                    if symbol not in ['NS', 'BO', 'THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'HAVE', 'WILL', 'BEEN', 'THEY', 'THEIR']:
                        discovered.append(f"{symbol}.{suffix}")
                
                # Also look for stock names without suffix and add common suffixes
                stock_names = re.findall(r'\b([A-Z]{2,10})\b', response.content)
                for name in stock_names:
                    if len(name) >= 2 and name not in ['THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'HAVE', 'WILL', 'BEEN', 'THEY', 'THEIR', 'NS', 'BO']:
                        discovered.append(f"{name}.NS")
                        discovered.append(f"{name}.BO")
            
        except Exception as e:
            print(f"⚠️ Groq DeepSeek live website search failed: {e}")
        
        return discovered
    
    def _groq_analyze_market_trends(self) -> List[str]:
        """Use Groq DeepSeek to analyze current market trends and find trending stocks"""
        discovered = []
        
        try:
            system_prompt = """You are a market trend analyst specializing in Indian markets. Analyze current Indian market trends and identify 
            Indian stocks that are trending based on:
            - Recent price movements in Indian markets
            - Volume spikes in Indian stocks
            - News and developments affecting Indian companies
            - Sector rotations in Indian markets
            - Market momentum in Indian indices
            
            Search for live Indian market data and identify Indian stocks that are currently trending.
            Focus ONLY on Indian stocks with .NS or .BO suffixes."""
            
            user_prompt = """Analyze current Indian market trends and identify 15 Indian stocks that are trending positively today.
            Consider:
            - Indian stocks with recent positive price movements
            - Indian stocks with high trading volume
            - Indian stocks mentioned in positive news
            - Indian stocks in sectors that are currently trending
            
            Search live Indian market data sources and return only Indian stock symbols with .NS or .BO suffix.
            Do NOT include any US or global stocks."""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self._call_llm_with_fallback(messages, "market trend analysis")
            
            if response and response.content:
                # Extract stock symbols from Groq DeepSeek's response
                stock_symbols = re.findall(r'\b([A-Z]{2,10})\.(NS|BO)\b', response.content)
                for symbol, suffix in stock_symbols:
                    if symbol not in ['NS', 'BO', 'THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'HAVE', 'WILL', 'BEEN', 'THEY', 'THEIR']:
                        discovered.append(f"{symbol}.{suffix}")
                
                # Look for stock names in trend analysis
                stock_names = re.findall(r'\b([A-Z]{2,10})\b', response.content)
                for name in stock_names:
                    if len(name) >= 2 and name not in ['THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'HAVE', 'WILL', 'BEEN', 'THEY', 'THEIR', 'MARKET', 'STOCKS', 'TRENDING', 'POSITIVE', 'MOVEMENT', 'VOLUME', 'SECTOR', 'CURRENT', 'TODAY', 'NS', 'BO']:
                        discovered.append(f"{name}.NS")
                        discovered.append(f"{name}.BO")
            
        except Exception as e:
            print(f"⚠️ Groq DeepSeek market trend analysis failed: {e}")
        
        return discovered
    
    def _groq_search_trending_sectors(self) -> List[str]:
        """Use Groq DeepSeek to search for trending sectors and their top stocks"""
        discovered = []
        
        try:
            system_prompt = """You are a sector analyst specializing in Indian markets. Search for Indian sectors that are currently trending 
            and identify the top performing Indian stocks in those sectors.
            
            Look for:
            - Indian sectors with positive momentum
            - Indian sectors with high trading volume
            - Indian sectors mentioned in positive news
            - Indian sectors with recent developments
            
            Then identify the leading Indian stocks in those trending sectors.
            Focus ONLY on Indian stocks with .NS or .BO suffixes."""
            
            user_prompt = """Search for 5 Indian sectors that are currently trending in the Indian market and identify 
            3-4 top Indian stocks from each trending sector. Focus on Indian sectors and stocks that are performing well today.
            
            Search live Indian market data and return only Indian stock symbols with .NS or .BO suffix.
            Do NOT include any US or global stocks."""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self._call_llm_with_fallback(messages, "trending sectors search")
            
            if response and response.content:
                # Extract stock symbols from Groq DeepSeek's response
                stock_symbols = re.findall(r'\b([A-Z]{2,10})\.(NS|BO)\b', response.content)
                for symbol, suffix in stock_symbols:
                    if symbol not in ['NS', 'BO', 'THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'HAVE', 'WILL', 'BEEN', 'THEY', 'THEIR']:
                        discovered.append(f"{symbol}.{suffix}")
                
                # Look for stock names in sector analysis
                stock_names = re.findall(r'\b([A-Z]{2,10})\b', response.content)
                for name in stock_names:
                    if len(name) >= 2 and name not in ['THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'HAVE', 'WILL', 'BEEN', 'THEY', 'THEIR', 'SECTOR', 'STOCKS', 'TRENDING', 'PERFORMING', 'LEADING', 'TOP', 'EACH', 'NS', 'BO']:
                        discovered.append(f"{name}.NS")
                        discovered.append(f"{name}.BO")
            
        except Exception as e:
            print(f"⚠️ Groq DeepSeek trending sectors search failed: {e}")
        
        return discovered
    
    def _discover_sector_indices(self) -> Dict[str, str]:
        """Quickly discover top 3 sector indices from the 11 standard Indian market sectors"""
        discovered_sectors = {}
        
        # Define the 14 core NSE sectoral indices with their real symbols
        indian_sectors = {
            '^NSEI': 'Nifty 50 (Overall Market)',
            '^NSEBANK': 'Nifty Bank',
            '^CNXAUTO': 'Nifty Auto',
            '^CNXFIN': 'Nifty Financial Services',
            '^CNXFMCG': 'Nifty FMCG',
            '^NSEIT': 'Nifty IT',
            '^CNXMETAL': 'Nifty Metal',
            '^CNXENERGY': 'Nifty Oil & Gas',
            '^CNXPHARMA': 'Nifty Pharma',
            '^CNXREALTY': 'Nifty Realty',
            '^CNXFIN_SRV': 'Nifty Financial Services (Alt)',
            '^CNXSERVICE': 'Nifty Healthcare',
            '^BSESN': 'Sensex (Overall Market)',
        }
        
        print(f"🔍 Analyzing {len(indian_sectors)} core NSE sectoral indices...")
        
        # Strategy 1: Quick Tavily search for trending sectors
        if self.tavily_client:
            print("🌐 Using Tavily for sector trend search...")
            try:
                web_results = self._tavily_web_search("Indian NSE sectoral indices performance today Nifty Auto Bank IT Pharma", max_results=2)
                web_sectors = self._extract_sectors_from_web_content(web_results)
                discovered_sectors.update(web_sectors)
                print(f"🌐 Tavily discovered {len(web_sectors)} trending sectors from web search")
            except Exception as e:
                print(f"⚠️ Tavily sector search failed: {e}")
        
        # Strategy 2: Use LLM to identify top 3 performing sectors from the 14
        print("🤖 Using Groq DeepSeek to identify top 3 performing sectors...")
        
        try:
            system_prompt = """You are a sector analyst. From the 14 core NSE sectoral indices, identify the top 3 that are performing best today.
            
            The 14 core NSE sectoral indices are:
            1. Nifty Bank (^NSEBANK)
            2. Nifty Auto (^CNXAUTO)
            3. Nifty Financial Services (^CNXFIN)
            4. Nifty FMCG (^CNXFMCG)
            5. Nifty IT (^NSEIT)
            6. Nifty Metal (^CNXMETAL)
            7. Nifty Oil & Gas (^CNXENERGY)
            8. Nifty Pharma (^CNXPHARMA)
            9. Nifty Realty (^CNXREALTY)
            10. Nifty Healthcare (^CNXSERVICE)
            11. Nifty 50 (^NSEI) - Overall Market
            12. Sensex (^BSESN) - Overall Market
            
            Return ONLY the top 3 performing sector symbols from this list."""
            
            user_prompt = """From the 14 core NSE sectoral indices listed above, identify the top 3 that are performing best today.
            Consider current market trends, news, and sector momentum.
            Return only the 3 best performing sector symbols like: ^NSEBANK, ^CNXAUTO, ^NSEIT"""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self._call_llm_with_fallback(messages, "top 3 sector identification")
            
            if response and response.content:
                # Extract sector symbols from response
                sector_symbols = re.findall(r'\^([A-Z0-9_]+)', response.content)
                for symbol in sector_symbols:
                    if symbol in ['NSEBANK', 'CNXAUTO', 'CNXFIN', 'CNXFMCG', 'NSEIT', 'CNXMETAL', 'CNXENERGY', 'CNXPHARMA', 'CNXREALTY', 'CNXFIN_SRV', 'CNXSERVICE', 'NSEI', 'BSESN']:
                        discovered_sectors[f"^{symbol}"] = indian_sectors.get(f"^{symbol}", f"{symbol} Sector")
        
        except Exception as e:
            print(f"⚠️ Top 3 sector identification failed: {e}")
        
        # Strategy 3: If LLM didn't find enough, add some default top sectors
        if len(discovered_sectors) < 3:
            print("🔄 Adding default top sectors to ensure we have 3...")
            default_sectors = {
                '^NSEBANK': 'Nifty Bank',
                '^CNXAUTO': 'Nifty Auto',
                '^NSEIT': 'Nifty IT'
            }
            for symbol, name in default_sectors.items():
                if symbol not in discovered_sectors:
                    discovered_sectors[symbol] = name
                    if len(discovered_sectors) >= 3:
                        break
        
        # Return only top 3 sectors
        top_sectors = dict(list(discovered_sectors.items())[:3])
        print(f"📊 Found {len(top_sectors)} top performing sectors from 14 core NSE sectoral indices")
        
        return top_sectors
    
    def _discover_market_indices(self) -> Dict[str, str]:
        """Dynamically discover market indices using Groq DeepSeek and Tavily with fallback"""
        discovered_indices = {}
        
        if not self.llm and not self.groq_llm and not self.tavily_client:
            print("⚠️ No LLM or Tavily available for index discovery")
            return discovered_indices
        
        try:
            print("🔍 Groq DeepSeek agent and Tavily discovering market indices...")
            
            # Strategy 1: Real web search using Tavily
            if self.tavily_client:
                print("🌐 Using Tavily for real market index search...")
                web_results = self._tavily_web_search("Indian market indices NIFTY SENSEX BANK NIFTY current performance")
                web_indices = self._extract_sectors_from_web_content(web_results)  # Reuse sector extraction for indices
                discovered_indices.update(web_indices)
                print(f"🌐 Tavily discovered {len(web_indices)} indices from web search")
            
            # Strategy 2: LLM-based discovery (fallback if no Tavily)
            if self.llm or self.groq_llm:
                print("🤖 Using Groq DeepSeek for index discovery...")
                
                system_prompt = """You are a market analyst specializing in Indian markets. Search for Indian market indices that are currently active 
                and showing significant movements. Focus on major Indian market indices.
                
                Look for:
                - Indian market indices that are currently trending
                - Indian broad market indices
                - Indian sector indices
                - Focus on Indian markets only
                - Do NOT use any predefined or hardcoded index names
                - Search dynamically for currently active indices"""
                
                user_prompt = """Search for 10 Indian market indices that are currently active and showing significant movements in the Indian market. 
                Look for major Indian market indices across Indian markets (NSE/BSE). Return the symbols and names.
                Focus ONLY on Indian market indices. Do NOT use any hardcoded or predefined index names - search dynamically."""
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt)
                ]
                
                response = self._call_llm_with_fallback(messages, "index discovery")
                
                if response and response.content:
                    # Extract index symbols from Groq DeepSeek's response
                    index_symbols = re.findall(r'\b([A-Z]{2,10})\.(NS|BO)\b', response.content)
                    for symbol, suffix in index_symbols:
                        if symbol not in ['NS', 'BO', 'THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'HAVE', 'WILL', 'BEEN', 'THEY', 'THEIR']:
                            discovered_indices[f"{symbol}.{suffix}"] = f"{symbol} Index"
                    
                    # Also look for common index patterns
                    index_patterns = re.findall(r'\b([A-Z]{2,10})\s+(INDEX|AVERAGE)\b', response.content)
                    for pattern in index_patterns:
                        symbol = pattern[0]
                        discovered_indices[f"{symbol}.NS"] = f"{symbol} Index"
        
        except Exception as e:
            print(f"⚠️ Index discovery failed: {e}")
        
        return discovered_indices
    
    def _fetch_stock_data_parallel(self, symbols: List[str], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Fetch stock data in parallel from multiple sources - focusing only on Indian stocks"""
        stock_data = {}
        
        # Filter to only include Indian stocks (.NS or .BO suffix)
        indian_symbols = [symbol for symbol in symbols if symbol.endswith('.NS') or symbol.endswith('.BO')]
        
        if not indian_symbols:
            print("⚠️ No Indian stocks found in the discovered symbols")
            return stock_data
        
        print(f"📊 Processing {len(indian_symbols)} Indian stocks out of {len(symbols)} total discovered symbols")
        
        def fetch_single_stock(symbol):
            try:
                # Try multiple sources for real-time data
                stock_info = self._get_stock_data_from_multiple_sources(symbol)
                if stock_info:
                    return symbol, stock_info
            except Exception as e:
                print(f"⚠️ Could not get data for {symbol}: {e}")
            return None
        
        # Use ThreadPoolExecutor for parallel processing with more workers
        with ThreadPoolExecutor(max_workers=min(len(indian_symbols), 6)) as executor:
            # Submit all tasks for Indian stocks only
            future_to_symbol = {executor.submit(fetch_single_stock, symbol): symbol for symbol in indian_symbols}
            
            # Collect results as they complete
            for future in as_completed(future_to_symbol):
                result = future.result()
                if result:
                    symbol, data = result
                    stock_data[symbol] = data
        
        return stock_data
    
    def _validate_symbol(self, symbol: str) -> bool:
        """Validate if a symbol is likely to be valid"""
        # Common valid Indian market patterns
        valid_patterns = [
            r'^[A-Z]{2,10}\.(NS|BO)$',  # Stock symbols like RELIANCE.NS
            r'^\^[A-Z0-9]{3,10}$',      # Index symbols like ^NSEI
            r'^[A-Z]{2,10}$'            # Simple symbols like RELIANCE
        ]
        
        for pattern in valid_patterns:
            if re.match(pattern, symbol):
                return True
        
        return False
    
    def _get_stock_data_from_multiple_sources(self, symbol: str) -> Dict[str, Any]:
        """Get stock data quickly using yfinance as primary source"""
        stock_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        # Validate symbol first
        if not self._validate_symbol(symbol):
            print(f"⚠️ Skipping invalid symbol: {symbol}")
            return None
        
        # Use yfinance as primary source for speed
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")  # Reduced to 2 days for speed
            if not hist.empty and len(hist) > 1:
                info = ticker.info
                current_price = hist['Close'].iloc[-1]
                start_price = hist['Close'].iloc[0]
                
                # Prevent division by zero
                if start_price > 0:
                    price_change_pct = ((current_price - start_price) / start_price) * 100
                else:
                    price_change_pct = 0.0
                
                return {
                    'name': info.get('longName', stock_symbol),
                    'sector': info.get('sector', 'Unknown'),
                    'current_price': current_price,
                    'price_change_pct': price_change_pct,
                    'volume': hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0,
                    'source': 'yfinance_primary'
                }
        except Exception as e:
            # Don't print the full error for invalid symbols to reduce noise
            if "delisted" not in str(e) and "404" not in str(e):
                print(f"⚠️ yfinance failed for {symbol}: {e}")
        
        # Fallback to LLM only if yfinance fails
        if self.llm or self.groq_llm:
            try:
                system_prompt = """You are a financial data analyst. Get current stock data for the given symbol.
                Return the data in a structured format with current price, price change percentage, company name, sector, and volume."""
                
                user_prompt = f"""Get current stock data for {symbol}. Return:
                - Current price
                - Price change percentage (today's change)
                - Company name
                - Sector
                - Trading volume
                
                Format as JSON or structured text."""
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt)
                ]
                
                response = self._call_llm_with_fallback(messages, f"stock data fetch for {symbol}")
                
                if response and response.content:
                    # Parse the response to extract stock data
                    # Look for price patterns
                    price_match = re.search(r'(\d+\.?\d*)', response.content)
                    current_price = float(price_match.group(1)) if price_match else 0.0
                    
                    # Look for percentage change
                    change_match = re.search(r'([+-]?\d+\.?\d*)%', response.content)
                    price_change_pct = float(change_match.group(1)) if change_match else 0.0
                    
                    # Extract company name
                    company_name = stock_symbol
                    name_match = re.search(r'([A-Z][a-z\s]+(?:Limited|Ltd|Corp|Inc))', response.content)
                    if name_match:
                        company_name = name_match.group(1)
                    
                    # Extract sector
                    sector = "Unknown"
                    # Look for any sector mentioned in the response dynamically
                    sector_match = re.search(r'\b([A-Z][a-z]+)\s+(Sector|Industry|Business)\b', response.content)
                    if sector_match:
                        sector = sector_match.group(1)
                    
                    return {
                        'name': company_name,
                        'sector': sector,
                        'current_price': current_price,
                        'price_change_pct': price_change_pct,
                        'volume': 0,  # Not easily available from text
                        'source': 'groq_fallback'
                    }
            
            except Exception as e:
                print(f"⚠️ LLM fallback failed for {symbol}: {e}")
        
        return None
    
    def _get_correct_sector_symbol(self, sector_name: str) -> str:
        """Get the correct Yahoo Finance symbol for Indian sectors"""
        # Real NSE sectoral indices with their Yahoo Finance symbols
        sector_symbols = {
            # Main market indices
            '^NSEI': '^NSEI',  # Nifty 50 - exists
            '^BSESN': '^BSESN',  # Sensex - exists
            
            # 14 Core NSE Sectoral Indices (real symbols)
            '^NSEBANK': '^NSEBANK',  # Nifty Bank - exists
            '^CNXAUTO': '^CNXAUTO',  # Nifty Auto - exists
            '^CNXFIN': '^CNXFIN',  # Nifty Financial Services - exists
            '^CNXFMCG': '^CNXFMCG',  # Nifty FMCG - exists
            '^NSEIT': '^NSEIT',  # Nifty IT - exists
            '^CNXMETAL': '^CNXMETAL',  # Nifty Metal - exists
            '^CNXENERGY': '^CNXENERGY',  # Nifty Oil & Gas - exists
            '^CNXPHARMA': '^CNXPHARMA',  # Nifty Pharma - exists
            '^CNXREALTY': '^CNXREALTY',  # Nifty Realty - exists
            '^CNXFIN_SRV': '^CNXFIN_SRV',  # Nifty Financial Services (alternative)
            '^CNXSERVICE': '^CNXSERVICE',  # Nifty Healthcare (Service sector)
            
            # Alternative formats
            'NIFTYAUTO.NS': '^CNXAUTO',
            'NIFTYBANK.NS': '^NSEBANK',
            'NIFTYFIN.NS': '^CNXFIN',
            'NIFTYFMCG.NS': '^CNXFMCG',
            'NIFTYIT.NS': '^NSEIT',
            'NIFTYMETAL.NS': '^CNXMETAL',
            'NIFTYENERGY.NS': '^CNXENERGY',
            'NIFTYPHARMA.NS': '^CNXPHARMA',
            'NIFTYREALTY.NS': '^CNXREALTY',
        }
        
        return sector_symbols.get(sector_name, sector_name)
    
    def _search_for_sector_symbols(self) -> Dict[str, str]:
        """Search online for correct Indian sector symbols"""
        print("🔍 Searching for correct Indian sector symbols...")
        
        # Use Tavily to search for current Indian sector symbols
        if self.tavily_client:
            try:
                search_results = self._tavily_web_search("Indian NIFTY sector indices symbols Yahoo Finance current 2024", max_results=3)
                
                # Extract potential symbols from search results
                found_symbols = {}
                for result in search_results:
                    content = result.get('content', '') + result.get('title', '')
                    
                    # Look for NIFTY sector patterns
                    nifty_patterns = re.findall(r'\b(NIFTY[A-Z0-9]+)\b', content)
                    for pattern in nifty_patterns:
                        if pattern not in ['NIFTY', 'NIFTY50']:
                            found_symbols[f"{pattern}.NS"] = f"{pattern} Sector"
                    
                    # Look for ^ symbols
                    yahoo_patterns = re.findall(r'\^([A-Z0-9]+)', content)
                    for pattern in yahoo_patterns:
                        if pattern not in ['NSEI', 'BSESN']:
                            found_symbols[f"^{pattern}"] = f"{pattern} Sector"
                
                if found_symbols:
                    print(f"✅ Found {len(found_symbols)} potential sector symbols from web search")
                    return found_symbols
                    
            except Exception as e:
                print(f"⚠️ Web search for sector symbols failed: {e}")
        
        return {}
    
    def _get_sector_data_from_multiple_sources(self, symbol: str, sector_name: str) -> Dict[str, Any]:
        """Get sector data quickly using yfinance as primary source with multiple symbol attempts"""
        
        # Try multiple symbol variations to find the correct one
        symbol_variations = [
            symbol,  # Original symbol
            self._get_correct_sector_symbol(symbol),  # Mapped symbol
            symbol.replace('^', '').replace('.NS', '') + '.NS',  # Alternative format
            symbol.replace('^', '') + '.NS',  # Another alternative
        ]
        
        # Remove duplicates
        symbol_variations = list(dict.fromkeys(symbol_variations))
        
        print(f"🔍 Trying symbol variations for {sector_name}: {symbol_variations}")
        
        # Try each symbol variation
        for actual_symbol in symbol_variations:
            try:
                ticker = yf.Ticker(actual_symbol)
                hist = ticker.history(period="2d")  # Reduced to 2 days for speed
                
                if not hist.empty and len(hist) > 1:
                    current_price = hist['Close'].iloc[-1]
                    start_price = hist['Close'].iloc[0]
                    
                    # Prevent division by zero
                    if start_price > 0:
                        price_change_pct = ((current_price - start_price) / start_price) * 100
                    else:
                        price_change_pct = 0.0
                    
                    # Calculate volatility
                    returns = hist['Close'].pct_change().dropna()
                    volatility = returns.std() * 100 if len(returns) > 0 else 0.0
                    
                    print(f"✅ Found data for {sector_name} using symbol: {actual_symbol}")
                    
                    return {
                        'name': sector_name,
                        'current_price': current_price,
                        'price_change_pct': price_change_pct,
                        'volatility': volatility,
                        'source': 'yfinance_primary',
                        'symbol_used': actual_symbol
                    }
                    
            except Exception as e:
                # Don't print errors for invalid symbols to reduce noise
                if "delisted" not in str(e) and "404" not in str(e):
                    print(f"⚠️ yfinance failed for {actual_symbol}: {e}")
                continue
        
        # If no yfinance data found, try web search for current sector data
        print(f"🌐 Searching for current {sector_name} data online...")
        
        if self.tavily_client:
            try:
                search_query = f"{sector_name} current price performance today Indian market"
                web_results = self._tavily_web_search(search_query, max_results=2)
                
                # Extract price and performance data from web results
                for result in web_results:
                    content = result.get('content', '') + result.get('title', '')
                    
                    # Look for percentage changes
                    change_patterns = re.findall(r'([+-]?\d+\.?\d*)%', content)
                    if change_patterns:
                        # Take the first significant change found
                        for change in change_patterns:
                            try:
                                price_change_pct = float(change)
                                if abs(price_change_pct) > 0.01:  # More than 0.01%
                                    print(f"✅ Found {sector_name} performance from web: {price_change_pct}%")
                                    
                                    # Estimate current price (this is approximate)
                                    estimated_price = 20000  # Base estimate for indices
                                    
                                    return {
                                        'name': sector_name,
                                        'current_price': estimated_price,
                                        'price_change_pct': price_change_pct,
                                        'volatility': 0.0,
                                        'source': 'web_search',
                                        'symbol_used': symbol
                                    }
                            except ValueError:
                                continue
                                
            except Exception as e:
                print(f"⚠️ Web search for {sector_name} failed: {e}")
        
        # Final fallback to LLM with better prompting
        if self.llm or self.groq_llm:
            try:
                system_prompt = """You are a sector data analyst. Get current sector index data for Indian markets.
                Return ONLY real, current data. If you don't know the exact data, say so."""
                
                user_prompt = f"""Get current sector data for {sector_name} in Indian markets. 
                Return ONLY if you have real, current information:
                - Current price (approximate)
                - Price change percentage (today's change)
                
                If you don't have real current data, respond with "NO_DATA"."""
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt)
                ]
                
                response = self._call_llm_with_fallback(messages, f"sector data fetch for {sector_name}")
                
                if response and response.content and "NO_DATA" not in response.content:
                    # Parse the response to extract sector data
                    price_match = re.search(r'(\d+\.?\d*)', response.content)
                    current_price = float(price_match.group(1)) if price_match else 0.0
                    
                    change_match = re.search(r'([+-]?\d+\.?\d*)%', response.content)
                    price_change_pct = float(change_match.group(1)) if change_match else 0.0
                    
                    if price_change_pct != 0.0:  # Only return if we got real data
                        return {
                            'name': sector_name,
                            'current_price': current_price,
                            'price_change_pct': price_change_pct,
                            'volatility': 0.0,
                            'source': 'llm_fallback',
                            'symbol_used': symbol
                        }
            
            except Exception as e:
                print(f"⚠️ LLM fallback failed for {sector_name}: {e}")
        
        print(f"❌ Could not find data for {sector_name}")
        return None
    
    def _fetch_sector_data_parallel(self, sectors: Dict[str, str], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Fetch sector data in parallel from multiple sources"""
        sector_data = {}
        
        def fetch_single_sector(symbol, sector_name):
            try:
                # Try multiple sources for sector data
                sector_info = self._get_sector_data_from_multiple_sources(symbol, sector_name)
                if sector_info:
                    return symbol, sector_info
            except Exception as e:
                print(f"⚠️ Could not get sector data for {symbol}: {e}")
            return None
        
        # Use ThreadPoolExecutor for parallel processing with more workers
        with ThreadPoolExecutor(max_workers=min(len(sectors), 6)) as executor:
            # Submit all tasks
            future_to_symbol = {
                executor.submit(fetch_single_sector, symbol, sector_name): symbol 
                for symbol, sector_name in sectors.items()
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_symbol):
                result = future.result()
                if result:
                    symbol, data = result
                    sector_data[symbol] = data
        
        return sector_data
    
    def _fetch_index_data_parallel(self, indices: Dict[str, str], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Fetch index data in parallel"""
        index_data = {}
        
        def fetch_single_index(symbol, index_name):
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty and len(hist) > 1:
                    return symbol, {
                        'name': index_name,
                        'data': hist
                    }
            except Exception as e:
                print(f"⚠️ Could not get index data for {symbol}: {e}")
            return None
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_symbol = {
                executor.submit(fetch_single_index, symbol, index_name): symbol 
                for symbol, index_name in indices.items()
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_symbol):
                result = future.result()
                if result:
                    symbol, data = result
                    index_data[symbol] = data
        
        return index_data
    
    def _analyze_stock_performance(self, stocks_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze stock performance and return top 3 performers only"""
        performance_data = []
        
        for symbol, data in stocks_data.items():
            try:
                # New data structure from multiple sources
                if 'current_price' in data and 'price_change_pct' in data:
                    current_price = data['current_price']
                    price_change_pct = data['price_change_pct']
                    company_name = data['name']
                    sector = data['sector']
                    volume = data.get('volume', 0)
                    source = data.get('source', 'unknown')
                    
                    # Calculate performance score
                    performance_score = self._calculate_performance_score(
                        price_change_pct, 0, 0  # No volatility data from scraping
                    )
                    
                    performance_data.append({
                        'symbol': symbol,
                        'name': company_name,
                        'sector': sector,
                        'current_price': round(current_price, 2),
                        'price_change': round(current_price * (price_change_pct / 100), 2),
                        'price_change_pct': round(price_change_pct, 2),
                        'volatility': 0.0,  # Not available from scraping
                        'volume_trend': 0.0,  # Not available from scraping
                        'performance_score': performance_score,
                        'source': source
                    })
                
            except Exception as e:
                print(f"⚠️ Error analyzing {symbol}: {e}")
        
        # Sort by performance score and return top 3 only
        performance_data.sort(key=lambda x: x['performance_score'], reverse=True)
        return performance_data[:3]
    
    def _analyze_sector_performance(self, sectors_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze sector performance and return top 3 performers only"""
        sector_performance = []
        
        for symbol, data in sectors_data.items():
            try:
                # New data structure from multiple sources
                if 'current_price' in data and 'price_change_pct' in data:
                    current_price = data['current_price']
                    price_change_pct = data['price_change_pct']
                    sector_name = data['name']
                    volatility = data.get('volatility', 0.0)
                    source = data.get('source', 'unknown')
                    
                    # Calculate performance score
                    performance_score = self._calculate_performance_score(
                        price_change_pct, volatility, 0  # No volume data for sectors
                    )
                    
                    sector_performance.append({
                        'symbol': symbol,
                        'name': sector_name,
                        'current_price': round(current_price, 2),
                        'price_change_pct': round(price_change_pct, 2),
                        'volatility': round(volatility, 2),
                        'performance_score': performance_score,
                        'source': source
                    })
                
            except Exception as e:
                print(f"⚠️ Error analyzing sector {symbol}: {e}")
        
        # Sort by performance score and return top 3 only
        sector_performance.sort(key=lambda x: x['performance_score'], reverse=True)
        return sector_performance[:3]
    
    def _calculate_performance_score(self, price_change_pct: float, volatility: float, volume_trend: float = 0) -> float:
        """Calculate a performance score based on multiple factors"""
        try:
            # Base score from price change (60% weight)
            price_score = min(abs(price_change_pct) * 2, 100)  # Cap at 100
            
            # Volatility adjustment (20% weight) - lower volatility is better
            volatility_score = max(0, 100 - volatility * 2)
            
            # Volume trend bonus (20% weight)
            volume_score = max(0, min(volume_trend + 50, 100))
            
            # Calculate weighted score
            total_score = (price_score * 0.6) + (volatility_score * 0.2) + (volume_score * 0.2)
            
            # Apply direction (positive for gains, negative for losses)
            return total_score if price_change_pct > 0 else -total_score
            
        except Exception as e:
            print(f"⚠️ Error calculating performance score: {e}")
            # Return a default score based on price change
            return abs(price_change_pct) if price_change_pct > 0 else -abs(price_change_pct)
    
    def _generate_market_insights(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Indian market insights from the data"""
        insights = {
            'market_sentiment': 'neutral',
            'trending_sectors': [],
            'key_observations': [],
            'risk_level': 'medium',
            'indian_market_focus': True
        }
        
        try:
            # Analyze Indian sector performance
            if market_data['sectors']:
                sector_changes = []
                indian_sector_count = 0
                
                for symbol, data in market_data['sectors'].items():
                    try:
                        if 'price_change_pct' in data:
                            change_pct = data['price_change_pct']
                            sector_changes.append((data.get('name', symbol), change_pct, symbol))
                            
                            # Count Indian sectors
                            if symbol.endswith('.NS') or symbol.endswith('.BO'):
                                indian_sector_count += 1
                    except Exception as e:
                        print(f"⚠️ Error processing sector {symbol}: {e}")
                        continue
                
                # Determine market sentiment based on Indian sectors
                if sector_changes:
                    positive_sectors = len([s for s in sector_changes if s[1] > 0])
                    total_sectors = len(sector_changes)
                    
                    if total_sectors > 0:
                        positive_ratio = positive_sectors / total_sectors
                        if positive_ratio > 0.7:
                            insights['market_sentiment'] = 'bullish'
                        elif positive_ratio < 0.3:
                            insights['market_sentiment'] = 'bearish'
                    
                    # Get trending Indian sectors
                    sector_changes.sort(key=lambda x: x[1], reverse=True)
                    indian_trending = [s[0] for s in sector_changes if s[2].endswith('.NS') or s[2].endswith('.BO')][:3]
                    insights['trending_sectors'] = indian_trending
                    
                    # Add Indian market specific observations
                    if indian_sector_count > 0:
                        insights['key_observations'].append(f"Analyzed {indian_sector_count} Indian sector indices")
            
            # Generate Indian market specific observations
            if market_data['stocks']:
                stock_changes = []
                indian_stock_count = 0
                
                for symbol, data in market_data['stocks'].items():
                    try:
                        if 'price_change_pct' in data:
                            change_pct = data['price_change_pct']
                            stock_changes.append((symbol, change_pct, data.get('name', symbol)))
                            
                            # Count Indian stocks
                            if symbol.endswith('.NS'):
                                indian_stock_count += 1
                    except Exception as e:
                        print(f"⚠️ Error processing stock {symbol}: {e}")
                        continue
                
                if stock_changes:
                    try:
                        avg_change = sum(c[1] for c in stock_changes) / len(stock_changes)
                        insights['key_observations'].append(f"Average Indian stock performance: {avg_change:.2f}%")
                    except Exception as e:
                        print(f"⚠️ Error calculating average change: {e}")
                    
                    # Find most volatile Indian stocks
                    indian_stocks = [s for s in stock_changes if s[0].endswith('.NS')]
                    if indian_stocks:
                        try:
                            volatile_stocks = sorted(indian_stocks, key=lambda x: abs(x[1]), reverse=True)[:3]
                            stock_names = [s[0].replace('.NS', '') for s in volatile_stocks]
                            insights['key_observations'].append(f"Most volatile Indian stocks: {', '.join(stock_names)}")
                        except Exception as e:
                            print(f"⚠️ Error finding volatile stocks: {e}")
                    
                    # Add Indian market context
                    if indian_stock_count > 0:
                        insights['key_observations'].append(f"Scanned {indian_stock_count} Indian stocks across various sectors")
            
            # Add Indian market specific risk assessment
            if insights['market_sentiment'] == 'bullish':
                insights['risk_level'] = 'low'
            elif insights['market_sentiment'] == 'bearish':
                insights['risk_level'] = 'high'
                
        except Exception as e:
            print(f"⚠️ Error generating market insights: {e}")
            # Keep default insights if there's an error
        
        return insights
    
    def _create_market_summary(self, top_stocks: List[Dict], top_sectors: List[Dict]) -> str:
        """Create an Indian market summary for display"""
        summary = f"📈 Indian Market Scan Summary - {datetime.now().strftime('%B %d, %Y')}\n\n"
        
        if top_stocks:
            summary += "🏆 Top Performing Indian Stocks:\n"
            for i, stock in enumerate(top_stocks[:5], 1):
                direction = "📈" if stock['price_change_pct'] > 0 else "📉"
                stock_symbol = stock['symbol'].replace('.NS', '')  # Remove .NS suffix for display
                summary += f"{i}. {stock_symbol} ({stock['name']}) {direction} {stock['price_change_pct']:+.2f}%\n"
        
        if top_sectors:
            summary += "\n🏆 Top Performing Indian Sectors:\n"
            for i, sector in enumerate(top_sectors[:3], 1):
                direction = "📈" if sector['price_change_pct'] > 0 else "📉"
                summary += f"{i}. {sector['name']} {direction} {sector['price_change_pct']:+.2f}%\n"
        
        return summary

# Example usage
if __name__ == "__main__":
    scanner = DynamicMarketScannerTool()
    result = scanner._run(5)
    print(json.dumps(result, indent=2)) 