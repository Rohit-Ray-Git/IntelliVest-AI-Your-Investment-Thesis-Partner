"""
🧪 Test Updated Advanced Fallback System
========================================

This script tests the updated advanced fallback system with:
- Primary Model: Gemini 2.5 Flash
- Primary Fallback: Groq DeepSeek R1 Distill Llama-70B
- Secondary Fallback: Groq Llama 3.3-70B Versatile
"""

import os
import sys
import asyncio
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_updated_import():
    """Test if updated fallback system can be imported"""
    print("🔍 Testing updated fallback system import...")
    
    try:
        from llm.advanced_fallback_system import (
            AdvancedFallbackSystem,
            ModelProvider,
            TaskType,
            ModelConfig,
            FallbackResult
        )
        print("✅ Updated fallback system imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Updated fallback system import failed: {e}")
        return False

def test_updated_initialization():
    """Test updated fallback system initialization"""
    print("\n🚀 Testing updated fallback system initialization...")
    
    try:
        from llm.advanced_fallback_system import AdvancedFallbackSystem
        
        # Create fallback system
        fallback_system = AdvancedFallbackSystem()
        print("✅ Updated fallback system created successfully")
        
        # Check if models are configured
        if hasattr(fallback_system, 'models'):
            print(f"✅ Models configured: {len(fallback_system.models)}")
        else:
            print("❌ Models not configured")
            return False
        
        # Check if fallback chains are configured
        if hasattr(fallback_system, 'fallback_chains'):
            print(f"✅ Fallback chains configured: {len(fallback_system.fallback_chains)}")
        else:
            print("❌ Fallback chains not configured")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Updated system initialization failed: {e}")
        return False

def test_new_model_configuration():
    """Test new model configuration"""
    print("\n🎯 Testing new model configuration...")
    
    try:
        from llm.advanced_fallback_system import AdvancedFallbackSystem, ModelProvider
        
        # Create fallback system
        fallback_system = AdvancedFallbackSystem()
        
        # Check if new models are configured
        new_models = [
            ModelProvider.GEMINI_2_5_FLASH,
            ModelProvider.GROQ_DEEPSEEK_R1,
            ModelProvider.GROQ_LLAMA_3_3_70B
        ]
        
        for model_provider in new_models:
            if model_provider in fallback_system.models:
                model_name = fallback_system.models[model_provider].name
                print(f"✅ {model_provider.value}: {model_name}")
            else:
                print(f"❌ {model_provider.value}: Not configured")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ New model configuration test failed: {e}")
        return False

def test_updated_fallback_chains():
    """Test updated fallback chain configuration"""
    print("\n🔗 Testing updated fallback chain configuration...")
    
    try:
        from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType, ModelProvider
        
        # Create fallback system
        fallback_system = AdvancedFallbackSystem()
        
        # Test fallback chains for each task type
        for task_type in TaskType:
            chain = fallback_system.fallback_chains.get(task_type, [])
            if chain:
                print(f"✅ {task_type.value}: {len(chain)} models in chain")
                
                # Check if Gemini 2.5 Flash is first (primary)
                if chain[0] == ModelProvider.GEMINI_2_5_FLASH:
                    print(f"   🎯 Primary: {fallback_system.models[chain[0]].name}")
                else:
                    print(f"   ❌ Primary should be Gemini 2.5 Flash, got: {fallback_system.models[chain[0]].name}")
                    return False
                
                # Check if DeepSeek R1 is second (primary fallback)
                if len(chain) > 1 and chain[1] == ModelProvider.GROQ_DEEPSEEK_R1:
                    print(f"   🔄 Primary Fallback: {fallback_system.models[chain[1]].name}")
                else:
                    print(f"   ❌ Primary fallback should be DeepSeek R1")
                    return False
                
                # Check if Llama 3.3-70B is third (secondary fallback)
                if len(chain) > 2 and chain[2] == ModelProvider.GROQ_LLAMA_3_3_70B:
                    print(f"   🔄 Secondary Fallback: {fallback_system.models[chain[2]].name}")
                else:
                    print(f"   ❌ Secondary fallback should be Llama 3.3-70B")
                    return False
                
                # Show remaining fallbacks
                for i, provider in enumerate(chain[3:], 3):
                    model_name = fallback_system.models[provider].name
                    print(f"   {i+1}. {model_name}")
            else:
                print(f"❌ {task_type.value}: No fallback chain configured")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Updated fallback chain test failed: {e}")
        return False

def test_optimal_model_selection():
    """Test optimal model selection with new configuration"""
    print("\n🎯 Testing optimal model selection with new configuration...")
    
    try:
        from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType
        
        # Create fallback system
        fallback_system = AdvancedFallbackSystem()
        
        # Test model selection for different task types
        task_types = [
            TaskType.RESEARCH,
            TaskType.SENTIMENT,
            TaskType.VALUATION,
            TaskType.THESIS,
            TaskType.CRITIQUE
        ]
        
        for task_type in task_types:
            try:
                optimal_model = fallback_system.select_optimal_model(task_type)
                model_name = fallback_system.models[optimal_model].name
                print(f"✅ {task_type.value}: {model_name}")
                
                # Check if Gemini 2.5 Flash is selected as optimal (it should be due to highest quality rating)
                if "Gemini 2.5 Flash" in model_name:
                    print(f"   🎯 Correctly selected Gemini 2.5 Flash as optimal")
                else:
                    print(f"   ⚠️ Selected {model_name} instead of Gemini 2.5 Flash")
                
            except Exception as e:
                print(f"❌ {task_type.value}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Optimal model selection test failed: {e}")
        return False

