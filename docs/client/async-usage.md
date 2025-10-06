# Async Usage

Use async/await patterns with ChoreoAI for concurrent operations and better performance.

## AsyncChoreoAI Client

```python
from choreoai import AsyncChoreoAI
import asyncio

async def main():
    client = AsyncChoreoAI(api_key="your-api-key")

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )

    print(response.choices[0].message.content)

asyncio.run(main())
```

## When to Use Async

**Use async when:**
- Making multiple concurrent API calls
- Building async web applications (FastAPI, aiohttp)
- Handling multiple user requests simultaneously
- Maximizing throughput

**Use sync when:**
- Simple scripts
- Single sequential requests
- Learning or prototyping
- No concurrency requirements

## Basic Async Examples

### Single Request

```python
from choreoai import AsyncChoreoAI
import asyncio

async def simple_chat():
    client = AsyncChoreoAI(api_key="your-api-key")

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "What is async programming?"}]
    )

    print(response.choices[0].message.content)

asyncio.run(simple_chat())
```

### Multiple Sequential Requests

```python
from choreoai import AsyncChoreoAI
import asyncio

async def sequential_requests():
    client = AsyncChoreoAI(api_key="your-api-key")

    # First request
    response1 = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "What is Python?"}]
    )
    print("Python:", response1.choices[0].message.content[:100])

    # Second request (waits for first to complete)
    response2 = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "What is JavaScript?"}]
    )
    print("JavaScript:", response2.choices[0].message.content[:100])

asyncio.run(sequential_requests())
```

## Concurrent Requests

### Using asyncio.gather

```python
from choreoai import AsyncChoreoAI
import asyncio

async def concurrent_requests():
    client = AsyncChoreoAI(api_key="your-api-key")

    # Create tasks
    task1 = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "What is Python?"}]
    )

    task2 = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "What is JavaScript?"}]
    )

    task3 = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "What is Rust?"}]
    )

    # Run concurrently
    responses = await asyncio.gather(task1, task2, task3)

    for i, response in enumerate(responses):
        print(f"\nResponse {i + 1}:")
        print(response.choices[0].message.content[:100])

asyncio.run(concurrent_requests())
```

### Using asyncio.create_task

```python
from choreoai import AsyncChoreoAI
import asyncio

async def process_question(client, question):
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

async def concurrent_tasks():
    client = AsyncChoreoAI(api_key="your-api-key")

    questions = [
        "What is machine learning?",
        "What is deep learning?",
        "What is neural networks?"
    ]

    # Create tasks
    tasks = [
        asyncio.create_task(process_question(client, q))
        for q in questions
    ]

    # Wait for all to complete
    results = await asyncio.gather(*tasks)

    for question, answer in zip(questions, results):
        print(f"\nQ: {question}")
        print(f"A: {answer[:100]}...")

asyncio.run(concurrent_tasks())
```

## Async Streaming

### Basic Async Streaming

```python
from choreoai import AsyncChoreoAI
import asyncio

async def async_stream():
    client = AsyncChoreoAI(api_key="your-api-key")

    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Write a haiku"}],
        stream=True
    )

    print("Assistant: ", end='', flush=True)

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

    print()

asyncio.run(async_stream())
```

### Concurrent Streaming

```python
from choreoai import AsyncChoreoAI
import asyncio

async def stream_response(client, question):
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
        "What is async programming?",
        "What is concurrency?",
        "What is parallelism?"
    ]

    # Stream all concurrently
    await asyncio.gather(*[
        stream_response(client, q) for q in questions
    ])

asyncio.run(main())
```

## Error Handling

### Basic Error Handling

```python
from choreoai import AsyncChoreoAI
import asyncio

async def safe_request():
    client = AsyncChoreoAI(api_key="your-api-key")

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}]
        )
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"Error: {e}")

asyncio.run(safe_request())
```

### Handle Individual Task Errors

```python
from choreoai import AsyncChoreoAI
import asyncio

async def safe_chat(client, question):
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}]
        )
        return {"question": question, "answer": response.choices[0].message.content}

    except Exception as e:
        return {"question": question, "error": str(e)}

async def main():
    client = AsyncChoreoAI(api_key="your-api-key")

    questions = [
        "What is Python?",
        "What is JavaScript?",
        "What is Rust?"
    ]

    results = await asyncio.gather(*[
        safe_chat(client, q) for q in questions
    ])

    for result in results:
        print(f"\nQ: {result['question']}")
        if 'answer' in result:
            print(f"A: {result['answer'][:100]}")
        else:
            print(f"Error: {result['error']}")

asyncio.run(main())
```

### Using return_exceptions

```python
from choreoai import AsyncChoreoAI
import asyncio

async def main():
    client = AsyncChoreoAI(api_key="your-api-key")

    tasks = [
        client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Question {i}"}]
        )
        for i in range(3)
    ]

    # Don't raise on first exception
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed: {result}")
        else:
            print(f"Task {i} succeeded: {result.choices[0].message.content[:50]}")

asyncio.run(main())
```

## Async Context Manager

### Using async with

```python
from choreoai import AsyncChoreoAI
import asyncio

async def main():
    async with AsyncChoreoAI(api_key="your-api-key") as client:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}]
        )
        print(response.choices[0].message.content)

asyncio.run(main())
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI
from choreoai import AsyncChoreoAI
from pydantic import BaseModel

app = FastAPI()
client = AsyncChoreoAI(api_key="your-api-key")

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-4"

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = await client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": request.message}]
    )

    return ChatResponse(
        response=response.choices[0].message.content
    )

# Run with: uvicorn app:app --reload
```

### FastAPI Streaming

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from choreoai import AsyncChoreoAI

