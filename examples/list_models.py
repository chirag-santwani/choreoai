# -*- coding: utf-8 -*-
"""
ChoreoAI Example: List Available Models

This example demonstrates how to list all available models from ChoreoAI.
It shows models from all configured providers (OpenAI, Claude, Gemini, etc.).

Requirements:
- Run: ./setup.sh (to create virtual environment and install dependencies)
- Set OPENAI_API_KEY environment variable (or other provider keys)
- ChoreoAI server running on http://localhost:8000
"""

import os
from openai import OpenAI


def main():
    """List available models example."""

    print("=" * 60)
    print("ChoreoAI Example: List Available Models")
    print("=" * 60)
    print()

    # Initialize OpenAI client with ChoreoAI base URL
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="http://localhost:8000/v1"
    )

    print("📋 Fetching available models from ChoreoAI...")
    print()

    try:
        # Fetch all models
        models = client.models.list()

        # Categorize models by provider and type
        model_categories = {
            "gpt-": [],
            "claude-": [],
            "gemini-": [],
            "grok-": [],
            "text-embedding": [],
            "other": []
        }

        for model in models.data:
            categorized = False
            for prefix in ["gpt-", "claude-", "gemini-", "grok-", "text-embedding"]:
                if model.id.startswith(prefix):
                    model_categories[prefix].append(model.id)
                    categorized = True
                    break
            if not categorized:
                model_categories["other"].append(model.id)

        # Display GPT models
        if model_categories["gpt-"]:
            print(f"🤖 OpenAI GPT Models ({len(model_categories['gpt-'])} available):")
            print("-" * 60)
            for model_id in sorted(model_categories["gpt-"]):
                print(f"  • {model_id}")
            print()

        # Display Claude models
        if model_categories["claude-"]:
            print(f"🧠 Anthropic Claude Models ({len(model_categories['claude-'])} available):")
            print("-" * 60)
            for model_id in sorted(model_categories["claude-"]):
                print(f"  • {model_id}")
            print()

        # Display Gemini models
        if model_categories["gemini-"]:
            print(f"💎 Google Gemini Models ({len(model_categories['gemini-'])} available):")
            print("-" * 60)
            for model_id in sorted(model_categories["gemini-"]):
                print(f"  • {model_id}")
            print()

        # Display Grok models
        if model_categories["grok-"]:
            print(f"🚀 xAI Grok Models ({len(model_categories['grok-'])} available):")
            print("-" * 60)
            for model_id in sorted(model_categories["grok-"]):
                print(f"  • {model_id}")
            print()

        # Display embedding models
        if model_categories["text-embedding"]:
            print(f"🔢 OpenAI Embedding Models ({len(model_categories['text-embedding'])} available):")
            print("-" * 60)
            for model_id in sorted(model_categories["text-embedding"]):
                print(f"  • {model_id}")
            print()

        # Display other models
        if model_categories["other"]:
            print(f"🔧 Other Models ({len(model_categories['other'])} available):")
            print("-" * 60)
            for model_id in sorted(model_categories["other"]):
                print(f"  • {model_id}")
            print()

        # Summary
        total_models = len(models.data)
        print("=" * 60)
        print(f"✓ Total models available: {total_models}")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Make sure ChoreoAI is running: docker-compose up -d")
        print("  2. Check that at least one provider API key is set")
        print("  3. Verify ChoreoAI is accessible: curl http://localhost:8000/health")
        return 1

    return 0


if __name__ == "__main__":
    # Check if at least one API key is set
    if not any([
        os.getenv("OPENAI_API_KEY"),
        os.getenv("ANTHROPIC_API_KEY"),
        os.getenv("GEMINI_API_KEY"),
        os.getenv("GROK_API_KEY")
    ]):
        print("❌ Error: No API keys configured")
        print()
        print("Please set at least one provider API key:")
        print("  export OPENAI_API_KEY=sk-your-key-here")
        print("  export ANTHROPIC_API_KEY=sk-ant-your-key-here")
        print()
        exit(1)

    exit(main())
