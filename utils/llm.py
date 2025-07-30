# utils/llm.py

import os
import google.generativeai as genai
from openai import OpenAI

# --- Load Gemini ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

def call_gemini(prompt: str, context: str = "") -> str:
    try:
        full_prompt = f"{context}\n\nQuestion: {prompt}" if context else prompt
        response = gemini_model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Gemini Error] {str(e)}"

# --- Fallback to Groq DeepSeek ---
def call_groq_deepseek(prompt: str, context: str = "") -> str:
    from openai import OpenAI  # Groq Cloud uses OpenAI-compatible API
    client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))

    try:
        system_msg = "You are a helpful financial research assistant. Use the context provided if available."
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"{prompt}\n\nContext:\n{context}" if context else prompt},
        ]
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=messages,
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Groq Error] {str(e)}"
