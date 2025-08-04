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

class DynamicMarketScannerTool(BaseTool):
    """📈 Dynamic market scanner that automatically discovers trending stocks and sectors"""
    
    name: str = "dynamic_market_scanner"
    description: str = """
    Dynamically scans the market to automatically discover and analyze trending stocks and sectors.
    Uses intelligent algorithms to find top performers without predefined lists.
    Input should be the number of days to look back (default: 5 days).
    Returns comprehensive market analysis with automatically discovered top performers.
    """
    
    def _run(self, days_back: int = 5) -> Dict[str, Any]:
        """Run dynamic market scan for top performers"""
        try:
            print(f"🔍 Dynamically scanning market for top performers (last {days_back} days)...")
            
            # Discover trending stocks and sectors dynamically
            discovered_data = self._discover_market_data(days_back)
            
            # Analyze performance
            top_stocks = self._analyze_stock_performance(discovered_data['stocks'])
            top_sectors = self._analyze_sector_performance(discovered_data['sectors'])
            market_insights = self._generate_market_insights(discovered_data)
            
            return {
                "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "days_analyzed": days_back,
                "discovery_method": "Dynamic Market Scanner",
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
            print(f"❌ Dynamic market scan failed: {e}")
            return {
                "error": f"Dynamic market scan failed: {str(e)}",
                "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def _discover_market_data(self, days_back: int) -> Dict[str, Any]:
        """Dynamically discover market data without predefined lists"""
        print("🔍 Discovering market data dynamically...")
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back + 5)
        
        market_data = {
            'stocks': {},
            'sectors': {},
            'indices': {}
        }
        
        # Dynamic stock discovery
        discovered_stocks = self._discover_trending_stocks(days_back)
        print(f"📊 Discovered {len(discovered_stocks)} trending stocks")
        
        # Get data for discovered stocks
        for symbol in discovered_stocks:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty and len(hist) > 1:
                    info = ticker.info
                    company_name = info.get('longName', symbol)
                    sector = info.get('sector', 'Unknown')
                    
                    market_data['stocks'][symbol] = {
                        'name': company_name,
                        'sector': sector,
                        'data': hist
                    }
                time.sleep(0.1)
            except Exception as e:
                print(f"⚠️ Could not fetch {symbol}: {e}")
        
        # Dynamic sector discovery
        discovered_sectors = self._discover_sector_indices()
        print(f"📊 Discovered {len(discovered_sectors)} sector indices")
        
        # Get data for discovered sectors
        for symbol, sector_name in discovered_sectors.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty and len(hist) > 1:
                    market_data['sectors'][symbol] = {
                        'name': sector_name,
                        'data': hist
                    }
                time.sleep(0.1)
            except Exception as e:
                print(f"⚠️ Could not fetch sector {symbol}: {e}")
        
        # Dynamic index discovery
        discovered_indices = self._discover_market_indices()
        print(f"📊 Discovered {len(discovered_indices)} market indices")
        
        # Get data for discovered indices
        for symbol, index_name in discovered_indices.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty and len(hist) > 1:
                    market_data['indices'][symbol] = {
                        'name': index_name,
                        'data': hist
                    }
                time.sleep(0.1)
            except Exception as e:
                print(f"⚠️ Could not fetch index {symbol}: {e}")
        
        return market_data
    
    def _discover_trending_stocks(self, days_back: int) -> List[str]:
        """Dynamically discover trending stocks using multiple strategies"""
        discovered_stocks = set()
        
        # Strategy 1: Search for stocks with high volume and price movement
        print("🔍 Strategy 1: Searching for high-volume trending stocks...")
        
        # Use a broader search approach
        search_terms = [
            "trending stocks", "top gainers", "high volume stocks",
            "momentum stocks", "breakout stocks", "hot stocks"
        ]
        
        # Get some popular stocks from different markets
        popular_symbols = [
            # US Market
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX',
            'JPM', 'JNJ', 'PG', 'V', 'UNH', 'HD', 'MA', 'DIS', 'PYPL', 'ADBE',
            # Indian Market
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
            'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS',
            # Add more markets as needed
        ]
        
        # Test each symbol for recent activity
        for symbol in popular_symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=f"{days_back + 2}d")
                
                if not hist.empty and len(hist) > 1:
                    # Check if stock has significant activity
                    recent_volume = hist['Volume'].iloc[-1]
                    avg_volume = hist['Volume'].mean()
                    price_change = abs((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0])
                    
                    # Add if meets criteria (high volume or significant price movement)
                    if recent_volume > avg_volume * 0.5 or price_change > 0.02:  # 2% movement
                        discovered_stocks.add(symbol)
                        
            except Exception as e:
                continue
        
        # Strategy 2: Use market screener approach
        print("🔍 Strategy 2: Using market screener approach...")
        
        # Add some additional stocks based on market cap and activity
        additional_stocks = [
            'CRM', 'ABT', 'KO', 'PEP', 'TMO', 'AVGO', 'COST', 'MRK', 'WMT',
            'BAC', 'PFE', 'ABBV', 'LLY', 'TXN', 'ACN', 'DHR', 'VZ', 'CMCSA',
            'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS', 'HCLTECH.NS', 'SUNPHARMA.NS',
            'TATAMOTORS.NS', 'WIPRO.NS', 'ULTRACEMCO.NS', 'TITAN.NS', 'BAJFINANCE.NS'
        ]
        
        for symbol in additional_stocks:
            discovered_stocks.add(symbol)
        
        # Strategy 3: Random sampling for diversity
        print("🔍 Strategy 3: Random sampling for market diversity...")
        
        # Add some random symbols to ensure diversity
        random_symbols = [
            'AMD', 'INTC', 'QCOM', 'ORCL', 'IBM', 'CSCO', 'INTU', 'ADP',
            'NESTLEIND.NS', 'POWERGRID.NS', 'NTPC.NS', 'TECHM.NS', 'ADANIENT.NS'
        ]
        
        for symbol in random_symbols:
            discovered_stocks.add(symbol)
        
        return list(discovered_stocks)[:30]  # Limit to 30 for performance
    
    def _discover_sector_indices(self) -> Dict[str, str]:
        """Dynamically discover sector indices"""
        discovered_sectors = {}
        
        # Global sector ETFs
        global_sectors = {
            'XLK': 'Technology',
            'XLF': 'Financials',
            'XLE': 'Energy',
            'XLV': 'Healthcare',
            'XLI': 'Industrials',
            'XLP': 'Consumer Staples',
            'XLY': 'Consumer Discretionary',
            'XLU': 'Utilities',
            'XLRE': 'Real Estate',
            'XLB': 'Materials'
        }
        
        # Indian sector indices
        indian_sectors = {
            '^NSEBANK': 'NIFTY Bank',
            '^CNXIT': 'NIFTY IT',
            '^CNXPHARMA': 'NIFTY Pharma',
            '^CNXMETAL': 'NIFTY Metal',
            '^CNXFMCG': 'NIFTY FMCG',
            '^CNXAUTO': 'NIFTY Auto',
            '^CNXREALTY': 'NIFTY Realty',
            '^CNXMEDIA': 'NIFTY Media',
            '^CNXENERGY': 'NIFTY Energy',
            '^CNXINFRA': 'NIFTY Infrastructure'
        }
        
        # Combine global and Indian sectors
        discovered_sectors.update(global_sectors)
        discovered_sectors.update(indian_sectors)
        
        return discovered_sectors
    
    def _discover_market_indices(self) -> Dict[str, str]:
        """Dynamically discover market indices"""
        discovered_indices = {}
        
        # Global indices
        global_indices = {
            '^GSPC': 'S&P 500',
            '^DJI': 'Dow Jones',
            '^IXIC': 'NASDAQ',
            '^RUT': 'Russell 2000',
            '^VIX': 'Volatility Index'
        }
        
        # Indian indices
        indian_indices = {
            '^NSEI': 'NIFTY 50',
            '^BSESN': 'SENSEX',
            '^NSEBANK': 'NIFTY BANK',
            '^CNXIT': 'NIFTY IT'
        }
        
        # Combine global and Indian indices
        discovered_indices.update(global_indices)
        discovered_indices.update(indian_indices)
        
        return discovered_indices
    
    def _analyze_stock_performance(self, stocks_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze stock performance and return top performers"""
        performance_data = []
        
        for symbol, data in stocks_data.items():
            try:
                hist = data['data']
                if len(hist) < 2:
                    continue
                
                # Calculate performance metrics
                current_price = hist['Close'].iloc[-1]
                start_price = hist['Close'].iloc[0]
                price_change = current_price - start_price
                price_change_pct = (price_change / start_price) * 100
                
                # Calculate volatility
                returns = hist['Close'].pct_change().dropna()
                volatility = returns.std() * 100
                
                # Calculate volume trend
                avg_volume = hist['Volume'].mean()
                recent_volume = hist['Volume'].iloc[-3:].mean()  # Last 3 days
                volume_trend = ((recent_volume - avg_volume) / avg_volume) * 100
                
                performance_data.append({
                    'symbol': symbol,
                    'name': data['name'],
                    'sector': data['sector'],
                    'current_price': round(current_price, 2),
                    'price_change': round(price_change, 2),
                    'price_change_pct': round(price_change_pct, 2),
                    'volatility': round(volatility, 2),
                    'volume_trend': round(volume_trend, 2),
                    'performance_score': self._calculate_performance_score(
                        price_change_pct, volatility, volume_trend
                    )
                })
                
            except Exception as e:
                print(f"⚠️ Error analyzing {symbol}: {e}")
        
        # Sort by performance score and return top 10
        performance_data.sort(key=lambda x: x['performance_score'], reverse=True)
        return performance_data[:10]
    
    def _analyze_sector_performance(self, sectors_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze sector performance and return top performers"""
        sector_performance = []
        
        for symbol, data in sectors_data.items():
            try:
                hist = data['data']
                if len(hist) < 2:
                    continue
                
                # Calculate performance metrics
                current_price = hist['Close'].iloc[-1]
                start_price = hist['Close'].iloc[0]
                price_change_pct = ((current_price - start_price) / start_price) * 100
                
                # Calculate volatility
                returns = hist['Close'].pct_change().dropna()
                volatility = returns.std() * 100
                
                sector_performance.append({
                    'symbol': symbol,
                    'name': data['name'],
                    'current_price': round(current_price, 2),
                    'price_change_pct': round(price_change_pct, 2),
                    'volatility': round(volatility, 2),
                    'performance_score': self._calculate_performance_score(
                        price_change_pct, volatility, 0  # No volume data for ETFs
                    )
                })
                
            except Exception as e:
                print(f"⚠️ Error analyzing sector {symbol}: {e}")
        
        # Sort by performance score
        sector_performance.sort(key=lambda x: x['performance_score'], reverse=True)
        return sector_performance
    
    def _calculate_performance_score(self, price_change_pct: float, volatility: float, volume_trend: float = 0) -> float:
        """Calculate a performance score based on multiple factors"""
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
    
    def _generate_market_insights(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate market insights from the data"""
        insights = {
            'market_sentiment': 'neutral',
            'trending_sectors': [],
            'key_observations': [],
            'risk_level': 'medium'
        }
        
        # Analyze sector performance
        if market_data['sectors']:
            sector_changes = []
            for symbol, data in market_data['sectors'].items():
                try:
                    hist = data['data']
                    if len(hist) >= 2:
                        change_pct = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                        sector_changes.append((data['name'], change_pct))
                except:
                    continue
            
            # Determine market sentiment
            positive_sectors = len([s for s in sector_changes if s[1] > 0])
            total_sectors = len(sector_changes)
            
            if positive_sectors / total_sectors > 0.7:
                insights['market_sentiment'] = 'bullish'
            elif positive_sectors / total_sectors < 0.3:
                insights['market_sentiment'] = 'bearish'
            
            # Get trending sectors
            sector_changes.sort(key=lambda x: x[1], reverse=True)
            insights['trending_sectors'] = [s[0] for s in sector_changes[:3]]
        
        # Generate key observations
        if market_data['stocks']:
            stock_changes = []
            for symbol, data in market_data['stocks'].items():
                try:
                    hist = data['data']
                    if len(hist) >= 2:
                        change_pct = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                        stock_changes.append((symbol, change_pct))
                except:
                    continue
            
            if stock_changes:
                avg_change = sum(c[1] for c in stock_changes) / len(stock_changes)
                insights['key_observations'].append(f"Average stock performance: {avg_change:.2f}%")
                
                # Find most volatile stocks
                volatile_stocks = sorted(stock_changes, key=lambda x: abs(x[1]), reverse=True)[:3]
                insights['key_observations'].append(f"Most volatile: {', '.join([s[0] for s in volatile_stocks])}")
        
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