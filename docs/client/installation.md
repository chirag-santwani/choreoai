# Installation

Install the ChoreoAI Python client to start building applications.

## Requirements

- **Python**: 3.9 or higher
- **pip**: Python package manager (included with Python)
- **Operating System**: Windows, macOS, or Linux

## Install with pip

```bash
pip install choreoai
```

### Verify Installation

```bash
python -c "import choreoai; print(choreoai.__version__)"
```

Expected output:
```
0.1.0
```

## Virtual Environment (Recommended)

Using a virtual environment keeps your project dependencies isolated.

### Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Install in Virtual Environment

```bash
pip install choreoai
```

### Deactivate Virtual Environment

```bash
deactivate
```

## Install from Source

For development or to use the latest unreleased features:

```bash
# Clone repository
git clone https://github.com/choreoai/choreoai.git
cd choreoai

# Install in editable mode
pip install -e .
```

## Install with Optional Dependencies

### Development Dependencies

```bash
pip install choreoai[dev]
```

Includes:
- pytest (testing)
- black (code formatting)
- mypy (type checking)
- ruff (linting)

### Async Support

Async support is included by default. No additional dependencies required.

## Upgrading

### Upgrade to Latest Version

```bash
pip install --upgrade choreoai
```

### Upgrade to Specific Version

```bash
pip install choreoai==0.2.0
```

### Check Current Version

```bash
pip show choreoai
```

## Uninstall

```bash
pip uninstall choreoai
```

## Common Installation Issues

### Issue: `pip: command not found`

**Solution:** Install pip or use `python -m pip`:

```bash
# macOS/Linux
python3 -m pip install choreoai

# Windows
python -m pip install choreoai
```

### Issue: Permission Denied

**Solution:** Install in user directory:

```bash
pip install --user choreoai
```

Or use a virtual environment (recommended).

### Issue: Python Version Too Old

**Solution:** Upgrade Python to 3.9 or higher:

**macOS:**
```bash
brew install python@3.9
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.9
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/)

### Issue: SSL Certificate Error

**Solution:** Upgrade pip and certifi:

```bash
pip install --upgrade pip certifi
```

## Dependencies

ChoreoAI automatically installs these dependencies:

- `httpx` - HTTP client
- `pydantic` - Data validation
- `typing-extensions` - Type hints (Python <3.10)

## Platform-Specific Notes

### macOS

Default Python on macOS may be outdated. Use Homebrew:

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.9

# Install ChoreoAI
pip3 install choreoai
```

### Windows

Use PowerShell or Command Prompt:

```powershell
# Check Python version
python --version

# Install ChoreoAI
python -m pip install choreoai
```

### Linux

Most distributions come with Python. Ensure pip is installed:

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install python3-pip

# CentOS/RHEL
sudo yum install python3-pip

# Install ChoreoAI
pip3 install choreoai
```

## Docker

Use ChoreoAI in Docker containers:

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install ChoreoAI
RUN pip install choreoai

# Copy your application
COPY . .

CMD ["python", "app.py"]
```

### Build and Run

```bash
docker build -t my-choreoai-app .
docker run my-choreoai-app
```

## Verify Installation

Create a test script `test_install.py`:

```python
from choreoai import ChoreoAI

# This should not raise any errors
client = ChoreoAI(api_key="test-key")
print("ChoreoAI installed successfully!")
```

Run the test:

```bash
python test_install.py
```

Expected output:
```
ChoreoAI installed successfully!
```

## IDE Setup

### VS Code

1. Install Python extension
2. Select Python interpreter with ChoreoAI installed
3. Create `.env` file:

```bash
CHOREOAI_API_KEY=your-api-key
```

4. Install python-dotenv:

```bash
pip install python-dotenv
```

### PyCharm

1. Create new Python project
2. Open Settings → Project → Python Interpreter
3. Click "+" and search for "choreoai"
4. Install package

### Jupyter Notebook

```bash
# Install Jupyter
pip install jupyter

# Install ChoreoAI
pip install choreoai

# Start Jupyter
jupyter notebook
```

In notebook:
```python
from choreoai import ChoreoAI

client = ChoreoAI(api_key="your-api-key")
# Use client...
```

## Environment Configuration

### API Key Setup

Create a `.env` file in your project root:

```bash
CHOREOAI_API_KEY=your-api-key
CHOREOAI_BASE_URL=http://localhost:8000  # Optional
```

### Load Environment Variables

```python
from dotenv import load_dotenv
from choreoai import ChoreoAI

load_dotenv()
client = ChoreoAI()  # Reads from environment
```

Install python-dotenv:
```bash
pip install python-dotenv
```

## Requirements File

For reproducible installations, use `requirements.txt`:

```txt
choreoai>=0.1.0
python-dotenv>=1.0.0
```

Install from requirements file:
```bash
pip install -r requirements.txt
```

## Next Steps

Now that you have ChoreoAI installed:

- **[Quick Start](quickstart.md)** - Make your first API call
- **[Chat Guide](chat.md)** - Learn about chat completions
- **[Authentication](../api/authentication.md)** - Configure API keys
