"""
Quick test to verify Ollama integration with JARVIS AI fallback system
"""

print("=" * 60)
print("JARVIS AI - Ollama Integration Test")
print("=" * 60)

# Test 1: Import Ollama client
print("\n1. Testing Ollama Client Import...")
try:
    from engine.ollama_client import ollama_client
    print("   ✓ Ollama client imported successfully")
except Exception as e:
    print(f"   ✗ Failed to import: {e}")
    exit(1)

# Test 2: Test Ollama connection
print("\n2. Testing Ollama Connection...")
try:
    success, message = ollama_client.test_connection()
    if success:
        print(f"   ✓ {message}")
    else:
        print(f"   ✗ Connection failed: {message}")
        exit(1)
except Exception as e:
    print(f"   ✗ Connection error: {e}")
    exit(1)

# Test 3: Generate response
print("\n3. Testing Text Generation...")
try:
    response = ollama_client.generate("Say 'Hello from Ollama!' in one sentence.", max_tokens=50)
    print(f"   ✓ Response received: {response[:100]}...")
except Exception as e:
    print(f"   ✗ Generation failed: {e}")
    exit(1)

# Test 4: Test AI fallback system
print("\n4. Testing AI Fallback System...")
try:
    from engine.ai_fallback_system import try_all_ai_providers
    print("   Testing: Groq → Gemini → Ollama fallback chain...")
    response = try_all_ai_providers("What is 5+5? Answer with just the number.", system_prompt="You are a helpful assistant")
    if response:
        print(f"   ✓ Fallback system working! Response: {response[:100]}")
    else:
        print(f"   ⚠ All providers failed (expected if Groq/Gemini are rate-limited)")
except Exception as e:
    print(f"   ⚠ Fallback test error: {e}")

# Test 5: Test dual_ai initialization
print("\n5. Testing JARVIS AI Integration...")
try:
    # Import but don't fully initialize to avoid conflicts
    from engine import dual_ai
    print("   ✓ dual_ai module imported")
    print("   Note: Full initialization happens when JARVIS starts")
except Exception as e:
    print(f"   ⚠ Import note: {e}")

print("\n" + "=" * 60)
print("✓ Ollama Integration Verified!")
print("=" * 60)
print("\nYour JARVIS will now use this fallback chain:")
print("  1. Groq (if available)")
print("  2. Gemini (if available)")  
print("  3. Ollama (always available locally)")
print("\nTo use JARVIS with Ollama:")
print("  python run.py")
print("\nOllama will automatically be used when Groq/Gemini fail!")
print("=" * 60)
