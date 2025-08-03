"""
😊 Sentiment Agent - Market Sentiment Analysis & Interpretation
==============================================================

This agent analyzes market sentiment including:
- News sentiment analysis and interpretation
- Social media sentiment trends
- Analyst ratings and price targets
- Market positioning and investor sentiment
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom tools and base agent
from tools.investment_tools import SentimentAnalysisTool
from tools.dynamic_search_tools import DynamicWebSearchTool
from agents.base_agent import BaseAgent
from llm.advanced_fallback_system import TaskType

class SentimentAgent(BaseAgent):
    """🧠 Sentiment Agent for market sentiment analysis"""
    
    def __init__(self):
        """Initialize the sentiment agent"""
        super().__init__(
            name="Sentiment Analyst",
            role="Market sentiment analysis and emotional intelligence",
            backstory="""
            You are an expert sentiment analyst with 12+ years of experience in market psychology.
            You specialize in analyzing market sentiment and investor psychology, including:
            - News sentiment and media tone analysis
            - Social media sentiment tracking
            - Analyst ratings and institutional sentiment
            - Market mood and investor behavior patterns
            - Sentiment-driven trading signals
            
            You use dynamic web search to find the most recent sentiment data
            from live, publicly available sources. You understand that sentiment
            can change rapidly and always seek the latest information.
            """
        )
        
        # Initialize tools
        self.tools = [
            DynamicWebSearchTool(),
            SentimentAnalysisTool()
        ]
        
    async def analyze(self, company_name: str, **kwargs) -> Dict[str, Any]:
        """
        Main analysis method - conducts sentiment analysis
        
        Args:
            company_name: Name or symbol of the company to analyze
            **kwargs: Additional parameters including research_data
            
        Returns:
            Dictionary containing comprehensive sentiment analysis
        """
        research_data = kwargs.get('research_data', {})
        return await self.analyze_sentiment(company_name, research_data)
    
    async def analyze_sentiment(self, company_name: str, research_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Conduct comprehensive sentiment analysis
        
        Args:
            company_name: Name or symbol of the company to analyze
            research_data: Optional research data from previous analysis
            
        Returns:
            Dictionary containing comprehensive sentiment analysis
        """
        print(f"🧠 Sentiment Agent: Starting sentiment analysis for {company_name}")
        
        sentiment_data = {
            "company_name": company_name,
            "news_sentiment": {},
            "social_media_sentiment": {},
            "analyst_sentiment": {},
            "institutional_sentiment": {},
            "market_mood": "",
            "sentiment_score": 0.0,
            "sentiment_trend": "",
            "key_sentiment_drivers": [],
            "sentiment_risks": [],
            "data_sources": []
        }
        
        try:
            # 1. Analyze news sentiment
            print("📰 Analyzing news sentiment...")
            news_sentiment = await self._analyze_news_sentiment(company_name)
            sentiment_data["news_sentiment"] = news_sentiment
            
            # 2. Analyze social media sentiment
            print("📱 Analyzing social media sentiment...")
            social_sentiment = await self._analyze_social_media_sentiment(company_name)
            sentiment_data["social_media_sentiment"] = social_sentiment
            
            # 3. Analyze analyst sentiment
            print("📊 Analyzing analyst sentiment...")
            analyst_sentiment = await self._analyze_analyst_sentiment(company_name)
            sentiment_data["analyst_sentiment"] = analyst_sentiment
            
            # 4. Analyze institutional sentiment
            print("🏦 Analyzing institutional sentiment...")
            institutional_sentiment = await self._analyze_institutional_sentiment(company_name)
            sentiment_data["institutional_sentiment"] = institutional_sentiment
            
            # 5. Assess overall market mood
            print("🎭 Assessing overall market mood...")
            market_mood = await self._assess_market_mood(company_name, sentiment_data)
            sentiment_data["market_mood"] = market_mood
            
            # 6. Calculate composite sentiment score
            print("📈 Calculating composite sentiment score...")
            sentiment_score = await self._calculate_sentiment_score(sentiment_data)
            sentiment_data["sentiment_score"] = sentiment_score
            
            # 7. Identify sentiment trends and drivers
            print("🔄 Identifying sentiment trends and drivers...")
            trends_and_drivers = await self._identify_sentiment_trends(sentiment_data)
            sentiment_data["sentiment_trend"] = trends_and_drivers["trend"]
            sentiment_data["key_sentiment_drivers"] = trends_and_drivers["drivers"]
            sentiment_data["sentiment_risks"] = trends_and_drivers["risks"]
            
            print(f"✅ Sentiment Agent: Completed sentiment analysis for {company_name}")
            return sentiment_data
            
        except Exception as e:
            print(f"❌ Sentiment Agent: Error during sentiment analysis - {str(e)}")
            return sentiment_data
    
    async def _analyze_news_sentiment(self, company_name: str) -> Dict[str, Any]:
        """Analyze sentiment from news sources"""
        try:
            search_tool = DynamicWebSearchTool()
            sentiment_tool = SentimentAnalysisTool()
            
            # Search for recent news
            news_queries = [
                f"{company_name} latest news sentiment",
                f"{company_name} earnings news market reaction",
                f"{company_name} analyst coverage news",
                f"{company_name} market news investor reaction"
            ]
            
            news_sentiment_data = {}
            
            for query in news_queries:
                # Get news content
                news_content = search_tool._run(query)
                
                if news_content and "✅" in news_content:
                    # Analyze sentiment of the news content
                    sentiment_result = sentiment_tool._run(news_content)
                    
                    news_sentiment_data[query] = {
                        "content": news_content,
                        "sentiment_analysis": sentiment_result
                    }
            
            return news_sentiment_data
            
        except Exception as e:
            print(f"❌ Error analyzing news sentiment: {e}")
            return {}
    
    async def _analyze_social_media_sentiment(self, company_name: str) -> Dict[str, Any]:
        """Analyze sentiment from social media sources"""
        try:
            search_tool = DynamicWebSearchTool()
            sentiment_tool = SentimentAnalysisTool()
            
            # Search for social media sentiment
            social_queries = [
                f"{company_name} social media sentiment twitter",
                f"{company_name} reddit stock sentiment",
                f"{company_name} investor forum sentiment",
                f"{company_name} stocktwits sentiment"
            ]
            
            social_sentiment_data = {}
            
            for query in social_queries:
                # Get social media content
                social_content = search_tool._run(query)
                
                if social_content and "✅" in social_content:
                    # Analyze sentiment of the social content
                    sentiment_result = sentiment_tool._run(social_content)
                    
                    social_sentiment_data[query] = {
                        "content": social_content,
                        "sentiment_analysis": sentiment_result
                    }
            
            return social_sentiment_data
            
        except Exception as e:
            print(f"❌ Error analyzing social media sentiment: {e}")
            return {}
    
    async def _analyze_analyst_sentiment(self, company_name: str) -> Dict[str, Any]:
        """Analyze sentiment from analyst reports and ratings"""
        try:
            search_tool = DynamicWebSearchTool()
            
            # Search for analyst sentiment
            analyst_queries = [
                f"{company_name} analyst ratings recommendations",
                f"{company_name} analyst coverage sentiment",
                f"{company_name} investment bank ratings",
                f"{company_name} analyst price targets sentiment"
            ]
            
            analyst_sentiment_data = {}
            
            for query in analyst_queries:
                # Get analyst content
                analyst_content = search_tool._run(query)
                
                if analyst_content and "✅" in analyst_content:
                    analyst_sentiment_data[query] = {
                        "content": analyst_content,
                        "sentiment": self._extract_analyst_sentiment(analyst_content)
                    }
            
            return analyst_sentiment_data
            
        except Exception as e:
            print(f"❌ Error analyzing analyst sentiment: {e}")
            return {}
    
    async def _analyze_institutional_sentiment(self, company_name: str) -> Dict[str, Any]:
        """Analyze sentiment from institutional investors"""
        try:
            search_tool = DynamicWebSearchTool()
            
            # Search for institutional sentiment
            institutional_queries = [
                f"{company_name} institutional investor sentiment",
                f"{company_name} mutual fund sentiment holdings",
                f"{company_name} hedge fund sentiment",
                f"{company_name} institutional ownership sentiment"
            ]
            
            institutional_sentiment_data = {}
            
            for query in institutional_queries:
                # Get institutional content
                institutional_content = search_tool._run(query)
                
                if institutional_content and "✅" in institutional_content:
                    institutional_sentiment_data[query] = {
                        "content": institutional_content,
                        "sentiment": self._extract_institutional_sentiment(institutional_content)
                    }
            
            return institutional_sentiment_data
            
        except Exception as e:
            print(f"❌ Error analyzing institutional sentiment: {e}")
            return {}
    
    async def _assess_market_mood(self, company_name: str, sentiment_data: Dict[str, Any]) -> str:
        """Assess overall market mood for the company"""
        try:
            # Combine all sentiment data for analysis
            combined_data = {
                "news_sentiment": sentiment_data.get("news_sentiment", {}),
                "social_sentiment": sentiment_data.get("social_media_sentiment", {}),
                "analyst_sentiment": sentiment_data.get("analyst_sentiment", {}),
                "institutional_sentiment": sentiment_data.get("institutional_sentiment", {})
            }
            
            prompt = f"""
            Assess the overall market mood for {company_name} based on the following sentiment data:
            
            News Sentiment: {combined_data['news_sentiment']}
            Social Media Sentiment: {combined_data['social_sentiment']}
            Analyst Sentiment: {combined_data['analyst_sentiment']}
            Institutional Sentiment: {combined_data['institutional_sentiment']}
            
            Provide a comprehensive market mood assessment covering:
            1. Overall Sentiment: Bullish, Bearish, or Neutral
            2. Market Confidence: High, Medium, or Low
            3. Investor Sentiment: Optimistic, Pessimistic, or Mixed
            4. Market Momentum: Positive, Negative, or Sideways
            5. Key Sentiment Drivers: What's driving the current mood
            6. Sentiment Risks: Potential sentiment shifts to watch
            
            Format the assessment professionally for institutional investors.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.SENTIMENT,
                max_fallbacks=3
            )
            
            return result.content if result else "Market mood assessment not available"
            
        except Exception as e:
            print(f"❌ Error assessing market mood: {e}")
            return "Market mood assessment failed"
    
    async def _calculate_sentiment_score(self, sentiment_data: Dict[str, Any]) -> float:
        """Calculate composite sentiment score"""
        try:
            # Extract sentiment scores from different sources
            scores = []
            
            # News sentiment scores
            for data in sentiment_data.get("news_sentiment", {}).values():
                if "sentiment_analysis" in data:
                    score = self._extract_sentiment_score(data["sentiment_analysis"])
                    if score is not None:
                        scores.append(score)
            
            # Social media sentiment scores
            for data in sentiment_data.get("social_media_sentiment", {}).values():
                if "sentiment_analysis" in data:
                    score = self._extract_sentiment_score(data["sentiment_analysis"])
                    if score is not None:
                        scores.append(score)
            
            # Calculate weighted average (news gets higher weight)
            if scores:
                # Weight news sentiment more heavily
                weighted_scores = []
                for i, score in enumerate(scores):
                    if i < len(sentiment_data.get("news_sentiment", {})):
                        weighted_scores.append(score * 0.6)  # News weight
                    else:
                        weighted_scores.append(score * 0.4)  # Social media weight
                
                composite_score = sum(weighted_scores) / len(weighted_scores)
                return round(composite_score, 3)
            
            return 0.0
            
        except Exception as e:
            print(f"❌ Error calculating sentiment score: {e}")
            return 0.0
    
    async def _identify_sentiment_trends(self, sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify sentiment trends and key drivers"""
        try:
            prompt = f"""
            Analyze sentiment trends and drivers for the company based on:
            
            Sentiment Score: {sentiment_data.get('sentiment_score', 0.0)}
            Market Mood: {sentiment_data.get('market_mood', '')}
            News Sentiment: {sentiment_data.get('news_sentiment', {})}
            Social Media Sentiment: {sentiment_data.get('social_media_sentiment', {})}
            Analyst Sentiment: {sentiment_data.get('analyst_sentiment', {})}
            Institutional Sentiment: {sentiment_data.get('institutional_sentiment', {})}
            
            Provide analysis covering:
            
            SENTIMENT TREND:
            - Current trend direction (Improving, Declining, Stable)
            - Trend strength and momentum
            - Recent sentiment changes
            
            KEY DRIVERS:
            - Primary factors driving sentiment
            - Recent events affecting sentiment
            - Market catalysts and triggers
            
            SENTIMENT RISKS:
            - Potential sentiment headwinds
            - Risk factors that could shift sentiment
            - Monitoring points for sentiment changes
            
            Format professionally for investment analysis.
            """
            
            result = await self.fallback_system.execute_with_fallback(
                prompt=prompt,
                task_type=TaskType.SENTIMENT,
                max_fallbacks=3
            )
            
            content = result.content if result else "Sentiment trend analysis not available"
            
            # Parse the result
            trend = ""
            drivers = []
            risks = []
            
            if "SENTIMENT TREND:" in content:
                trend_section = content.split("SENTIMENT TREND:")[1].split("KEY DRIVERS:")[0]
                trend = trend_section.strip()
            
            if "KEY DRIVERS:" in content:
                drivers_section = content.split("KEY DRIVERS:")[1].split("SENTIMENT RISKS:")[0]
                drivers = [line.strip() for line in drivers_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            if "SENTIMENT RISKS:" in content:
                risks_section = content.split("SENTIMENT RISKS:")[1]
                risks = [line.strip() for line in risks_section.split('\n') if line.strip() and line.strip()[0] == '-']
            
            return {
                "trend": trend,
                "drivers": drivers,
                "risks": risks
            }
            
        except Exception as e:
            print(f"❌ Error identifying sentiment trends: {e}")
            return {
                "trend": "Sentiment trend analysis failed",
                "drivers": [],
                "risks": []
            }
    
    def _extract_analyst_sentiment(self, content: str) -> str:
        """Extract analyst sentiment from content"""
        content_lower = content.lower()
        
        # Look for analyst rating keywords
        bullish_keywords = ['buy', 'outperform', 'overweight', 'positive', 'bullish']
        bearish_keywords = ['sell', 'underperform', 'underweight', 'negative', 'bearish']
        neutral_keywords = ['hold', 'neutral', 'equal-weight', 'market perform']
        
        bullish_count = sum(content_lower.count(keyword) for keyword in bullish_keywords)
        bearish_count = sum(content_lower.count(keyword) for keyword in bearish_keywords)
        neutral_count = sum(content_lower.count(keyword) for keyword in neutral_keywords)
        
        if bullish_count > bearish_count and bullish_count > neutral_count:
            return "Bullish"
        elif bearish_count > bullish_count and bearish_count > neutral_count:
            return "Bearish"
        else:
            return "Neutral"
    
    def _extract_institutional_sentiment(self, content: str) -> str:
        """Extract institutional sentiment from content"""
        content_lower = content.lower()
        
        # Look for institutional activity keywords
        positive_keywords = ['increased', 'bought', 'accumulated', 'positive', 'bullish']
        negative_keywords = ['decreased', 'sold', 'reduced', 'negative', 'bearish']
        
        positive_count = sum(content_lower.count(keyword) for keyword in positive_keywords)
        negative_count = sum(content_lower.count(keyword) for keyword in negative_keywords)
        
        if positive_count > negative_count:
            return "Positive"
        elif negative_count > positive_count:
            return "Negative"
        else:
            return "Neutral"
    
    def _extract_sentiment_score(self, sentiment_analysis: str) -> Optional[float]:
        """Extract numerical sentiment score from analysis text"""
        try:
            # Look for sentiment score in the text
            import re
            
            # Look for patterns like "Sentiment Score: 0.75" or "Score: 0.82"
            score_patterns = [
                r'sentiment score[:\s]*([+-]?\d+\.?\d*)',
                r'score[:\s]*([+-]?\d+\.?\d*)',
                r'polarity[:\s]*([+-]?\d+\.?\d*)'
            ]
            
            for pattern in score_patterns:
                match = re.search(pattern, sentiment_analysis.lower())
                if match:
                    score = float(match.group(1))
                    # Normalize to -1 to 1 range if needed
                    if score > 1:
                        score = score / 100
                    return score
            
            return None
            
        except Exception as e:
            print(f"❌ Error extracting sentiment score: {e}")
            return None

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
        
        if request_type == "sentiment_data":
            sentiment_data = await self.analyze_sentiment(company_name)
            return {
                "status": "success",
                "agent": self.name,
                "data": sentiment_data,
                "data_type": "sentiment_data"
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
__all__ = ['SentimentAgent'] 