# -*- coding: utf-8 -*-
"""
ChoreoAI Example: Streaming Chat Completion

This example demonstrates how to use streaming responses with ChoreoAI.
Streaming allows you to receive the response token-by-token as it's generated,
providing a better user experience for longer responses.

Requirements:
- Run: ./setup.sh (to create virtual environment and install dependencies)
- Set OPENAI_API_KEY environment variable
- ChoreoAI server running on http://localhost:8000
"""

import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    """Streaming chat completion example."""

    print("=" * 60)
    print("ChoreoAI Example: Streaming Chat Completion")
    print("=" * 60)
    print()

    # Initialize OpenAI client with ChoreoAI base URL
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="http://localhost:8000/v1"
    )

    print("📤 Sending streaming request to ChoreoAI...")
    print()
    print("💬 Assistant's response (streaming):")
    print("-" * 60)

    try:
        # Create a streaming chat completion
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Write a short poem about AI orchestration (3-4 lines)."
                }
            ],
            max_tokens=150,
            temperature=0.8,
            stream=True  # Enable streaming
        )

        # Process the stream and print tokens as they arrive
        full_response = ""
        for chunk in stream:
            # Extract the content delta from the chunk
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                # Print without newline to show streaming effect
                print(content, end="", flush=True)

        print()  # New line after streaming is complete
        print("-" * 60)
        print()
        print(f"📊 Total characters received: {len(full_response)}")
        print()
        print("✓ Success! Streaming completed.")

    except Exception as e:
        print()
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
