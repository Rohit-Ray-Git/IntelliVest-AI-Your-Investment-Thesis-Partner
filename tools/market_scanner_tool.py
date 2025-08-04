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

class DynamicMarketScannerTool(BaseTool):
    """📈 Dynamic market scanner that automatically discovers trending stocks and sectors"""
    
    name: str = "dynamic_market_scanner"
    description: str = """
    Dynamically scans the market to automatically discover and analyze trending stocks and sectors.
    Uses intelligent algorithms to find top performers without predefined lists.
    Input should be the number of days to look back (default: 5 days).
    Returns comprehensive market analysis with automatically discovered top performers.
    """
    max_workers: int = Field(default=10, description="Number of parallel workers for data fetching")
    session: Optional[requests.Session] = Field(default=None, exclude=True)
    
    def __init__(self, max_workers: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
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
                "discovery_method": "Dynamic Market Scanner (Parallel)",
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
        """Dynamically discover market data without predefined lists using parallel processing"""
        print("🔍 Discovering market data dynamically with parallel processing...")
        
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
        
        # Parallel data fetching for stocks
        print("⚡ Fetching stock data in parallel...")
        stock_data = self._fetch_stock_data_parallel(discovered_stocks, start_date, end_date)
        market_data['stocks'] = stock_data
        
        # Dynamic sector discovery
        discovered_sectors = self._discover_sector_indices()
        print(f"📊 Discovered {len(discovered_sectors)} sector indices")
        
        # Parallel data fetching for sectors
        print("⚡ Fetching sector data in parallel...")
        sector_data = self._fetch_sector_data_parallel(discovered_sectors, start_date, end_date)
        market_data['sectors'] = sector_data
        
        # Dynamic index discovery
        discovered_indices = self._discover_market_indices()
        print(f"📊 Discovered {len(discovered_indices)} market indices")
        
        # Parallel data fetching for indices
        print("⚡ Fetching index data in parallel...")
        index_data = self._fetch_index_data_parallel(discovered_indices, start_date, end_date)
        market_data['indices'] = index_data
        
        return market_data
    
    def _discover_trending_stocks(self, days_back: int) -> List[str]:
        """Dynamically discover trending stocks using web scraping and market data"""
        discovered_stocks = set()
        
        # Strategy 1: Web scraping for trending stocks
        print("🔍 Strategy 1: Web scraping for trending stocks...")
        web_discovered = self._scrape_trending_stocks()
        discovered_stocks.update(web_discovered)
        
        # Strategy 2: Market screener API approach
        print("🔍 Strategy 2: Market screener approach...")
        screener_discovered = self._screener_discover_stocks()
        discovered_stocks.update(screener_discovered)
        
        # Strategy 3: High volume and momentum discovery
        print("🔍 Strategy 3: High volume and momentum discovery...")
        momentum_discovered = self._discover_momentum_stocks(days_back)
        discovered_stocks.update(momentum_discovered)
        
        # Strategy 4: Market cap based discovery
        print("🔍 Strategy 4: Market cap based discovery...")
        marketcap_discovered = self._discover_by_market_cap()
        discovered_stocks.update(marketcap_discovered)
        
        return list(discovered_stocks)[:40]  # Limit to 40 for performance
    
    def _scrape_trending_stocks(self) -> List[str]:
        """Scrape trending stocks from financial websites in parallel"""
        discovered = []
        
        def scrape_yahoo_finance():
            try:
                url = "https://finance.yahoo.com/trending-tickers"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    symbols = re.findall(r'[A-Z]{1,5}\.[A-Z]{2}|[A-Z]{1,5}', response.text)
                    return symbols[:20]
            except Exception as e:
                print(f"⚠️ Yahoo Finance scraping failed: {e}")
            return []
        
        def scrape_marketwatch():
            try:
                url = "https://www.marketwatch.com/tools/screener/stock"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    symbols = re.findall(r'[A-Z]{1,5}\.[A-Z]{2}|[A-Z]{1,5}', response.text)
                    return symbols[:15]
            except Exception as e:
                print(f"⚠️ MarketWatch scraping failed: {e}")
            return []
        
        # Use ThreadPoolExecutor for parallel scraping
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_yahoo = executor.submit(scrape_yahoo_finance)
            future_marketwatch = executor.submit(scrape_marketwatch)
            
            # Collect results
            discovered.extend(future_yahoo.result())
            discovered.extend(future_marketwatch.result())
        
        return discovered
    
    def _screener_discover_stocks(self) -> List[str]:
        """Use market screener approach to discover stocks"""
        discovered = []
        
        try:
            # Use yfinance to get some popular stocks by searching
            search_terms = [
                "trending", "gainers", "losers", "volume", "momentum",
                "breakout", "hot", "popular", "active"
            ]
            
            for term in search_terms:
                try:
                    # Search for stocks using yfinance
                    search_results = yf.Tickers(term)
                    if hasattr(search_results, 'tickers'):
                        for ticker in search_results.tickers[:5]:
                            discovered.append(ticker.ticker)
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Screener discovery failed: {e}")
        
        return discovered
    
    def _discover_momentum_stocks(self, days_back: int) -> List[str]:
        """Discover stocks with high momentum and volume"""
        discovered = []
        
        try:
            # Use S&P 500 as a starting point for discovery
            sp500 = yf.Ticker("^GSPC")
            sp500_components = self._get_sp500_components()
            
            # Sample from S&P 500 components
            sample_size = min(50, len(sp500_components))
            sampled_stocks = random.sample(sp500_components, sample_size)
            
            for symbol in sampled_stocks:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period=f"{days_back + 2}d")
                    
                    if not hist.empty and len(hist) > 1:
                        # Check for momentum
                        recent_volume = hist['Volume'].iloc[-1]
                        avg_volume = hist['Volume'].mean()
                        price_change = abs((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0])
                        
                        # Add if meets momentum criteria
                        if recent_volume > avg_volume * 0.8 or price_change > 0.015:  # 1.5% movement
                            discovered.append(symbol)
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Momentum discovery failed: {e}")
        
        return discovered
    
    def _discover_by_market_cap(self) -> List[str]:
        """Discover stocks by market capitalization"""
        discovered = []
        
        try:
            # Try to get large cap stocks
            large_cap_symbols = self._get_large_cap_stocks()
            discovered.extend(large_cap_symbols)
            
            # Try to get mid cap stocks
            mid_cap_symbols = self._get_mid_cap_stocks()
            discovered.extend(mid_cap_symbols)
            
        except Exception as e:
            print(f"⚠️ Market cap discovery failed: {e}")
        
        return discovered
    
    def _get_sp500_components(self) -> List[str]:
        """Get S&P 500 components dynamically"""
        try:
            # Try to get S&P 500 components from Wikipedia
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                table = soup.find('table', {'class': 'wikitable'})
                
                if table:
                    symbols = []
                    rows = table.find_all('tr')[1:]  # Skip header
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) > 0:
                            symbol = cells[0].text.strip()
                            if symbol and len(symbol) <= 5:
                                symbols.append(symbol)
                    return symbols[:100]  # Return first 100
        except:
            pass
        
        # Fallback: return some common large cap stocks
        return ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'JPM', 'JNJ']
    
    def _get_large_cap_stocks(self) -> List[str]:
        """Get large cap stocks dynamically"""
        try:
            # Try to get from a financial API or website
            url = "https://finance.yahoo.com/screener/predefined/large_cap"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                symbols = re.findall(r'[A-Z]{1,5}\.[A-Z]{2}|[A-Z]{1,5}', response.text)
                return symbols[:20]
        except:
            pass
        
        return []
    
    def _get_mid_cap_stocks(self) -> List[str]:
        """Get mid cap stocks dynamically"""
        try:
            # Try to get from a financial API or website
            url = "https://finance.yahoo.com/screener/predefined/mid_cap"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                symbols = re.findall(r'[A-Z]{1,5}\.[A-Z]{2}|[A-Z]{1,5}', response.text)
                return symbols[:20]
        except:
            pass
        
        return []
    
    def _discover_sector_indices(self) -> Dict[str, str]:
        """Dynamically discover sector indices in parallel"""
        discovered_sectors = {}
        
        def fetch_sector_info(etf):
            try:
                ticker = yf.Ticker(etf)
                info = ticker.info
                if info and 'longName' in info:
                    return etf, info['longName']
            except:
                pass
            return None
        
        try:
            # Sector ETFs to check
            sector_etfs = [
                'XLK', 'XLF', 'XLE', 'XLV', 'XLI', 'XLP', 'XLY', 'XLU', 'XLRE', 'XLB',
                'VGT', 'VFH', 'VDE', 'VHT', 'VIS', 'VDC', 'VCR', 'VPU', 'VNQ', 'VAW'
            ]
            
            # Indian sector indices
            indian_sectors = [
                '^NSEBANK', '^CNXIT', '^CNXPHARMA', '^CNXMETAL', '^CNXFMCG',
                '^CNXAUTO', '^CNXREALTY', '^CNXMEDIA', '^CNXENERGY', '^CNXINFRA'
            ]
            
            all_sectors = sector_etfs + indian_sectors
            
            # Use ThreadPoolExecutor for parallel discovery
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_sector = {executor.submit(fetch_sector_info, sector): sector for sector in all_sectors}
                
                # Collect results as they complete
                for future in as_completed(future_to_sector):
                    result = future.result()
                    if result:
                        symbol, name = result
                        discovered_sectors[symbol] = name
                    
        except Exception as e:
            print(f"⚠️ Sector discovery failed: {e}")
        
        return discovered_sectors
    
    def _discover_market_indices(self) -> Dict[str, str]:
        """Dynamically discover market indices in parallel"""
        discovered_indices = {}
        
        def fetch_index_info(index):
            try:
                ticker = yf.Ticker(index)
                info = ticker.info
                if info and 'longName' in info:
                    return index, info['longName']
            except:
                pass
            return None
        
        try:
            # Global indices
            global_indices = [
                '^GSPC', '^DJI', '^IXIC', '^RUT', '^VIX', '^FTSE', '^GDAXI', '^FCHI'
            ]
            
            # Indian indices
            indian_indices = ['^NSEI', '^BSESN']
            
            all_indices = global_indices + indian_indices
            
            # Use ThreadPoolExecutor for parallel discovery
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_index = {executor.submit(fetch_index_info, index): index for index in all_indices}
                
                # Collect results as they complete
                for future in as_completed(future_to_index):
                    result = future.result()
                    if result:
                        symbol, name = result
                        discovered_indices[symbol] = name
                    
        except Exception as e:
            print(f"⚠️ Index discovery failed: {e}")
        
        return discovered_indices
    
    def _fetch_stock_data_parallel(self, symbols: List[str], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Fetch stock data in parallel"""
        stock_data = {}
        
        def fetch_single_stock(symbol):
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty and len(hist) > 1:
                    info = ticker.info
                    company_name = info.get('longName', symbol)
                    sector = info.get('sector', 'Unknown')
                    
                    return symbol, {
                        'name': company_name,
                        'sector': sector,
                        'data': hist
                    }
            except Exception as e:
                print(f"⚠️ Could not get data for {symbol}: {e}")
            return None
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_symbol = {executor.submit(fetch_single_stock, symbol): symbol for symbol in symbols}
            
            # Collect results as they complete
            for future in as_completed(future_to_symbol):
                result = future.result()
                if result:
                    symbol, data = result
                    stock_data[symbol] = data
        
        return stock_data
    
    def _fetch_sector_data_parallel(self, sectors: Dict[str, str], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Fetch sector data in parallel"""
        sector_data = {}
        
        def fetch_single_sector(symbol, sector_name):
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                if not hist.empty and len(hist) > 1:
                    return symbol, {
                        'name': sector_name,
                        'data': hist
                    }
            except Exception as e:
                print(f"⚠️ Could not get sector data for {symbol}: {e}")
            return None
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
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