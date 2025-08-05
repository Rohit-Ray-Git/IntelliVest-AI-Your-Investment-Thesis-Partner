#!/usr/bin/env python3
"""
Test script to debug sector discovery issues
"""
import os
import sys
import re
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tools.market_scanner_tool import DynamicMarketScannerTool

def test_sector_discovery_debug():
    """Debug the sector discovery issue"""
    print("🔍 Debugging Sector Discovery")
    print("=" * 50)
    
    try:
        print("\n🔧 Initializing scanner...")
        scanner = DynamicMarketScannerTool(max_workers=3)
        
        if not scanner.llm and not scanner.groq_llm:
            print("❌ No LLM available")
            return False
        
        print("\n🔍 Testing sector discovery with detailed output...")
        
        # Test the sector discovery method directly
        discovered_sectors = scanner._discover_sector_indices()
        print(f"📊 Discovered {len(discovered_sectors)} sectors")
        
        if discovered_sectors:
            print("✅ Sectors found:")
            for symbol, name in discovered_sectors.items():
                print(f"   - {symbol}: {name}")
        else:
            print("❌ No sectors discovered")
        
        # Always show the raw response for debugging
        print("\n🔍 Testing LLM response directly...")
        
        system_prompt = """You are a sector analyst specializing in Indian markets. Search for Indian sector indices that are currently trending 
        and performing well in the Indian market. Focus on finding Indian sector ETFs and indices that show positive momentum.
        
        Look for:
        - Indian sector indices and ETFs
        - Indian sector-specific indices
        - Focus on Indian markets only
        - Do NOT use any predefined or hardcoded index names
        - Search dynamically for currently trending sector indices"""
        
        user_prompt = """Search for 10 Indian sector indices that are currently trending and performing well in the Indian market. 
        Look for Indian sector ETFs and indices across Indian markets (NSE/BSE). Return the symbols and names.
        Focus ONLY on Indian sector indices. Do NOT use any hardcoded or predefined index names - search dynamically."""
        
        from langchain.schema import HumanMessage, SystemMessage
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = scanner._call_llm_with_fallback(messages, "sector discovery debug")
        
        if response and response.content:
            print(f"\n📝 Raw LLM Response:")
            print("=" * 30)
            print(response.content)
            print("=" * 30)
            
            # Test regex patterns
            print(f"\n🔍 Testing regex patterns:")
            
            # Pattern 1: Stock symbols with .NS or .BO
            sector_symbols = re.findall(r'\b([A-Z]{2,10})\.(NS|BO)\b', response.content)
            print(f"   Pattern 1 (.NS/.BO): {len(sector_symbols)} matches")
            for symbol, suffix in sector_symbols:
                print(f"     - {symbol}.{suffix}")
            
            # Pattern 2: Sector patterns
            sector_patterns = re.findall(r'\b([A-Z]{2,10})\s+(SECTOR|ETF|INDEX)\b', response.content)
            print(f"   Pattern 2 (SECTOR/ETF/INDEX): {len(sector_patterns)} matches")
            for pattern in sector_patterns:
                print(f"     - {pattern[0]} {pattern[1]}")
            
            # Pattern 3: Any capital words that might be sectors
            capital_words = re.findall(r'\b([A-Z]{2,10})\b', response.content)
            print(f"   Pattern 3 (Capital words): {len(capital_words)} matches")
            filtered_words = [word for word in capital_words if word not in ['THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'HAVE', 'WILL', 'BEEN', 'THEY', 'THEIR', 'NS', 'BO', 'SECTOR', 'ETF', 'INDEX']]
            print(f"   Filtered capital words: {filtered_words[:10]}")
            
            # Pattern 4: NIFTY symbols
            nifty_symbols = re.findall(r'\*\*Symbol:\*\*\s*([A-Z0-9]+)', response.content)
            print(f"   Pattern 4 (NIFTY symbols): {len(nifty_symbols)} matches")
            for symbol in nifty_symbols:
                print(f"     - {symbol}")
            
            # Pattern 5: NIFTY patterns
            nifty_patterns = re.findall(r'\b(NIFTY[A-Z0-9]+)\b', response.content)
            print(f"   Pattern 5 (NIFTY patterns): {len(nifty_patterns)} matches")
            for pattern in nifty_patterns:
                print(f"     - {pattern}")
            
            # Pattern 6: Bold text patterns
            bold_patterns = re.findall(r'\*\*([A-Z\s]+)\*\*', response.content)
            print(f"   Pattern 6 (Bold patterns): {len(bold_patterns)} matches")
            for pattern in bold_patterns:
                print(f"     - {pattern}")
            
        else:
            print("❌ No response from LLM")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sector_discovery_debug()
    sys.exit(0 if success else 1) 