"""
🌐 Global Agentic System - True Multi-Agent Intelligence
=======================================================

This system enables ALL agents to:
- Think, plan, and make decisions autonomously
- React to changes and new information
- Take actions based on their analysis
- Communicate with ANY other agent when needed
- Collaborate intelligently across the entire system
"""

import asyncio
import os
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AgentState(Enum):
    """States an agent can be in"""
    IDLE = "idle"
    THINKING = "thinking"
    PLANNING = "planning"
    DECIDING = "deciding"
    ACTING = "acting"
    COMMUNICATING = "communicating"
    COLLABORATING = "collaborating"
    WAITING = "waiting"

class MessageType(Enum):
    """Types of messages agents can send to each other"""
    DATA_REQUEST = "data_request"
    DATA_RESPONSE = "data_response"
    COLLABORATION_REQUEST = "collaboration_request"
    ANALYSIS_REQUEST = "analysis_request"
    VALIDATION_REQUEST = "validation_request"
    DECISION_REQUEST = "decision_request"
    PLANNING_REQUEST = "planning_request"
    ACTION_REQUEST = "action_request"
    THINKING_REQUEST = "thinking_request"
    REACTION_REQUEST = "reaction_request"
    ERROR_NOTIFICATION = "error_notification"
    WORKFLOW_UPDATE = "workflow_update"
    BROADCAST = "broadcast"

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
    context: Dict[str, Any] = None  # Additional context for the message

