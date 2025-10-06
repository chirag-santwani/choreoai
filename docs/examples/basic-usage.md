# Basic Usage Tutorial

Learn how to use ChoreoAI for chat completions, streaming, embeddings, and more. This tutorial covers the fundamentals you need to get started.

## Table of Contents

1. [Installation](#installation)
2. [First API Call](#first-api-call)
3. [Chat Completions](#chat-completions)
4. [Streaming Responses](#streaming-responses)
5. [Multi-Turn Conversations](#multi-turn-conversations)
6. [Working with Embeddings](#working-with-embeddings)
7. [Function Calling](#function-calling)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)

## Installation

### Install ChoreoAI Client

```bash
pip install choreoai
```

### Install OpenAI SDK (Alternative)

You can also use the OpenAI SDK with ChoreoAI:

```bash
pip install openai
```

### Set Up Environment Variables

Create a `.env` file or export environment variables:

```bash
export CHOREOAI_API_KEY=your-api-key
export CHOREOAI_BASE_URL=http://localhost:8000
```

### Verify Installation

```python
from choreoai import ChoreoAI

client = ChoreoAI()
print("ChoreoAI client initialized successfully!")
```

## First API Call

Let's make your first API call to ChoreoAI.

### Complete Example

```python
from choreoai import ChoreoAI

# Initialize the client
client = ChoreoAI(api_key="your-api-key")

# Create a chat completion
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Say hello!"}
    ]
)

# Print the response
print(response.choices[0].message.content)
```

### Expected Output

```
Hello! How can I assist you today?
```

### Step-by-Step Breakdown

1. **Import the client**: `from choreoai import ChoreoAI`
2. **Initialize**: `client = ChoreoAI(api_key="your-api-key")`
3. **Create request**: Call `client.chat.completions.create()`
4. **Extract response**: Access `response.choices[0].message.content`

## Chat Completions

Chat completions are the core feature of ChoreoAI. Here's how to use them effectively.

### Basic Chat Completion

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "What is artificial intelligence?"
        }
    ]
)

print(response.choices[0].message.content)
```

### Message Roles

ChoreoAI supports three message roles:

1. **System**: Sets the assistant's behavior and context
2. **User**: The user's input or question
3. **Assistant**: The AI's response (used in multi-turn conversations)

### Example with All Roles

```python
messages = [
    {
        "role": "system",
        "content": "You are a Python programming expert."
    },
    {
        "role": "user",
        "content": "How do I create a list in Python?"
    },
    {
        "role": "assistant",
        "content": "You can create a list using square brackets: my_list = [1, 2, 3]"
    },
    {
        "role": "user",
        "content": "How do I add items to it?"
    }
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)

print(response.choices[0].message.content)
```

### Common Parameters

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[...],

    # Control creativity (0.0 = deterministic, 2.0 = very creative)
    temperature=0.7,

    # Maximum tokens in response
    max_tokens=150,

    # Nucleus sampling (alternative to temperature)
    top_p=1.0,

    # Penalize new topics (-2.0 to 2.0)
    presence_penalty=0,

    # Penalize repetition (-2.0 to 2.0)
    frequency_penalty=0,

    # Stop sequences
    stop=["END", "\n\n"]
)
```

### Understanding Temperature

Temperature controls randomness in responses:

```python
# Low temperature (0.0-0.3): Focused, deterministic
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    temperature=0.1
)
# Output: "2+2 equals 4."

# Medium temperature (0.4-0.9): Balanced
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Write a creative story opening."}],
    temperature=0.7
)

# High temperature (1.0-2.0): Very creative, less predictable
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Generate a unique product name."}],
    temperature=1.5
)
```

### Accessing Response Metadata

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Response content
content = response.choices[0].message.content
print(f"Response: {content}")

# Model used
print(f"Model: {response.model}")

# Finish reason
print(f"Finish reason: {response.choices[0].finish_reason}")

# Token usage
usage = response.usage
print(f"Prompt tokens: {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")
```

### Expected Output

```
Response: Hello! How can I assist you today?
Model: gpt-3.5-turbo
Finish reason: stop
Prompt tokens: 8
Completion tokens: 9
Total tokens: 17
```

## Streaming Responses

Streaming provides real-time responses as they're generated, improving user experience for longer responses.

### Basic Streaming

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

print("Assistant: ", end='', flush=True)

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Write a short poem about coding."}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)

print()  # New line at the end
```

### Expected Output (Streaming)

```
Assistant: In lines of code we find our way,
Through logic's dance both night and day,
Algorithms weave their magic spell,
In digital realms where ideas dwell.
```

### Collecting Streamed Response

```python
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Count from 1 to 5"}],
    stream=True
)

full_response = ""
for chunk in stream:
    if chunk.choices[0].delta.content:
        content = chunk.choices[0].delta.content
        full_response += content
        print(content, end='', flush=True)

print(f"\n\nFull response: {full_response}")
```

### Handling Streaming Errors

```python
try:
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

except Exception as e:
    print(f"\nStreaming error: {e}")
```

## Multi-Turn Conversations

Build conversational applications by maintaining message history.

### Simple Conversation

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Initialize conversation history
messages = []

# First turn
messages.append({"role": "user", "content": "My name is Alice."})
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)
assistant_msg = response.choices[0].message.content
messages.append({"role": "assistant", "content": assistant_msg})
print(f"Assistant: {assistant_msg}")

# Second turn
messages.append({"role": "user", "content": "What's my name?"})
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)
print(f"Assistant: {response.choices[0].message.content}")
```

### Expected Output

```
Assistant: Hello Alice! It's nice to meet you. How can I help you today?
Assistant: Your name is Alice.
```

### Interactive Chat Loop

```python
from choreoai import ChoreoAI

def chat_loop():
    client = ChoreoAI(api_key="your-api-key")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

    print("Chat with AI (type 'quit' to exit)")
    print("-" * 50)

    while True:
        # Get user input
        user_input = input("You: ")

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break

        # Add user message
        messages.append({"role": "user", "content": user_input})

        try:
            # Get AI response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            assistant_message = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_message})

            print(f"Assistant: {assistant_message}\n")

        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    chat_loop()
```

### Managing Conversation Context

Long conversations can exceed token limits. Here's how to manage context:

```python
def truncate_messages(messages, max_tokens=4000):
    """Keep only recent messages to stay within token limit."""
    # Always keep system message
    system_msg = [msg for msg in messages if msg["role"] == "system"]
    other_msgs = [msg for msg in messages if msg["role"] != "system"]

    # Keep last N messages (rough estimate: 1 message ≈ 100 tokens)
    max_messages = max_tokens // 100
    recent_msgs = other_msgs[-max_messages:]

    return system_msg + recent_msgs

# Use in conversation
messages = [...] # Long conversation history
messages = truncate_messages(messages)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)
```

## Working with Embeddings

Embeddings convert text to numerical vectors for semantic search, clustering, and recommendations.

### Create Embeddings

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Create embedding for a single text
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="ChoreoAI is an AI orchestration platform."
)

embedding = response.data[0].embedding
print(f"Embedding dimension: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
```

### Expected Output

```
Embedding dimension: 1536
First 5 values: [0.0234, -0.0156, 0.0891, -0.0445, 0.0623]
```

### Batch Embeddings

```python
# Create embeddings for multiple texts at once
texts = [
    "ChoreoAI supports multiple AI providers.",
    "OpenAI provides GPT models.",
    "Claude is developed by Anthropic."
]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)

embeddings = [item.embedding for item in response.data]
print(f"Created {len(embeddings)} embeddings")
```

### Semantic Search with Embeddings

```python
import numpy as np
from choreoai import ChoreoAI

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

client = ChoreoAI(api_key="your-api-key")

# Knowledge base
documents = [
    "ChoreoAI is a unified API orchestration platform.",
    "OpenAI created GPT-4 and ChatGPT.",
    "Claude 3 is Anthropic's latest language model.",
    "ChoreoAI supports OpenAI, Claude, and Gemini."
]

# Create embeddings for documents
doc_response = client.embeddings.create(
    model="text-embedding-3-small",
    input=documents
)
doc_embeddings = [item.embedding for item in doc_response.data]

# Query
query = "What is ChoreoAI?"
query_response = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)
query_embedding = query_response.data[0].embedding

# Find most similar document
similarities = [
    cosine_similarity(query_embedding, doc_emb)
    for doc_emb in doc_embeddings
]

most_similar_idx = np.argmax(similarities)
print(f"Query: {query}")
print(f"Most similar: {documents[most_similar_idx]}")
print(f"Similarity: {similarities[most_similar_idx]:.4f}")
```

### Expected Output

```
Query: What is ChoreoAI?
Most similar: ChoreoAI is a unified API orchestration platform.
Similarity: 0.8734
```

## Function Calling

Enable AI models to call external functions and APIs.

### Define Functions

```python
from choreoai import ChoreoAI
import json

# Define available functions
def get_weather(location: str, unit: str = "fahrenheit") -> dict:
    """Get current weather for a location."""
    # Mock data - replace with real API call
    return {
        "location": location,
        "temperature": 72,
        "unit": unit,
        "condition": "Sunny"
    }

# Function schema for the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g., San Francisco"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    }
]
```

### Use Function Calling

```python
client = ChoreoAI(api_key="your-api-key")

messages = [
    {"role": "user", "content": "What's the weather in San Francisco?"}
]

# First request - model decides to call function
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Check if model wants to call a function
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]

    # Extract function details
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    print(f"Calling: {function_name}")
    print(f"Arguments: {function_args}")

    # Call the actual function
    function_result = get_weather(**function_args)
    print(f"Result: {function_result}")

    # Add function result to messages
    messages.append(response.choices[0].message)
    messages.append({
        "tool_call_id": tool_call.id,
        "role": "tool",
        "name": function_name,
        "content": json.dumps(function_result)
    })

    # Second request - get final response
    final_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    print(f"\nAssistant: {final_response.choices[0].message.content}")
```

### Expected Output

```
Calling: get_weather
Arguments: {'location': 'San Francisco', 'unit': 'fahrenheit'}
Result: {'location': 'San Francisco', 'temperature': 72, 'unit': 'fahrenheit', 'condition': 'Sunny'}