app = FastAPI()
client = AsyncChoreoAI(api_key="your-api-key")

@app.get("/stream")
async def stream_chat(message: str):
    async def generate():
        stream = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}],
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    return StreamingResponse(generate(), media_type="text/plain")
```

### aiohttp Integration

```python
from aiohttp import web
from choreoai import AsyncChoreoAI

client = AsyncChoreoAI(api_key="your-api-key")

async def chat_handler(request):
    data = await request.json()
    message = data.get("message")

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message}]
    )

    return web.json_response({
        "response": response.choices[0].message.content
    })

app = web.Application()
app.router.add_post('/chat', chat_handler)

if __name__ == '__main__':
    web.run_app(app)
```

## Advanced Patterns

### Rate Limiting with Semaphore

```python
from choreoai import AsyncChoreoAI
import asyncio

async def rate_limited_requests():
    client = AsyncChoreoAI(api_key="your-api-key")
    semaphore = asyncio.Semaphore(5)  # Max 5 concurrent requests

    async def limited_chat(question):
        async with semaphore:
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": question}]
            )
            return response.choices[0].message.content

    questions = [f"Question {i}" for i in range(20)]

    results = await asyncio.gather(*[
        limited_chat(q) for q in questions
    ])

    return results

asyncio.run(rate_limited_requests())
```

### Timeout Handling

```python
from choreoai import AsyncChoreoAI
import asyncio

async def request_with_timeout():
    client = AsyncChoreoAI(api_key="your-api-key")

    try:
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Long task"}]
            ),
            timeout=10.0  # 10 second timeout
        )
        print(response.choices[0].message.content)

    except asyncio.TimeoutError:
        print("Request timed out after 10 seconds")

asyncio.run(request_with_timeout())
```

### Retry with Exponential Backoff

```python
from choreoai import AsyncChoreoAI
import asyncio

async def retry_request(client, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            wait_time = 2 ** attempt
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)

async def main():
    client = AsyncChoreoAI(api_key="your-api-key")

    response = await retry_request(
        client,
        [{"role": "user", "content": "Hello"}]
    )

    print(response.choices[0].message.content)

asyncio.run(main())
```

### Background Task Processing

```python
from choreoai import AsyncChoreoAI
import asyncio
from asyncio import Queue

async def worker(client, queue, results):
    while True:
        question = await queue.get()

        if question is None:  # Poison pill
            break

        try:
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": question}]
            )
            results.append({
                "question": question,
                "answer": response.choices[0].message.content
            })
        except Exception as e:
            results.append({
                "question": question,
                "error": str(e)
            })
        finally:
            queue.task_done()

async def main():
    client = AsyncChoreoAI(api_key="your-api-key")
    queue = Queue()
    results = []

    # Start workers
    workers = [
        asyncio.create_task(worker(client, queue, results))
        for _ in range(5)  # 5 concurrent workers
    ]

    # Add tasks
    questions = [f"Question {i}" for i in range(20)]
    for question in questions:
        await queue.put(question)

    # Wait for all tasks to complete
    await queue.join()

    # Stop workers
    for _ in workers:
        await queue.put(None)

    await asyncio.gather(*workers)

    print(f"Processed {len(results)} questions")

asyncio.run(main())
```

## Best Practices

### 1. Reuse Client Instance

```python
# Good: Create once, reuse
client = AsyncChoreoAI(api_key="your-api-key")

async def process():
    for i in range(10):
        await client.chat.completions.create(...)

# Bad: Create in loop
async def process():
    for i in range(10):
        client = AsyncChoreoAI(api_key="your-api-key")
        await client.chat.completions.create(...)
```

### 2. Use Semaphores for Rate Limiting

```python
semaphore = asyncio.Semaphore(10)  # Max 10 concurrent

async def limited_request():
    async with semaphore:
        return await client.chat.completions.create(...)
```

### 3. Set Appropriate Timeouts

```python
# Good: Set timeout
response = await asyncio.wait_for(
    client.chat.completions.create(...),
    timeout=30.0
)

# Bad: No timeout (can hang forever)
response = await client.chat.completions.create(...)
```

### 4. Handle Errors Gracefully

```python
# Use return_exceptions to avoid stopping on first error
results = await asyncio.gather(
    *tasks,
    return_exceptions=True
)
```

### 5. Use asyncio.gather for Concurrency

```python
# Good: Concurrent execution
responses = await asyncio.gather(*tasks)

# Less efficient: Sequential
responses = []
for task in tasks:
    response = await task
    responses.append(response)
```

## Performance Comparison

### Sequential vs Concurrent

```python
import time
from choreoai import AsyncChoreoAI
import asyncio

async def sequential():
    client = AsyncChoreoAI(api_key="your-api-key")
    questions = [f"Question {i}" for i in range(10)]

    start = time.time()

    for question in questions:
        await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )

    print(f"Sequential: {time.time() - start:.2f}s")

async def concurrent():
    client = AsyncChoreoAI(api_key="your-api-key")
    questions = [f"Question {i}" for i in range(10)]

    start = time.time()

    tasks = [
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        for question in questions
    ]

    await asyncio.gather(*tasks)

    print(f"Concurrent: {time.time() - start:.2f}s")

# Compare
asyncio.run(sequential())   # ~20-30 seconds
asyncio.run(concurrent())   # ~3-5 seconds
```

## Next Steps

- **[Streaming](streaming.md)** - Async streaming patterns
- **[Chat Guide](chat.md)** - Chat completions basics
- **[Error Handling](../api/error-handling.md)** - Handle async errors
- **[FastAPI Example](https://fastapi.tiangolo.com/)** - Build async APIs
