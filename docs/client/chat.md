# Chat Completions

Master chat completions with the ChoreoAI Python client.

## Basic Usage

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What is Python?"}
    ]
)

print(response.choices[0].message.content)
```

## Message Roles

### System Messages

Guide the assistant's behavior:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful Python tutor. Explain concepts simply with examples."
        },
        {
            "role": "user",
            "content": "What are list comprehensions?"
        }
    ]
)
```

### User Messages

Represent user input:

```python
messages = [
    {"role": "user", "content": "Hello!"}
]
```

### Assistant Messages

Include previous AI responses for context:

```python
messages = [
    {"role": "user", "content": "What is 2+2?"},
    {"role": "assistant", "content": "2+2 equals 4."},
    {"role": "user", "content": "What about 2+3?"}
]
```

## Multi-Turn Conversations

Build conversations by maintaining message history:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Initialize conversation
conversation = [
    {"role": "system", "content": "You are a helpful math tutor."}
]

def chat(user_message):
    # Add user message
    conversation.append({"role": "user", "content": user_message})

    # Get response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation
    )

    # Add assistant response
    assistant_message = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_message})

    return assistant_message

# Use it
print(chat("What is 5 + 3?"))
# Output: "5 + 3 equals 8."

print(chat("What about multiplying those numbers?"))
# Output: "5 multiplied by 3 equals 15."
```

## Setting Parameters

### Temperature

Control randomness (0.0 = deterministic, 2.0 = very random):

```python
# Factual, consistent responses
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    temperature=0.0
)

# Creative, varied responses
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a creative story"}],
    temperature=1.5
)
```

### Max Tokens

Limit response length:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Explain quantum physics"}],
    max_tokens=100  # Short response
)
```

### Top P (Nucleus Sampling)

Alternative to temperature for controlling randomness:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Tell me a joke"}],
    top_p=0.9  # Consider top 90% probability mass
)
```

### Stop Sequences

Stop generation at specific strings:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Count from 1 to 10"}],
    stop=["5"]  # Stop when "5" appears
)
```

### Presence Penalty

Encourage new topics (-2.0 to 2.0):

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write about AI"}],
    presence_penalty=0.6  # Encourage diverse topics
)
```

### Frequency Penalty

Reduce repetition (-2.0 to 2.0):

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Describe a forest"}],
    frequency_penalty=0.5  # Reduce repeated words
)
```

## All Parameters Example

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a creative writer."},
        {"role": "user", "content": "Write a short poem"}
    ],
    temperature=0.8,
    max_tokens=200,
    top_p=0.95,
    presence_penalty=0.6,
    frequency_penalty=0.3,
    stop=["\n\n"],
    n=1
)
```

## Function Calling

Define functions that the model can call:

```python
from choreoai import ChoreoAI
import json

client = ChoreoAI(api_key="your-api-key")

# Define tools
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

# Make request
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Boston?"}],
    tools=tools
)

# Check if function was called
message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    print(f"Function: {function_name}")
    print(f"Arguments: {arguments}")

    # Execute function (implement your logic)
    if function_name == "get_weather":
        weather_data = get_weather(arguments["location"])

        # Send function result back
        messages = [
            {"role": "user", "content": "What's the weather in Boston?"},
            message,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(weather_data)
            }
        ]

        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        print(final_response.choices[0].message.content)
```

## Response Format

### Access Response Content

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)

# Content
content = response.choices[0].message.content
print(content)

# Role
role = response.choices[0].message.role
print(role)  # "assistant"

# Finish reason
finish_reason = response.choices[0].finish_reason
print(finish_reason)  # "stop", "length", "tool_calls"
```

### Token Usage

```python
usage = response.usage

print(f"Prompt tokens: {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")
```

### Multiple Choices

Request multiple completions:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a haiku"}],
    n=3  # Generate 3 completions
)

for i, choice in enumerate(response.choices):
    print(f"\nHaiku {i + 1}:")
    print(choice.message.content)
