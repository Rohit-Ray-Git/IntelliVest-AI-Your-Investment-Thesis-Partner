# agents/thesis_rewrite_agent.py

import asyncio
from utils.ai_client import ai_client

class ThesisRewriteAgent:
    def __init__(self):
        pass

    async def revise_thesis(self, thesis_markdown: str, critique: str, company_name: str) -> str:
        """Revise the investment thesis based on the critique"""
        
        prompt = f"""
        Revise the following investment thesis for {company_name} based on the provided critique to create a more robust and balanced analysis.
        
        **Original Investment Thesis:**
        {thesis_markdown}
        
        **Critique and Feedback:**
        {critique}
        
        Create an improved investment thesis that:
        1. Addresses the key issues raised in the critique
        2. Maintains objectivity and balance
        3. Incorporates additional risk factors and counter-arguments
        4. Strengthens the analysis with more robust reasoning
        5. Provides a more comprehensive view of the investment opportunity
        
        Format your response in clear markdown with proper structure and headings.
        Ensure the revised thesis is more thorough and addresses the critique constructively.
        """
        
        messages = [
            {"role": "system", "content": "You are a senior investment analyst specializing in creating comprehensive and balanced investment theses."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            result = await ai_client.get_completion(messages, max_tokens=3000)
            return result
        except Exception as e:
            print(f"❌ Thesis revision failed: {e}")
            return "Thesis revision could not be completed due to technical issues. Please try again later."
