# Embeddings

Generate vector embeddings for text inputs, useful for semantic search, clustering, and retrieval-augmented generation (RAG).

## Endpoint

```
POST /v1/embeddings
```

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Embedding model identifier |
| `input` | string/array | Yes | Text(s) to embed. Can be a string or array of strings |
| `encoding_format` | string | No | Format for embeddings: "float" or "base64". Default: "float" |

## Request Example

### Single Input

```bash
curl -X POST http://localhost:8000/v1/embeddings \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-ada-002",
    "input": "The quick brown fox jumps over the lazy dog"
  }'
```

### Multiple Inputs

```bash
curl -X POST http://localhost:8000/v1/embeddings \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-ada-002",
    "input": [
      "First document to embed",
      "Second document to embed",
      "Third document to embed"
    ]
  }'
```

## Response Format

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "index": 0,
      "embedding": [
        -0.006929283,
        -0.005336422,
        0.014660476,
        ...
        -0.009327292
      ]
    }
  ],
  "model": "text-embedding-ada-002",
  "usage": {
    "prompt_tokens": 8,
    "total_tokens": 8
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `object` | string | Always "list" |
| `data` | array | Array of embedding objects |
| `data[].object` | string | Always "embedding" |
| `data[].index` | integer | Index of the input text |
| `data[].embedding` | array | Vector embedding (array of floats) |
| `model` | string | Model used for embedding |
| `usage` | object | Token usage information |
| `usage.prompt_tokens` | integer | Number of tokens processed |
| `usage.total_tokens` | integer | Total tokens used |

## Supported Models

### OpenAI Embedding Models

| Model | Dimensions | Max Tokens |
|-------|------------|------------|
| `text-embedding-ada-002` | 1536 | 8191 |
| `text-embedding-3-small` | 1536 | 8191 |
| `text-embedding-3-large` | 3072 | 8191 |

### Other Providers

!!! note
    Embedding support varies by provider. Check provider documentation for availability.

## Use Cases

### 1. Semantic Search

Find similar documents based on meaning, not just keywords:

```python
from choreoai import ChoreoAI
import numpy as np

client = ChoreoAI(api_key="your-api-key")

# Embed documents
documents = [
    "Python is a programming language",
    "JavaScript is used for web development",
    "Machine learning models require training data"
]

doc_embeddings = []
for doc in documents:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=doc
    )
    doc_embeddings.append(response.data[0].embedding)

# Embed query
query = "Tell me about Python"
query_response = client.embeddings.create(
    model="text-embedding-ada-002",
    input=query
)
query_embedding = query_response.data[0].embedding

# Calculate cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

similarities = [
    cosine_similarity(query_embedding, doc_emb)
    for doc_emb in doc_embeddings
]

# Most similar document
most_similar_idx = np.argmax(similarities)
print(f"Most similar: {documents[most_similar_idx]}")
```

### 2. Retrieval-Augmented Generation (RAG)

Retrieve relevant context for LLM prompts:

```python
# Step 1: Embed and store documents
knowledge_base = [
    "ChoreoAI supports OpenAI, Claude, and Gemini",
    "Use the chat completions endpoint for conversations",
    "Streaming is enabled with stream=true parameter"
]

# Embed knowledge base
kb_embeddings = []
for doc in knowledge_base:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=doc
    )
    kb_embeddings.append(response.data[0].embedding)

# Step 2: Find relevant context for user query
user_query = "How do I enable streaming?"

query_response = client.embeddings.create(
    model="text-embedding-ada-002",
    input=user_query
)
query_emb = query_response.data[0].embedding

# Find most similar document
similarities = [
    cosine_similarity(query_emb, kb_emb)
    for kb_emb in kb_embeddings
]
most_relevant_idx = np.argmax(similarities)
context = knowledge_base[most_relevant_idx]

# Step 3: Use context in chat completion
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": f"Use this context: {context}"},
        {"role": "user", "content": user_query}
    ]
)
print(response.choices[0].message.content)
```

### 3. Text Clustering

Group similar texts together:

```python
from sklearn.cluster import KMeans

# Embed multiple documents
texts = [
    "Python programming tutorial",
    "JavaScript web development",
    "Machine learning basics",
    "Python data analysis",
    "React framework guide",
    "Deep learning introduction"
]

embeddings = []
for text in texts:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    embeddings.append(response.data[0].embedding)

# Cluster into 2 groups
embeddings_array = np.array(embeddings)
kmeans = KMeans(n_clusters=2, random_state=42)
clusters = kmeans.fit_predict(embeddings_array)

# Print clusters
for i, text in enumerate(texts):
    print(f"Cluster {clusters[i]}: {text}")
```

## Code Examples

### Python (ChoreoAI Client)

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")

# Single text
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Hello, world!"
)

