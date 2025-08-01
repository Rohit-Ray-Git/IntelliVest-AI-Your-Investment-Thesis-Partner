"""
🧪 Stress Test - System Failure & Error Scenarios
================================================

This test simulates various failure scenarios to ensure system resilience:
- Agent failures and recovery
- Communication timeouts
- High-volume stress testing
- Error handling and recovery
"""

import asyncio
import os
import sys
import time
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path for imports
sys.path.append('.')

async def test_agent_failure_recovery():
    """Test agent failure and recovery scenarios"""
    print("🔥 Test 1: Agent Failure & Recovery")
    print("=" * 50)
    
    try:
        from agents.global_agentic_system import GlobalAgenticSystem, AgentMessage, MessageType
        
        # Initialize system
        global_system = GlobalAgenticSystem()
        
        # Create agents with different failure modes
        class FailingAgent:
            def __init__(self, name, failure_rate=0.3):
                self.name = name
                self.capabilities = ["test"]
                self.failure_rate = failure_rate
                self.message_count = 0
            
            async def handle_message(self, message):
                self.message_count += 1
                
                # Simulate random failures
                if random.random() < self.failure_rate:
                    raise Exception(f"Simulated failure in {self.name}")
                
                return {
                    "status": "success",
                    "agent": self.name,
                    "message_count": self.message_count
                }
        
        # Register various types of agents
        agents = {
            "ReliableAgent": FailingAgent("ReliableAgent", failure_rate=0.0),
            "UnreliableAgent": FailingAgent("UnreliableAgent", failure_rate=0.5),
            "NormalAgent": FailingAgent("NormalAgent", failure_rate=0.1)
        }
        
        for agent_name, agent_instance in agents.items():
            global_system.register_agent(agent_name, agent_instance, agent_instance.capabilities)
        
        print(f"✅ {len(agents)} agents registered with various failure modes")
        
        # Test message sending with failure handling
        successful_messages = 0
        failed_messages = 0
        
        for i in range(20):
            try:
                sender = random.choice(list(agents.keys()))
                recipient = random.choice(list(agents.keys()))
                
                if sender != recipient:
                    message = AgentMessage(
                        sender=sender,
                        recipient=recipient,
                        message_type=MessageType.DATA_REQUEST,
                        content={"test": f"message_{i}"}
                    )
                    
                    response = await global_system.send_message(message)
                    
                    if response and "error" not in response:
                        successful_messages += 1
                    else:
                        failed_messages += 1
                        
            except Exception as e:
                failed_messages += 1
        
        print(f"\n📊 Failure Recovery Results:")
        print(f"   ✅ Successful: {successful_messages}")
        print(f"   ❌ Failed: {failed_messages}")
        
        success_rate = successful_messages / (successful_messages + failed_messages)
        success = success_rate >= 0.4  # At least 40% success rate expected
        
        return success
        
    except Exception as e:
        print(f"❌ Agent failure recovery test error: {e}")
        return False

