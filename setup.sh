#!/bin/bash

# Multi-Agent QA AI System - AWS Bedrock Setup Script
echo "🚀 Setting up Multi-Agent QA AI System with AWS Bedrock..."

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

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "⚠️  AWS CLI is not installed. Please install AWS CLI for Bedrock access:"
    echo "   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    echo "   After installing, run: aws configure"
else
    echo "✅ AWS CLI is installed"
    
    # Check if AWS is configured
    if aws sts get-caller-identity &> /dev/null; then
        echo "✅ AWS credentials configured"
    else
        echo "⚠️  AWS credentials not configured. Run: aws configure"
    fi
fi

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
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
# AWS Bedrock Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here

# Jira Configuration
JIRA_URL=https://your-company.atlassian.net
JIRA_USER=your_email@company.com
JIRA_API_TOKEN=your_jira_api_token
STORY_KEY=your_jira_story_key

# WebdriverIO Server
SERVER_URL=http://localhost:3000

# Optional: Ollama Configuration (if running on different host/port)
# OLLAMA_BASE_URL=http://localhost:11434
EOF
    echo "✅ .env file created. Please edit it with your AWS and Jira configuration."
else
    echo "✅ .env file already exists"
fi

# Run validation script
echo ""
echo "🔍 Running AWS Bedrock validation..."
python3 validate_bedrock_setup.py

echo ""
echo "🎉 Setup complete! Next steps:"
echo ""
echo "1. Edit the .env file with your configuration:"
echo "   - AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY: Your AWS credentials"
echo "   - JIRA_URL, JIRA_USER, JIRA_API_TOKEN: Your Jira configuration"
echo "   - STORY_KEY: The Jira story key you want to test"
echo ""
echo "2. Ensure Bedrock model access:"
echo "   - Go to AWS Bedrock Console → Model Access"
echo "   - Request access to Anthropic Claude models"
echo ""
echo "3. Start the WebdriverIO server:"
echo "   npm start"
echo ""
echo "4. In another terminal, start Jupyter:"
echo "   jupyter notebook multi-agent-qa-ai-system.ipynb"
echo ""
echo "5. Run the notebook cells to execute the multi-agent workflow!"
echo ""
echo "📚 For detailed migration info, see: BEDROCK_MIGRATION.md"