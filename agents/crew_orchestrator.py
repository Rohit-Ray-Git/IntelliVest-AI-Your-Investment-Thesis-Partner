"""
🚀 Crew Orchestrator - Multi-Agent Investment Analysis System
===========================================================

This orchestrator coordinates all individual agents to perform comprehensive
investment analysis including research, sentiment, valuation, thesis generation,
critique, and cryptocurrency analysis with dynamic web search capabilities.
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import all individual agents
from agents.research_agent import ResearchAgent
from agents.sentiment_agent import SentimentAgent
from agents.valuation_agent import ValuationAgent
from agents.thesis_agent import ThesisAgent
from agents.critique_agent import CritiqueAgent
from agents.crypto_agent import CryptoAgent

class CrewOrchestrator:
    """🚀 Crew Orchestrator for multi-agent investment analysis"""
    
    def __init__(self):
        self.name = "Investment Analysis Crew"
        self.description = "Comprehensive multi-agent investment analysis system"
        
        # Initialize all agents
        self.research_agent = ResearchAgent()
        self.sentiment_agent = SentimentAgent()
        self.valuation_agent = ValuationAgent()
        self.thesis_agent = ThesisAgent()
        self.critique_agent = CritiqueAgent()
        self.crypto_agent = CryptoAgent()
        
        # Analysis history
        self.analysis_history = []
        
    async def run_comprehensive_analysis(self, company_name: str, analysis_type: str = "full") -> Dict[str, Any]:
        """
        Run comprehensive investment analysis using all agents
        
        Args:
            company_name: Name or symbol of the company/cryptocurrency
            analysis_type: Type of analysis ("full", "stock", "crypto", "research", "sentiment", "valuation", "thesis", "critique")
            
        Returns:
            Dictionary containing comprehensive analysis results
        """
        print(f"🚀 Crew Orchestrator: Starting {analysis_type} analysis for {company_name}")
        
        # Initialize analysis result
        analysis_result = {
            "company_name": company_name,
            "analysis_type": analysis_type,
            "timestamp": datetime.now().isoformat(),
            "research_analysis": {},
            "sentiment_analysis": {},
            "valuation_analysis": {},
            "thesis_analysis": {},
            "critique_analysis": {},
            "crypto_analysis": {},
            "summary": "",
            "recommendation": "",
            "confidence_score": 0.0,
            "execution_time": 0.0,
            "status": "completed"
        }
        
        start_time = datetime.now()
        
        try:
            # Determine if this is a cryptocurrency analysis
            is_crypto = self._is_cryptocurrency(company_name)
            
            if analysis_type == "full":
                if is_crypto:
                    # Run comprehensive crypto analysis
                    await self._run_crypto_analysis(company_name, analysis_result)
                else:
                    # Run comprehensive stock analysis
                    await self._run_stock_analysis(company_name, analysis_result)
            
            elif analysis_type == "crypto":
                # Run crypto-specific analysis
                await self._run_crypto_analysis(company_name, analysis_result)
            
            elif analysis_type == "stock":
                # Run stock-specific analysis
                await self._run_stock_analysis(company_name, analysis_result)
            
            elif analysis_type == "research":
                # Run research-only analysis
                await self._run_research_only(company_name, analysis_result)
            
            elif analysis_type == "sentiment":
                # Run sentiment-only analysis
                await self._run_sentiment_only(company_name, analysis_result)
            
            elif analysis_type == "valuation":
                # Run valuation-only analysis
                await self._run_valuation_only(company_name, analysis_result)
            
            elif analysis_type == "thesis":
                # Run thesis-only analysis
                await self._run_thesis_only(company_name, analysis_result)
            
            elif analysis_type == "critique":
                # Run critique-only analysis
                await self._run_critique_only(company_name, analysis_result)
            
            # Generate summary and recommendation
            await self._generate_summary_and_recommendation(analysis_result)
            
            # Calculate execution time
            end_time = datetime.now()
            analysis_result["execution_time"] = (end_time - start_time).total_seconds()
            
            # Add to history
            self.analysis_history.append(analysis_result)
            
            print(f"✅ Crew Orchestrator: Completed {analysis_type} analysis for {company_name}")
            return analysis_result
            
        except Exception as e:
            print(f"❌ Crew Orchestrator: Error during analysis - {str(e)}")
            analysis_result["status"] = "failed"
            analysis_result["error"] = str(e)
            return analysis_result
    
    async def _run_stock_analysis(self, company_name: str, analysis_result: Dict[str, Any]):
        """Run comprehensive stock analysis"""
        print("📈 Running comprehensive stock analysis...")
        
        # 1. Research Analysis
        print("🔍 Step 1: Research Analysis")
        research_data = await self.research_agent.research_company(company_name)
        analysis_result["research_analysis"] = research_data
        
        # 2. Sentiment Analysis
        print("🧠 Step 2: Sentiment Analysis")
        sentiment_data = await self.sentiment_agent.analyze_sentiment(company_name, research_data)
        analysis_result["sentiment_analysis"] = sentiment_data
        
        # 3. Valuation Analysis
        print("💰 Step 3: Valuation Analysis")
        valuation_data = await self.valuation_agent.perform_valuation(company_name, research_data)
        analysis_result["valuation_analysis"] = valuation_data
        
        # 4. Thesis Generation
        print("📝 Step 4: Thesis Generation")
        thesis_data = await self.thesis_agent.generate_thesis(company_name, research_data, sentiment_data, valuation_data)
        analysis_result["thesis_analysis"] = thesis_data
        
        # 5. Critique Analysis
        print("🔍 Step 5: Critique Analysis")
        critique_data = await self.critique_agent.critique_thesis(company_name, thesis_data, research_data, sentiment_data, valuation_data)
        analysis_result["critique_analysis"] = critique_data
    
    async def _run_crypto_analysis(self, crypto_name: str, analysis_result: Dict[str, Any]):
        """Run comprehensive cryptocurrency analysis"""
        print("🪙 Running comprehensive cryptocurrency analysis...")
        
        # 1. Crypto Analysis
        print("🪙 Step 1: Cryptocurrency Analysis")
        crypto_data = await self.crypto_agent.analyze_cryptocurrency(crypto_name)
        analysis_result["crypto_analysis"] = crypto_data
        
        # 2. Research Analysis (for additional context)
        print("🔍 Step 2: Research Analysis")
        research_data = await self.research_agent.research_company(crypto_name)
        analysis_result["research_analysis"] = research_data
        
        # 3. Sentiment Analysis
        print("🧠 Step 3: Sentiment Analysis")
        sentiment_data = await self.sentiment_agent.analyze_sentiment(crypto_name, research_data)
        analysis_result["sentiment_analysis"] = sentiment_data
        
        # 4. Thesis Generation (crypto-focused)
        print("📝 Step 4: Thesis Generation")
        thesis_data = await self.thesis_agent.generate_thesis(crypto_name, research_data, sentiment_data, crypto_data)
        analysis_result["thesis_analysis"] = thesis_data
        
        # 5. Critique Analysis
        print("🔍 Step 5: Critique Analysis")
        critique_data = await self.critique_agent.critique_thesis(crypto_name, thesis_data, research_data, sentiment_data, crypto_data)
        analysis_result["critique_analysis"] = critique_data
    
    async def _run_research_only(self, company_name: str, analysis_result: Dict[str, Any]):
        """Run research-only analysis"""
        print("🔍 Running research-only analysis...")
        research_data = await self.research_agent.research_company(company_name)
        analysis_result["research_analysis"] = research_data
    
    async def _run_sentiment_only(self, company_name: str, analysis_result: Dict[str, Any]):
        """Run sentiment-only analysis"""
        print("🧠 Running sentiment-only analysis...")
        sentiment_data = await self.sentiment_agent.analyze_sentiment(company_name)
        analysis_result["sentiment_analysis"] = sentiment_data
    
    async def _run_valuation_only(self, company_name: str, analysis_result: Dict[str, Any]):
        """Run valuation-only analysis"""
        print("💰 Running valuation-only analysis...")
        valuation_data = await self.valuation_agent.perform_valuation(company_name)
        analysis_result["valuation_analysis"] = valuation_data
    
    async def _run_thesis_only(self, company_name: str, analysis_result: Dict[str, Any]):
        """Run thesis-only analysis"""
        print("📝 Running thesis-only analysis...")
        # For thesis-only, we need some basic data
        research_data = await self.research_agent.research_company(company_name)
        sentiment_data = await self.sentiment_agent.analyze_sentiment(company_name, research_data)
        valuation_data = await self.valuation_agent.perform_valuation(company_name, research_data)
        
        thesis_data = await self.thesis_agent.generate_thesis(company_name, research_data, sentiment_data, valuation_data)
        analysis_result["thesis_analysis"] = thesis_data
    
    async def _run_critique_only(self, company_name: str, analysis_result: Dict[str, Any]):
        """Run critique-only analysis"""
        print("🔍 Running critique-only analysis...")
        # For critique-only, we need a thesis to critique
        research_data = await self.research_agent.research_company(company_name)
        sentiment_data = await self.sentiment_agent.analyze_sentiment(company_name, research_data)
        valuation_data = await self.valuation_agent.perform_valuation(company_name, research_data)
        thesis_data = await self.thesis_agent.generate_thesis(company_name, research_data, sentiment_data, valuation_data)
        
        critique_data = await self.critique_agent.critique_thesis(company_name, thesis_data, research_data, sentiment_data, valuation_data)
        analysis_result["critique_analysis"] = critique_data
    
    async def _generate_summary_and_recommendation(self, analysis_result: Dict[str, Any]):
        """Generate summary and recommendation based on all analysis"""
        try:
            # Extract key data from analysis
            research_data = analysis_result.get("research_analysis", {})
            sentiment_data = analysis_result.get("sentiment_analysis", {})
            valuation_data = analysis_result.get("valuation_analysis", {})
            thesis_data = analysis_result.get("thesis_analysis", {})
            critique_data = analysis_result.get("critique_analysis", {})
            crypto_data = analysis_result.get("crypto_analysis", {})
            
            # Generate summary
            summary = self._create_analysis_summary(
                analysis_result["company_name"],
                analysis_result["analysis_type"],
                research_data,
                sentiment_data,
                valuation_data,
                thesis_data,
                critique_data,
                crypto_data
            )
            analysis_result["summary"] = summary
            
            # Generate recommendation
            recommendation = self._create_recommendation(
                thesis_data,
                critique_data,
                sentiment_data,
                valuation_data
            )
            analysis_result["recommendation"] = recommendation
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(
                thesis_data,
                critique_data,
                sentiment_data,
                valuation_data
            )
            analysis_result["confidence_score"] = confidence_score
            
        except Exception as e:
            print(f"❌ Error generating summary and recommendation: {e}")
            analysis_result["summary"] = "Summary generation failed"
            analysis_result["recommendation"] = "Recommendation generation failed"
            analysis_result["confidence_score"] = 0.0
    
    def _create_analysis_summary(self, company_name: str, analysis_type: str, 
                               research_data: Dict, sentiment_data: Dict, valuation_data: Dict,
                               thesis_data: Dict, critique_data: Dict, crypto_data: Dict) -> str:
        """Create analysis summary"""
        summary = f"""
