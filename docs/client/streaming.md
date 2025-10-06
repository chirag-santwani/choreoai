# Streaming

Stream responses in real-time for better user experience and faster perceived latency.

## Basic Streaming

Enable streaming by setting `stream=True`:

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a short story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)

print()  # New line at the end
```

## Synchronous Streaming

### Simple Example

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
    content = chunk.choices[0].delta.content
    if content:
        print(content, end='', flush=True)

print()
```

### Accumulate Full Response

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Explain Python"}],
    stream=True
)

full_response = ""

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        full_response += content
        print(content, end='', flush=True)

print("\n\nFull response length:", len(full_response))
```

### Check Finish Reason

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a poem"}],
    stream=True
)

for chunk in stream:
    delta = chunk.choices[0].delta

    if delta.content:
        print(delta.content, end='', flush=True)

    finish_reason = chunk.choices[0].finish_reason
    if finish_reason:
        print(f"\n[Finished: {finish_reason}]")
```

## Asynchronous Streaming

### Basic Async Streaming

```python
from choreoai import AsyncChoreoAI
import asyncio

async def stream_response():
    client = AsyncChoreoAI(api_key="your-api-key")

    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Tell me a joke"}],
        stream=True
    )

    print("Assistant: ", end='', flush=True)

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

    print()

# Run async function
asyncio.run(stream_response())
```

### Concurrent Streaming

Stream multiple responses concurrently:

```python
from choreoai import AsyncChoreoAI
import asyncio

async def stream_question(client, question):
    print(f"\nQ: {question}")
    print("A: ", end='', flush=True)

    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}],
        stream=True
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

    print()

async def main():
    client = AsyncChoreoAI(api_key="your-api-key")

    questions = [
        "What is Python?",
        "What is JavaScript?",
        "What is Rust?"
    ]

    # Stream all concurrently
    await asyncio.gather(*[
        stream_question(client, q) for q in questions
    ])

asyncio.run(main())
```

## Streaming Patterns

### Streaming Chat Loop

```python
from choreoai import ChoreoAI

def streaming_chat():
    client = ChoreoAI(api_key="your-api-key")
    messages = []

    print("Streaming Chat (type 'quit' to exit)")
    print("-" * 50)

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == 'quit':
            break

        messages.append({"role": "user", "content": user_input})

        print("Assistant: ", end='', flush=True)

        stream = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            stream=True
        )

        assistant_message = ""

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                assistant_message += content
                print(content, end='', flush=True)

        print()
        messages.append({"role": "assistant", "content": assistant_message})

if __name__ == "__main__":
    streaming_chat()
```

### Streaming with Progress Indicator

```python
import sys
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Show loading indicator
print("Generating response", end='', flush=True)
for _ in range(3):
    print('.', end='', flush=True)
    import time
    time.sleep(0.3)
print('\n')

# Stream response
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Explain AI"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)

print()
```

### Streaming with Buffering

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a story"}],
    stream=True
)

buffer = []
buffer_size = 5  # Buffer 5 chunks before printing

for i, chunk in enumerate(stream):
    content = chunk.choices[0].delta.content

    if content:
        buffer.append(content)

        # Flush buffer when full
        if len(buffer) >= buffer_size:
            print(''.join(buffer), end='', flush=True)
            buffer = []

# Flush remaining buffer
if buffer:
    print(''.join(buffer), end='', flush=True)

print()
```

## Streaming with Different Models

### Stream from Multiple Providers

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

models = ["gpt-4", "claude-3-sonnet-20240229", "gemini-pro"]
question = "What is machine learning?"

for model in models:
    print(f"\n{model}: ", end='', flush=True)

    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

    print()
```

## Error Handling

### Basic Error Handling

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

try:
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

    print()

except Exception as e:
    print(f"\nStreaming error: {e}")
```

### Retry on Stream Failure

```python
from choreoai import ChoreoAI
import time

def stream_with_retry(client, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            stream = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                stream=True
            )

            full_response = ""

            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    print(content, end='', flush=True)

            print()
            return full_response

        except Exception as e:
            print(f"\nAttempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

# Use it
client = ChoreoAI(api_key="your-api-key")
stream_with_retry(
    client,
    [{"role": "user", "content": "Hello"}]
)
```

### Partial Response Recovery

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a long story"}],
    stream=True
)

partial_response = ""

try:
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            partial_response += content
            print(content, end='', flush=True)

except Exception as e:
    print(f"\n[Stream interrupted: {e}]")
    print(f"\nPartial response ({len(partial_response)} chars):")
    print(partial_response)
```

## Advanced Usage

### Streaming with Function Calling

```python
from choreoai import ChoreoAI
import json

client = ChoreoAI(api_key="your-api-key")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    }
]

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in NYC?"}],
    tools=tools,
    stream=True
)

for chunk in stream:
    delta = chunk.choices[0].delta

    if delta.content:
        print(delta.content, end='', flush=True)

    if delta.tool_calls:
        print("\n[Function call detected]")
```

### Streaming to File

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a long article about AI"}],
    stream=True
)

with open('output.txt', 'w') as f:
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            f.write(content)
            print(content, end='', flush=True)

print("\n\nSaved to output.txt")
```

### Real-time Translation

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

def translate_stream(text, target_language):
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Translate to {target_language}: {text}"
        }],
        stream=True
    )

    print(f"Translation ({target_language}): ", end='', flush=True)

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

    print()

# Use it
translate_stream("Hello, how are you?", "Spanish")
translate_stream("Hello, how are you?", "French")
```

## Performance Tips

### 1. Flush Output Immediately

```python
# Good: immediate display
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)

# Bad: buffered output
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='')
```

### 2. Use Async for Concurrency

```python
# Good: concurrent streaming
async def stream_all():
    tasks = [stream_question(q) for q in questions]
    await asyncio.gather(*tasks)

# Less efficient: sequential
for q in questions:
    stream_question(q)
```

### 3. Buffer for UI Performance

```python
# For UI rendering, batch updates
buffer = []
BATCH_SIZE = 10

for chunk in stream:
    if chunk.choices[0].delta.content:
        buffer.append(chunk.choices[0].delta.content)

        if len(buffer) >= BATCH_SIZE:
            update_ui(''.join(buffer))
            buffer = []
```

### 4. Close Streams Properly

```python
# Streams auto-close when exhausted
stream = client.chat.completions.create(..., stream=True)

try:
    for chunk in stream:
        # Process chunk
        pass
finally:
    # Cleanup if needed
    pass
```

## Best Practices

### 1. Always Check for Content

```python
for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:  # Always check before using
        print(content, end='', flush=True)
```

### 2. Handle Empty Chunks

```python
for chunk in stream:
    delta = chunk.choices[0].delta

    # First chunk may only have role
    if hasattr(delta, 'role') and delta.role:
        print(f"[Role: {delta.role}]")

    # Content chunks
    if delta.content:
        print(delta.content, end='', flush=True)
```

### 3. Monitor Finish Reason

```python
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)

    if chunk.choices[0].finish_reason:
        reason = chunk.choices[0].finish_reason

        if reason == "length":
            print("\n[Max tokens reached]")
        elif reason == "stop":
            print("\n[Completed]")
```

### 4. Provide User Feedback

```python
print("Generating response...")

chunk_count = 0
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
        chunk_count += 1

print(f"\n[Received {chunk_count} chunks]")
```

## Next Steps

- **[Async Usage](async-usage.md)** - Advanced async patterns
- **[Chat Guide](chat.md)** - Chat completions basics
- **[API Streaming](../api/streaming.md)** - API-level streaming details
- **[Error Handling](../api/error-handling.md)** - Handle streaming errors
