# Glossary

Comprehensive glossary of terms and concepts used in ChoreoAI.

## A

### API (Application Programming Interface)
A set of protocols and tools that allow different software applications to communicate with each other. ChoreoAI provides a REST API for accessing AI models.

### API Key
A unique identifier used to authenticate requests to the ChoreoAI API. API keys are passed in the `Authorization` header of HTTP requests.

### Adapter
A software component in ChoreoAI that translates between the unified API format and provider-specific formats. Each AI provider has its own adapter (e.g., OpenAI adapter, Claude adapter).

### Async/Await
A programming pattern in Python and JavaScript for handling asynchronous operations. ChoreoAI provides async support for non-blocking API calls.

### Anthropic
The company that created Claude, one of the AI models supported by ChoreoAI. Also referred to as the Claude provider.

### Azure OpenAI
Microsoft's cloud service offering OpenAI models through Azure. Requires separate configuration from standard OpenAI.

## B

### Base URL
The root URL for API requests. Default is `http://localhost:8000` for local development. In production, this would be your deployed API endpoint.

### Bearer Token
An authentication scheme where the API key is prefixed with "Bearer" in the Authorization header. Format: `Authorization: Bearer your-api-key`

### Bedrock
Amazon Web Services (AWS) service providing access to foundation models from various providers. Requires AWS credentials for access.

### Backoff (Exponential)
A retry strategy where wait time increases exponentially between retry attempts (e.g., 1s, 2s, 4s, 8s). Used to handle rate limits and temporary failures.

## C

### Chat Completion
The primary API operation for generating conversational AI responses. Takes a list of messages and returns the AI's response.

### Context Length
The maximum number of tokens (words/subwords) a model can process in a single request. Different models have different context lengths (e.g., GPT-4: 8K, Claude: 200K).

### Context Window
See Context Length. The "window" of text the model can see and process at once.

### CORS (Cross-Origin Resource Sharing)
A security mechanism that controls which web domains can access the API. Configured via `ALLOWED_ORIGINS` environment variable.

### Choreoai
The Python client library for interacting with the ChoreoAI API. Provides both sync (`ChoreoAI`) and async (`AsyncChoreoAI`) clients.

### Claude
An AI model family created by Anthropic. Includes Claude 3 Opus, Sonnet, and Haiku variants.

## D

### Deployment
The process of making the ChoreoAI API available in a production environment. Supports Docker, Kubernetes, and Helm deployments.

### Delta
In streaming responses, the incremental piece of text received in each chunk. Contains the newly generated tokens since the last chunk.

### dotenv
A library and pattern for loading environment variables from a `.env` file. Used to configure API keys and settings.

## E

### Embedding
A numerical representation of text as a vector. Used for semantic search, clustering, and similarity comparisons. Created via the `/v1/embeddings` endpoint.

### Endpoint
A specific URL path that performs a particular API operation (e.g., `/v1/chat/completions`, `/v1/models`).

### Environment Variable
A configuration value set in the operating system or deployment environment (e.g., `OPENAI_API_KEY`). Used to configure ChoreoAI without hardcoding values.

### Error Code
A specific identifier for an error type (e.g., `rate_limit_exceeded`, `model_not_found`). Used to programmatically handle different error conditions.

## F

### Fallback
A strategy where if one AI provider fails, the system automatically tries another provider. Improves reliability and uptime.

### FastAPI
The Python web framework used to build the ChoreoAI API server. Provides automatic API documentation and validation.

### Finish Reason
Indicates why the model stopped generating text. Common values:
- `stop`: Natural completion
- `length`: Hit max_tokens limit
- `content_filter`: Blocked by content policy

### Frequency Penalty
A parameter (-2.0 to 2.0) that reduces repetition by penalizing tokens that have already appeared. Higher values mean less repetition.

## G

### Gemini
Google's family of AI models. Includes Gemini Pro and Gemini Pro Vision variants.

### GPT (Generative Pre-trained Transformer)
The architecture behind OpenAI's models. GPT-4 and GPT-3.5 are the most common variants used in ChoreoAI.

### Grok
AI models created by xAI. Supported as a provider in ChoreoAI.

## H

### Helm
A package manager for Kubernetes. ChoreoAI provides Helm charts for easy Kubernetes deployment.