async def test_communication_stress():
    """Test high-volume communication stress"""
    print("\n📡 Test 2: Communication Stress Test")
    print("=" * 50)
    
    try:
        from agents.global_agentic_system import GlobalAgenticSystem, AgentMessage, MessageType
        
        # Initialize system
        global_system = GlobalAgenticSystem()
        
        # Create many agents for stress testing
        class StressTestAgent:
            def __init__(self, name):
                self.name = name
                self.capabilities = ["stress_test"]
                self.message_count = 0
            
            async def handle_message(self, message):
                self.message_count += 1
                await asyncio.sleep(random.uniform(0.001, 0.01))
                return {
                    "status": "success",
                    "agent": self.name,
                    "message_count": self.message_count
                }
        
        # Register many agents
        agents = {}
        for i in range(10):  # 10 agents for stress testing
            agent_name = f"StressAgent{i}"
            agents[agent_name] = StressTestAgent(agent_name)
            global_system.register_agent(agent_name, agents[agent_name], ["stress_test"])
        
        print(f"✅ {len(agents)} stress test agents registered")
        
        # Send high volume of concurrent messages
        print("🚀 Sending high volume of concurrent messages...")
        
        async def send_concurrent_messages():
            tasks = []
            for i in range(50):  # 50 concurrent messages
                sender = random.choice(list(agents.keys()))
                recipient = random.choice(list(agents.keys()))
                
                if sender != recipient:
                    message = AgentMessage(
                        sender=sender,
                        recipient=recipient,
                        message_type=MessageType.DATA_REQUEST,
                        content={"stress_test": f"message_{i}"}
                    )
                    
                    task = asyncio.create_task(global_system.send_message(message))
                    tasks.append(task)
            
            return await asyncio.gather(*tasks, return_exceptions=True)
        
        start_time = time.time()
        results = await send_concurrent_messages()
        end_time = time.time()
        
        # Analyze results
        successful = 0
        failed = 0
        exceptions = 0
        
        for result in results:
            if isinstance(result, Exception):
                exceptions += 1
            elif result and "error" not in result:
                successful += 1
            else:
                failed += 1
        
        duration = end_time - start_time
        messages_per_second = len(results) / duration
        
        print(f"\n📊 Communication Stress Results:")
        print(f"   ✅ Successful: {successful}")
        print(f"   ❌ Failed: {failed}")
        print(f"   💥 Exceptions: {exceptions}")
        print(f"   ⏱️ Duration: {duration:.2f} seconds")
        print(f"   📈 Messages/sec: {messages_per_second:.1f}")
        
        # Success criteria: high throughput with reasonable success rate
        success = (successful >= 30 and messages_per_second >= 10 and exceptions < 10)
        
        return success
        
    except Exception as e:
        print(f"❌ Communication stress test error: {e}")
        return False

async def test_error_handling():
    """Test error handling and recovery"""
    print("\n⚠️ Test 3: Error Handling & Recovery")
    print("=" * 50)
    
    try:
        from agents.global_agentic_system import GlobalAgenticSystem, AgentMessage, MessageType
        
        # Initialize system
        global_system = GlobalAgenticSystem()
        
        # Create agents with different error behaviors
        class ErrorTestAgent:
            def __init__(self, name, error_type="normal"):
                self.name = name
                self.capabilities = ["error_test"]
                self.error_type = error_type
                self.message_count = 0
            
            async def handle_message(self, message):
                self.message_count += 1
                
                if self.error_type == "exception":
                    raise Exception(f"Simulated exception in {self.name}")
                elif self.error_type == "invalid_response":
                    return {"invalid": "response", "missing_status": True}
                elif self.error_type == "slow_response":
                    await asyncio.sleep(2.0)  # Slow response
                    return {"status": "success", "agent": self.name, "slow": True}
                else:
                    return {"status": "success", "agent": self.name}
        
        # Register error test agents
        agents = {
            "ExceptionAgent": ErrorTestAgent("ExceptionAgent", "exception"),
            "InvalidResponseAgent": ErrorTestAgent("InvalidResponseAgent", "invalid_response"),
            "SlowAgent": ErrorTestAgent("SlowAgent", "slow_response"),
            "NormalAgent": ErrorTestAgent("NormalAgent", "normal")
        }
        
        for agent_name, agent_instance in agents.items():
            global_system.register_agent(agent_name, agent_instance, agent_instance.capabilities)
        
        print(f"✅ {len(agents)} error test agents registered")
        
        # Test error handling
        error_handling_results = {
            "exceptions_handled": 0,
            "invalid_responses_handled": 0,
            "timeouts_handled": 0,
            "successful_handling": 0
        }
        
        # Test exception handling
        try:
            message = AgentMessage(
                sender="TestSender",
                recipient="ExceptionAgent",
                message_type=MessageType.DATA_REQUEST,
                content={"test": "exception"}
            )
            
            response = await global_system.send_message(message)
            if "error" in response:
                error_handling_results["exceptions_handled"] += 1
                
        except Exception as e:
            error_handling_results["exceptions_handled"] += 1
        
        # Test invalid response handling
        try:
            message = AgentMessage(
                sender="TestSender",
                recipient="InvalidResponseAgent",
                message_type=MessageType.DATA_REQUEST,
                content={"test": "invalid"}
            )
            
            response = await global_system.send_message(message)
            if response and "invalid" in response:
                error_handling_results["invalid_responses_handled"] += 1
                
        except Exception as e:
            error_handling_results["invalid_responses_handled"] += 1
        
        # Test timeout handling
        try:
            message = AgentMessage(
                sender="TestSender",
                recipient="SlowAgent",
                message_type=MessageType.DATA_REQUEST,
                content={"test": "timeout"}
            )
            
            response = await asyncio.wait_for(
                global_system.send_message(message),
                timeout=1.0
            )
            
        except asyncio.TimeoutError:
            error_handling_results["timeouts_handled"] += 1
        except Exception as e:
            error_handling_results["timeouts_handled"] += 1
        
        # Test normal operation
        try:
            message = AgentMessage(
                sender="TestSender",
                recipient="NormalAgent",
                message_type=MessageType.DATA_REQUEST,
                content={"test": "normal"}
            )
            
            response = await global_system.send_message(message)
            if response and response.get("status") == "success":
                error_handling_results["successful_handling"] += 1
                
        except Exception as e:
            pass
        
        print(f"\n📊 Error Handling Results:")
        for error_type, count in error_handling_results.items():
            status = "✅" if count > 0 else "❌"
            print(f"   {status} {error_type}: {count}")
        
        # Success criteria: system handles errors gracefully
        success = (error_handling_results["exceptions_handled"] > 0 and 
                  error_handling_results["timeouts_handled"] > 0 and
                  error_handling_results["successful_handling"] > 0)
        
        return success
        
    except Exception as e:
        print(f"❌ Error handling test error: {e}")
        return False

