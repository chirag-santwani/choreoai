# Azure OpenAI Provider Guide

This guide covers how to use Azure OpenAI Service through ChoreoAI, including setup, configuration, and best practices.

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Supported Models](#supported-models)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Rate Limits](#rate-limits)
- [Pricing](#pricing)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Azure OpenAI Service provides access to OpenAI's powerful language models through Microsoft Azure, offering enterprise-grade security, compliance, and regional availability.

### Key Features
- **Enterprise Security**: Private endpoints, VNet integration, Azure AD authentication
- **Compliance**: SOC 2, HIPAA, ISO 27001, and more
- **Regional Deployment**: Deploy models in your preferred Azure region
- **SLA**: Enterprise-grade service level agreements
- **Content Filtering**: Built-in content safety features

### Status
🚧 **Azure OpenAI integration is currently in development**

ChoreoAI's Azure OpenAI adapter is being developed. This documentation provides the planned implementation and configuration.

## Getting Started

### Prerequisites

1. **Azure Subscription**: Active Azure subscription
2. **Azure OpenAI Access**: Request access at [Azure OpenAI Access](https://aka.ms/oai/access)
3. **Resource Creation**: Create an Azure OpenAI resource

### 1. Create Azure OpenAI Resource

#### Using Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Azure OpenAI"
4. Click "Create"
5. Fill in the details:
   - **Subscription**: Select your subscription
   - **Resource Group**: Create new or select existing
   - **Region**: Choose your region (e.g., East US, West Europe)
   - **Name**: Enter a unique name
   - **Pricing Tier**: Select Standard S0
6. Click "Review + Create" then "Create"

#### Using Azure CLI

```bash
# Login to Azure
az login

# Create resource group
az group create \
  --name choreoai-rg \
  --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create \
  --name choreoai-openai \
  --resource-group choreoai-rg \
  --kind OpenAI \
  --sku S0 \
  --location eastus
```

### 2. Deploy Models

Models must be deployed before use:

#### Using Azure Portal

1. Navigate to your Azure OpenAI resource
2. Go to "Model deployments" → "Manage Deployments"
3. Click "Create new deployment"
4. Select model (e.g., gpt-4, gpt-35-turbo)
5. Enter deployment name
6. Configure capacity (TPM - Tokens Per Minute)
7. Click "Create"

#### Using Azure CLI

```bash
# Deploy GPT-4
az cognitiveservices account deployment create \
  --name choreoai-openai \
  --resource-group choreoai-rg \
  --deployment-name gpt-4-deployment \
  --model-name gpt-4 \
  --model-version "0613" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name "Standard"

# Deploy GPT-3.5 Turbo
az cognitiveservices account deployment create \
  --name choreoai-openai \
  --resource-group choreoai-rg \
  --deployment-name gpt-35-turbo \
  --model-name gpt-35-turbo \
  --model-version "0613" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name "Standard"
```

### 3. Get API Keys and Endpoint

#### Using Azure Portal

1. Navigate to your Azure OpenAI resource
2. Go to "Keys and Endpoint"
3. Copy one of the keys and the endpoint URL

#### Using Azure CLI

```bash
# Get keys
az cognitiveservices account keys list \
  --name choreoai-openai \
  --resource-group choreoai-rg

# Get endpoint
az cognitiveservices account show \
  --name choreoai-openai \
  --resource-group choreoai-rg \
  --query properties.endpoint \
  --output tsv
```

### 4. Set Up Environment

Set your Azure OpenAI credentials as environment variables:

```bash
export AZURE_OPENAI_API_KEY=your-azure-key-here
export AZURE_OPENAI_ENDPOINT=https://choreoai-openai.openai.azure.com
export AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

Or create a `.env` file:

```bash
# .env file
AZURE_OPENAI_API_KEY=your-azure-key-here
AZURE_OPENAI_ENDPOINT=https://choreoai-openai.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 5. Make Your First Request (Coming Soon)

Once implemented, you'll be able to use Azure OpenAI like this:

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-azure-key",
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="gpt-4-deployment",  # Your deployment name
    messages=[
        {"role": "user", "content": "What is ChoreoAI?"}
    ]
)

print(response.choices[0].message.content)
```

## Supported Models

Azure OpenAI supports the same models as OpenAI, but they must be deployed first.

### Available Models

| Model Family | Versions | Use Case |
|-------------|----------|----------|
| **GPT-4** | 0613, 1106-Preview, 0125-Preview | Complex reasoning, latest features |
| **GPT-4 32K** | 0613 | Extended context tasks |
| **GPT-4 Turbo** | 1106-Preview, 0125-Preview | Large context, vision |
| **GPT-3.5 Turbo** | 0613, 1106 | Fast, cost-effective |
| **GPT-3.5 Turbo 16K** | 0613 | Extended context |
| **Embeddings** | ada-002 | Text embeddings |
| **DALL-E 3** | - | Image generation |
| **Whisper** | - | Speech-to-text |

### Model Naming

Azure uses deployment names instead of model names:

```python
# OpenAI
model="gpt-4"

# Azure OpenAI
model="gpt-4-deployment"  # Your custom deployment name
```

### Regional Availability

Model availability varies by region. Check the [Model Availability](https://learn.microsoft.com/azure/ai-services/openai/concepts/models) page.

## Configuration

### Basic Configuration (Planned)

```python
from openai import AzureOpenAI

# Using Azure SDK directly
client = AzureOpenAI(
    api_key="your-azure-key",
    api_version="2024-02-15-preview",
    azure_endpoint="https://choreoai-openai.openai.azure.com"
)

# Using ChoreoAI (when implemented)
from openai import OpenAI

client = OpenAI(
    api_key="your-azure-key",
    base_url="http://localhost:8000/v1"
)
```

### Authentication Methods

#### 1. API Key Authentication

```bash
export AZURE_OPENAI_API_KEY=your-key
```

#### 2. Azure AD Authentication

```python
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

credential = DefaultAzureCredential()
token = credential.get_token("https://cognitiveservices.azure.com/.default")

client = AzureOpenAI(
    azure_ad_token=token.token,
    api_version="2024-02-15-preview",
    azure_endpoint="https://choreoai-openai.openai.azure.com"
)
```

#### 3. Managed Identity

```python
from azure.identity import ManagedIdentityCredential

credential = ManagedIdentityCredential()
token = credential.get_token("https://cognitiveservices.azure.com/.default")
```

### Environment Variables

```bash
# Required
export AZURE_OPENAI_API_KEY=your-key
export AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# Optional
export AZURE_OPENAI_API_VERSION=2024-02-15-preview
export AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4-deployment
```

## Usage Examples

### Basic Chat Completion (Planned)

```python
response = client.chat.completions.create(
    model="gpt-4-deployment",  # Your deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain Azure OpenAI"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### Streaming Responses (Planned)

```python
stream = client.chat.completions.create(
    model="gpt-35-turbo",
    messages=[
        {"role": "user", "content": "Write a story about Azure"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Function Calling (Planned)

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_deployment_status",
            "description": "Get Azure deployment status",
            "parameters": {
                "type": "object",
                "properties": {
                    "deployment_name": {
                        "type": "string",
                        "description": "Name of the deployment"
                    }
                },
                "required": ["deployment_name"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4-deployment",
    messages=[{"role": "user", "content": "Check status of my GPT-4 deployment"}],
    tools=tools
)
```

### Embeddings (Planned)

```python
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Azure OpenAI provides enterprise-grade AI"
)

embedding = response.data[0].embedding
print(f"Embedding dimensions: {len(embedding)}")
```

## Rate Limits

Azure OpenAI uses Tokens Per Minute (TPM) quotas set during deployment.

### Quota Types

| Quota Type | Description | Default |
|-----------|-------------|---------|
| **TPM** | Tokens Per Minute | Varies by model |
| **RPM** | Requests Per Minute | Derived from TPM |
| **Concurrent Requests** | Max simultaneous requests | 100 |

### Typical TPM Quotas

| Model | Default TPM | Max TPM (with approval) |
|-------|------------|------------------------|
| GPT-4 | 10K | 300K+ |
| GPT-4 32K | 10K | 150K+ |
| GPT-3.5 Turbo | 60K | 1M+ |
| Embeddings | 120K | 1M+ |

### Requesting Quota Increase

1. Navigate to your Azure OpenAI resource
2. Go to "Quotas" → "Request quota increase"
3. Fill in the form:
   - Model type
   - Deployment name
   - Current quota
   - Requested quota
   - Business justification
4. Submit and wait for approval (usually 1-2 business days)

### Handling Rate Limits (Planned)

```python
import time
from openai import RateLimitError

def chat_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-4-deployment",
                messages=messages
            )
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            # Azure returns retry-after header
            retry_after = int(e.response.headers.get('retry-after', 60))
            print(f"Rate limited. Waiting {retry_after}s...")
            time.sleep(retry_after)
```

## Pricing

Azure OpenAI pricing varies by region and may differ from OpenAI's pricing.

### Pay-As-You-Go Pricing (East US)

| Model | Price per 1K tokens |
|-------|-------------------|
| GPT-4 (8K) | $0.03 (input) / $0.06 (output) |
| GPT-4 (32K) | $0.06 (input) / $0.12 (output) |
| GPT-4 Turbo | $0.01 (input) / $0.03 (output) |
| GPT-3.5 Turbo | $0.0005 (input) / $0.0015 (output) |
| Embeddings | $0.0001 |

### Regional Pricing

Pricing varies by region. Check [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for your region.

### Commitment Tier Pricing

Azure offers discounted rates for committed usage:

| Commitment | Discount | Duration |
|-----------|----------|----------|
| 100M tokens | ~15% | 1 month |
| 1B tokens | ~25% | 1 month |
| 10B tokens | ~35% | 1 month |

### Cost Management

#### 1. Set Budget Alerts

```bash
# Create budget using Azure CLI
az consumption budget create \
  --resource-group choreoai-rg \
  --budget-name openai-monthly-budget \
  --amount 1000 \
  --time-grain Monthly \
  --category Cost
```

#### 2. Monitor Costs

```python
# Track usage in your application
response = client.chat.completions.create(...)

usage = response.usage
cost = (usage.prompt_tokens * 0.03 + usage.completion_tokens * 0.06) / 1000

# Log to Azure Monitor or Application Insights
```

#### 3. Use Cheaper Models

```python
def select_model(complexity):
    if complexity == "simple":
        return "gpt-35-turbo"  # Cheaper
    else:
        return "gpt-4-deployment"  # More expensive
```

## Best Practices

### 1. Security

#### Private Endpoints

```bash
# Create private endpoint
az network private-endpoint create \
  --name choreoai-openai-pe \
  --resource-group choreoai-rg \
  --vnet-name choreoai-vnet \
  --subnet choreoai-subnet \
  --private-connection-resource-id $(az cognitiveservices account show \
    --name choreoai-openai \
    --resource-group choreoai-rg \
    --query id -o tsv) \
  --group-id account \
  --connection-name choreoai-openai-connection
```

#### Managed Identity

```python
# Use managed identity instead of API keys
from azure.identity import ManagedIdentityCredential

credential = ManagedIdentityCredential()
```

#### Key Rotation

```bash
# Regenerate keys regularly
az cognitiveservices account keys regenerate \
  --name choreoai-openai \
  --resource-group choreoai-rg \
  --key-name key1
```

### 2. High Availability

#### Multi-Region Deployment

```python
# Fallback to different regions
regions = [
    {
        "endpoint": "https://choreoai-eastus.openai.azure.com",
        "key": "east-us-key"
    },
    {
        "endpoint": "https://choreoai-westus.openai.azure.com",
        "key": "west-us-key"
    }
]

for region in regions:
    try:
        client = AzureOpenAI(
            api_key=region["key"],
            azure_endpoint=region["endpoint"]
        )
        response = client.chat.completions.create(...)
        break
    except Exception as e:
        continue
```

### 3. Content Filtering

Azure OpenAI includes content filtering:

```python
# Check if content was filtered
response = client.chat.completions.create(...)

if hasattr(response.choices[0], 'content_filter_results'):
    filters = response.choices[0].content_filter_results
    print(f"Content filter results: {filters}")
```

### 4. Monitoring

#### Azure Monitor Integration

```python
from azure.monitor.opentelemetry import configure_azure_monitor

# Configure Application Insights
configure_azure_monitor(
    connection_string="InstrumentationKey=your-key"
)

# Calls will be automatically tracked
```

#### Custom Metrics

```python
from azure.monitor.ingestion import LogsIngestionClient

# Log custom metrics
client.log_custom_event(
    "OpenAI_Request",
    {
        "model": "gpt-4-deployment",
        "tokens": response.usage.total_tokens,
        "cost": estimated_cost
    }
)
```

### 5. Deployment Strategy

```bash
# Use deployment slots for testing
az cognitiveservices account deployment create \
  --name choreoai-openai \
  --resource-group choreoai-rg \
  --deployment-name gpt-4-test \
  --model-name gpt-4 \
  --model-version "0613" \
  --sku-capacity 5 \
  --sku-name "Standard"
```

## Troubleshooting

### Common Issues

#### 1. Resource Not Found

```
Error: The specified resource does not exist
```

**Solution**:
```bash
# Verify resource exists
az cognitiveservices account show \
  --name choreoai-openai \
  --resource-group choreoai-rg

# Check endpoint URL
echo $AZURE_OPENAI_ENDPOINT
```

#### 2. Deployment Not Found

```
Error: The deployment 'gpt-4' does not exist
```

**Solution**:
```bash
# List deployments
az cognitiveservices account deployment list \
  --name choreoai-openai \
  --resource-group choreoai-rg

# Create deployment if missing
az cognitiveservices account deployment create \
  --name choreoai-openai \
  --resource-group choreoai-rg \
  --deployment-name gpt-4-deployment \
  --model-name gpt-4
```

#### 3. Quota Exceeded

```
Error: Rate limit exceeded. Quota limit reached.
```

**Solution**:
- Check current quota in Azure Portal
- Request quota increase
- Implement backoff and retry logic
- Scale across multiple deployments

#### 4. Authentication Failed

```
Error: Access denied due to invalid subscription key
```

**Solution**:
```bash
# Verify API key
az cognitiveservices account keys list \
  --name choreoai-openai \
  --resource-group choreoai-rg

# Check endpoint matches key
echo $AZURE_OPENAI_ENDPOINT
```

#### 5. Network Access Denied

```
Error: Network access denied
```

**Solution**:
```bash
# Check network rules
az cognitiveservices account network-rule list \
  --name choreoai-openai \
  --resource-group choreoai-rg

# Add your IP
az cognitiveservices account network-rule add \
  --name choreoai-openai \
  --resource-group choreoai-rg \
  --ip-address your-ip-address
```

## Compliance and Security

### Certifications

Azure OpenAI Service complies with:
- SOC 2 Type 2
- ISO 27001, 27018, 27701
- HIPAA BAA
- FedRAMP Moderate
- And many more

### Data Residency

- Data is processed in the deployment region
- No data leaves the region
- Customer data is not used to train models

### Privacy

- Microsoft does not use customer data for model training
- Data is encrypted at rest and in transit
- Customer data retention can be configured

## Additional Resources

- **Azure OpenAI Documentation**: https://learn.microsoft.com/azure/ai-services/openai/
- **Quickstart Guide**: https://learn.microsoft.com/azure/ai-services/openai/quickstart
- **Model Availability**: https://learn.microsoft.com/azure/ai-services/openai/concepts/models
- **Pricing**: https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/
- **Service Limits**: https://learn.microsoft.com/azure/ai-services/openai/quotas-limits
- **Azure Portal**: https://portal.azure.com

## Next Steps

- **[OpenAI Provider](openai.md)** - Compare with standard OpenAI
- **[Claude Provider](claude.md)** - Try Anthropic's models
- **[Provider Overview](README.md)** - Compare all providers
- **[API Reference](../api/README.md)** - Learn the API

---

**Note**: Azure OpenAI integration in ChoreoAI is currently under development. This documentation will be updated once the feature is available.