### HTTP Status Code
A numeric code indicating the result of an HTTP request (e.g., 200 OK, 401 Unauthorized, 429 Rate Limit). Used to determine request success or failure type.

## I

### Inference
The process of using a trained AI model to generate predictions or responses. When you call the API, you're performing inference.

### Input Tokens
The tokens in your request messages. Used to calculate costs and check against context length limits.

## J

### JSON (JavaScript Object Notation)
The data format used for API requests and responses. A text-based format for structured data.

## K

### Kubernetes (K8s)
A container orchestration platform. ChoreoAI can be deployed to Kubernetes for production use.

## L

### LLM (Large Language Model)
AI models trained on large amounts of text data to understand and generate human language. Examples: GPT-4, Claude, Gemini.

### Log Level
Controls the verbosity of application logs. Values: DEBUG, INFO, WARNING, ERROR, CRITICAL.

## M

### Max Tokens
The maximum number of tokens to generate in the response. Used to control response length and costs.

### Message
A single unit in a conversation, containing a `role` (system, user, or assistant) and `content` (the text).

### Middleware
Software components that process requests before they reach the main application logic. ChoreoAI uses middleware for authentication, logging, and rate limiting.

### Model
An AI system trained to perform specific tasks. ChoreoAI supports models from multiple providers (OpenAI, Claude, Gemini, etc.).

### Model ID
The unique identifier for a specific model (e.g., `gpt-4`, `claude-3-opus-20240229`). Used in API requests to specify which model to use.

### Multimodal
Models that can process multiple types of input (text, images, etc.). Example: Gemini Pro Vision.

## N

### Nucleus Sampling (Top-P)
A generation strategy that samples from the smallest set of tokens whose cumulative probability exceeds p. Controlled by the `top_p` parameter.

## O

### OpenAI
The company that created GPT models. One of the primary providers supported by ChoreoAI.

### OpenAI-Compatible
APIs that follow OpenAI's API specification. ChoreoAI is OpenAI-compatible, allowing use of OpenAI SDKs.

### Orchestration
The process of coordinating multiple services or providers. ChoreoAI orchestrates access to multiple AI providers through a single interface.

### Output Tokens
The tokens in the model's response. Used to calculate costs and measure response length.

## P

### Parameter
A configurable value in an API request that controls model behavior (e.g., `temperature`, `max_tokens`, `top_p`).

### Presence Penalty
A parameter (-2.0 to 2.0) that encourages the model to talk about new topics. Higher values mean more topic diversity.

### Provider
An AI service that offers models (e.g., OpenAI, Anthropic, Google). ChoreoAI supports multiple providers.

### Prompt
The input text given to an AI model. In chat completions, this is the conversation history (messages).

### Python SDK
The official Python client library for ChoreoAI. Provides a clean API for making requests.

## Q

### Quota
A limit on API usage, typically measured in requests per time period or total tokens. Can cause `quota_exceeded` errors when exceeded.

## R

### Rate Limit
A restriction on how many API requests can be made in a given time period. Prevents abuse and ensures fair usage.

### REST (Representational State Transfer)
An architectural style for web APIs. ChoreoAI provides a RESTful API with standard HTTP methods.

### Retry
The act of attempting a failed request again. Recommended for transient errors like rate limits or timeouts.

### Role
The participant type in a conversation message. Valid roles:
- `system`: Instructions for the model
- `user`: User input
- `assistant`: Model responses

## S

### Server-Sent Events (SSE)
A protocol for streaming data from server to client. Used in ChoreoAI for streaming responses.

### Streaming
A mode where the model's response is sent incrementally as it's generated, rather than waiting for completion. Enabled with `stream=True`.

### Stop Sequence
A string or list of strings that, when generated, cause the model to stop generating further tokens.

### System Message
A message with role `system` that provides instructions or context for the AI model. Typically the first message in a conversation.

## T

### Temperature
A parameter (0.0 to 2.0) controlling response randomness. Lower values (0.0-0.3) are more focused and deterministic, higher values (0.7-1.0) are more creative and random.

### Timeout
The maximum time to wait for a request to complete. Prevents indefinite waiting if a provider is slow or unresponsive.