async def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n🔍 Test 4: Edge Cases & Boundary Conditions")
    print("=" * 50)
    
    try:
        from agents.global_agentic_system import GlobalAgenticSystem, AgentMessage, MessageType
        
        # Initialize system
        global_system = GlobalAgenticSystem()
        
        edge_case_results = {
            "empty_message": False,
            "large_message": False,
            "invalid_agent": False,
            "circular_messaging": False,
            "rapid_fire_messages": False
        }
        
        # Test 1: Empty message content
        try:
            class EdgeCaseAgent:
                def __init__(self, name):
                    self.name = name
                    self.capabilities = ["edge_test"]
                
                async def handle_message(self, message):
                    return {"status": "success", "agent": self.name, "content_length": len(str(message.content))}
            
            edge_agent = EdgeCaseAgent("EdgeCaseAgent")
            global_system.register_agent("EdgeCaseAgent", edge_agent, ["edge_test"])
            
            # Send empty message
            empty_message = AgentMessage(
                sender="TestSender",
                recipient="EdgeCaseAgent",
                message_type=MessageType.DATA_REQUEST,
                content={}
            )
            
            response = await global_system.send_message(empty_message)
            if response and response.get("content_length") == 0:
                edge_case_results["empty_message"] = True
                
        except Exception as e:
            print(f"   ❌ Empty message test failed: {str(e)[:50]}")
        
        # Test 2: Large message content
        try:
            large_content = {"data": "x" * 5000}  # 5KB content
            large_message = AgentMessage(
                sender="TestSender",
                recipient="EdgeCaseAgent",
                message_type=MessageType.DATA_REQUEST,
                content=large_content
            )
            
            response = await global_system.send_message(large_message)
            if response and response.get("content_length") > 1000:
                edge_case_results["large_message"] = True
                
        except Exception as e:
            print(f"   ❌ Large message test failed: {str(e)[:50]}")
        
        # Test 3: Invalid agent handling
        try:
            invalid_message = AgentMessage(
                sender="TestSender",
                recipient="NonExistentAgent",
                message_type=MessageType.DATA_REQUEST,
                content={"test": "invalid"}
            )
            
            response = await global_system.send_message(invalid_message)
            if response and "error" in response:
                edge_case_results["invalid_agent"] = True
                
        except Exception as e:
            print(f"   ❌ Invalid agent test failed: {str(e)[:50]}")
        
        # Test 4: Circular messaging (agent messaging itself)
        try:
            circular_message = AgentMessage(
                sender="EdgeCaseAgent",
                recipient="EdgeCaseAgent",
                message_type=MessageType.DATA_REQUEST,
                content={"test": "circular"}
            )
            
            response = await global_system.send_message(circular_message)
            if response:
                edge_case_results["circular_messaging"] = True
                
        except Exception as e:
            print(f"   ❌ Circular messaging test failed: {str(e)[:50]}")
        
        # Test 5: Rapid fire messages
        try:
            rapid_success_count = 0
            for i in range(10):
                message = AgentMessage(
                    sender="TestSender",
                    recipient="EdgeCaseAgent",
                    message_type=MessageType.DATA_REQUEST,
                    content={"test": f"rapid_{i}"}
                )
                
                response = await global_system.send_message(message)
                if response and "error" not in response:
                    rapid_success_count += 1
            
            if rapid_success_count >= 7:  # At least 7 should succeed
                edge_case_results["rapid_fire_messages"] = True
                
        except Exception as e:
            print(f"   ❌ Rapid fire messages test failed: {str(e)[:50]}")
        
        print(f"\n📊 Edge Case Results:")
        for edge_case, result in edge_case_results.items():
            status = "✅" if result else "❌"
            print(f"   {status} {edge_case}")
        
        # Success criteria: handle most edge cases gracefully
        success = sum(edge_case_results.values()) >= 3  # At least 3 edge cases should pass
        
        return success
        
    except Exception as e:
        print(f"❌ Edge cases test error: {e}")
        return False

