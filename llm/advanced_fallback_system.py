"""
🧠 Advanced Multi-LLM Fallback System
=====================================

This module provides sophisticated LLM orchestration with:
- Multi-LLM fallback chains
- Automatic failover and recovery
- Load balancing and performance optimization
- Quality assessment and model selection
- Intelligent routing based on task type
- Health monitoring and circuit breakers
"""

import os
import asyncio
import time
import random
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import LLM providers
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

class ModelProvider(Enum):
    """Available model providers"""
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GROQ_DEEPSEEK_R1 = "groq/deepseek-r1-distill-llama-70b"
    GROQ_LLAMA_3_3_70B = "groq/llama-3.3-70b-versatile"
    GROQ_LLAMA_70B = "groq/llama3.1-70b-8192"
    GROQ_LLAMA_8B = "groq/llama3.1-8b-8192"
    GROQ_MIXTRAL = "groq/mixtral-8x7b-32768"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"

class TaskType(Enum):
    """Task types for intelligent routing"""
    RESEARCH = "research"
    SENTIMENT = "sentiment"
    VALUATION = "valuation"
    THESIS = "thesis"
    CRITIQUE = "critique"
    GENERAL = "general"

@dataclass
class ModelConfig:
    """Configuration for a model"""
    provider: ModelProvider
    name: str
    max_tokens: int
    temperature: float
    cost_per_1k_tokens: float
    speed_rating: float  # 1-10 scale
    quality_rating: float  # 1-10 scale
    reliability: float  # 0-1 scale
    task_specialties: List[TaskType]
    is_available: bool = True
    last_used: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    avg_response_time: float = 0.0

@dataclass
class FallbackResult:
    """Result from fallback system"""
    content: str
    model_used: str
    provider: ModelProvider
    response_time: float
    cost_estimate: float
    confidence_score: float
    fallback_count: int
    errors: List[str]

