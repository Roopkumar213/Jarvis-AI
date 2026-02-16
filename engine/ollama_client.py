import requests
import json
from engine.ollama_config import OLLAMA_ENDPOINT, OLLAMA_MODEL

class OllamaClient:
    """Client for interacting with local Ollama LLM"""
    
    def __init__(self, endpoint=None, model=None):
        self.endpoint = endpoint or OLLAMA_ENDPOINT
        self.model = model or OLLAMA_MODEL
        
    def generate(self, prompt, system_prompt="", max_tokens=2000, temperature=0.7):
        """Generate text using Ollama API
        
        Args:
            prompt: The user prompt/query
            system_prompt: Optional system instructions
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-1)
            
        Returns:
            Generated text string
        """
        try:
            # Build the full prompt with system message if provided
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(
                self.endpoint,
                json=payload,
                timeout=300  # 300 second timeout for local model
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception("Ollama request timeout - is Ollama running?")
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to Ollama - make sure it's running on localhost:11434")
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")
    
    def chat(self, messages, temperature=0.7, max_tokens=2000):
        """Chat-style interface compatible with OpenAI/Groq format
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text string
        """
        try:
            # Convert chat messages to a single prompt
            prompt_parts = []
            system_parts = []
            
            for msg in messages:
                role = msg.get('role', '')
                content = msg.get('content', '')
                
                if role == 'system':
                    system_parts.append(content)
                elif role == 'user':
                    prompt_parts.append(f"User: {content}")
                elif role == 'assistant':
                    prompt_parts.append(f"Assistant: {content}")
            
            # Combine system messages
            system_prompt = "\n".join(system_parts) if system_parts else ""
            
            # Combine conversation
            conversation = "\n".join(prompt_parts)
            conversation += "\nAssistant:"
            
            return self.generate(conversation, system_prompt, max_tokens, temperature)
            
        except Exception as e:
            raise Exception(f"Ollama chat error: {str(e)}")
    
    def test_connection(self):
        """Test if Ollama is running and accessible
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            response = self.generate("Hello", max_tokens=10)
            if response:
                return True, f"Ollama connected successfully using model {self.model}"
            return False, "Ollama returned empty response"
        except Exception as e:
            return False, str(e)

# Global instance
ollama_client = OllamaClient()