### Token
The basic unit of text processed by AI models. Roughly equivalent to a word or subword. Used for pricing and context limits.

### Top-P
See Nucleus Sampling. A parameter (0.0 to 1.0) for controlling output diversity.

## U

### Unified API
A single, consistent API interface that works across multiple providers. ChoreoAI's core value proposition.

### Usage
Information about token consumption in a request. Includes `prompt_tokens`, `completion_tokens`, and `total_tokens`.

## V

### Vector
A numerical representation of text (embedding). Used for semantic operations like similarity search.

### Virtual Environment (venv)
An isolated Python environment for managing dependencies. Recommended for installing ChoreoAI client.

## W

### Webhook
An HTTP callback for event notifications. While not currently implemented in ChoreoAI, webhooks could be used for async notifications.

## X

### xAI
The company behind Grok AI models. One of the providers supported by ChoreoAI.

## Acronyms

| Acronym | Full Form | Description |
|---------|-----------|-------------|
| API | Application Programming Interface | Interface for software interaction |
| AWS | Amazon Web Services | Cloud computing platform |
| CORS | Cross-Origin Resource Sharing | Web security mechanism |
| GPT | Generative Pre-trained Transformer | OpenAI's model architecture |
| HTTP | Hypertext Transfer Protocol | Web communication protocol |
| JSON | JavaScript Object Notation | Data interchange format |
| K8s | Kubernetes | Container orchestration (8 chars between K and s) |
| LLM | Large Language Model | AI language model |
| REST | Representational State Transfer | API architectural style |
| SDK | Software Development Kit | Developer tools and libraries |
| SSE | Server-Sent Events | Streaming protocol |
| URL | Uniform Resource Locator | Web address |

## Common Model Identifiers

| Model ID | Provider | Description |
|----------|----------|-------------|
| `gpt-4` | OpenAI | GPT-4 base model |
| `gpt-4-turbo-preview` | OpenAI | Latest GPT-4 with extended context |
| `gpt-3.5-turbo` | OpenAI | Fast, cost-effective model |
| `claude-3-opus-20240229` | Anthropic | Most capable Claude model |
| `claude-3-sonnet-20240229` | Anthropic | Balanced Claude model |
| `claude-3-haiku-20240307` | Anthropic | Fastest Claude model |
| `gemini-pro` | Google | Gemini's main model |
| `gemini-pro-vision` | Google | Multimodal Gemini |
| `text-embedding-ada-002` | OpenAI | Embedding model |

## HTTP Status Codes

| Code | Name | Meaning |
|------|------|---------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication failed |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 502 | Bad Gateway | Provider error |
| 503 | Service Unavailable | Service down |

## Common Parameter Ranges

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `temperature` | float | 0.0 - 2.0 | 1.0 | Response randomness |
| `top_p` | float | 0.0 - 1.0 | 1.0 | Nucleus sampling |
| `max_tokens` | integer | 1 - model max | null | Max response length |
| `presence_penalty` | float | -2.0 - 2.0 | 0.0 | Topic diversity |
| `frequency_penalty` | float | -2.0 - 2.0 | 0.0 | Repetition reduction |

## Environment Variable Prefixes

| Prefix | Purpose | Example |
|--------|---------|---------|
| `CHOREOAI_` | Client configuration | `CHOREOAI_API_KEY` |
| `OPENAI_` | OpenAI provider | `OPENAI_API_KEY` |
| `ANTHROPIC_` | Anthropic provider | `ANTHROPIC_API_KEY` |
| `AZURE_` | Azure provider | `AZURE_OPENAI_API_KEY` |
| `GEMINI_` | Google provider | `GEMINI_API_KEY` |
| `AWS_` | AWS configuration | `AWS_REGION` |

## File Extensions

| Extension | Description |
|-----------|-------------|
| `.env` | Environment variables file |
| `.py` | Python source code |
| `.yaml` / `.yml` | YAML configuration |
| `.json` | JSON data |
| `.md` | Markdown documentation |
| `.toml` | TOML configuration |

## Related Documentation

- **[Environment Variables](environment-vars.md)** - Configuration reference
- **[Error Codes](error-codes.md)** - Error code reference
- **[FAQ](faq.md)** - Frequently asked questions
- **[API Documentation](../api/README.md)** - API reference
