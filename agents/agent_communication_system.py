"""
🤖 Agent Communication System - Intelligent Inter-Agent Collaboration
====================================================================

This system enables agents to communicate with each other intelligently,
request additional data, collaborate on analysis, and dynamically adapt
their workflows based on needs and requirements.
"""

import asyncio
import os
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MessageType(Enum):
    """Types of messages agents can send to each other"""
    DATA_REQUEST = "data_request"
    DATA_RESPONSE = "data_response"
    COLLABORATION_REQUEST = "collaboration_request"
    ANALYSIS_REQUEST = "analysis_request"
    VALIDATION_REQUEST = "validation_request"
    ERROR_NOTIFICATION = "error_notification"
    WORKFLOW_UPDATE = "workflow_update"

@dataclass
class AgentMessage:
    """Message structure for inter-agent communication"""
    sender: str
    recipient: str
    message_type: MessageType
    content: Dict[str, Any]
    priority: int = 1  # 1=low, 2=medium, 3=high, 4=critical
    timestamp: float = None
    requires_response: bool = True
    response_timeout: float = 30.0  # seconds

class AgentCommunicationSystem:
    """🤖 Central communication system for inter-agent collaboration"""
    
    def __init__(self):
        self.agents = {}
        self.message_queue = asyncio.Queue()
        self.response_handlers = {}
        self.agent_capabilities = {}
        self.communication_log = []
        
    def register_agent(self, agent_name: str, agent_instance: Any, capabilities: List[str]):
        """Register an agent with its capabilities"""
        self.agents[agent_name] = agent_instance
        self.agent_capabilities[agent_name] = capabilities
        print(f"✅ Registered agent: {agent_name} with capabilities: {capabilities}")
    
    async def send_message(self, message: AgentMessage) -> Optional[Dict[str, Any]]:
        """Send a message to another agent and wait for response"""
        try:
            # Add timestamp if not provided
            if message.timestamp is None:
                message.timestamp = asyncio.get_event_loop().time()
            
            # Log the message
            self.communication_log.append({
                "timestamp": message.timestamp,
                "sender": message.sender,
                "recipient": message.recipient,
                "type": message.message_type.value,
                "priority": message.priority
            })
            
            print(f"📤 {message.sender} → {message.recipient}: {message.message_type.value}")
            
            # Check if recipient exists
            if message.recipient not in self.agents:
                return {"error": f"Agent {message.recipient} not found"}
            
            # Send message to recipient
            recipient_agent = self.agents[message.recipient]
            
            # Handle different message types
            if message.message_type == MessageType.DATA_REQUEST:
                response = await self._handle_data_request(recipient_agent, message)
            elif message.message_type == MessageType.COLLABORATION_REQUEST:
                response = await self._handle_collaboration_request(recipient_agent, message)
            elif message.message_type == MessageType.ANALYSIS_REQUEST:
                response = await self._handle_analysis_request(recipient_agent, message)
            elif message.message_type == MessageType.VALIDATION_REQUEST:
                response = await self._handle_validation_request(recipient_agent, message)
            else:
                response = {"error": f"Unknown message type: {message.message_type}"}
            
            # Log the response
            print(f"📥 {message.recipient} → {message.sender}: Response received")
            
            return response
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return {"error": str(e)}
    
    async def _handle_data_request(self, recipient_agent: Any, message: AgentMessage) -> Dict[str, Any]:
        """Handle data request messages"""
        try:
            # Extract request details
            request_type = message.content.get("request_type")
            company_name = message.content.get("company_name")
            specific_data = message.content.get("specific_data", [])
            
            # Route to appropriate agent method
            if hasattr(recipient_agent, 'provide_data'):
                return await recipient_agent.provide_data(request_type, company_name, specific_data)
            elif hasattr(recipient_agent, 'get_data'):
                return await recipient_agent.get_data(request_type, company_name, specific_data)
            else:
                return {"error": f"Agent {message.recipient} cannot provide data"}
                
        except Exception as e:
            return {"error": f"Error handling data request: {str(e)}"}
    
    async def _handle_collaboration_request(self, recipient_agent: Any, message: AgentMessage) -> Dict[str, Any]:
        """Handle collaboration request messages"""
        try:
            # Extract collaboration details
            collaboration_type = message.content.get("collaboration_type")
            shared_data = message.content.get("shared_data", {})
            collaboration_params = message.content.get("params", {})
            
            # Route to appropriate agent method
            if hasattr(recipient_agent, 'collaborate'):
                return await recipient_agent.collaborate(collaboration_type, shared_data, collaboration_params)
            else:
                return {"error": f"Agent {message.recipient} cannot collaborate"}
                
        except Exception as e:
            return {"error": f"Error handling collaboration request: {str(e)}"}
    
    async def _handle_analysis_request(self, recipient_agent: Any, message: AgentMessage) -> Dict[str, Any]:
        """Handle analysis request messages"""
        try:
            # Extract analysis details
            analysis_type = message.content.get("analysis_type")
            data_to_analyze = message.content.get("data", {})
            analysis_params = message.content.get("params", {})
            
            # Route to appropriate agent method
            if hasattr(recipient_agent, 'perform_analysis'):
                return await recipient_agent.perform_analysis(analysis_type, data_to_analyze, analysis_params)
            else:
                return {"error": f"Agent {message.recipient} cannot perform analysis"}
                
        except Exception as e:
            return {"error": f"Error handling analysis request: {str(e)}"}
    
    async def _handle_validation_request(self, recipient_agent: Any, message: AgentMessage) -> Dict[str, Any]:
        """Handle validation request messages"""
        try:
            # Extract validation details
            validation_type = message.content.get("validation_type")
            data_to_validate = message.content.get("data", {})
            validation_criteria = message.content.get("criteria", {})
            
            # Route to appropriate agent method
            if hasattr(recipient_agent, 'validate'):
                return await recipient_agent.validate(validation_type, data_to_validate, validation_criteria)
            else:
                return {"error": f"Agent {message.recipient} cannot validate"}
                
        except Exception as e:
            return {"error": f"Error handling validation request: {str(e)}"}
    
    def find_agent_with_capability(self, capability: str) -> Optional[str]:
        """Find an agent that has a specific capability"""
        for agent_name, capabilities in self.agent_capabilities.items():
            if capability in capabilities:
                return agent_name
        return None
    
    async def broadcast_message(self, sender: str, message_type: MessageType, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Broadcast a message to all agents"""
        responses = []
        for agent_name in self.agents.keys():
            if agent_name != sender:
                message = AgentMessage(
                    sender=sender,
                    recipient=agent_name,
                    message_type=message_type,
                    content=content,
                    requires_response=True
                )
                response = await self.send_message(message)
                responses.append({"recipient": agent_name, "response": response})
        return responses
    
    def get_communication_log(self) -> List[Dict[str, Any]]:
        """Get the communication log"""
        return self.communication_log

# Global communication system instance
communication_system = AgentCommunicationSystem()

class CommunicatingAgent:
    """Base class for agents that can communicate with each other"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.communication_system = communication_system
        
        # Register this agent with the communication system
        self.communication_system.register_agent(name, self, capabilities)
    
    async def request_data(self, recipient: str, request_type: str, company_name: str, specific_data: List[str] = None) -> Dict[str, Any]:
        """Request data from another agent"""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient,
            message_type=MessageType.DATA_REQUEST,
            content={
                "request_type": request_type,
                "company_name": company_name,
                "specific_data": specific_data or []
            }
        )
        return await self.communication_system.send_message(message)
    
    async def request_collaboration(self, recipient: str, collaboration_type: str, shared_data: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Request collaboration from another agent"""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient,
            message_type=MessageType.COLLABORATION_REQUEST,
            content={
                "collaboration_type": collaboration_type,
                "shared_data": shared_data,
                "params": params or {}
            }
        )
        return await self.communication_system.send_message(message)
    
    async def request_analysis(self, recipient: str, analysis_type: str, data: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Request analysis from another agent"""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient,
            message_type=MessageType.ANALYSIS_REQUEST,
            content={
                "analysis_type": analysis_type,
                "data": data,
                "params": params or {}
            }
        )
        return await self.communication_system.send_message(message)
    
    async def request_validation(self, recipient: str, validation_type: str, data: Dict[str, Any], criteria: Dict[str, Any] = None) -> Dict[str, Any]:
        """Request validation from another agent"""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient,
            message_type=MessageType.VALIDATION_REQUEST,
            content={
                "validation_type": validation_type,
                "data": data,
                "criteria": criteria or {}
            }
        )
        return await self.communication_system.send_message(message)
    
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide data to another agent (to be implemented by subclasses)"""
        return {"error": f"Agent {self.name} cannot provide data"}
    
    async def collaborate(self, collaboration_type: str, shared_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with another agent (to be implemented by subclasses)"""
        return {"error": f"Agent {self.name} cannot collaborate"}
    
    async def perform_analysis(self, analysis_type: str, data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform analysis for another agent (to be implemented by subclasses)"""
        return {"error": f"Agent {self.name} cannot perform analysis"}
    
    async def validate(self, validation_type: str, data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for another agent (to be implemented by subclasses)"""
        return {"error": f"Agent {self.name} cannot validate"}

# Export the communication system
__all__ = ['AgentCommunicationSystem', 'CommunicatingAgent', 'AgentMessage', 'MessageType', 'communication_system'] 