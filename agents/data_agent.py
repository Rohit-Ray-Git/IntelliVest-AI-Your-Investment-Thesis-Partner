# data_agent.py
# agents/financial_data_agent.py

import yfinance as yf

class FinancialDataAgent:
    def __init__(self):
        pass

    def fetch_summary(self, ticker: str):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            summary = {
                "Company Name": info.get("longName"),
                "Ticker": ticker.upper(),
                "Sector": info.get("sector"),
                "Industry": info.get("industry"),
                "Market Cap": info.get("marketCap"),
                "Current Price": info.get("currentPrice"),
                "P/E Ratio": info.get("trailingPE"),
                "EPS": info.get("trailingEps"),
                "52 Week High": info.get("fiftyTwoWeekHigh"),
                "52 Week Low": info.get("fiftyTwoWeekLow"),
                "Dividend Yield": info.get("dividendYield"),
                "Beta": info.get("beta"),
                "Website": info.get("website"),
                "Description": info.get("longBusinessSummary"),
            }

            return summary

        except Exception as e:
            print(f"❌ Error fetching financial data for {ticker}: {e}")
            return None


# For testing
if __name__ == "__main__":
    agent = FinancialDataAgent()
    result = agent.fetch_summary("AAPL")  # Apple Inc.
    for k, v in result.items():
        print(f"{k}: {v}")