embedding = response.data[0].embedding
print(f"Embedding dimensions: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
```

### Python (OpenAI Client)

```python
import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = "your-api-key"

response = openai.Embedding.create(
    model="text-embedding-ada-002",
    input="Hello, world!"
)

embedding = response['data'][0]['embedding']
print(f"Embedding: {embedding[:5]}...")
```

### JavaScript/TypeScript

```javascript
const response = await fetch('http://localhost:8000/v1/embeddings', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-api-key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'text-embedding-ada-002',
    input: 'Hello, world!'
  })
});

const data = await response.json();
const embedding = data.data[0].embedding;
console.log(`Dimensions: ${embedding.length}`);
```

### Batch Processing

```python
# Process multiple texts efficiently
texts = ["Text 1", "Text 2", "Text 3", ...]

# Send in batches
batch_size = 100
all_embeddings = []

for i in range(0, len(texts), batch_size):
    batch = texts[i:i + batch_size]
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=batch
    )
    all_embeddings.extend([item.embedding for item in response.data])

print(f"Processed {len(all_embeddings)} embeddings")
```

## Error Responses

### Invalid Model

```json
{
  "error": {
    "message": "Model 'invalid-embedding-model' not found",
    "type": "invalid_request_error",
    "code": "model_not_found"
  }
}
```

### Input Too Long

```json
{
  "error": {
    "message": "Input text exceeds maximum token limit of 8191",
    "type": "invalid_request_error",
    "code": "context_length_exceeded"
  }
}
```

### Missing Input

```json
{
  "error": {
    "message": "Missing required parameter: input",
    "type": "invalid_request_error",
    "code": "missing_parameter"
  }
}
```

## Best Practices

### 1. Choose the Right Model

- **text-embedding-ada-002**: Good balance of cost and performance
- **text-embedding-3-small**: Lower cost, slightly lower quality
- **text-embedding-3-large**: Highest quality, higher dimensions

### 2. Normalize Input Text

Clean and normalize text before embedding:

```python
def normalize_text(text):
    # Remove extra whitespace
    text = " ".join(text.split())
    # Lowercase for consistency
    text = text.lower()
    return text

input_text = normalize_text("  Hello,   World!  ")
```

### 3. Batch Requests

Process multiple texts in one request for efficiency:

```python
# Good: Batch processing
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input=["text1", "text2", "text3"]
)

# Less efficient: Individual requests
for text in texts:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
```

### 4. Cache Embeddings

Store embeddings to avoid recomputing:

```python
import pickle

# Compute and save
embeddings = {...}  # Your embeddings dict
with open('embeddings.pkl', 'wb') as f:
    pickle.dump(embeddings, f)

# Load cached embeddings
with open('embeddings.pkl', 'rb') as f:
    embeddings = pickle.load(f)
```

### 5. Use Appropriate Similarity Metrics

- **Cosine similarity**: Most common for text embeddings
- **Euclidean distance**: Alternative for some use cases
- **Dot product**: Faster, assumes normalized vectors

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euclidean_distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))
```

## Next Steps

- **[Chat Completions](chat-completions.md)** - Use embeddings for RAG
- **[Models](models.md)** - Explore embedding models
- **[Error Handling](error-handling.md)** - Handle embedding errors
