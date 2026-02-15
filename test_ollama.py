"""
Test script to verify Ollama integration with JARVIS
"""

print("Testing Ollama integration...")
print("=" * 50)

# Test 1: Import Ollama client
print("\n1. Testing imports...")
try:
    from engine.ollama_client import ollama_client
    from engine.ollama_config import OLLAMA_ENDPOINT, OLLAMA_MODEL
    print(f"✓ Imports successful")
    print(f"  Endpoint: {OLLAMA_ENDPOINT}")
    print(f"  Model: {OLLAMA_MODEL}")
except Exception as e:
    print(f"✗ Import failed: {e}")
    exit(1)

# Test 2: Test Ollama connection
print("\n2. Testing Ollama connection...")
try:
    success, message = ollama_client.test_connection()
    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ Connection test failed: {message}")
        print("\nMake sure:")
        print("  1. Ollama is installed")
        print("  2. Ollama service is running (ollama serve)")
        print("  3. Model llama3:8b is pulled (ollama pull llama3:8b)")
        exit(1)
except Exception as e:
    print(f"✗ Connection error: {e}")
    exit(1)

# Test 3: Test simple generation with Ollama
print("\n3. Testing text generation...")
try:
    response = ollama_client.generate("Say hello in one sentence", max_tokens=50)
    print(f"✓ Generation successful")
    print(f"  Response: {response}")
except Exception as e:
    print(f"✗ Generation failed: {e}")
    exit(1)

# Test 4: Test chat interface
print("\n4. Testing chat interface...")
try:
    messages = [
        {"role": "user", "content": "What is 2+2? Answer in one word."}
    ]
    response = ollama_client.chat(messages, max_tokens=10)
    print(f"✓ Chat successful")
    print(f"  Response: {response}")
except Exception as e:
    print(f"✗ Chat failed: {e}")
    exit(1)

# Test 5: Test fallback system
print("\n5. Testing AI fallback system...")
try:
    from engine.ai_fallback_system import try_all_ai_providers
    # This will try Groq -> Gemini -> Ollama
    response = try_all_ai_providers("Say 'test' in one word", system_prompt="You are a helpful assistant")
    if response:
        print(f"✓ Fallback system working")
        print(f"  Response: {response}")
    else:
        print(f"⚠ All providers failed (this is expected if Groq and Gemini APIs are unavailable)")
except Exception as e:
    print(f"✗ Fallback test error: {e}")

print("\n" + "=" * 50)
print("✓ Ollama integration test complete!")
print("\nYour JARVIS will now use this fallback chain:")
print("  1. Groq (if API key is valid)")
print("  2. Gemini (if API key is valid)")
print("  3. Ollama (local Llama model)")
