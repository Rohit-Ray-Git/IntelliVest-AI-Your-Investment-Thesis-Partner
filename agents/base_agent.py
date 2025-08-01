"""
🧠 Base Agent - Intelligent Inter-Agent Communication System
==========================================================

This base class provides intelligent communication capabilities for all agents,
enabling them to request additional data from other agents when needed.
"""

import asyncio
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """🧠 Base class for all agents with intelligent communication capabilities"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.agent_registry = {}  # Registry of other agents
        self.communication_log = []  # Log of inter-agent communications
        
    def register_agents(self, agents: Dict[str, 'BaseAgent']):
        """Register other agents for communication"""
        self.agent_registry = agents
        print(f"✅ {self.name}: Registered {len(agents)} agents for communication")
    
    async def request_data_from_agent(self, agent_name: str, request_type: str, 
                                    parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request additional data from another agent
        
        Args:
            agent_name: Name of the agent to request data from
            request_type: Type of data needed
            parameters: Parameters for the request
            
        Returns:
            Data from the requested agent
        """
        try:
            if agent_name not in self.agent_registry:
                return {"error": f"Agent {agent_name} not found in registry"}
            
            target_agent = self.agent_registry[agent_name]
            
            # Log the communication
            communication = {
                "from": self.name,
                "to": agent_name,
                "request_type": request_type,
                "parameters": parameters,
                "timestamp": asyncio.get_event_loop().time()
            }
            self.communication_log.append(communication)
            
            print(f"🤝 {self.name} → {agent_name}: Requesting {request_type}")
            
            # Request data based on agent type
            if agent_name == "ResearchAgent":
                return await self._request_from_research_agent(target_agent, request_type, parameters)
            elif agent_name == "SentimentAgent":
                return await self._request_from_sentiment_agent(target_agent, request_type, parameters)
            elif agent_name == "ValuationAgent":
                return await self._request_from_valuation_agent(target_agent, request_type, parameters)
            elif agent_name == "ThesisAgent":
                return await self._request_from_thesis_agent(target_agent, request_type, parameters)
            elif agent_name == "CritiqueAgent":
                return await self._request_from_critique_agent(target_agent, request_type, parameters)
            elif agent_name == "CryptoAgent":
                return await self._request_from_crypto_agent(target_agent, request_type, parameters)
            else:
                return {"error": f"Unknown agent type: {agent_name}"}
                
        except Exception as e:
            print(f"❌ Error requesting data from {agent_name}: {e}")
            return {"error": str(e)}
    
    async def _request_from_research_agent(self, agent, request_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Request data from ResearchAgent"""
        company_name = parameters.get("company_name", "")
        
        if request_type == "additional_research":
            return await agent.conduct_research(company_name)
        elif request_type == "institutional_data":
            return await agent._get_institutional_data(company_name)
        elif request_type == "competitive_analysis":
            return await agent._analyze_competition(company_name, {})
        else:
            return {"error": f"Unknown request type: {request_type}"}
    
    async def _request_from_sentiment_agent(self, agent, request_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Request data from SentimentAgent"""
        company_name = parameters.get("company_name", "")
        research_data = parameters.get("research_data", {})
        
        if request_type == "sentiment_analysis":
            return await agent.analyze_sentiment(company_name, research_data)
        elif request_type == "news_sentiment":
            return await agent._analyze_news_sentiment(company_name)
        elif request_type == "analyst_sentiment":
            return await agent._analyze_analyst_sentiment(company_name)
        else:
            return {"error": f"Unknown request type: {request_type}"}
    
    async def _request_from_valuation_agent(self, agent, request_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Request data from ValuationAgent"""
        company_name = parameters.get("company_name", "")
        research_data = parameters.get("research_data", {})
        
        if request_type == "valuation_analysis":
            return await agent.perform_valuation(company_name, research_data)
        elif request_type == "dcf_analysis":
            return await agent._perform_dcf_analysis(company_name, {})
        elif request_type == "comparable_analysis":
            return await agent._perform_comparable_analysis(company_name, {})
        else:
            return {"error": f"Unknown request type: {request_type}"}
    
    async def _request_from_thesis_agent(self, agent, request_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Request data from ThesisAgent"""
        company_name = parameters.get("company_name", "")
        research_data = parameters.get("research_data", {})
        sentiment_data = parameters.get("sentiment_data", {})
        valuation_data = parameters.get("valuation_data", {})
        
        if request_type == "thesis_generation":
            return await agent.generate_thesis(company_name, research_data, sentiment_data, valuation_data)
        elif request_type == "investment_recommendation":
            return await agent._generate_recommendation(company_name, research_data, sentiment_data, valuation_data)
        else:
            return {"error": f"Unknown request type: {request_type}"}
    
    async def _request_from_critique_agent(self, agent, request_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Request data from CritiqueAgent"""
        company_name = parameters.get("company_name", "")
        thesis_data = parameters.get("thesis_data", {})
        research_data = parameters.get("research_data", {})
        sentiment_data = parameters.get("sentiment_data", {})
        valuation_data = parameters.get("valuation_data", {})
        
        if request_type == "thesis_critique":
            return await agent.critique_thesis(company_name, thesis_data, research_data, sentiment_data, valuation_data)
        elif request_type == "bias_analysis":
            return await agent._analyze_biases(company_name, thesis_data, research_data, sentiment_data, valuation_data)
        else:
            return {"error": f"Unknown request type: {request_type}"}
    
    async def _request_from_crypto_agent(self, agent, request_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Request data from CryptoAgent"""
        crypto_name = parameters.get("crypto_name", "")
        
        if request_type == "crypto_analysis":
            return await agent.analyze_cryptocurrency(crypto_name)
        elif request_type == "market_analysis":
            return await agent._analyze_market_data(crypto_name)
        else:
            return {"error": f"Unknown request type: {request_type}"}
    
    def get_communication_log(self) -> List[Dict[str, Any]]:
        """Get the communication log for this agent"""
        return self.communication_log
    
    def clear_communication_log(self):
        """Clear the communication log"""
        self.communication_log = []
    
    @abstractmethod
    async def process_request(self, request_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming requests from other agents"""
        pass

# Export the base agent
__all__ = ['BaseAgent'] 