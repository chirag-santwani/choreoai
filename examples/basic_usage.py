# -*- coding: utf-8 -*-
"""
ChoreoAI Example: Basic Chat Completion

This example demonstrates how to use the OpenAI SDK client with ChoreoAI
for basic chat completions with multiple AI providers (OpenAI, Claude, etc.).

Requirements:
- Run: ./setup.sh (to create virtual environment and install dependencies)
- Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable
- ChoreoAI server running on http://localhost:8000
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def test_model(client, model_name, provider_name):
    """Test a specific model."""
    print(f"📤 Testing {model_name}...")
    print()

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides concise answers."
                },
                {
                    "role": "user",
                    "content": "Explain what ChoreoAI is in one sentence."
                }
            ],
            max_tokens=100,
            temperature=0.7
        )

        # Extract and display the response
        message = response.choices[0].message.content
        usage = response.usage

        print(f"✅ Response from {provider_name}:")
        print("-" * 60)
        print(message)
        print("-" * 60)
        print()
        print("📊 Usage statistics:")
        print(f"  • Prompt tokens: {usage.prompt_tokens}")
        print(f"  • Completion tokens: {usage.completion_tokens}")
        print(f"  • Total tokens: {usage.total_tokens}")
        print()
        return True

    except Exception as e:
        print(f"❌ Error with {provider_name}: {e}")
        print()
        return False


def main():
    """Basic chat completion example."""

    print("=" * 60)
    print("ChoreoAI Example: Basic Chat Completion")
    print("=" * 60)
    print()

    # Check which API keys are available
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))

    if not has_openai and not has_anthropic:
        print("❌ Error: No API keys configured")
        print()
        print("Please set at least one API key:")
        print("  export OPENAI_API_KEY=sk-your-key-here")
        print("  export ANTHROPIC_API_KEY=sk-ant-your-key-here")
        print()
        return 1

    success_count = 0
    total_tests = 0

    # Test OpenAI if key is available
    if has_openai:
        print("🤖 Testing OpenAI GPT-3.5 Turbo")
        print("=" * 60)
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="http://localhost:8000/v1"
        )
        total_tests += 1
        if test_model(client, "gpt-3.5-turbo", "OpenAI GPT-3.5 Turbo"):
            success_count += 1

    # Test Claude if key is available
    if has_anthropic:
        print("🧠 Testing Anthropic Claude 3 Haiku")
        print("=" * 60)
        client = OpenAI(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            base_url="http://localhost:8000/v1"
        )
        total_tests += 1
        if test_model(client, "claude-3-haiku-20240307", "Anthropic Claude 3 Haiku"):
            success_count += 1

    # Summary
    print("=" * 60)
    print(f"✓ Tests completed: {success_count}/{total_tests} successful")
    print("=" * 60)

    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    exit(main())
