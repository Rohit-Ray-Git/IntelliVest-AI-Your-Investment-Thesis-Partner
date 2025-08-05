from tools.market_scanner_tool import DynamicMarketScannerTool

print("🚀 Testing Live Data Market Scanner (No Hardcoding)...")
scanner = DynamicMarketScannerTool()
result = scanner._run(30)

print("\n📊 Live Data Results:")
stocks = result.get('top_performing_stocks', [])
sectors = result.get('top_performing_sectors', [])

print(f"Stocks found: {len(stocks)}")
print(f"Sectors found: {len(sectors)}")

if stocks:
    print("\n🏆 Top Stocks (Live Data):")
    for stock in stocks:
        print(f"- {stock['symbol']}: {stock.get('source', 'unknown')}")

if sectors:
    print("\n🏆 Top Sectors (Live Data):")
    for sector in sectors:
        print(f"- {sector['symbol']}: {sector.get('source', 'unknown')}")

print("\n✅ Live data test completed!") 