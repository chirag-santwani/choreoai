# ChoreoAI Python Client

Official Python client library for ChoreoAI.

## Installation

```bash
pip install choreoai
```

## Usage

```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```