# 📊 Investment Analysis Summary for {company_name}

## 🎯 Analysis Type: {analysis_type.upper()}

## 📋 Key Findings:

"""
        
        if research_data:
            summary += f"""
### 🔍 Research Analysis:
- Company Overview: {research_data.get('company_name', 'N/A')}
- Business Model: {research_data.get('business_analysis', 'N/A')[:200]}...
- Competitive Landscape: {research_data.get('competitive_landscape', 'N/A')[:200]}...
"""
        
        if sentiment_data:
            summary += f"""
### 🧠 Sentiment Analysis:
- Market Mood: {sentiment_data.get('market_mood', 'N/A')[:200]}...
- Sentiment Score: {sentiment_data.get('sentiment_score', 'N/A')}
- Sentiment Trend: {sentiment_data.get('sentiment_trend', 'N/A')[:200]}...
"""
        
        if valuation_data:
            summary += f"""
### 💰 Valuation Analysis:
- Fair Value Estimate: {valuation_data.get('fair_value_estimate', 'N/A')[:200]}...
- Valuation Range: {valuation_data.get('valuation_range', 'N/A')[:200]}...
"""
        
        if thesis_data:
            summary += f"""
### 📝 Investment Thesis:
- Recommendation: {thesis_data.get('investment_recommendation', 'N/A')[:200]}...
- Thesis Strength: {thesis_data.get('thesis_strength', 'N/A')}
- Confidence Level: {thesis_data.get('confidence_level', 'N/A')}
"""
        
        if critique_data:
            summary += f"""