class AdvancedFallbackSystem:
    """
    🚀 Advanced multi-LLM fallback system with intelligent orchestration
    """
    
    def __init__(self):
        """Initialize the advanced fallback system"""
        self.setup_models()
        self.setup_fallback_chains()
        self.health_monitor = HealthMonitor()
        
    def setup_models(self):
        """Setup all available models with configurations"""
        # Check API key availability
        google_api_key = os.getenv("GOOGLE_API_KEY")
        groq_api_key = os.getenv("GROQ_API_KEY")
        
        print(f"🔍 Checking API key availability...")
        print(f"  - Google API Key: {'✅ Available' if google_api_key else '❌ Not configured'}")
        print(f"  - Groq API Key: {'✅ Available' if groq_api_key else '❌ Not configured'}")
        
        self.models = {
            ModelProvider.GEMINI_2_5_FLASH: ModelConfig(
                provider=ModelProvider.GEMINI_2_5_FLASH,
                name="Gemini 2.5 Flash",
                max_tokens=8192,
                temperature=0.7,
                cost_per_1k_tokens=0.0005,
                speed_rating=9.0,
                quality_rating=9.5,
                reliability=0.92,
                task_specialties=[TaskType.RESEARCH, TaskType.SENTIMENT, TaskType.VALUATION, TaskType.THESIS, TaskType.CRITIQUE, TaskType.GENERAL],
                is_available=bool(google_api_key)  # Only available if Google API key exists
            ),
            ModelProvider.GROQ_DEEPSEEK_R1: ModelConfig(
                provider=ModelProvider.GROQ_DEEPSEEK_R1,
                name="Groq DeepSeek R1 Distill Llama-70B",
                max_tokens=8192,
                temperature=0.7,
                cost_per_1k_tokens=0.0006,
                speed_rating=9.2,
                quality_rating=8.8,
                reliability=0.94,
                task_specialties=[TaskType.RESEARCH, TaskType.VALUATION, TaskType.THESIS, TaskType.CRITIQUE],
                is_available=bool(groq_api_key)  # Only available if Groq API key exists
            ),
            ModelProvider.GROQ_LLAMA_3_3_70B: ModelConfig(
                provider=ModelProvider.GROQ_LLAMA_3_3_70B,
                name="Groq Llama 3.3-70B Versatile",
                max_tokens=8192,
                temperature=0.7,
                cost_per_1k_tokens=0.0007,
                speed_rating=8.8,
                quality_rating=9.0,
                reliability=0.93,
                task_specialties=[TaskType.RESEARCH, TaskType.SENTIMENT, TaskType.VALUATION, TaskType.THESIS, TaskType.CRITIQUE, TaskType.GENERAL],
                is_available=bool(groq_api_key)  # Only available if Groq API key exists
            ),
            ModelProvider.GROQ_LLAMA_70B: ModelConfig(
                provider=ModelProvider.GROQ_LLAMA_70B,
                name="Groq Llama3.1-70B",
                max_tokens=8192,
                temperature=0.7,
                cost_per_1k_tokens=0.0007,
                speed_rating=9.0,
                quality_rating=8.5,
                reliability=0.95,
                task_specialties=[TaskType.RESEARCH, TaskType.VALUATION, TaskType.THESIS],
                is_available=bool(groq_api_key)  # Only available if Groq API key exists
            ),
            ModelProvider.GROQ_LLAMA_8B: ModelConfig(
                provider=ModelProvider.GROQ_LLAMA_8B,
                name="Groq Llama3.1-8B",
                max_tokens=8192,
                temperature=0.7,
                cost_per_1k_tokens=0.0002,
                speed_rating=9.5,
                quality_rating=7.0,
                reliability=0.98,
                task_specialties=[TaskType.SENTIMENT, TaskType.GENERAL],
                is_available=bool(groq_api_key)  # Only available if Groq API key exists
            ),
            ModelProvider.GROQ_MIXTRAL: ModelConfig(
                provider=ModelProvider.GROQ_MIXTRAL,
                name="Groq Mixtral-8x7B",
                max_tokens=8192,
                temperature=0.7,
                cost_per_1k_tokens=0.0003,
                speed_rating=9.3,
                quality_rating=8.0,
                reliability=0.96,
                task_specialties=[TaskType.RESEARCH, TaskType.SENTIMENT, TaskType.GENERAL],
                is_available=bool(groq_api_key)  # Only available if Groq API key exists
            ),
            ModelProvider.GEMINI_2_0_FLASH: ModelConfig(
                provider=ModelProvider.GEMINI_2_0_FLASH,
                name="Gemini 2.0 Flash",
                max_tokens=8192,
                temperature=0.7,
                cost_per_1k_tokens=0.0004,
                speed_rating=8.5,
                quality_rating=8.5,
                reliability=0.90,
                task_specialties=[TaskType.RESEARCH, TaskType.SENTIMENT, TaskType.GENERAL],
                is_available=bool(google_api_key)  # Only available if Google API key exists
            ),
            ModelProvider.GEMINI_1_5_FLASH: ModelConfig(
                provider=ModelProvider.GEMINI_1_5_FLASH,
                name="Gemini 1.5 Flash",
                max_tokens=8192,
                temperature=0.7,
                cost_per_1k_tokens=0.0003,
                speed_rating=8.0,
                quality_rating=8.0,
                reliability=0.88,
                task_specialties=[TaskType.RESEARCH, TaskType.SENTIMENT, TaskType.GENERAL],
                is_available=bool(google_api_key)  # Only available if Google API key exists
            )
        }
        
        # Print available models
        available_models = [name for name, config in self.models.items() if config.is_available]
        print(f"✅ Available models: {len(available_models)}")
        for model in available_models:
            print(f"  - {self.models[model].name}")
        
        if not available_models:
            print("⚠️ No models available! Please configure API keys in .env file")
            print("   Required: GOOGLE_API_KEY for Gemini models")
            print("   Required: GROQ_API_KEY for Groq models")
    
    def setup_fallback_chains(self):
        """Setup intelligent fallback chains for different task types"""
        # Get available models
        available_models = [provider for provider, config in self.models.items() if config.is_available]
        
        if not available_models:
            print("⚠️ No models available for fallback chains!")
            self.fallback_chains = {task_type: [] for task_type in TaskType}
            return
        
        # Create fallback chains using only available models
        self.fallback_chains = {}
        
        for task_type in TaskType:
            # Filter models that are good for this task type
            suitable_models = [
                provider for provider in available_models
                if task_type in self.models[provider].task_specialties
            ]
            
            # If no specific models for this task, use all available models
            if not suitable_models:
                suitable_models = available_models.copy()
            
            # Sort by quality rating for this task
            suitable_models.sort(
                key=lambda p: self.models[p].quality_rating + self.models[p].reliability,
                reverse=True
            )
            
            self.fallback_chains[task_type] = suitable_models
        
        # Print the configured chains
        print("✅ Fallback chains configured for all task types")
        for task_type, chain in self.fallback_chains.items():
            if chain:
                primary_model = self.models[chain[0]].name
                print(f"  - {task_type.value}: {primary_model} → {len(chain)-1} fallbacks")
            else:
                print(f"  - {task_type.value}: No available models")
        
        # Show the primary chain
        if available_models:
            primary_model = self.models[available_models[0]].name
            print(f"🎯 Primary Model: {primary_model}")
            if len(available_models) > 1:
                fallback_model = self.models[available_models[1]].name
                print(f"🔄 Primary Fallback: {fallback_model}")
    
    def get_llm_instance(self, provider: ModelProvider) -> Optional[ChatOpenAI]:
        """Get LLM instance for a specific provider"""
        try:
            if provider.value.startswith("groq/"):
                return ChatOpenAI(
                    model=provider.value,
                    api_key=os.getenv("GROQ_API_KEY"),
                    base_url="https://api.groq.com/openai/v1",  # Groq's OpenAI-compatible endpoint
                    temperature=self.models[provider].temperature,
                    max_tokens=self.models[provider].max_tokens
                )
            elif provider.value.startswith("gemini"):
                return ChatGoogleGenerativeAI(
                    model=provider.value,
                    google_api_key=os.getenv("GOOGLE_API_KEY"),
                    temperature=self.models[provider].temperature,
                    max_output_tokens=self.models[provider].max_tokens
                )
            else:
                print(f"❌ Unknown provider: {provider.value}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating LLM instance for {provider.value}: {e}")
            return None
    
    def select_optimal_model(self, task_type: TaskType, budget_limit: float = None) -> ModelProvider:
        """Select the optimal model based on task type, performance, and budget"""
        available_models = [
            provider for provider in self.fallback_chains[task_type]
            if self.models[provider].is_available and 
            (budget_limit is None or self.models[provider].cost_per_1k_tokens <= budget_limit)
        ]
        
        if not available_models:
            # Fallback to any available model
            available_models = [
                provider for provider in self.models.keys()
                if self.models[provider].is_available
            ]
        
        if not available_models:
            raise Exception("No available models found")
        
        # Score models based on multiple factors
        model_scores = {}
        for provider in available_models:
            config = self.models[provider]
            
            # Calculate composite score
            performance_score = (config.speed_rating * 0.3 + 
                               config.quality_rating * 0.4 + 
                               config.reliability * 10 * 0.3)
            
            # Adjust for recent performance
            success_rate = (config.success_count / (config.success_count + config.failure_count + 1))
            performance_score *= success_rate
            
            # Adjust for load balancing (prefer less recently used models)
            time_since_last_use = time.time() - config.last_used
            load_balance_factor = min(time_since_last_use / 60, 1.0)  # Normalize to 1 minute
            performance_score *= (1 + load_balance_factor * 0.2)
            
            model_scores[provider] = performance_score
        
        # Select model with highest score
        optimal_model = max(model_scores.items(), key=lambda x: x[1])[0]
        
        print(f"🎯 Selected optimal model for {task_type.value}: {self.models[optimal_model].name}")
        return optimal_model
    
    async def execute_with_fallback(self, 
                                  prompt: str, 
                                  task_type: TaskType = TaskType.GENERAL,
                                  budget_limit: float = None,
                                  max_fallbacks: int = 3) -> FallbackResult:
        """
        Execute prompt with intelligent fallback system
        
        Args:
            prompt: The prompt to execute
            task_type: Type of task for optimal model selection
            budget_limit: Maximum cost per 1k tokens
            max_fallbacks: Maximum number of fallback attempts
            
        Returns:
            FallbackResult with content and metadata
        """
        start_time = time.time()
        fallback_count = 0
        errors = []
        
        # Get fallback chain for task type
        fallback_chain = self.fallback_chains[task_type]
        
        # Check if any models are available
        if not fallback_chain:
            error_msg = "No LLM models available. Please configure API keys in .env file"
            errors.append(error_msg)
            print(f"❌ {error_msg}")
            return FallbackResult(
                content="No LLM models available. Please configure API keys in .env file",
                model_used="None",
                provider=None,
                response_time=time.time() - start_time,
                cost_estimate=0.0,
                confidence_score=0.0,
                fallback_count=0,
                errors=errors
            )
        
        for attempt in range(min(len(fallback_chain), max_fallbacks + 1)):
            try:
                # Select optimal model
                if attempt == 0:
                    selected_provider = self.select_optimal_model(task_type, budget_limit)
                else:
                    # Use next model in fallback chain
                    selected_provider = fallback_chain[attempt - 1]
                
                # Check if model is available
                if not self.models[selected_provider].is_available:
                    errors.append(f"Model {selected_provider.value} is not available")
                    continue
                
                # Get LLM instance
                llm = self.get_llm_instance(selected_provider)
                if not llm:
                    errors.append(f"Failed to create LLM instance for {selected_provider.value}")
                    continue
                
                # Execute prompt
                print(f"🤖 Attempting with {self.models[selected_provider].name} (attempt {attempt + 1})")
                attempt_start = time.time()
                
                messages = [HumanMessage(content=prompt)]
                response = await llm.ainvoke(messages)
                
                attempt_time = time.time() - attempt_start
                total_time = time.time() - start_time
                
                # Update model statistics
                self.models[selected_provider].success_count += 1
                self.models[selected_provider].last_used = time.time()
                self.models[selected_provider].avg_response_time = (
                    (self.models[selected_provider].avg_response_time * 
                     (self.models[selected_provider].success_count - 1) + attempt_time) /
                    self.models[selected_provider].success_count
                )
                
                # Calculate cost estimate
                estimated_tokens = len(prompt.split()) + len(response.content.split())
                cost_estimate = (estimated_tokens / 1000) * self.models[selected_provider].cost_per_1k_tokens
                
                # Calculate confidence score
                confidence_score = self.calculate_confidence_score(
                    selected_provider, attempt_time, fallback_count
                )
                
                print(f"✅ Success with {self.models[selected_provider].name} in {attempt_time:.2f}s")
                
                return FallbackResult(
                    content=response.content,
                    model_used=self.models[selected_provider].name,
                    provider=selected_provider,
                    response_time=total_time,
                    cost_estimate=cost_estimate,
                    confidence_score=confidence_score,
                    fallback_count=fallback_count,
                    errors=errors
                )
                
            except Exception as e:
                error_msg = f"Attempt {attempt + 1} failed with {selected_provider.value}: {str(e)}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
                
                # Update failure statistics
                self.models[selected_provider].failure_count += 1
                
                # Check if we should mark model as unavailable
                failure_rate = (self.models[selected_provider].failure_count / 
                              (self.models[selected_provider].success_count + 
                               self.models[selected_provider].failure_count))
                
                if failure_rate > 0.5 and self.models[selected_provider].failure_count > 3:
                    print(f"⚠️ Marking {selected_provider.value} as unavailable due to high failure rate")
                    self.models[selected_provider].is_available = False
                
                fallback_count += 1
                continue
        
        # All attempts failed
        total_time = time.time() - start_time
        return FallbackResult(
            content="All LLM attempts failed. Please check your API keys and network connection.",
            model_used="None",
            provider=None,
            response_time=total_time,
            cost_estimate=0.0,
            confidence_score=0.0,
            fallback_count=fallback_count,
            errors=errors
        )
    
    def calculate_confidence_score(self, 
                                 provider: ModelProvider, 
                                 response_time: float, 
                                 fallback_count: int) -> float:
        """Calculate confidence score for the result"""
        config = self.models[provider]
        
        # Base confidence from model quality
        base_confidence = config.quality_rating / 10.0
        
        # Adjust for response time (faster is better, up to a point)
        time_factor = min(response_time / 5.0, 1.0)  # Normalize to 5 seconds
        time_confidence = 1.0 - (time_factor * 0.2)
        
        # Adjust for fallback count (fewer fallbacks is better)
        fallback_penalty = fallback_count * 0.1
        
        # Adjust for reliability
        reliability_factor = config.reliability
        
        # Calculate final confidence
        confidence = (base_confidence * 0.4 + 
                     time_confidence * 0.2 + 
                     reliability_factor * 0.3 - 
                     fallback_penalty)
        
        return max(0.0, min(1.0, confidence))
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            "total_models": len(self.models),
            "available_models": len([m for m in self.models.values() if m.is_available]),
            "model_status": {},
            "performance_metrics": {},
            "fallback_chains": {task.value: [p.value for p in chain] 
                              for task, chain in self.fallback_chains.items()}
        }
        
        for provider, config in self.models.items():
            status["model_status"][provider.value] = {
                "name": config.name,
                "available": config.is_available,
                "success_count": config.success_count,
                "failure_count": config.failure_count,
                "success_rate": (config.success_count / 
                               (config.success_count + config.failure_count + 1)),
                "avg_response_time": config.avg_response_time,
                "last_used": config.last_used
            }
        
        return status

