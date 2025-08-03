"""
🪙 Crypto Agent - Cryptocurrency Analysis & Research
===================================================

This agent handles comprehensive cryptocurrency analysis including:
- Cryptocurrency price and market cap analysis
- Trading volume and institutional adoption research
- Blockchain technology development tracking
- Market sentiment and news analysis
- Institutional investment data gathering
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools
from tools.dynamic_search_tools import CryptoDataTool, DynamicWebSearchTool
from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType

class CryptoAgent:
    """🪙 Crypto Agent for cryptocurrency analysis"""
    
    def __init__(self):
        self.name = "Cryptocurrency Analyst"
        self.role = "Cryptocurrency and blockchain analysis"
        self.backstory = """
        You are an expert cryptocurrency analyst with 8+ years of experience in blockchain technology.
        You specialize in comprehensive cryptocurrency analysis including:
        - Cryptocurrency market dynamics and trends
        - Blockchain technology assessment and innovation
        - Tokenomics and token economics analysis
        - DeFi (Decentralized Finance) ecosystem analysis
        - NFT (Non-Fungible Token) market analysis
        - Regulatory environment and adoption trends
        
        You use dynamic web search to find the latest cryptocurrency data and information
        from live, publicly available sources. You understand the rapidly evolving nature
        of the crypto market and always seek the most current information.
        """
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool(),
            CryptoDataTool()
        ]
        
        # Initialize advanced fallback system
        self.fallback_system = AdvancedFallbackSystem()
        
    async def analyze_cryptocurrency(self, crypto_name: str) -> Dict[str, Any]:
        """
        Perform comprehensive cryptocurrency analysis
        
        Args:
            crypto_name: Name or symbol of the cryptocurrency to analyze
            
        Returns:
            Dictionary containing comprehensive cryptocurrency analysis
        """
        print(f"🪙 Crypto Agent: Starting cryptocurrency analysis for {crypto_name}")
        
        crypto_data = {
            "crypto_name": crypto_name,
            "market_analysis": {},
            "blockchain_analysis": {},
            "tokenomics_analysis": {},
            "defi_analysis": {},
            "nft_analysis": {},
            "regulatory_analysis": "",
            "adoption_trends": "",
            "investment_potential": "",
            "risk_assessment": "",
            "technical_analysis": "",
            "data_sources": []
        }
        
        try:
            # 1. Analyze cryptocurrency market data
            print("📊 Analyzing cryptocurrency market data...")
            market_analysis = await self._analyze_market_data(crypto_name)
            crypto_data["market_analysis"] = market_analysis
            
            # 2. Analyze blockchain technology
            print("🔗 Analyzing blockchain technology...")
            blockchain_analysis = await self._analyze_blockchain_technology(crypto_name)
            crypto_data["blockchain_analysis"] = blockchain_analysis
            
            # 3. Analyze tokenomics
            print("💰 Analyzing tokenomics...")
            tokenomics_analysis = await self._analyze_tokenomics(crypto_name)
            crypto_data["tokenomics_analysis"] = tokenomics_analysis
            
            # 4. Analyze DeFi ecosystem
            print("🏦 Analyzing DeFi ecosystem...")
            defi_analysis = await self._analyze_defi_ecosystem(crypto_name)
            crypto_data["defi_analysis"] = defi_analysis
            
            # 5. Analyze NFT market
            print("🎨 Analyzing NFT market...")
            nft_analysis = await self._analyze_nft_market(crypto_name)
            crypto_data["nft_analysis"] = nft_analysis
            
            # 6. Analyze regulatory environment
            print("📋 Analyzing regulatory environment...")
            regulatory_analysis = await self._analyze_regulatory_environment(crypto_name)
            crypto_data["regulatory_analysis"] = regulatory_analysis
            
            # 7. Analyze adoption trends
            print("📈 Analyzing adoption trends...")
            adoption_trends = await self._analyze_adoption_trends(crypto_name)
            crypto_data["adoption_trends"] = adoption_trends
            
            # 8. Assess investment potential
            print("🎯 Assessing investment potential...")
            investment_potential = await self._assess_investment_potential(crypto_name, crypto_data)
            crypto_data["investment_potential"] = investment_potential
            
            # 9. Assess risks
            print("⚠️ Assessing risks...")
            risk_assessment = await self._assess_risks(crypto_name, crypto_data)
            crypto_data["risk_assessment"] = risk_assessment
            
            # 10. Perform technical analysis
            print("📉 Performing technical analysis...")
            technical_analysis = await self._perform_technical_analysis(crypto_name, crypto_data)
            crypto_data["technical_analysis"] = technical_analysis
            
            print(f"✅ Crypto Agent: Completed cryptocurrency analysis for {crypto_name}")
            return crypto_data
            
        except Exception as e:
            print(f"❌ Crypto Agent: Error during cryptocurrency analysis - {str(e)}")
            return crypto_data
    
    async def _analyze_market_data(self, crypto_name: str) -> Dict[str, Any]:
        """Analyze cryptocurrency market data"""
        try:
            # Use crypto data tool
            crypto_tool = CryptoDataTool()
            basic_crypto_data = crypto_tool._run(crypto_name)
            
            # Use dynamic search for additional market data
            search_tool = DynamicWebSearchTool()
            market_queries = [
                f"{crypto_name} cryptocurrency market cap price",
                f"{crypto_name} crypto trading volume market data",
                f"{crypto_name} cryptocurrency price history chart",
                f"{crypto_name} crypto market performance analysis"
            ]
            
            additional_market_data = {}
            for query in market_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    additional_market_data[query] = result
            
            return {
                "basic_data": basic_crypto_data,
                "additional_market_data": additional_market_data
            }
            
        except Exception as e:
            print(f"❌ Error analyzing market data: {e}")
            return {}
    
    async def _analyze_blockchain_technology(self, crypto_name: str) -> Dict[str, Any]:
        """Analyze blockchain technology and innovation"""
        try:
            search_tool = DynamicWebSearchTool()
            blockchain_queries = [
                f"{crypto_name} blockchain technology innovation",
                f"{crypto_name} consensus mechanism algorithm",
                f"{crypto_name} blockchain scalability solutions",
                f"{crypto_name} smart contracts development"
            ]
            
            blockchain_data = {}
            for query in blockchain_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    blockchain_data[query] = result
            
            # Use AI to analyze blockchain technology
            prompt = f"""
            Analyze the blockchain technology for {crypto_name} based on:
            
            Blockchain Data: {blockchain_data}
            
            Provide analysis covering:
            1. Consensus Mechanism: How the blockchain achieves consensus
            2. Scalability: Current and planned scaling solutions
            3. Security: Security features and vulnerabilities
            4. Innovation: Unique technological features
            5. Development Activity: Ongoing development and updates
            6. Technical Architecture: Overall technical design
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.RESEARCH,
                max_fallbacks=3
            )
            
            return {
                "blockchain_analysis": result.content if result else "Blockchain analysis not available",
                "blockchain_data": blockchain_data
            }
            
        except Exception as e:
            print(f"❌ Error analyzing blockchain technology: {e}")
            return {"blockchain_analysis": "Blockchain analysis failed", "blockchain_data": {}}
    
    async def _analyze_tokenomics(self, crypto_name: str) -> Dict[str, Any]:
        """Analyze tokenomics and token economics"""
        try:
            search_tool = DynamicWebSearchTool()
            tokenomics_queries = [
                f"{crypto_name} tokenomics token economics",
                f"{crypto_name} token supply distribution",
                f"{crypto_name} token utility use cases",
                f"{crypto_name} token burning staking rewards"
            ]
            
            tokenomics_data = {}
            for query in tokenomics_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    tokenomics_data[query] = result
            
            # Use AI to analyze tokenomics
            prompt = f"""
            Analyze the tokenomics for {crypto_name} based on:
            
            Tokenomics Data: {tokenomics_data}
            
            Provide analysis covering:
            1. Token Supply: Total supply, circulating supply, and distribution
            2. Token Utility: Use cases and value proposition
            3. Token Economics: Inflation/deflation mechanisms
            4. Token Distribution: Allocation and vesting schedules
            5. Token Governance: Voting and governance mechanisms
            6. Token Value Drivers: Factors affecting token value
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.RESEARCH,
                max_fallbacks=3
            )
            
            return {
                "tokenomics_analysis": result.content if result else "Tokenomics analysis not available",
                "tokenomics_data": tokenomics_data
            }
            
        except Exception as e:
            print(f"❌ Error analyzing tokenomics: {e}")
            return {"tokenomics_analysis": "Tokenomics analysis failed", "tokenomics_data": {}}
    
    async def _analyze_defi_ecosystem(self, crypto_name: str) -> Dict[str, Any]:
        """Analyze DeFi ecosystem and applications"""
        try:
            search_tool = DynamicWebSearchTool()
            defi_queries = [
                f"{crypto_name} DeFi decentralized finance",
                f"{crypto_name} DeFi protocols applications",
                f"{crypto_name} yield farming liquidity mining",
                f"{crypto_name} DeFi ecosystem growth"
            ]
            
            defi_data = {}
            for query in defi_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    defi_data[query] = result
            
            # Use AI to analyze DeFi ecosystem
            prompt = f"""
            Analyze the DeFi ecosystem for {crypto_name} based on:
            
            DeFi Data: {defi_data}
            
            Provide analysis covering:
            1. DeFi Protocols: Major protocols and applications
            2. Total Value Locked (TVL): DeFi ecosystem size
            3. Yield Opportunities: Staking and farming options
            4. DeFi Innovation: Unique DeFi features
            5. Ecosystem Growth: Adoption and development trends
            6. DeFi Risks: Smart contract and protocol risks
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.RESEARCH,
                max_fallbacks=3
            )
            
            return {
                "defi_analysis": result.content if result else "DeFi analysis not available",
                "defi_data": defi_data
            }
            
        except Exception as e:
            print(f"❌ Error analyzing DeFi ecosystem: {e}")
            return {"defi_analysis": "DeFi analysis failed", "defi_data": {}}
    
    async def _analyze_nft_market(self, crypto_name: str) -> Dict[str, Any]:
        """Analyze NFT market and applications"""
        try:
            search_tool = DynamicWebSearchTool()
            nft_queries = [
                f"{crypto_name} NFT non-fungible tokens",
                f"{crypto_name} NFT marketplace collections",
                f"{crypto_name} NFT trading volume sales",
                f"{crypto_name} NFT use cases applications"
            ]
            
            nft_data = {}
            for query in nft_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    nft_data[query] = result
            
            # Use AI to analyze NFT market
            prompt = f"""
            Analyze the NFT market for {crypto_name} based on:
            
            NFT Data: {nft_data}
            
            Provide analysis covering:
            1. NFT Collections: Popular collections and creators
            2. Trading Volume: NFT market activity
            3. NFT Use Cases: Gaming, art, collectibles, etc.
            4. NFT Innovation: Unique NFT features
            5. Market Trends: NFT market dynamics
            6. NFT Ecosystem: Marketplace and infrastructure
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.RESEARCH,
                max_fallbacks=3
            )
            
            return {
                "nft_analysis": result.content if result else "NFT analysis not available",
                "nft_data": nft_data
            }
            
        except Exception as e:
            print(f"❌ Error analyzing NFT market: {e}")
            return {"nft_analysis": "NFT analysis failed", "nft_data": {}}
    
    async def _analyze_regulatory_environment(self, crypto_name: str) -> str:
        """Analyze regulatory environment and compliance"""
        try:
            search_tool = DynamicWebSearchTool()
            regulatory_queries = [
                f"{crypto_name} cryptocurrency regulation compliance",
                f"{crypto_name} crypto legal status countries",
                f"{crypto_name} cryptocurrency tax implications",
                f"{crypto_name} crypto regulatory developments"
            ]
            
            regulatory_data = []
            for query in regulatory_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    regulatory_data.append(result)
            
            # Use AI to analyze regulatory environment
            prompt = f"""
            Analyze the regulatory environment for {crypto_name} based on:
            
            Regulatory Data: {regulatory_data}
            
            Provide analysis covering:
            1. Legal Status: Current legal status in major jurisdictions
            2. Regulatory Framework: Applicable regulations and compliance requirements
            3. Tax Implications: Tax treatment and implications
            4. Regulatory Risks: Potential regulatory challenges
            5. Compliance Strategy: How the project addresses compliance
            6. Future Regulatory Outlook: Expected regulatory developments
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.RESEARCH,
                max_fallbacks=3
            )
            
            return result.content if result else "Regulatory analysis not available"
            
        except Exception as e:
            print(f"❌ Error analyzing regulatory environment: {e}")
            return "Regulatory analysis failed"
    
    async def _analyze_adoption_trends(self, crypto_name: str) -> str:
        """Analyze adoption trends and market penetration"""
        try:
            search_tool = DynamicWebSearchTool()
            adoption_queries = [
                f"{crypto_name} cryptocurrency adoption trends",
                f"{crypto_name} crypto institutional adoption",
                f"{crypto_name} cryptocurrency user growth",
                f"{crypto_name} crypto merchant adoption"
            ]
            
            adoption_data = []
            for query in adoption_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    adoption_data.append(result)
            
            # Use AI to analyze adoption trends
            prompt = f"""
            Analyze adoption trends for {crypto_name} based on:
            
            Adoption Data: {adoption_data}
            
            Provide analysis covering:
            1. User Adoption: Growth in user base and active users
            2. Institutional Adoption: Corporate and institutional interest
            3. Merchant Adoption: Business acceptance and integration
            4. Geographic Adoption: Regional adoption patterns
            5. Use Case Adoption: Specific use case penetration
            6. Adoption Barriers: Challenges to widespread adoption
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.RESEARCH,
                max_fallbacks=3
            )
            
            return result.content if result else "Adoption trends analysis not available"
            
        except Exception as e:
            print(f"❌ Error analyzing adoption trends: {e}")
            return "Adoption trends analysis failed"
    
    async def _assess_investment_potential(self, crypto_name: str, crypto_data: Dict[str, Any]) -> str:
        """Assess investment potential of the cryptocurrency"""
        try:
            # Combine all crypto data for investment assessment
            combined_data = {
                "market_analysis": crypto_data.get("market_analysis", {}),
                "blockchain_analysis": crypto_data.get("blockchain_analysis", {}),
                "tokenomics_analysis": crypto_data.get("tokenomics_analysis", {}),
                "defi_analysis": crypto_data.get("defi_analysis", {}),
                "nft_analysis": crypto_data.get("nft_analysis", {}),
                "regulatory_analysis": crypto_data.get("regulatory_analysis", ""),
                "adoption_trends": crypto_data.get("adoption_trends", "")
            }
            
            prompt = f"""
            Assess the investment potential for {crypto_name} based on comprehensive analysis:
            
            Market Analysis: {combined_data['market_analysis']}
            Blockchain Analysis: {combined_data['blockchain_analysis']}
            Tokenomics Analysis: {combined_data['tokenomics_analysis']}
            DeFi Analysis: {combined_data['defi_analysis']}
            NFT Analysis: {combined_data['nft_analysis']}
            Regulatory Analysis: {combined_data['regulatory_analysis']}
            Adoption Trends: {combined_data['adoption_trends']}
            
            Provide investment assessment covering:
            1. Investment Thesis: Key investment rationale
            2. Growth Potential: Upside potential and catalysts
            3. Competitive Position: Market position and advantages
            4. Investment Timeline: Short-term and long-term outlook
            5. Investment Risks: Key risks and challenges
            6. Investment Recommendation: Buy/Hold/Sell with rationale
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.THESIS,
                max_fallbacks=3
            )
            
            return result.content if result else "Investment potential assessment not available"
            
        except Exception as e:
            print(f"❌ Error assessing investment potential: {e}")
            return "Investment potential assessment failed"
    
    async def _assess_risks(self, crypto_name: str, crypto_data: Dict[str, Any]) -> str:
        """Assess risks associated with the cryptocurrency"""
        try:
            # Combine all crypto data for risk assessment
            combined_data = {
                "market_analysis": crypto_data.get("market_analysis", {}),
                "blockchain_analysis": crypto_data.get("blockchain_analysis", {}),
                "tokenomics_analysis": crypto_data.get("tokenomics_analysis", {}),
                "defi_analysis": crypto_data.get("defi_analysis", {}),
                "nft_analysis": crypto_data.get("nft_analysis", {}),
                "regulatory_analysis": crypto_data.get("regulatory_analysis", ""),
                "adoption_trends": crypto_data.get("adoption_trends", "")
            }
            
            prompt = f"""
            Assess the risks for {crypto_name} based on comprehensive analysis:
            
            Market Analysis: {combined_data['market_analysis']}
            Blockchain Analysis: {combined_data['blockchain_analysis']}
            Tokenomics Analysis: {combined_data['tokenomics_analysis']}
            DeFi Analysis: {combined_data['defi_analysis']}
            NFT Analysis: {combined_data['nft_analysis']}
            Regulatory Analysis: {combined_data['regulatory_analysis']}
            Adoption Trends: {combined_data['adoption_trends']}
            
            Provide risk assessment covering:
            1. Technical Risks: Blockchain and smart contract risks
            2. Market Risks: Volatility and market dynamics
            3. Regulatory Risks: Legal and compliance risks
            4. Adoption Risks: User adoption and network effects
            5. Competitive Risks: Competition and market disruption
            6. Operational Risks: Team, development, and execution risks
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.CRITIQUE,
                max_fallbacks=3
            )
            
            return result.content if result else "Risk assessment not available"
            
        except Exception as e:
            print(f"❌ Error assessing risks: {e}")
            return "Risk assessment failed"
    
    async def _perform_technical_analysis(self, crypto_name: str, crypto_data: Dict[str, Any]) -> str:
        """Perform technical analysis of the cryptocurrency"""
        try:
            # Search for technical analysis data
            search_tool = DynamicWebSearchTool()
            technical_queries = [
                f"{crypto_name} cryptocurrency technical analysis",
                f"{crypto_name} crypto price chart patterns",
                f"{crypto_name} cryptocurrency support resistance levels",
                f"{crypto_name} crypto trading indicators signals"
            ]
            
            technical_data = []
            for query in technical_queries:
                result = search_tool._run(query)
                if result and "✅" in result:
                    technical_data.append(result)
            
            # Use AI to perform technical analysis
            prompt = f"""
            Perform technical analysis for {crypto_name} based on:
            
            Technical Data: {technical_data}
            Market Analysis: {crypto_data.get('market_analysis', {})}
            
            Provide technical analysis covering:
            1. Price Action: Current price trends and patterns
            2. Support and Resistance: Key price levels
            3. Technical Indicators: Moving averages, RSI, MACD, etc.
            4. Chart Patterns: Bullish/bearish patterns
            5. Volume Analysis: Trading volume trends
            6. Technical Outlook: Short-term and long-term technical view
            
            Format professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.VALUATION,
                max_fallbacks=3
            )
            
            return result.content if result else "Technical analysis not available"
            
        except Exception as e:
            print(f"❌ Error performing technical analysis: {e}")
            return "Technical analysis failed"

    async def handle_message(self, message):
        """
        Handle incoming messages from other agents
        
        Args:
            message: AgentMessage object containing the message
            
        Returns:
            Response dictionary
        """
        try:
            if message.message_type.value == "data_request":
                return await self._handle_data_request(message)
            elif message.message_type.value == "collaboration_request":
                return await self._handle_collaboration_request(message)
            elif message.message_type.value == "analysis_request":
                return await self._handle_analysis_request(message)
            elif message.message_type.value == "validation_request":
                return await self._handle_validation_request(message)
            else:
                return {
                    "status": "success",
                    "agent": self.name,
                    "message_type": message.message_type.value,
                    "response": f"Processed {message.message_type.value} from {message.sender}"
                }
        except Exception as e:
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e)
            }
    
    async def _handle_data_request(self, message):
        """Handle data requests from other agents"""
        company_name = message.content.get("company_name", "")
        request_type = message.content.get("request_type", "")
        
        if request_type == "crypto_data":
            crypto_data = await self.analyze_cryptocurrency(company_name)
            return {
                "status": "success",
                "agent": self.name,
                "data": crypto_data,
                "data_type": "crypto_data"
            }
        else:
            return {
                "status": "success",
                "agent": self.name,
                "response": f"Provided {request_type} data for {company_name}"
            }
    
    async def _handle_collaboration_request(self, message):
        """Handle collaboration requests from other agents"""
        collaboration_type = message.content.get("collaboration_type", "")
        shared_data = message.content.get("shared_data", {})
        
        return {
            "status": "success",
            "agent": self.name,
            "collaboration_type": collaboration_type,
            "response": f"Collaborating on {collaboration_type}"
        }
    
    async def _handle_analysis_request(self, message):
        """Handle analysis requests from other agents"""
        analysis_type = message.content.get("analysis_type", "")
        data = message.content.get("data", {})
        
        return {
            "status": "success",
            "agent": self.name,
            "analysis_type": analysis_type,
            "response": f"Performed {analysis_type} analysis"
        }
    
    async def _handle_validation_request(self, message):
        """Handle validation requests from other agents"""
        validation_type = message.content.get("validation_type", "")
        data = message.content.get("data", {})
        
        return {
            "status": "success",
            "agent": self.name,
            "validation_type": validation_type,
            "response": f"Validated {validation_type}"
        }

# Export the agent
__all__ = ['CryptoAgent'] 