### 🔍 Critique Analysis:
- Validation Status: {critique_data.get('validation_status', 'N/A')}
- Critique Score: {critique_data.get('critique_score', 'N/A')}
"""
        
        if crypto_data:
            summary += f"""
### 🪙 Cryptocurrency Analysis:
- Market Analysis: {crypto_data.get('market_analysis', 'N/A')[:200]}...
- Investment Potential: {crypto_data.get('investment_potential', 'N/A')[:200]}...
"""
        
        summary += f"""
## 📅 Analysis Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*Generated by IntelliVest AI - Advanced Agentic Investment Analysis System*
"""
        
        return summary
    
    def _create_recommendation(self, thesis_data: Dict, critique_data: Dict,
                             sentiment_data: Dict, valuation_data: Dict) -> str:
        """Create investment recommendation"""
        try:
            # Extract key recommendation data
            thesis_recommendation = thesis_data.get('investment_recommendation', '')
            critique_status = critique_data.get('validation_status', '')
            sentiment_score = sentiment_data.get('sentiment_score', 0.0)
            thesis_strength = thesis_data.get('thesis_strength', 0.0)
            
            recommendation = f"""
# 🎯 Investment Recommendation

## 📊 Analysis Summary:
- **Thesis Recommendation**: {thesis_recommendation[:300]}...
- **Validation Status**: {critique_status}
- **Sentiment Score**: {sentiment_score}
- **Thesis Strength**: {thesis_strength}/10

