# -*- coding: utf-8 -*-
"""
ChoreoAI Example: Basic Chat Completion

This example demonstrates how to use the OpenAI SDK client with ChoreoAI
for basic chat completions.

Requirements:
- Run: ./setup.sh (to create virtual environment and install dependencies)
- Set OPENAI_API_KEY environment variable
- ChoreoAI server running on http://localhost:8000
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    """Basic chat completion example."""

    print("=" * 60)
    print("ChoreoAI Example: Basic Chat Completion")
    print("=" * 60)
    print()

    # Initialize OpenAI client with ChoreoAI base URL
    # This routes all requests through ChoreoAI instead of directly to OpenAI
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="http://localhost:8000/v1"  # Point to ChoreoAI
    )

    print("📤 Sending request to ChoreoAI...")
    print()

    # Create a basic chat completion
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
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

        print("✅ Response received!")
        print()
        print("💬 Assistant's response:")
        print("-" * 60)
        print(message)
        print("-" * 60)
        print()
        print("📊 Usage statistics:")
        print(f"  • Prompt tokens: {usage.prompt_tokens}")
        print(f"  • Completion tokens: {usage.completion_tokens}")
        print(f"  • Total tokens: {usage.total_tokens}")
        print()

        print("✓ Success! ChoreoAI is routing requests correctly.")

    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Make sure ChoreoAI is running: docker-compose up -d")
        print("  2. Check that OPENAI_API_KEY is set: echo $OPENAI_API_KEY")
        print("  3. Verify ChoreoAI is accessible: curl http://localhost:8000/health")
        return 1

    print()
    print("=" * 60)

    return 0


if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print()
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY=sk-your-key-here")
        print()
        exit(1)

    exit(main())
