# Ollama Integration Guide for JARVIS

## Overview
JARVIS has been updated to use **Ollama** with the local **Llama3:8b** model as a fallback when Groq and Gemini APIs hit their rate limits.

## Fallback Chain
Your JARVIS will now try AI providers in this order:
1. **Groq** (if API is available)
2. **Gemini** (if API is available)
3. **Ollama** (local Llama model - always available!)

## Setup Instructions

### Step 1: Install Ollama
1. Download Ollama from: https://ollama.ai/download
2. Run the installer for Windows
3. Ollama will install and start automatically

### Step 2: Pull the Llama Model
Open PowerShell or Command Prompt and run:
```powershell
ollama pull llama3:8b
```

This will download the Llama3 8B model (~4.7GB). Wait for it to complete.

### Step 3: Verify Ollama is Running
Check if Ollama is running:
```powershell
ollama list
```

You should see `llama3:8b` in the list.

### Step 4: Test the Integration
Run the test script:
```powershell
python test_ollama.py
```

If all tests pass, you're ready to go!

### Step 5: Start JARVIS
```powershell
python run.py
```

JARVIS will now automatically use Ollama when Groq and Gemini fail!

## Configuration

The Ollama settings are in `engine/ollama_config.py`:
```python
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3:8b"
```

You can change the model if you want to use a different one:
- `llama3:8b` - Fast, balanced (4.7GB)
- `llama3:70b` - More powerful but slower (40GB)
- `mistral` - Alternative model (4.1GB)

To change the model:
1. Pull the new model: `ollama pull <model-name>`
2. Update `OLLAMA_MODEL` in `engine/ollama_config.py`

## Troubleshooting

### "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check if the service is active: `ollama list`

### "Model not found"
- Pull the model: `ollama pull llama3:8b`
- Verify it downloaded: `ollama list`

### Slow responses
- Llama3:8b is fast on most systems
- If too slow, ensure no other heavy applications are running
- Consider using a smaller model like `tinyllama`

## Performance

Ollama/Llama3:8b runs locally on your machine:
- **Speed**: ~20-50 tokens/second (depending on your hardware)
- **Privacy**: All data stays on your computer
- **Cost**: Free - no API limits!
- **Availability**: Works offline

## What Changed?

### New Files Created:
1. `engine/ollama_config.py` - Ollama configuration
2. `engine/ollama_client.py` - Ollama API wrapper
3. `test_ollama.py` - Test script

### Modified Files:
1. `engine/ai_fallback_system.py` - Added Ollama fallback
2. `engine/dual_ai.py` - Added Ollama initialization

## Additional Notes

- Ollama runs as a background service
- The first response might be slower (model loading)
- Subsequent responses are much faster
- You can use Ollama for other projects too!

## Enjoy your API-limit-free JARVIS! 🎉
