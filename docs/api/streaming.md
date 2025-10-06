# Streaming

Enable real-time streaming responses using Server-Sent Events (SSE) for a better user experience with long-running completions.

## What is Streaming?

Streaming allows you to receive the model's response incrementally as it's generated, rather than waiting for the complete response. This provides:

- **Better UX**: Users see responses appear in real-time
- **Faster perceived latency**: First tokens arrive quickly
- **Reduced timeout risk**: Long responses don't timeout
- **Progressive rendering**: Display partial results immediately

## When to Use Streaming

**Use streaming when:**
- Building chat interfaces
- Generating long-form content
- User experience is critical
- Response time is unpredictable

**Don't use streaming when:**
- You need the complete response for processing
- Implementing simple scripts or batch jobs
- Response size is small and predictable

## Enabling Streaming

Set `stream: true` in your request:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Write a short story"}],
    "stream": true
  }'
```

## Server-Sent Events Format

Streaming responses use the SSE (Server-Sent Events) format:

```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1699564800,"model":"gpt-4","choices":[{"index":0,"delta":{"role":"assistant","content":""},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1699564800,"model":"gpt-4","choices":[{"index":0,"delta":{"content":"Once"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1699564800,"model":"gpt-4","choices":[{"index":0,"delta":{"content":" upon"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1699564800,"model":"gpt-4","choices":[{"index":0,"delta":{"content":" a"},"finish_reason":null}]}

data: [DONE]
```

Each line starts with `data: ` followed by a JSON object.

## Chunk Format

### First Chunk (Role)

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1699564800,
  "model": "gpt-4",
  "choices": [
    {
      "index": 0,
      "delta": {
        "role": "assistant",
        "content": ""
      },
      "finish_reason": null
    }
  ]
}
```

### Content Chunks

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1699564800,
  "model": "gpt-4",
  "choices": [
    {
      "index": 0,
      "delta": {
        "content": "Hello"
      },
      "finish_reason": null
    }
  ]
}
```

### Final Chunk

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1699564800,
  "model": "gpt-4",
  "choices": [
    {
      "index": 0,
      "delta": {},
      "finish_reason": "stop"
    }
  ]
}
```

### Stream End Marker

```
data: [DONE]
```

## Code Examples

### Python (ChoreoAI Client)

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Create streaming completion
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a haiku about coding"}],
    stream=True
)

# Iterate over chunks
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)

print()  # New line at the end
```

Output:
```
Code flows like water
Bugs emerge from the shadows
Debug, refine, deploy
```

### Python (OpenAI Client)

```python
import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Tell me a joke"}],
    stream=True
)

for chunk in response:
    content = chunk['choices'][0]['delta'].get('content', '')
    if content:
        print(content, end='', flush=True)
```

### JavaScript (Fetch API)

```javascript
const response = await fetch('http://localhost:8000/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-api-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'gpt-4',
    messages: [{role: 'user', content: 'Write a poem'}],
    stream: true
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const {done, value} = await reader.read();
  if (done) break;

  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = line.slice(6);
      if (data === '[DONE]') continue;

      try {
        const json = JSON.parse(data);
        const content = json.choices[0]?.delta?.content || '';
        if (content) {
          process.stdout.write(content);
        }
      } catch (e) {
        // Skip malformed JSON
      }
    }
  }
}
```

### TypeScript (React Component)

```typescript
import { useState } from 'react';

function ChatComponent() {
  const [response, setResponse] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  const streamResponse = async (prompt: string) => {
    setResponse('');
    setIsStreaming(true);

    const res = await fetch('http://localhost:8000/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer your-api-key',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'gpt-4',
        messages: [{role: 'user', content: prompt}],
        stream: true
      })
    });

    const reader = res.body?.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const {done, value} = await reader!.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') continue;

          try {
            const json = JSON.parse(data);
            const content = json.choices[0]?.delta?.content || '';
            if (content) {
              setResponse(prev => prev + content);
            }
          } catch (e) {
            // Skip malformed JSON
          }
        }
      }
    }

    setIsStreaming(false);
  };

  return (
    <div>
      <button onClick={() => streamResponse('Hello!')}>
        Stream Response
      </button>
      <div>{response}</div>
    </div>
  );
}
```

### Python (Async Client)

```python
from choreoai import AsyncChoreoAI
import asyncio

