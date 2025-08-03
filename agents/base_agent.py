"""
🤖 Base Agent - Standardized Agent Interface
===========================================

This module defines the base agent class that all specialized agents should inherit from.
It provides a standardized interface for agent communication and functionality.
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our advanced fallback system
from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType

class BaseAgent(ABC):
    """🤖 Base agent class with standardized interface"""
    
    def __init__(self, name: str, role: str, backstory: str):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            role: Agent role description
            backstory: Agent backstory and expertise
        """
        self.name = name
        self.role = role
        self.backstory = backstory
        
        # Initialize advanced fallback system
        try:
            self.fallback_system = AdvancedFallbackSystem()
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize fallback system for {name}: {e}")
            self.fallback_system = None
    
    @abstractmethod
    async def analyze(self, company_name: str, **kwargs) -> Dict[str, Any]:
        """
        Main analysis method - must be implemented by all agents
        
        Args:
            company_name: Name or symbol of the company to analyze
            **kwargs: Additional parameters specific to each agent
            
        Returns:
            Dictionary containing analysis results
        """
        pass
    
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming messages from other agents
        
        Args:
            message: Message dictionary with sender, type, content, etc.
            
        Returns:
            Response dictionary
        """
        try:
            message_type = message.get("type", "unknown")
            
            if message_type == "data_request":
                return await self._handle_data_request(message)
            elif message_type == "collaboration_request":
                return await self._handle_collaboration_request(message)
            elif message_type == "analysis_request":
                return await self._handle_analysis_request(message)
            elif message_type == "validation_request":
                return await self._handle_validation_request(message)
            else:
                return {"error": f"Unknown message type: {message_type}"}
                
        except Exception as e:
            return {"error": f"Error handling message: {str(e)}"}
    
    async def _handle_data_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle data request messages"""
        try:
            request_type = message.get("content", {}).get("request_type", "")
            company_name = message.get("content", {}).get("company_name", "")
            specific_data = message.get("content", {}).get("specific_data", [])
            
            return await self.provide_data(request_type, company_name, specific_data)
            
        except Exception as e:
            return {"error": f"Error handling data request: {str(e)}"}
    
    async def _handle_collaboration_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle collaboration request messages"""
        try:
            collaboration_type = message.get("content", {}).get("collaboration_type", "")
            shared_data = message.get("content", {}).get("shared_data", {})
            params = message.get("content", {}).get("params", {})
            
            return await self.collaborate(collaboration_type, shared_data, params)
            
        except Exception as e:
            return {"error": f"Error handling collaboration request: {str(e)}"}
    
    async def _handle_analysis_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle analysis request messages"""
        try:
            analysis_type = message.get("content", {}).get("analysis_type", "")
            data = message.get("content", {}).get("data", {})
            params = message.get("content", {}).get("params", {})
            
            return await self.perform_analysis(analysis_type, data, params)
            
        except Exception as e:
            return {"error": f"Error handling analysis request: {str(e)}"}
    
    async def _handle_validation_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle validation request messages"""
        try:
            validation_type = message.get("content", {}).get("validation_type", "")
            data = message.get("content", {}).get("data", {})
            criteria = message.get("content", {}).get("criteria", {})
            
            return await self.validate(validation_type, data, criteria)
            
        except Exception as e:
            return {"error": f"Error handling validation request: {str(e)}"}
    
    async def provide_data(self, request_type: str, company_name: str, specific_data: List[str]) -> Dict[str, Any]:
        """Provide data to other agents - override in subclasses"""
        return {
            "agent": self.name,
            "data_type": request_type,
            "company_name": company_name,
            "data": {},
            "message": f"{self.name} does not provide {request_type} data"
        }
    
    async def collaborate(self, collaboration_type: str, shared_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with other agents - override in subclasses"""
        return {
            "agent": self.name,
            "collaboration_type": collaboration_type,
            "result": {},
            "message": f"{self.name} does not support {collaboration_type} collaboration"
        }
    
    async def perform_analysis(self, analysis_type: str, data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform analysis for other agents - override in subclasses"""
        return {
            "agent": self.name,
            "analysis_type": analysis_type,
            "result": {},
            "message": f"{self.name} does not support {analysis_type} analysis"
        }
    
    async def validate(self, validation_type: str, data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for other agents - override in subclasses"""
        return {
            "agent": self.name,
            "validation_type": validation_type,
            "result": {},
            "message": f"{self.name} does not support {validation_type} validation"
        }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "name": self.name,
            "role": self.role,
            "backstory": self.backstory,
            "fallback_system_available": self.fallback_system is not None
        }
    
    def _get_llm_for_task(self, task_type: TaskType):
        """Get appropriate LLM for task type"""
        if self.fallback_system:
            # Select optimal model for the task
            optimal_model = self.fallback_system.select_optimal_model(task_type)
            # Get LLM instance for the selected model
            return self.fallback_system.get_llm_instance(optimal_model)
        else:
            # Fallback to default LLM if fallback system is not available
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(model="gemini-2.5-flash") 