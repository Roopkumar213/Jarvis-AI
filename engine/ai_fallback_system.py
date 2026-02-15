def try_all_ai_providers(prompt, system_prompt="", messages=None):
    """Try Groq -> Gemini -> Ollama in order"""
    
    # Try Groq first
    try:
        from engine.dual_ai import dual_ai
        if hasattr(dual_ai, 'groq_client'):
            response = dual_ai.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages or [{"role": "user", "content": prompt}],
                temperature=0.4
            )
            return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq failed: {e}")
    
    # Try Gemini second
    try:
        from engine.dual_ai import dual_ai
        if hasattr(dual_ai, 'gemini_model'):
            response = dual_ai.gemini_model.generate_content(prompt)
            return response.text.strip()
    except Exception as e:
        print(f"Gemini failed: {e}")
    
    # Try Ollama third (local fallback)
    try:
        from engine.ollama_client import ollama_client
        print("Using Ollama (local Llama model)...")
        if messages:
            response = ollama_client.chat(messages, temperature=0.4)
        else:
            response = ollama_client.generate(prompt, system_prompt, temperature=0.4)
        return response
    except Exception as e:
        print(f"Ollama failed: {e}")
 
    # All failed
    return None