class HealthMonitor:
    """Monitor system health and performance"""
    
    def __init__(self):
        self.health_checks = []
        self.performance_metrics = {}
    
    def add_health_check(self, check_func: Callable) -> None:
        """Add a health check function"""
        self.health_checks.append(check_func)
    
    async def run_health_checks(self) -> Dict[str, bool]:
        """Run all health checks"""
        results = {}
        for check in self.health_checks:
            try:
                results[check.__name__] = await check()
            except Exception as e:
                results[check.__name__] = False
                print(f"❌ Health check {check.__name__} failed: {e}")
        return results

# Example usage
if __name__ == "__main__":
    # Test the advanced fallback system
    async def test_fallback_system():
        fallback_system = AdvancedFallbackSystem()
        
        # Test with different task types
        test_prompts = [
            ("Research Apple Inc. and provide a brief overview.", TaskType.RESEARCH),
            ("Analyze the sentiment of this text: 'Apple reported strong earnings.'", TaskType.SENTIMENT),
            ("Create an investment thesis for Tesla.", TaskType.THESIS)
        ]
        
        for prompt, task_type in test_prompts:
            print(f"\n🧪 Testing {task_type.value} task...")
            result = await fallback_system.execute_with_fallback(prompt, task_type)
            
            print(f"📊 Result:")
            print(f"   Model: {result.model_used}")
            print(f"   Time: {result.response_time:.2f}s")
            print(f"   Cost: ${result.cost_estimate:.6f}")
            print(f"   Confidence: {result.confidence_score:.2f}")
            print(f"   Fallbacks: {result.fallback_count}")
            print(f"   Content: {result.content[:100]}...")
        
        # Show system status
        status = fallback_system.get_system_status()
        print(f"\n📈 System Status:")
        print(f"   Available Models: {status['available_models']}/{status['total_models']}")
        
        for model, info in status['model_status'].items():
            print(f"   {model}: {info['success_rate']:.2f} success rate, "
                  f"{info['avg_response_time']:.2f}s avg time")
    
    # Run the test
    asyncio.run(test_fallback_system()) 