async def stream_chat():
    client = AsyncChoreoAI(api_key="your-api-key")

    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Count to 10"}],
        stream=True
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

    print()

# Run async function
asyncio.run(stream_chat())
```

## Error Handling

### Handle Connection Errors

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

except Exception as e:
    print(f"\nStreaming error: {e}")
```

### Handle Incomplete Streams

```python
complete_response = ""

try:
    for chunk in stream:
        content = chunk.choices[0].delta.content or ''
        complete_response += content
        print(content, end='', flush=True)

        # Check finish reason
        if chunk.choices[0].finish_reason:
            if chunk.choices[0].finish_reason == 'stop':
                print("\n[Completed]")
            elif chunk.choices[0].finish_reason == 'length':
                print("\n[Max tokens reached]")

except Exception as e:
    print(f"\n[Error: {e}]")
    print(f"Partial response: {complete_response}")
```

### Timeout Handling

```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Stream timeout")

# Set 30 second timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)

try:
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)
finally:
    signal.alarm(0)  # Cancel timeout
```

## Advanced Usage

### Accumulate Full Response

```python
def stream_and_accumulate(messages):
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        stream=True
    )

    full_response = ""

    for chunk in stream:
        content = chunk.choices[0].delta.content or ''
        full_response += content
        print(content, end='', flush=True)

    print()
    return full_response

# Use it
response = stream_and_accumulate([
    {"role": "user", "content": "Explain AI"}
])

# Now you have the full response
print(f"\nFull response length: {len(response)} characters")
```

### Display Streaming Indicators

```python
import sys
import time

def stream_with_indicator(messages):
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        stream=True
    )

    print("Generating", end='', flush=True)

    # Show dots while waiting for first chunk
    for _ in range(3):
        print('.', end='', flush=True)
        time.sleep(0.3)

    print('\n')

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

    print()
```

### Multi-Choice Streaming

```python
# Request multiple choices (if supported by provider)
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a haiku"}],
    n=2,  # Request 2 completions
    stream=True
)

responses = ["", ""]

for chunk in stream:
    for choice in chunk.choices:
        content = choice.delta.content or ''
        responses[choice.index] += content
        print(f"[{choice.index}] {content}", end='', flush=True)

print("\n\nFinal responses:")
for i, response in enumerate(responses):
    print(f"\n{i+1}. {response}")
```

## Best Practices

### 1. Always Close Streams

```python
stream = client.chat.completions.create(..., stream=True)

try:
    for chunk in stream:
        # Process chunk
        pass
finally:
    # Stream automatically closes when exhausted
    pass
```

### 2. Buffer Output

For better performance, buffer chunks before rendering:

```python
buffer = []
for i, chunk in enumerate(stream):
    content = chunk.choices[0].delta.content or ''
    buffer.append(content)

    # Flush buffer every 5 chunks
    if i % 5 == 0:
        print(''.join(buffer), end='', flush=True)
        buffer = []

# Flush remaining
if buffer:
    print(''.join(buffer), end='', flush=True)
```

### 3. Handle Network Issues

```python
from requests.exceptions import ChunkedEncodingError

try:
    for chunk in stream:
        # Process chunk
        pass
except ChunkedEncodingError:
    print("\nConnection interrupted. Retrying...")
    # Retry logic here
```

### 4. Provide User Feedback

```python
import sys

print("Assistant: ", end='', flush=True)

chunk_count = 0
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
        chunk_count += 1

print(f"\n[Received {chunk_count} chunks]")
```

## Next Steps

- **[Chat Completions](chat-completions.md)** - Learn about chat API
- **[Client Streaming](../client/streaming.md)** - Use Python SDK for streaming
- **[Async Usage](../client/async-usage.md)** - Async streaming patterns
- **[Error Handling](error-handling.md)** - Handle streaming errors