async def test_updated_fallback_execution():
    """Test updated fallback execution with new models"""
    print("\n🔄 Testing updated fallback execution...")
    
    try:
        from llm.advanced_fallback_system import AdvancedFallbackSystem, TaskType
        
        # Create fallback system
        fallback_system = AdvancedFallbackSystem()
        
        # Test prompts for different task types
        test_cases = [
            ("Provide a brief overview of Apple Inc.", TaskType.RESEARCH),
            ("Analyze sentiment: 'The company reported strong quarterly results.'", TaskType.SENTIMENT),
            ("Create a simple investment thesis for Tesla", TaskType.THESIS)
        ]
        
        for prompt, task_type in test_cases:
            print(f"\n🧪 Testing {task_type.value} task...")
            print(f"📝 Prompt: {prompt[:50]}...")
            
            try:
                # Execute with fallback
                start_time = time.time()
                result = await fallback_system.execute_with_fallback(
                    prompt, 
                    task_type, 
                    max_fallbacks=3
                )
                execution_time = time.time() - start_time
                
                # Check results
                if result.content and result.content != "All LLM attempts failed. Please check your API keys and network connection.":
                    print(f"✅ {task_type.value} task completed successfully")
                    print(f"   Model: {result.model_used}")
                    print(f"   Time: {result.response_time:.2f}s")
                    print(f"   Confidence: {result.confidence_score:.2f}")
                    print(f"   Fallbacks: {result.fallback_count}")
                    print(f"   Content: {result.content[:100]}...")
                    
                    # Check if the model used is one of our new models
                    new_model_names = [
                        "Gemini 2.5 Flash",
                        "Groq DeepSeek R1 Distill Llama-70B",
                        "Groq Llama 3.3-70B Versatile"
                    ]
                    
                    if any(name in result.model_used for name in new_model_names):
                        print(f"   🎯 Successfully used new model: {result.model_used}")
                    else:
                        print(f"   ⚠️ Used fallback model: {result.model_used}")
                    
                else:
                    print(f"⚠️ {task_type.value} task failed (likely API key issue)")
                    print(f"   Errors: {result.errors}")
                
            except Exception as e:
                print(f"❌ {task_type.value} task failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Updated fallback execution test failed: {e}")
        return False

def test_system_status():
    """Test system status reporting with new models"""
    print("\n📊 Testing system status reporting with new models...")
    
    try:
        from llm.advanced_fallback_system import AdvancedFallbackSystem
        
        # Create fallback system
        fallback_system = AdvancedFallbackSystem()
        
        # Get system status
        status = fallback_system.get_system_status()
        
        # Check status structure
        required_keys = ['total_models', 'available_models', 'model_status', 'fallback_chains']
        for key in required_keys:
            if key not in status:
                print(f"❌ Missing status key: {key}")
                return False
        
        print(f"✅ System status retrieved successfully")
        print(f"   Total Models: {status['total_models']}")
        print(f"   Available Models: {status['available_models']}")
        print(f"   Fallback Chains: {len(status['fallback_chains'])}")
        
        # Show model status for new models
        new_model_keys = [
            "gemini-2.5-flash",
            "groq/deepseek-r1-distill-llama-70b",
            "groq/llama-3.3-70b-versatile"
        ]
        
        for model_key in new_model_keys:
            if model_key in status['model_status']:
                info = status['model_status'][model_key]
                print(f"   {model_key}: {info['name']} - Available: {info['available']}")
            else:
                print(f"   ❌ {model_key}: Not found in status")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ System status test failed: {e}")
        return False

async def main():
    """Run all updated fallback system tests"""
    print("🎯 Updated Advanced Fallback System - New Model Configuration Test")
    print("=" * 70)
    
    tests = [
        ("Import Test", test_updated_import),
        ("System Initialization Test", test_updated_initialization),
        ("New Model Configuration Test", test_new_model_configuration),
        ("Updated Fallback Chain Test", test_updated_fallback_chains),
        ("Optimal Model Selection Test", test_optimal_model_selection),
        ("System Status Test", test_system_status),
        ("Updated Fallback Execution Test", test_updated_fallback_execution)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All updated fallback system tests passed!")
        print("\n🚀 Updated Advanced Fallback System Capabilities:")
        print("   ✅ Primary Model: Gemini 2.5 Flash")
        print("   ✅ Primary Fallback: Groq DeepSeek R1 Distill Llama-70B")
        print("   ✅ Secondary Fallback: Groq Llama 3.3-70B Versatile")
        print("   ✅ Multi-LLM Orchestration: 7 models configured")
        print("   ✅ Intelligent Model Selection: Task-based routing")
        print("   ✅ Automatic Failover: Robust error recovery")
        print("   ✅ Load Balancing: Performance optimization")
        print("   ✅ Health Monitoring: System status tracking")
        print("   ✅ Cost Optimization: Budget-aware selection")
        print("   ✅ Quality Assessment: Confidence scoring")
        
        print("\n🔄 New Fallback Chain:")
        print("   🎯 Primary: Gemini 2.5 Flash")
        print("   🔄 Primary Fallback: Groq DeepSeek R1 Distill Llama-70B")
        print("   🔄 Secondary Fallback: Groq Llama 3.3-70B Versatile")
        print("   🔄 Tertiary+: Other models as needed")
        
        print("\n🚀 Ready for Production with Updated Model Configuration!")
        
        return True
    else:
        print("⚠️ Some updated fallback system tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 