"""
ChoreoAI Example: Function Calling

This example demonstrates how to use function calling (tool use) with ChoreoAI.
Function calling allows the AI model to call external functions/APIs to retrieve
information or perform actions.

Requirements:
- Run: ./setup.sh (to create virtual environment and install dependencies)
- Set OPENAI_API_KEY environment variable
- ChoreoAI server running on http://localhost:8000
"""

import os
import json
from openai import OpenAI


# Example functions that the AI can call
def get_current_weather(location: str, unit: str = "fahrenheit") -> dict:
    """
    Get the current weather for a location.
    This is a mock function - in production, you'd call a real weather API.
    """
    # Mock weather data
    weather_data = {
        "San Francisco": {"temperature": 65, "condition": "Partly cloudy"},
        "Tokyo": {"temperature": 72, "condition": "Sunny"},
        "Paris": {"temperature": 58, "condition": "Rainy"},
        "New York": {"temperature": 55, "condition": "Cloudy"}
    }

    location_data = weather_data.get(location, {"temperature": 70, "condition": "Unknown"})

    return {
        "location": location,
        "temperature": location_data["temperature"],
        "unit": unit,
        "condition": location_data["condition"]
    }


def calculate_cost(provider: str, tokens: int) -> dict:
    """
    Calculate the cost for using a specific AI provider.
    Mock pricing data.
    """
    pricing = {
        "openai": 0.002,  # per 1K tokens
        "claude": 0.008,
        "gemini": 0.001
    }

    rate = pricing.get(provider.lower(), 0.001)
    cost = (tokens / 1000) * rate

    return {
        "provider": provider,
        "tokens": tokens,
        "cost_usd": round(cost, 4),
        "rate_per_1k": rate
    }


def main():
    """Function calling example."""

    print("=" * 60)
    print("ChoreoAI Example: Function Calling")
    print("=" * 60)
    print()

    # Initialize OpenAI client with ChoreoAI base URL
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="http://localhost:8000/v1"
    )

    # Define the functions/tools available to the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The temperature unit"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_cost",
                "description": "Calculate the cost of using an AI provider for a given number of tokens",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "provider": {
                            "type": "string",
                            "description": "The AI provider name (openai, claude, gemini)"
                        },
                        "tokens": {
                            "type": "integer",
                            "description": "Number of tokens to calculate cost for"
                        }
                    },
                    "required": ["provider", "tokens"]
                }
            }
        }
    ]

    # Map function names to actual functions
    available_functions = {
        "get_current_weather": get_current_weather,
        "calculate_cost": calculate_cost
    }

    # Initial user message
    messages = [
        {
            "role": "user",
            "content": "What's the weather like in San Francisco and how much would it cost to use OpenAI for 10,000 tokens?"
        }
    ]

    print("=¬ User query:")
    print(f"   {messages[0]['content']}")
    print()

    try:
        # First API call: Let the model decide which functions to call
        print("= Sending request to ChoreoAI...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Check if the model wants to call functions
        if tool_calls:
            print(f" Model requested {len(tool_calls)} function call(s)")
            print()

            # Add the assistant's response to messages
            messages.append(response_message)

            # Execute each function call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"=' Calling function: {function_name}")
                print(f"   Arguments: {function_args}")

                # Call the actual function
                function_to_call = available_functions[function_name]
                function_response = function_to_call(**function_args)

                print(f"   Response: {function_response}")
                print()

                # Add function response to messages
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response)
                })

            # Second API call: Get final response from the model
            print("= Getting final response from model...")
            final_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            final_message = final_response.choices[0].message.content

            print(" Final response received!")
            print()
            print("=Ý Assistant's answer:")
            print("-" * 60)
            print(final_message)
            print("-" * 60)
            print()
            print("( Success! Function calling completed.")

        else:
            # Model didn't call any functions
            print("9  Model responded directly without calling functions")
            print()
            print("=Ý Response:")
            print("-" * 60)
            print(response_message.content)
            print("-" * 60)

    except Exception as e:
        print(f"L Error: {e}")
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
        print("L Error: OPENAI_API_KEY environment variable not set")
        print()
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY=sk-your-key-here")
        print()
        exit(1)

    exit(main())
