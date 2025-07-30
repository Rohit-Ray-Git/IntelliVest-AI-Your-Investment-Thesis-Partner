# utils/ai_client.py

import asyncio
import time
import random
from typing import List, Dict, Any
import litellm
from litellm import completion

class RobustAIClient:
    def __init__(self):
        self.providers = [
            "gemini/gemini-2.0-flash-exp",
            "groq/deepseek-coder",
            "groq/llama3.1-70b-8192",
            "openai/gpt-4o-mini",
            "anthropic/claude-3-haiku-20240307"
        ]
        self.current_provider_index = 0
        self.retry_delays = [1, 2, 5, 10, 30]  # Progressive delays
        self.max_retries = 3
        
    async def get_completion(self, messages: List[Dict], max_tokens: int = 4000) -> str:
        """Get completion with automatic fallback and retry logic"""
        
        for attempt in range(self.max_retries):
            try:
                # Try current provider
                provider = self.providers[self.current_provider_index]
                print(f"🤖 Using AI provider: {provider}")
                
                response = completion(
                    model=provider,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                error_msg = str(e).lower()
                print(f"❌ Error with {provider}: {e}")
                
                # Check if it's a rate limit error
                if "429" in error_msg or "quota" in error_msg or "rate limit" in error_msg:
                    print(f"⏳ Rate limit hit, switching provider...")
                    self.current_provider_index = (self.current_provider_index + 1) % len(self.providers)
                    
                    # Add delay before retry
                    delay = self.retry_delays[min(attempt, len(self.retry_delays) - 1)]
                    print(f"⏰ Waiting {delay} seconds before retry...")
                    await asyncio.sleep(delay)
                    
                elif "timeout" in error_msg or "connection" in error_msg:
                    print(f"🌐 Connection issue, retrying...")
                    await asyncio.sleep(2)
                    
                else:
                    # For other errors, try next provider
                    self.current_provider_index = (self.current_provider_index + 1) % len(self.providers)
                    await asyncio.sleep(1)
        
        # If all providers fail, return a fallback response
        print("⚠️ All AI providers failed, using fallback response")
        return self._get_fallback_response(messages)
    
    def _get_fallback_response(self, messages: List[Dict]) -> str:
        """Provide a basic fallback response when all AI providers fail"""
        last_message = messages[-1]["content"] if messages else ""
        
        if "sentiment" in last_message.lower():
            return "Based on the available information, the sentiment appears to be neutral to slightly positive. However, a comprehensive analysis requires access to the full content and AI processing capabilities."
        
        elif "valuation" in last_message.lower():
            return "Valuation analysis requires detailed financial data and market context. Without full AI processing capabilities, I cannot provide a complete valuation assessment."
        
        elif "thesis" in last_message.lower():
            return "Investment thesis generation requires comprehensive analysis of multiple data points. Due to technical limitations, I cannot provide a complete investment thesis at this time."
        
        else:
            return "I apologize, but I'm unable to process this request due to technical limitations with the AI service providers. Please try again later or contact support if the issue persists."
    
    def reset_provider_index(self):
        """Reset to first provider for new requests"""
        self.current_provider_index = 0

# Global instance
ai_client = RobustAIClient() 