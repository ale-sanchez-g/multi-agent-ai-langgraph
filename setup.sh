#!/bin/bash

# Multi-Agent QA AI System - Quick Start Script
echo "🚀 Setting up Multi-Agent QA AI System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if Python 3.10+ is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)"; then
    echo "❌ Python 3.10+ is required. Current version: $python_version"
    echo "Please install Python 3.10+ and try again."
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

node_version=$(node --version)
echo "✅ Node.js version check passed: $node_version"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo "✅ Python dependencies installed successfully"

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi

echo "✅ Node.js dependencies installed successfully"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama is not installed. Please install Ollama from https://ollama.ai"
    echo "   After installing Ollama, run: ollama pull nomic-embed-text:v1.5"
else
    echo "✅ Ollama is installed"
    
    # Pull required model
    echo "📥 Pulling required Ollama model..."
    ollama pull nomic-embed-text:v1.5
    
    if [ $? -eq 0 ]; then
        echo "✅ Ollama model pulled successfully"
    else
        echo "⚠️  Failed to pull Ollama model. You may need to do this manually:"
        echo "   ollama pull nomic-embed-text:v1.5"
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your API keys and configuration."
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete! Next steps:"
echo ""
echo "1. Edit the .env file with your API keys:"
echo "   - OPENAI_API_KEY: Get from https://platform.openai.com/api-keys"
echo "   - JIRA_URL, JIRA_USER, JIRA_API_TOKEN: Your Jira configuration"
echo "   - STORY_KEY: The Jira story key you want to test"
echo ""
echo "2. Start the WebdriverIO server:"
echo "   npm start"
echo ""
echo "3. In another terminal, start Jupyter:"
echo "   jupyter notebook multi-agent-qa-ai-system.ipynb"
echo ""
echo "4. Run the notebook cells to execute the multi-agent workflow!"
echo ""
echo "For troubleshooting, check the README.md file."