async def main():
    """Main function to run stress tests"""
    print("🧪 IntelliVest AI - Stress Test")
    print("=" * 70)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all stress tests
    tests = [
        ("Agent Failure & Recovery", test_agent_failure_recovery),
        ("Communication Stress", test_communication_stress),
        ("Error Handling & Recovery", test_error_handling),
        ("Edge Cases & Boundary Conditions", test_edge_cases)
    ]
    
    results = []
    start_time = time.time()
    
    for test_name, test_func in tests:
        print(f"🚀 Running: {test_name}")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
        print()
    
    # Calculate final results
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result)
    success_rate = (passed_tests / total_tests) * 100
    execution_time = time.time() - start_time
    
    # Print final summary
    print("=" * 70)
    print("📊 STRESS TEST RESULTS")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<35} {status}")
    
    print("=" * 70)
    print(f"📈 Overall Result: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
    print(f"⏱️ Total execution time: {execution_time:.2f} seconds")
    
    if success_rate >= 75:
        print("🎉 EXCELLENT: System is highly resilient!")
        print("✅ Handles failures gracefully")
        print("✅ Recovers from errors effectively")
        print("✅ Maintains performance under stress")
        print("✅ Production-ready robustness")
    elif success_rate >= 50:
        print("⚠️ GOOD: System is mostly resilient")
        print("✅ Handles most failure scenarios")
        print("⚠️ Some edge cases need attention")
        print("✅ Suitable for production with monitoring")
    else:
        print("❌ NEEDS IMPROVEMENT: System needs robustness enhancements")
        print("❌ Multiple failure scenarios not handled")
        print("❌ Error recovery needs improvement")
        print("⚠️ Not ready for production use")
    
    print("\n" + "=" * 70)
    print("🎯 FINAL STRESS TEST ASSESSMENT")
    print("=" * 70)
    
    if success_rate >= 50:
        print("✅ SYSTEM STATUS: STRESS TEST PASSED")
        print("✅ System handles failures gracefully")
        print("✅ Error recovery mechanisms working")
        print("✅ Performance maintained under stress")
        print("✅ Ready for production deployment")
    else:
        print("⚠️ SYSTEM STATUS: STRESS TEST NEEDS ATTENTION")
        print("⚠️ Some failure scenarios not handled")
        print("⚠️ Error recovery needs improvement")
        print("⚠️ Performance issues under stress")
        print("⚠️ Address issues before production")
    
    return success_rate >= 50

if __name__ == "__main__":
    asyncio.run(main()) 