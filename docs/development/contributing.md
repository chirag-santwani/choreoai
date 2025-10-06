# Contributing Guidelines

Thank you for considering contributing to ChoreoAI! This document provides guidelines and best practices for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, gender, gender identity, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

### Expected Behavior

- Be respectful and considerate in all interactions
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what's best for the project and community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, trolling, or discriminatory language
- Personal attacks or insults
- Publishing others' private information
- Other conduct that could reasonably be considered inappropriate

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/choreoai.git
cd choreoai
```

### 2. Set Up Upstream Remote

```bash
git remote add upstream https://github.com/original-org/choreoai.git
git fetch upstream
```

### 3. Create a Development Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name
```

### 4. Set Up Development Environment

Follow the [Setup Guide](./setup.md) to configure your local development environment.

## Development Workflow

### 1. Keep Your Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream main into your main
git checkout main
git merge upstream/main

# Rebase your feature branch
git checkout feature/your-feature-name
git rebase main
```

### 2. Make Your Changes

- Write clean, readable code
- Follow the coding standards
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term

# Run linting
flake8 api/app client/choreoai

# Run type checking
mypy api/app
```

### 4. Commit Your Changes

Follow the [Commit Guidelines](#commit-guidelines) below.

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

See the [Pull Request Process](#pull-request-process) below.

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

- Line length: 100 characters (not 79)
- Use 4 spaces for indentation
- Use double quotes for strings (unless single quotes avoid escaping)

### Code Formatting

Use **Black** for automatic code formatting:

```bash
# Install Black
pip install black

# Format code
black api/app client/choreoai

# Check formatting without changing files
black --check api/app
```

### Linting

Use **flake8** for linting:

```bash
# Install flake8
pip install flake8

# Run linting
flake8 api/app client/choreoai
```

Configure flake8 in `.flake8`:

```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__,venv,build,dist
ignore = E203, W503
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import Dict, Any, List, Optional

async def chat_completion(
    self,
    request: Dict[str, Any],
    stream: bool = False
) -> Dict[str, Any]:
    """Create a chat completion."""
    pass
```

### Imports Organization

Organize imports in three groups, sorted alphabetically:

```python
# Standard library imports
import json
import time
from typing import Dict, Any

# Third-party imports
from fastapi import FastAPI, HTTPException
import httpx

# Local imports
from app.adapters.base import BaseAdapter
from app.config import settings
```

Use **isort** to automatically organize imports:

```bash
pip install isort
isort api/app client/choreoai
```

### Naming Conventions

- **Variables and functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`
- **Module names**: `lowercase` or `snake_case`

```python
# Good
class ChatAdapter:
    MAX_RETRIES = 3

    def __init__(self):
        self.api_key = None

    def _convert_message(self, message):
        pass

    async def chat_completion(self, request):
        pass
```

### Documentation

#### Module Docstrings

```python
"""
app/adapters/openai_adapter.py

OpenAI API adapter implementation.

This module provides the adapter for integrating with OpenAI's API,
converting between OpenAI format and ChoreoAI's unified format.
"""
```

#### Class Docstrings

```python
class OpenAIAdapter(BaseAdapter):
    """
    Adapter for OpenAI API integration.

    This adapter handles communication with OpenAI's API, including
    chat completions, streaming, and embeddings.

    Attributes:
        api_key: OpenAI API key
        client: Async OpenAI client instance
    """
```

#### Function Docstrings

Use Google-style docstrings:

```python
async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a chat completion using OpenAI API.

    Args:
        request: Request parameters in OpenAI format containing:
            - model: Model identifier
            - messages: List of message dicts
            - temperature: Sampling temperature (0-2)
            - max_tokens: Maximum tokens to generate

    Returns:
        Dict containing the completion response with keys:
            - id: Completion ID
            - choices: List of completion choices
            - usage: Token usage information

    Raises:
        Exception: If the API request fails

    Example:
        >>> request = {
        ...     "model": "gpt-4",
        ...     "messages": [{"role": "user", "content": "Hello"}]
        ... }
        >>> response = await adapter.chat_completion(request)
    """
```

### Error Handling

Always provide informative error messages:

```python
# Good
try:
    response = await self.client.chat.completions.create(**request)
except httpx.HTTPError as e:
    raise Exception(f"OpenAI API request failed: {str(e)}")
except Exception as e:
    raise Exception(f"Unexpected error in chat completion: {str(e)}")

# Bad
try:
    response = await self.client.chat.completions.create(**request)
except Exception:
    raise
```

### Logging

Use Python's `logging` module:

```python
import logging

logger = logging.getLogger(__name__)

async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
    logger.info(f"Creating chat completion for model: {request.get('model')}")
    try:
        response = await self.client.create(**request)
        logger.debug(f"Received response with ID: {response.id}")
        return response
    except Exception as e:
        logger.error(f"Chat completion failed: {str(e)}")
        raise
```

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates

### Scopes

- **api**: API service changes
- **client**: Python client changes
- **adapters**: Adapter implementations
- **docs**: Documentation
- **infra**: Infrastructure/deployment
- **examples**: Example scripts

### Examples

```
feat(adapters): add support for Gemini API

Implement GeminiAdapter with chat completion and streaming support.
Includes message format conversion and response normalization.

Closes #123
```

```
fix(api): handle rate limit errors gracefully

Add retry logic with exponential backoff for rate limit errors.
Update error messages to be more informative.

Fixes #456
```

```
docs(development): add testing guide

Create comprehensive testing documentation including:
- Unit testing examples
- Integration testing patterns
- Coverage requirements
```

### Commit Best Practices

- Write clear, descriptive commit messages
- Keep commits focused on a single change
- Reference issues and PRs where appropriate
- Use present tense ("add feature" not "added feature")
- Start with a lowercase letter after the colon
- Keep subject line under 72 characters

## Pull Request Process

### Before Submitting

- [ ] Code follows the project's style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages follow guidelines
- [ ] Branch is up to date with main

### PR Title Format

Use the same format as commit messages:

```
feat(adapters): add Gemini API support
fix(client): handle connection timeout errors
docs(api): update authentication documentation
```

### PR Description Template

```markdown
## Description
Brief description of the changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to not work as expected)
- [ ] Documentation update

## Testing
Describe the tests you ran and how to reproduce them.

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally

## Screenshots (if applicable)

## Related Issues
Closes #123
Related to #456
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Code Review**: At least one maintainer reviews the code
3. **Discussion**: Address feedback and make requested changes
4. **Approval**: Maintainer approves the PR
5. **Merge**: Maintainer merges the PR

### Addressing Feedback

```bash
# Make requested changes
git add .
git commit -m "address review feedback"
git push origin feature/your-feature-name

# If requested to squash commits
git rebase -i main
# Follow interactive rebase instructions
git push --force-with-lease origin feature/your-feature-name
```

## Testing Requirements

### Coverage Requirements

- Overall coverage: 80%+
- New code: 90%+
- Critical paths: 95%+

### Required Tests

- **Unit tests** for all new functions and methods
- **Integration tests** for new API endpoints or flows
- **Edge case tests** for error conditions
- **Regression tests** for bug fixes

### Running Tests Locally

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_adapters.py

# With coverage
pytest --cov=app --cov-report=html

# Integration tests only
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

See the [Testing Guide](./testing.md) for detailed testing practices.

## Documentation

### When to Update Documentation

- Adding new features
- Changing existing functionality
- Fixing bugs that affect usage
- Adding new configuration options
- Changing API endpoints

### Documentation Locations

- **API docs**: `/docs/api/`
- **Client docs**: `/docs/client/`
- **Development docs**: `/docs/development/`
- **Deployment docs**: `/docs/deployment/`
- **Code comments**: Inline in source files

### Documentation Style

- Use clear, concise language
- Include code examples
- Provide context and explanations
- Keep formatting consistent
- Use proper Markdown syntax

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Configure '...'
2. Call endpoint '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment**
- OS: [e.g., macOS 13.0]
- Python version: [e.g., 3.12]
- ChoreoAI version: [e.g., 1.0.0]

**Additional context**
Any other relevant information.

**Logs**
```
Paste relevant logs here
```
```

### Feature Requests

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other relevant information.
```

### Questions

For questions:
1. Check existing documentation
2. Search existing issues
3. Ask in discussions
4. Create an issue with the "question" label

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

## Getting Help

- **Documentation**: Check the [development docs](./README.md)
- **Discussions**: Use GitHub Discussions
- **Issues**: Search existing issues
- **Maintainers**: Tag maintainers in issues/PRs

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## Thank You!

Your contributions make ChoreoAI better for everyone. We appreciate your time and effort!
