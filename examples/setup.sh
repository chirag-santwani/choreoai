#!/bin/bash

# ChoreoAI Examples - Setup Script
# This script creates a virtual environment and installs the OpenAI SDK client

set -e

echo "======================================"
echo "ChoreoAI Examples - Environment Setup"
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
VENV_DIR="venv"
if [ -d "$VENV_DIR" ]; then
    echo "⚠️  Virtual environment already exists at ./$VENV_DIR"
    read -p "Do you want to recreate it? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf "$VENV_DIR"
    else
        echo "ℹ️  Using existing virtual environment"
        source "$VENV_DIR/bin/activate"
        echo "✅ Virtual environment activated"
        exit 0
    fi
fi

echo "📦 Creating virtual environment..."
python3 -m venv "$VENV_DIR"
echo "✅ Virtual environment created at ./$VENV_DIR"
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q
echo "✅ Pip upgraded"
echo ""

# Install OpenAI SDK
echo "📥 Installing OpenAI SDK..."
pip install openai -q
echo "✅ OpenAI SDK installed"
echo ""

# Install other useful dependencies
echo "📥 Installing additional dependencies..."
pip install python-dotenv requests -q
echo "✅ Additional dependencies installed"
echo ""

# Show installed packages
echo "📋 Installed packages:"
pip list | grep -E "openai|dotenv|requests"
echo ""

echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate when you're done:"
echo "  deactivate"
echo ""
echo "Before running examples, set your OpenAI API key:"
echo "  export OPENAI_API_KEY=sk-your-key-here"
echo ""
echo "Or create a .env file with:"
echo "  OPENAI_API_KEY=sk-your-key-here"
echo "  CHOREOAI_BASE_URL=http://localhost:8000/v1"
echo ""
