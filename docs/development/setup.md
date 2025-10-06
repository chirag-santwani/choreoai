# Local Development Setup

This guide will walk you through setting up ChoreoAI for local development.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12 or higher**
  ```bash
  python --version  # Should be 3.12+
  ```

- **pip** (Python package installer)
  ```bash
  pip --version
  ```

- **Git**
  ```bash
  git --version
  ```

- **Docker** (optional, for containerized development)
  ```bash
  docker --version
  ```

- **Docker Compose** (optional, for running the full stack)
  ```bash
  docker-compose --version
  ```

## Clone the Repository

```bash
git clone https://github.com/your-org/choreoai.git
cd choreoai
```

## API Server Setup

### 1. Navigate to the API directory

```bash
cd api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
# Server Configuration
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=INFO
ENVIRONMENT=development

# CORS - Allow all origins in development
ALLOWED_ORIGINS=*

# Provider API Keys
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GEMINI_API_KEY=your-gemini-key-here
GROK_API_KEY=xai-your-grok-key-here

# Azure OpenAI (optional)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your-azure-key-here

# AWS Bedrock (optional)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
```

**Note:** You don't need all API keys. ChoreoAI will work with whichever providers you configure.

### 6. Run the API server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 7. Verify the server is running

Open your browser and navigate to:
- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Python Client Setup

### 1. Navigate to the client directory

```bash
cd ../client
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install the client in development mode

```bash
pip install -e .
```

This installs the client in editable mode, so changes you make to the code are immediately reflected.

### 5. Install development dependencies

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

## Running Examples

### 1. Navigate to the examples directory

```bash
cd ../examples
```

### 2. Set up the examples environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install openai anthropic python-dotenv
```

### 3. Configure environment variables

Create a `.env` file in the examples directory:

```bash
# API Keys for testing
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GEMINI_API_KEY=your-gemini-key-here
```

### 4. Run example scripts

Make sure the API server is running, then:

```bash
# Basic usage example
python basic_usage.py

# List available models
python list_models.py

# Function calling example
python function_calling.py

# Streaming example (in basic_usage.py)
python basic_usage.py

# Cost optimization example
python cost_optimization.py

# A/B testing example
python ab_testing.py

# Embeddings and RAG example
python embeddings_rag.py
```

## Docker Development Setup

If you prefer to use Docker for development:

### 1. Build and run with Docker Compose

```bash
# From the project root directory
docker-compose up --build
```

This will:
- Build the API service
- Start the API server on port 8000
- Mount your local code as volumes for live reloading

### 2. Access the containerized API

The API will be available at `http://localhost:8000`

### 3. Stop the services

```bash
docker-compose down
```

## Development Tools

### Code Formatting

We use **Black** for code formatting:

```bash
pip install black
black .
```

### Linting

We use **flake8** for linting:

```bash
pip install flake8
flake8 api/app client/choreoai
```

### Type Checking

We use **mypy** for type checking:

```bash
pip install mypy
mypy api/app
```

### Auto-formatting on Save

Configure your IDE to auto-format on save:

**VS Code:** Install the Python extension and add to `settings.json`:
```json
{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true
}
```

## Testing Your Setup

### 1. Test the API directly

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Test with OpenAI SDK

Create a test script `test_setup.py`:

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-openai-key",
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

Run it:
```bash
python test_setup.py
```

### 3. Run the test suite

```bash
# API tests
cd api
pytest tests/

# Client tests
cd ../client
pytest tests/
```

## Common Issues and Solutions

### Issue: Port 8000 already in use

**Solution:** Either stop the process using port 8000 or run on a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Issue: Module not found errors

**Solution:** Make sure you're in the correct directory and the virtual environment is activated:
```bash
which python  # Should point to your venv
pip list      # Should show installed packages
```

### Issue: API key errors

**Solution:** Verify your `.env` file is in the correct location and properly formatted:
```bash
cat api/.env  # Check the file exists and has correct keys
```

### Issue: Import errors in development mode

**Solution:** Reinstall the package in editable mode:
```bash
pip install -e .
```

## Hot Reloading

### API Server

The `--reload` flag enables hot reloading for the API server. Changes to Python files will automatically restart the server.

### Client Development

When installed with `pip install -e .`, changes to the client code are immediately available without reinstallation.

## IDE Setup

### VS Code

Recommended extensions:
- Python
- Pylance
- Python Test Explorer
- Docker
- YAML

### PyCharm

1. Open the project root directory
2. Configure Python interpreters for each module (api, client, examples)
3. Enable pytest as the default test runner
4. Configure code style to use Black

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | No | 8000 | API server port |
| `HOST` | No | 0.0.0.0 | API server host |
| `LOG_LEVEL` | No | INFO | Logging level |
| `ENVIRONMENT` | No | development | Environment name |
| `ALLOWED_ORIGINS` | No | * | CORS allowed origins |
| `OPENAI_API_KEY` | Optional | None | OpenAI API key |
| `ANTHROPIC_API_KEY` | Optional | None | Anthropic API key |
| `GEMINI_API_KEY` | Optional | None | Google Gemini API key |
| `GROK_API_KEY` | Optional | None | xAI Grok API key |
| `AZURE_OPENAI_ENDPOINT` | Optional | None | Azure OpenAI endpoint |
| `AZURE_OPENAI_API_KEY` | Optional | None | Azure OpenAI key |
| `AWS_REGION` | No | us-east-1 | AWS region for Bedrock |
| `AWS_ACCESS_KEY_ID` | Optional | None | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Optional | None | AWS secret key |

## Next Steps

Now that your development environment is set up:

1. Review the [Project Structure](./project-structure.md) to understand the codebase
2. Check out the [Testing Guide](./testing.md) to learn about testing
3. Read the [Contributing Guidelines](./contributing.md) before making changes
4. Try [Adding a New Provider](./adding-providers.md) to understand the adapter pattern
