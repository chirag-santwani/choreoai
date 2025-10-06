# Quick Start

Get started with ChoreoAI in 5 minutes. This guide will walk you through your first API call.

## Prerequisites

- Python 3.9 or higher installed
- ChoreoAI Python client installed ([Installation Guide](installation.md))
- ChoreoAI API running (locally or remote)
- API key (if authentication is enabled)

## Step 1: Import the Client

Create a new Python file `hello_choreoai.py`:

```python
from choreoai import ChoreoAI
```

## Step 2: Initialize the Client

```python
from choreoai import ChoreoAI

# Initialize with API key
client = ChoreoAI(api_key="your-api-key")
```

!!! tip
    Use environment variables for API keys:
    ```bash
    export CHOREOAI_API_KEY=your-api-key
    ```
    Then initialize without passing the key:
    ```python
    client = ChoreoAI()  # Reads from environment
    ```

## Step 3: Create Your First Completion

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Create a chat completion
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Say hello!"}
    ]
)

# Print the response
print(response.choices[0].message.content)
```

## Step 4: Run the Script

```bash
python hello_choreoai.py
```

**Expected Output:**
```
Hello! How can I assist you today?
```

## Complete Example

Here's a complete working example with error handling:

```python
from choreoai import ChoreoAI

def main():
    # Initialize client
    client = ChoreoAI(api_key="your-api-key")

    try:
        # Create chat completion
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is artificial intelligence?"}
            ],
            temperature=0.7,
            max_tokens=150
        )

        # Print the response
        print("Assistant:", response.choices[0].message.content)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## Configuration Options

### Set Base URL

If your ChoreoAI API is running on a different host:

```python
client = ChoreoAI(
    api_key="your-api-key",
    base_url="https://api.yourcompany.com"
)
```

### Set Timeout

For long-running requests:

```python
client = ChoreoAI(
    api_key="your-api-key",
    timeout=60.0  # 60 seconds
)
```

### Enable Retries

Automatically retry failed requests:

```python
client = ChoreoAI(
    api_key="your-api-key",
    max_retries=3
)
```

## Using Environment Variables

### Create .env File

```bash
# .env
CHOREOAI_API_KEY=your-api-key
CHOREOAI_BASE_URL=http://localhost:8000
```

### Load Environment Variables

```python
from dotenv import load_dotenv
from choreoai import ChoreoAI

# Load .env file
load_dotenv()

# Client reads from environment
client = ChoreoAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

Install python-dotenv:
```bash
pip install python-dotenv
```

## Switch Between Models

ChoreoAI makes it easy to use different AI providers:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Use GPT-4 (OpenAI)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
print("GPT-4:", response.choices[0].message.content)

# Use Claude (Anthropic)
response = client.chat.completions.create(
    model="claude-3-sonnet-20240229",
    messages=[{"role": "user", "content": "Hello!"}]
)
print("Claude:", response.choices[0].message.content)

# Use Gemini (Google)
response = client.chat.completions.create(
    model="gemini-pro",
    messages=[{"role": "user", "content": "Hello!"}]
)
print("Gemini:", response.choices[0].message.content)
```

## Multi-Turn Conversation

Build a conversation with context:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Initialize conversation history
messages = []

# First turn
messages.append({"role": "user", "content": "My name is Alice."})
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)
assistant_message = response.choices[0].message.content
messages.append({"role": "assistant", "content": assistant_message})
print("Assistant:", assistant_message)

# Second turn
messages.append({"role": "user", "content": "What's my name?"})
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)
print("Assistant:", response.choices[0].message.content)
```

**Output:**
```
Assistant: Hello Alice! It's nice to meet you. How can I help you today?
Assistant: Your name is Alice.
```

## Streaming Responses

Get real-time responses as they're generated:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

print("Assistant: ", end='', flush=True)

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Count from 1 to 5"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)

print()  # New line
```

**Output:**
```
Assistant: 1, 2, 3, 4, 5
```

See [Streaming Guide](streaming.md) for more details.

## Error Handling

Always handle potential errors:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)

except ValueError as e:
    print(f"Invalid parameters: {e}")

except ConnectionError as e:
    print(f"Connection error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Interactive Chat Loop

Build a simple interactive chat:

```python
from choreoai import ChoreoAI

def chat_loop():
    client = ChoreoAI(api_key="your-api-key")
    messages = []

    print("Chat with AI (type 'quit' to exit)")
    print("-" * 50)

    while True:
        # Get user input
        user_input = input("You: ")

        if user_input.lower() == 'quit':
            break

        # Add user message
        messages.append({"role": "user", "content": user_input})

        try:
            # Get AI response
            response = client.chat.completions.create(
                model="gpt-4",
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

## Access Response Metadata

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Response content
print("Content:", response.choices[0].message.content)

# Metadata
print("Model:", response.model)
print("Finish reason:", response.choices[0].finish_reason)

# Token usage
print("Prompt tokens:", response.usage.prompt_tokens)
print("Completion tokens:", response.usage.completion_tokens)
print("Total tokens:", response.usage.total_tokens)
```

**Output:**
```
Content: Hello! How can I help you today?
Model: gpt-4
Finish reason: stop
Prompt tokens: 8
Completion tokens: 9
Total tokens: 17
```

## Common Parameters

```python
response = client.chat.completions.create(
    model="gpt-4",                           # Model to use
    messages=[...],                          # Conversation messages
    temperature=0.7,                         # Creativity (0.0 - 2.0)
    max_tokens=150,                          # Max response length
    top_p=1.0,                               # Nucleus sampling
    stream=False,                            # Enable streaming
    presence_penalty=0,                      # Penalize new topics
    frequency_penalty=0,                     # Penalize repetition
    stop=["END"],                            # Stop sequences
)
```

## Next Steps

Now that you've made your first API call, explore more features:

- **[Chat Completions](chat.md)** - Advanced chat features
- **[Streaming](streaming.md)** - Real-time streaming responses
- **[Async Usage](async-usage.md)** - Async/await patterns
- **[Multi-Provider](../examples/multi-provider.md)** - Use multiple AI providers
- **[Error Handling](../api/error-handling.md)** - Handle errors gracefully

## Troubleshooting

### Issue: Module not found

```python
ModuleNotFoundError: No module named 'choreoai'
```

**Solution:** Install the package:
```bash
pip install choreoai
```

### Issue: Authentication failed

```
AuthenticationError: Invalid API key
```

**Solution:**
- Check your API key is correct
- Verify the API key is properly set in environment variables
- Ensure the ChoreoAI API is running

### Issue: Connection refused

```
ConnectionError: Connection refused
```

**Solution:**
- Verify the ChoreoAI API is running
- Check the base URL is correct
- Ensure there are no firewall issues

### Issue: Model not found

```
Error: Model 'gpt-4' not found
```

**Solution:**
- Verify the provider API key is configured on the server
- Check the model name is spelled correctly
- Use `client.models.list()` to see available models
