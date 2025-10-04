# ChoreoAI Examples

This directory contains example scripts demonstrating how to use the OpenAI SDK client with ChoreoAI.

## Quick Start

### 1. Setup Environment

Run the setup script to create a virtual environment and install dependencies:

```bash
cd examples
./setup.sh
```

This will:
- Create a Python virtual environment in `./venv`
- Install the OpenAI SDK
- Install additional dependencies (python-dotenv, requests, numpy)

### 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 3. Set Your OpenAI API Key

```bash
export OPENAI_API_KEY=sk-your-actual-key-here
```

Or create a `.env` file in the examples directory:

```bash
cat > .env << EOF
OPENAI_API_KEY=sk-your-actual-key-here
CHOREOAI_BASE_URL=http://localhost:8000/v1
EOF
```

### 4. Start ChoreoAI Server

Make sure the ChoreoAI server is running:

```bash
cd ..
docker-compose up -d
```

Verify it's running:

```bash
curl http://localhost:8000/health
```

### 5. Run Examples

```bash
# Basic chat completion
python basic_usage.py

# Streaming responses
python streaming.py

# Embeddings and RAG
python embeddings_rag.py

# Function calling
python function_calling.py
```

## Examples Overview

### 1. basic_usage.py

**What it demonstrates:**
- Setting up the OpenAI client with ChoreoAI base URL
- Making a simple chat completion request
- Extracting response content and usage statistics

**Key concepts:**
- Client initialization with custom `base_url`
- Basic chat completion API
- Token usage tracking

**Run it:**
```bash
python basic_usage.py
```

**Expected output:**
```
📝 Assistant's response:
ChoreoAI is a unified API orchestration platform that routes requests
to multiple AI providers through a single interface.

📊 Usage statistics:
  • Prompt tokens: 45
  • Completion tokens: 22
  • Total tokens: 67
```

---

### 2. streaming.py

**What it demonstrates:**
- Real-time streaming of responses
- Processing response chunks as they arrive
- Creating a better UX for longer responses

**Key concepts:**
- Setting `stream=True` in the request
- Iterating over response chunks
- Displaying content in real-time

**Run it:**
```bash
python streaming.py
```

**Expected output:**
```
📝 Assistant's response (streaming):
Through APIs it weaves with grace,
Multiple models, one interface,
AI orchestration finds its place.

📊 Total characters received: 95
```

---

### 3. embeddings_rag.py

**What it demonstrates:**
- Creating embeddings for text
- Building a simple knowledge base
- Implementing semantic search
- Basic Retrieval-Augmented Generation (RAG)

**Key concepts:**
- Text embeddings API
- Cosine similarity for semantic search
- Using retrieved context for better answers
- RAG pipeline

**Requirements:**
- NumPy (installed by setup.sh)

**Run it:**
```bash
python embeddings_rag.py
```

**Expected output:**
```
📊 Top 3 most relevant documents:
1. Similarity: 0.8734
   ChoreoAI supports OpenAI, Claude, Gemini, and other AI models.

📝 Answer:
ChoreoAI supports OpenAI, Claude, Gemini, and other AI models.
```

---

### 4. function_calling.py

**What it demonstrates:**
- Defining functions/tools for the model to use
- Multi-step conversation flow
- Executing function calls based on model requests
- Combining function results into final response

**Key concepts:**
- Function/tool definitions
- Tool calling workflow
- JSON schema for function parameters
- Multi-turn conversations

**Run it:**
```bash
python function_calling.py
```

**Expected output:**
```
🔧 Calling function: get_current_weather
   Arguments: {'location': 'San Francisco'}
   Response: {'location': 'San Francisco', 'temperature': 65,
              'unit': 'fahrenheit', 'condition': 'Partly cloudy'}

🔧 Calling function: calculate_cost
   Arguments: {'provider': 'openai', 'tokens': 10000}
   Response: {'provider': 'openai', 'tokens': 10000,
              'cost_usd': 0.02, 'rate_per_1k': 0.002}

📝 Assistant's answer:
The current weather in San Francisco is partly cloudy with a
temperature of 65°F. Using OpenAI for 10,000 tokens would cost
approximately $0.02.
```

---

## How ChoreoAI Works

All examples use the OpenAI SDK client but point to ChoreoAI instead of OpenAI directly:

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="http://localhost:8000/v1"  # ChoreoAI endpoint
)
```

When you make a request:
1. Your app sends request to ChoreoAI (localhost:8000)
2. ChoreoAI validates and routes the request
3. ChoreoAI forwards to the appropriate provider (OpenAI, Claude, etc.)
4. Provider processes and returns response
5. ChoreoAI returns response to your app

**Benefits:**
- ✅ Single interface for multiple providers
- ✅ Easy to switch providers without code changes
- ✅ Built-in failover and load balancing
- ✅ Cost optimization across providers
- ✅ Request logging and monitoring

## Troubleshooting

### "Connection refused" Error

**Problem:** Cannot connect to ChoreoAI

**Solution:**
```bash
# Check if ChoreoAI is running
docker ps | grep choreoai

# If not running, start it
docker-compose up -d

# Verify health
curl http://localhost:8000/health
```

### "Authentication Error" or "Invalid API Key"

**Problem:** API key not set or invalid

**Solution:**
```bash
# Check if key is set
echo $OPENAI_API_KEY

# Set it if missing
export OPENAI_API_KEY=sk-your-key-here

# Or create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### "Module not found" Error

**Problem:** Dependencies not installed

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install openai python-dotenv requests numpy
```

### Virtual Environment Issues

**Problem:** Virtual environment not working

**Solution:**
```bash
# Remove and recreate
rm -rf venv
./setup.sh

# Activate
source venv/bin/activate
```

## Advanced Usage

### Using Different Models

Change the `model` parameter in any example:

```python
# Use GPT-4
response = client.chat.completions.create(
    model="gpt-4",  # or "gpt-4-turbo", "gpt-4o"
    messages=messages
)

# Use different embedding model
embeddings = client.embeddings.create(
    model="text-embedding-3-large",  # or "text-embedding-ada-002"
    input=text
)
```

### Adding Request Parameters

Customize requests with additional parameters:

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.7,        # Creativity (0.0 - 2.0)
    max_tokens=500,         # Response length limit
    top_p=0.9,             # Nucleus sampling
    frequency_penalty=0.5,  # Reduce repetition
    presence_penalty=0.5    # Encourage new topics
)
```

### Error Handling

Add robust error handling:

```python
from openai import OpenAI, OpenAIError

try:
    response = client.chat.completions.create(...)
except OpenAIError as e:
    print(f"OpenAI API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Next Steps

1. **Explore the API:** Check ChoreoAI's API documentation
2. **Try other providers:** Add Claude or Gemini API keys and test
3. **Build your app:** Use these examples as templates
4. **Production deployment:** Review security and scaling best practices

## Resources

- [OpenAI SDK Documentation](https://github.com/openai/openai-python)
- [ChoreoAI Documentation](../README.md)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review ChoreoAI logs: `docker logs choreoai-api -f`
3. Open an issue on the ChoreoAI GitHub repository

---

Happy coding! 🚀