## 🚀 Final Recommendation:
"""
            
            # Determine final recommendation based on multiple factors
            if thesis_strength >= 7.0 and sentiment_score >= 0.3 and critique_status == "Validated":
                recommendation += "**STRONG BUY** - High confidence in investment thesis with positive sentiment and validated analysis."
            elif thesis_strength >= 6.0 and sentiment_score >= 0.0:
                recommendation += "**BUY** - Good investment opportunity with solid fundamentals."
            elif thesis_strength >= 5.0:
                recommendation += "**HOLD** - Neutral position with mixed signals."
            elif thesis_strength >= 4.0:
                recommendation += "**WEAK HOLD** - Cautious position with some concerns."
            else:
                recommendation += "**SELL** - Significant concerns outweigh positive factors."
            
            return recommendation
            
        except Exception as e:
            return f"Recommendation generation failed: {str(e)}"
    
    def _calculate_confidence_score(self, thesis_data: Dict, critique_data: Dict,
                                  sentiment_data: Dict, valuation_data: Dict) -> float:
        """Calculate overall confidence score"""
        try:
            # Extract scores
            thesis_strength = thesis_data.get('thesis_strength', 5.0)
            critique_score = critique_data.get('critique_score', 5.0)
            sentiment_score = abs(sentiment_data.get('sentiment_score', 0.0)) * 10  # Convert to 0-10 scale
            
            # Calculate weighted average
            confidence_score = (thesis_strength * 0.4 + critique_score * 0.3 + sentiment_score * 0.3)
            
            return round(confidence_score, 2)
            
        except Exception as e:
            return 5.0  # Default neutral score
    
    def _is_cryptocurrency(self, name: str) -> bool:
        """Determine if the input is a cryptocurrency"""
        # Common cryptocurrency keywords
        crypto_keywords = [
            'bitcoin', 'btc', 'ethereum', 'eth', 'binance', 'bnb', 'cardano', 'ada',
            'solana', 'sol', 'polkadot', 'dot', 'chainlink', 'link', 'litecoin', 'ltc',
            'ripple', 'xrp', 'dogecoin', 'doge', 'shiba', 'shib', 'avalanche', 'avax',
            'polygon', 'matic', 'cosmos', 'atom', 'uniswap', 'uni', 'aave', 'aave'
        ]
        
        name_lower = name.lower()
        return any(keyword in name_lower for keyword in crypto_keywords)
    
    def get_analysis_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent analysis history"""
        return self.analysis_history[-limit:] if self.analysis_history else []
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "research_agent": "Active",
            "sentiment_agent": "Active", 
            "valuation_agent": "Active",
            "thesis_agent": "Active",
            "critique_agent": "Active",
            "crypto_agent": "Active",
            "total_analyses": len(self.analysis_history),
            "system_status": "Operational"
        }

# Export the orchestrator
__all__ = ['CrewOrchestrator'] 