```

## Switch Models

Easily switch between providers:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

messages = [{"role": "user", "content": "Explain AI in one sentence"}]

# Try OpenAI
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)
print("GPT-4:", response.choices[0].message.content)

# Try Claude
response = client.chat.completions.create(
    model="claude-3-sonnet-20240229",
    messages=messages
)
print("Claude:", response.choices[0].message.content)

# Try Gemini
response = client.chat.completions.create(
    model="gemini-pro",
    messages=messages
)
print("Gemini:", response.choices[0].message.content)
```

## Conversation Management

### Conversation Class

```python
class Conversation:
    def __init__(self, client, model="gpt-4", system_message=None):
        self.client = client
        self.model = model
        self.messages = []

        if system_message:
            self.messages.append({"role": "system", "content": system_message})

    def send(self, user_message):
        # Add user message
        self.messages.append({"role": "user", "content": user_message})

        # Get response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )

        # Add assistant message
        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def reset(self):
        # Keep system message if present
        if self.messages and self.messages[0]["role"] == "system":
            self.messages = [self.messages[0]]
        else:
            self.messages = []

# Use it
client = ChoreoAI(api_key="your-api-key")
conv = Conversation(
    client,
    model="gpt-4",
    system_message="You are a helpful coding assistant."
)

print(conv.send("What is Python?"))
print(conv.send("Show me a list comprehension example"))

# Reset conversation
conv.reset()
```

### Context Window Management

Prevent exceeding context limits:

```python
def truncate_conversation(messages, max_tokens=4000):
    """Keep only recent messages within token limit"""
    # Rough estimate: 1 token ≈ 4 characters
    total_chars = sum(len(m["content"]) for m in messages)
    estimated_tokens = total_chars // 4

    if estimated_tokens <= max_tokens:
        return messages

    # Keep system message if present
    system_messages = [m for m in messages if m["role"] == "system"]
    other_messages = [m for m in messages if m["role"] != "system"]

    # Keep most recent messages
    while estimated_tokens > max_tokens and len(other_messages) > 2:
        removed = other_messages.pop(0)
        total_chars -= len(removed["content"])
        estimated_tokens = total_chars // 4

    return system_messages + other_messages

# Use it
messages = truncate_conversation(conversation_history, max_tokens=4000)
response = client.chat.completions.create(model="gpt-4", messages=messages)
```

## Error Handling

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)

except ValueError as e:
    print(f"Invalid parameter: {e}")

except Exception as e:
    print(f"Error: {e}")
```

## Best Practices

### 1. Use System Messages

```python
# Good: Clear instructions
messages = [
    {"role": "system", "content": "You are a JSON API. Return only valid JSON."},
    {"role": "user", "content": "User profile for John"}
]

# Better than trying to enforce in user message
messages = [
    {"role": "user", "content": "Return user profile for John as JSON"}
]
```

### 2. Set Appropriate Temperature

```python
# Factual tasks: low temperature
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    temperature=0.0
)

# Creative tasks: higher temperature
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a poem"}],
    temperature=0.9
)
```

### 3. Manage Context

```python
# Keep conversations focused
MAX_MESSAGES = 20

if len(messages) > MAX_MESSAGES:
    # Keep system message + recent messages
    messages = [messages[0]] + messages[-(MAX_MESSAGES-1):]
```

### 4. Handle Streaming for Long Responses

```python
# For long responses, use streaming for better UX
if expected_long_response:
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='')
```

### 5. Reuse Client Instance

```python
# Good: Create once
client = ChoreoAI(api_key="your-api-key")

for msg in messages:
    response = client.chat.completions.create(...)

# Bad: Create in loop
for msg in messages:
    client = ChoreoAI(api_key="your-api-key")
    response = client.chat.completions.create(...)
```

## Next Steps

- **[Streaming](streaming.md)** - Real-time streaming responses
- **[Async Usage](async-usage.md)** - Async/await patterns
- **[Multi-Provider](../examples/multi-provider.md)** - Use multiple providers
- **[Error Handling](../api/error-handling.md)** - Handle errors gracefully