class GlobalAgenticSystem:
    """🌐 Global agentic system for true multi-agent intelligence"""
    
    def __init__(self):
        self.agents = {}
        self.agent_capabilities = {}
        self.agent_states = {}
        self.communication_log = []
        self.system_events = []
        self.global_knowledge_base = {}
        self.agent_relationships = {}  # Track which agents work well together
        
    def register_agent(self, agent_name: str, agent_instance: Any, capabilities: List[str]):
        """Register an agent with the global system"""
        self.agents[agent_name] = agent_instance
        self.agent_capabilities[agent_name] = capabilities
        self.agent_states[agent_name] = AgentState.IDLE
        self.agent_relationships[agent_name] = {}
        print(f"🌐 Registered agent: {agent_name} with capabilities: {capabilities}")
    
    async def send_message(self, message: AgentMessage) -> Optional[Dict[str, Any]]:
        """Send a message to another agent and wait for response"""
        try:
            # Add timestamp if not provided
            if message.timestamp is None:
                message.timestamp = asyncio.get_event_loop().time()
            
            # Update agent states
            self.agent_states[message.sender] = AgentState.COMMUNICATING
            self.agent_states[message.recipient] = AgentState.COMMUNICATING
            
            # Log the message
            self.communication_log.append({
                "timestamp": message.timestamp,
                "sender": message.sender,
                "recipient": message.recipient,
                "type": message.message_type.value,
                "priority": message.priority,
                "context": message.context
            })
            
            print(f"📤 {message.sender} → {message.recipient}: {message.message_type.value}")
            
            # Check if recipient exists
            if message.recipient not in self.agents:
                return {"error": f"Agent {message.recipient} not found"}
            
            # Send message to recipient
            recipient_agent = self.agents[message.recipient]
            
            # Handle different message types
            response = await self._route_message(recipient_agent, message)
            
            # Update agent states back to idle
            self.agent_states[message.sender] = AgentState.IDLE
            self.agent_states[message.recipient] = AgentState.IDLE
            
            # Log the response
            print(f"📥 {message.recipient} → {message.sender}: Response received")
            
            # Update agent relationships based on successful communication
            if "error" not in response:
                self._update_agent_relationships(message.sender, message.recipient, True)
            
            return response
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            # Update agent states back to idle on error
            self.agent_states[message.sender] = AgentState.IDLE
            if message.recipient in self.agent_states:
                self.agent_states[message.recipient] = AgentState.IDLE
            return {"error": str(e)}
    
    async def _route_message(self, recipient_agent: Any, message: AgentMessage) -> Dict[str, Any]:
        """Route message to appropriate handler based on type"""
        try:
            # Use the unified handle_message method that all agents have
            if hasattr(recipient_agent, 'handle_message'):
                return await recipient_agent.handle_message(message)
            else:
                return {"error": f"Agent {message.recipient} does not have handle_message method"}
                
        except Exception as e:
            return {"error": f"Error routing message: {str(e)}"}
    
    def find_agent_with_capability(self, capability: str) -> Optional[str]:
        """Find an agent that has a specific capability"""
        for agent_name, capabilities in self.agent_capabilities.items():
            if capability in capabilities:
                return agent_name
        return None
    
    def find_best_agent_for_task(self, task_type: str, context: Dict[str, Any] = None) -> Optional[str]:
        """Find the best agent for a specific task based on capabilities and relationships"""
        suitable_agents = []
        
        for agent_name, capabilities in self.agent_capabilities.items():
            if self._agent_can_handle_task(agent_name, task_type, context):
                # Calculate agent suitability score
                score = self._calculate_agent_suitability(agent_name, task_type, context)
                suitable_agents.append((agent_name, score))
        
        if suitable_agents:
            # Sort by score and return the best agent
            suitable_agents.sort(key=lambda x: x[1], reverse=True)
            return suitable_agents[0][0]
        
        return None
    
    def _agent_can_handle_task(self, agent_name: str, task_type: str, context: Dict[str, Any] = None) -> bool:
        """Check if an agent can handle a specific task"""
        capabilities = self.agent_capabilities.get(agent_name, [])
        
        # Basic capability matching
        if task_type in capabilities:
            return True
        
        # Context-based matching
        if context:
            required_capabilities = context.get("required_capabilities", [])
            return any(cap in capabilities for cap in required_capabilities)
        
        return False
    
    def _calculate_agent_suitability(self, agent_name: str, task_type: str, context: Dict[str, Any] = None) -> float:
        """Calculate how suitable an agent is for a specific task"""
        score = 0.0
        
        # Base score from capabilities
        capabilities = self.agent_capabilities.get(agent_name, [])
        if task_type in capabilities:
            score += 1.0
        
        # Relationship score (if context includes sender)
        if context and "sender" in context:
            sender = context["sender"]
            relationship_score = self.agent_relationships.get(agent_name, {}).get(sender, 0.5)
            score += relationship_score * 0.5
        
        # State score (prefer idle agents)
        agent_state = self.agent_states.get(agent_name, AgentState.IDLE)
        if agent_state == AgentState.IDLE:
            score += 0.3
        elif agent_state == AgentState.THINKING:
            score += 0.1
        
        return score
    
    def _update_agent_relationships(self, agent1: str, agent2: str, success: bool):
        """Update relationship scores between agents"""
        if success:
            # Increase relationship score for successful communication
            current_score = self.agent_relationships.get(agent1, {}).get(agent2, 0.5)
            new_score = min(1.0, current_score + 0.1)
            
            if agent1 not in self.agent_relationships:
                self.agent_relationships[agent1] = {}
            if agent2 not in self.agent_relationships:
                self.agent_relationships[agent2] = {}
            
            self.agent_relationships[agent1][agent2] = new_score
            self.agent_relationships[agent2][agent1] = new_score
    
    async def broadcast_message(self, sender: str, message_type: MessageType, content: Dict[str, Any], 
                              context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Broadcast a message to all agents"""
        responses = []
        for agent_name in self.agents.keys():
            if agent_name != sender:
                message = AgentMessage(
                    sender=sender,
                    recipient=agent_name,
                    message_type=message_type,
                    content=content,
                    context=context,
                    requires_response=True
                )
                response = await self.send_message(message)
                responses.append({"recipient": agent_name, "response": response})
        return responses
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get the current status of the global agentic system"""
        return {
            "total_agents": len(self.agents),
            "agent_states": {name: state.value for name, state in self.agent_states.items()},
            "agent_capabilities": self.agent_capabilities,
            "total_communications": len(self.communication_log),
            "system_events": len(self.system_events),
            "global_knowledge_base_size": len(self.global_knowledge_base)
        }
    
    def get_communication_log(self) -> List[Dict[str, Any]]:
        """Get the communication log"""
        return self.communication_log

# Global agentic system instance
global_agentic_system = GlobalAgenticSystem()

class AgenticAgent(ABC):
    """Base class for all agentic agents that can think, plan, decide, act, and communicate"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.agentic_system = global_agentic_system
        self.current_state = AgentState.IDLE
        self.thought_process = []
        self.plans = []
        self.decisions = []
        self.actions = []
        
        # Register this agent with the global system
        self.agentic_system.register_agent(name, self, capabilities)
    
    @abstractmethod
    async def think(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Think about the given context and return thoughts"""
        pass
    
    @abstractmethod
    async def plan(self, thoughts: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a plan based on thoughts and context"""
        pass
    
    @abstractmethod
    async def decide(self, plans: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Make decisions based on plans and context"""
        pass
    
    @abstractmethod
    async def act(self, decisions: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Take actions based on decisions and context"""
        pass
    
    @abstractmethod
    async def react(self, event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """React to events and changes"""
        pass
    
    async def communicate_with_agent(self, recipient: str, message_type: MessageType, 
                                   content: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Communicate with another agent"""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient,
            message_type=message_type,
            content=content,
            context=context,
            requires_response=True
        )
        return await self.agentic_system.send_message(message)
    
    async def find_and_communicate_with_best_agent(self, task_type: str, message_type: MessageType,
                                                  content: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Find the best agent for a task and communicate with them"""
        best_agent = self.agentic_system.find_best_agent_for_task(task_type, context)
        if best_agent:
            return await self.communicate_with_agent(best_agent, message_type, content, context)
        else:
            return {"error": f"No suitable agent found for task: {task_type}"}
    
    async def broadcast_to_all_agents(self, message_type: MessageType, content: Dict[str, Any], 
                                    context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Broadcast a message to all agents"""
        return await self.agentic_system.broadcast_message(self.name, message_type, content, context)
    
    # Message handlers for different types of requests
    async def handle_data_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Handle data request messages"""
        return await self.provide_data(message.content.get("request_type"), 
                                     message.content.get("company_name"), 
                                     message.content.get("specific_data", []))
    
    async def handle_collaboration_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Handle collaboration request messages"""
        return await self.collaborate(message.content.get("collaboration_type"),
                                    message.content.get("shared_data", {}),
                                    message.content.get("params", {}))
    
    async def handle_analysis_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Handle analysis request messages"""
        return await self.perform_analysis(message.content.get("analysis_type"),
                                         message.content.get("data", {}),
                                         message.content.get("params", {}))
    
    async def handle_validation_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Handle validation request messages"""
        return await self.validate(message.content.get("validation_type"),
                                 message.content.get("data", {}),
                                 message.content.get("criteria", {}))
    
    async def handle_decision_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Handle decision request messages"""
        return await self.make_decision(message.content.get("decision_type"),
                                      message.content.get("context", {}),
                                      message.content.get("options", []))
    
    async def handle_planning_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Handle planning request messages"""
        return await self.create_plan(message.content.get("planning_type"),
                                    message.content.get("context", {}),
                                    message.content.get("goals", []))
    
    async def handle_action_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Handle action request messages"""
        return await self.take_action(message.content.get("action_type"),
                                    message.content.get("context", {}),
                                    message.content.get("parameters", {}))
    
    async def handle_thinking_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Handle thinking request messages"""
        return await self.think(message.content.get("context", {}))
    
    async def handle_reaction_request(self, message: AgentMessage) -> Dict[str, Any]:
        """Handle reaction request messages"""
        return await self.react(message.content.get("event", {}),
                               message.content.get("context", {}))
    
    # Default implementations for common agent capabilities
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide data to other agents (to be implemented by subclasses)"""
        return {"error": f"Agent {self.name} cannot provide data"}
    
    async def collaborate(self, collaboration_type: str, shared_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other agents (to be implemented by subclasses)"""
        return {"error": f"Agent {self.name} cannot collaborate"}
    
    async def perform_analysis(self, analysis_type: str, data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform analysis for other agents (to be implemented by subclasses)"""
        return {"error": f"Agent {self.name} cannot perform analysis"}
    
    async def validate(self, validation_type: str, data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for other agents (to be implemented by subclasses)"""
        return {"error": f"Agent {self.name} cannot validate"}
    
    async def make_decision(self, decision_type: str, context: Dict[str, Any], options: List[str]) -> Dict[str, Any]:
        """Make decisions for other agents (to be implemented by subclasses)"""
        return {"error": f"Agent {self.name} cannot make decisions"}
    
    async def create_plan(self, planning_type: str, context: Dict[str, Any], goals: List[str]) -> Dict[str, Any]:
        """Create plans for other agents (to be implemented by subclasses)"""
        return {"error": f"Agent {self.name} cannot create plans"}
    
    async def take_action(self, action_type: str, context: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Take actions for other agents (to be implemented by subclasses)"""
        return {"error": f"Agent {self.name} cannot take actions"}

# Export the global agentic system
__all__ = ['GlobalAgenticSystem', 'AgenticAgent', 'AgentMessage', 'MessageType', 'AgentState', 'global_agentic_system'] 