"""
Quick test script for OpenAI adapter.
Usage: Set OPENAI_API_KEY environment variable and run: python test_openai_adapter.py
"""
import asyncio
import os
from api.app.adapters.openai_adapter import OpenAIAdapter


async def test_chat_completion():
    """Test basic chat completion"""
    print("Testing chat completion...")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return

    adapter = OpenAIAdapter(api_key=api_key)

    request = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say 'Hello from ChoreoAI!' and nothing else."}
        ],
        "max_tokens": 20
    }

    try:
        response = await adapter.chat_completion(request)
        print(f"✅ Chat completion successful")
        print(f"   Response: {response['choices'][0]['message']['content']}")
    except Exception as e:
        print(f"❌ Chat completion failed: {e}")


async def test_streaming():
    """Test streaming chat completion"""
    print("\nTesting streaming...")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return

    adapter = OpenAIAdapter(api_key=api_key)

    request = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Count from 1 to 3."}
        ],
        "max_tokens": 20
    }

    try:
        chunks = []
        async for chunk in adapter.chat_completion_stream(request):
            if chunk['choices'][0].get('delta', {}).get('content'):
                chunks.append(chunk['choices'][0]['delta']['content'])

        print(f"✅ Streaming successful")
        print(f"   Streamed content: {''.join(chunks)}")
    except Exception as e:
        print(f"❌ Streaming failed: {e}")


async def test_embeddings():
    """Test embeddings"""
    print("\nTesting embeddings...")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return

    adapter = OpenAIAdapter(api_key=api_key)

    request = {
        "model": "text-embedding-3-small",
        "input": "Hello, world!"
    }

    try:
        response = await adapter.create_embedding(request)
        embedding_length = len(response['data'][0]['embedding'])
        print(f"✅ Embeddings successful")
        print(f"   Embedding dimension: {embedding_length}")
    except Exception as e:
        print(f"❌ Embeddings failed: {e}")


async def test_list_models():
    """Test list models"""
    print("\nTesting list models...")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return

    adapter = OpenAIAdapter(api_key=api_key)

    try:
        models = await adapter.list_models()
        print(f"✅ List models successful")
        print(f"   Available models: {len(models['data'])} models")
        for model in models['data'][:5]:  # Show first 5 models
            print(f"   - {model['id']}")
        if len(models['data']) > 5:
            print(f"   ... and {len(models['data']) - 5} more")
    except Exception as e:
        print(f"❌ List models failed: {e}")


async def main():
    print("=" * 50)
    print("OpenAI Adapter Test Suite")
    print("=" * 50)

    # Check for API key before running other tests
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Set OPENAI_API_KEY to run API tests")
        return

    # Test API methods
    await test_list_models()
    await test_chat_completion()
    await test_streaming()
    await test_embeddings()

    print("\n" + "=" * 50)
    print("Tests complete!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
