"""
📈 Market Scanner Tool for IntelliVest AI
=========================================

Identifies top-performing stocks and sectors from recent market data
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

class MarketScannerTool(BaseTool):
    """📈 Market scanner for identifying top-performing stocks and sectors"""
    
    name: str = "market_scanner"
    description: str = """
    Scans the market to identify top-performing stocks and sectors from recent trading days.
    Returns trending stocks, sector performance, and market insights.
    Input should be the number of days to look back (default: 5 days).
    Returns comprehensive market analysis with top performers.
    """
    
    def _run(self, days_back: int = 5) -> Dict[str, Any]:
        """Run market scan for top performers"""
        try:
            print(f"🔍 Scanning market for top performers (last {days_back} days)...")
            
            # Get market data
            market_data = self._get_market_data(days_back)
            
            # Analyze performance
            top_stocks = self._analyze_stock_performance(market_data['stocks'])
            top_sectors = self._analyze_sector_performance(market_data['sectors'])
            market_insights = self._generate_market_insights(market_data)
            
            return {
                "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "days_analyzed": days_back,
                "top_performing_stocks": top_stocks,
                "top_performing_sectors": top_sectors,
                "market_insights": market_insights,
                "market_summary": self._create_market_summary(top_stocks, top_sectors)
            }
            
        except Exception as e:
            print(f"❌ Market scan failed: {e}")
            return {
                "error": f"Market scan failed: {str(e)}",
                "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def _get_market_data(self, days_back: int) -> Dict[str, Any]:
        """Get market data for analysis"""
        # Major indices and ETFs for sector analysis
        indices = {
            'SPY': 'S&P 500 ETF',
            'QQQ': 'NASDAQ-100 ETF', 
            'IWM': 'Russell 2000 ETF',
            'DIA': 'Dow Jones ETF'
        }
        
        # Sector ETFs
        sectors = {
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
        
        # Popular stocks for analysis
        popular_stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX',
            'JPM', 'JNJ', 'PG', 'V', 'UNH', 'HD', 'MA', 'DIS', 'PYPL', 'ADBE',
            'CRM', 'ABT', 'KO', 'PEP', 'TMO', 'AVGO', 'COST', 'MRK', 'WMT',
            'BAC', 'PFE', 'ABBV', 'LLY', 'TXN', 'ACN', 'DHR', 'VZ', 'CMCSA'
        ]
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back + 5)  # Extra days for weekends
        
        market_data = {
            'stocks': {},
            'sectors': {},
            'indices': {}
        }
        
        # Get stock data
        print("📊 Fetching stock data...")
        for symbol in popular_stocks[:20]:  # Limit to 20 for speed
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty:
                    market_data['stocks'][symbol] = {
                        'name': ticker.info.get('longName', symbol),
                        'sector': ticker.info.get('sector', 'Unknown'),
                        'data': hist
                    }
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                print(f"⚠️ Could not fetch {symbol}: {e}")
        
        # Get sector data
        print("📊 Fetching sector data...")
        for symbol, sector_name in sectors.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty:
                    market_data['sectors'][symbol] = {
                        'name': sector_name,
                        'data': hist
                    }
                time.sleep(0.1)
            except Exception as e:
                print(f"⚠️ Could not fetch sector {symbol}: {e}")
        
        # Get index data
        print("📊 Fetching index data...")
        for symbol, index_name in indices.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty:
                    market_data['indices'][symbol] = {
                        'name': index_name,
                        'data': hist
                    }
                time.sleep(0.1)
            except Exception as e:
                print(f"⚠️ Could not fetch index {symbol}: {e}")
        
        return market_data
    
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
        """Create a market summary for display"""
        summary = f"📈 Market Scan Summary - {datetime.now().strftime('%B %d, %Y')}\n\n"
        
        if top_stocks:
            summary += "🏆 Top Performing Stocks:\n"
            for i, stock in enumerate(top_stocks[:5], 1):
                direction = "📈" if stock['price_change_pct'] > 0 else "📉"
                summary += f"{i}. {stock['symbol']} ({stock['name']}) {direction} {stock['price_change_pct']:+.2f}%\n"
        
        if top_sectors:
            summary += "\n🏆 Top Performing Sectors:\n"
            for i, sector in enumerate(top_sectors[:3], 1):
                direction = "📈" if sector['price_change_pct'] > 0 else "📉"
                summary += f"{i}. {sector['name']} {direction} {sector['price_change_pct']:+.2f}%\n"
        
        return summary

# Example usage
if __name__ == "__main__":
    scanner = MarketScannerTool()
    result = scanner._run(5)
    print(json.dumps(result, indent=2)) 