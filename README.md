# Multi-Agent QA AI System with LangGraph - AWS Bedrock Implementation

This project is a **multi-agent AI system** built on top of LangGraph and LangChain, specifically designed for **automated QA testing workflows**. The system integrates with Jira for requirements gathering, generates BDD test cases, and performs automated web testing using a multi-agent architecture.

**🚀 Recently migrated from OpenAI to AWS Bedrock for enhanced cost-efficiency and enterprise-grade features!**

## Features

- **Jira Integration:** Fetches user stories and requirements directly from Jira using REST API
- **BDD Test Case Generation:** Automatically generates Behavior-Driven Development test cases in Gherkin format using AWS Bedrock Claude models
- **Vector Database Storage:** Uses Chroma with Ollama embeddings for efficient document retrieval (RAG)
- **Web Test Automation:** Performs automated browser testing using WebdriverIO integration
- **Multi-Agent Orchestration:** QA Manager agent coordinates two specialized agents:
  - **QA Agent:** Generates BDD test cases from requirements using Claude 3 Sonnet
  - **QA Automation Agent:** Executes automated web tests
- **Supervisor Architecture:** Uses LangGraph supervisor for intelligent task routing and coordination
- **AWS Bedrock Integration:** Enterprise-grade LLM capabilities with enhanced security and cost controls

## Architecture

The system follows a multi-agent architecture with clear separation of concerns:

```
QA Manager Agent (Supervisor)
├── QA Agent (BDD Test Case Generation)
│   ├── Jira API Integration
│   ├── Text Chunking & Embedding
│   ├── Vector Database (Chroma)
│   └── LLM-powered Test Case Generation
└── QA Automation Agent (Web Testing)
    ├── WebdriverIO Server Integration
    ├── Browser Automation Tools
    └── Test Execution & Reporting
```

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.10+** - Required for LangChain and LangGraph
- **Node.js 16+** - Required for WebdriverIO server
- **Chrome Browser** - Required for web automation
- **Ollama** - Required for local embeddings (install from [ollama.ai](https://ollama.ai))
- **AWS Account** - Required for Bedrock access with Claude models enabled

## Quick Start

For a fast setup, use the provided setup script:

```bash
# Clone and enter the repository
git clone https://github.com/siri100/multi-agent-ai-langgraph.git
cd multi-agent-ai-langgraph

# Run the automated setup script
./setup.sh

# Follow the prompts and edit .env file with your API keys
# Then start the WebdriverIO server and Jupyter notebook
```

## Manual Installation

### 1. Clone the Repository
```bash
git clone https://github.com/siri100/multi-agent-ai-langgraph.git
cd multi-agent-ai-langgraph
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies
```bash
npm install express webdriverio
```

### 4. Install and Setup Ollama
```bash
# Install Ollama (visit https://ollama.ai for your OS)
# Pull the required embedding model
ollama pull nomic-embed-text:v1.5
```

### 5. Environment Configuration
Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
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
```

**How to get AWS Bedrock access:**
1. Create an AWS account and set up IAM user with Bedrock permissions
2. Go to AWS Bedrock Console → Model Access
3. Request access to Anthropic Claude models
4. Generate AWS access keys in IAM console

**How to get Jira API Token:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a label and copy the generated token

### 6. Validate Your Setup
Run the validation script to ensure everything is configured correctly:

```bash
python3 validate_setup.py
```

This script will check:
- Python version and dependencies
- Environment variables configuration
- Ollama installation and model availability
- WebdriverIO server dependencies

## Setup and Usage

### 1. Start the WebdriverIO Server
In a separate terminal, start the browser automation server:
```bash
node server.js
```
The server will run on `http://localhost:3000`

### 2. Open the Jupyter Notebook
```bash
jupyter notebook multi-agent-qa-ai-system.ipynb
```
Or open it in VS Code with Jupyter extension installed.

### 3. Execute the Notebook Cells
Run the cells in sequence:

1. **Import Libraries & Setup** - Loads required dependencies
2. **Jira Integration** - Fetches story description from Jira
3. **Text Processing** - Chunks and embeds the content
4. **Vector Database** - Stores chunks in Chroma for retrieval
5. **LLM Setup** - Initializes AWS Bedrock Claude model
6. **QA Agent** - Creates BDD test case generation agent
7. **Automation Agent** - Creates web testing automation agent
8. **Manager Agent** - Creates supervisor to orchestrate both agents
9. **Execution** - Runs the complete workflow

## Workflow Description

### Complete Process Flow:

1. **Requirements Gathering**: System fetches user story from Jira using the configured story key
2. **Text Processing**: Story content is chunked and embedded using Ollama's nomic-embed-text model
3. **Vector Storage**: Chunks are stored in Chroma vector database for efficient retrieval
4. **BDD Generation**: QA Agent generates BDD test cases in Gherkin format using RAG and LLM
5. **Test Automation**: QA Automation Agent executes the generated test cases using browser automation
6. **Coordination**: QA Manager Agent orchestrates the entire workflow between agents

### Agents Detailed:

#### QA Agent (BDD Test Case Generator)
- **Purpose**: Generate BDD test cases from Jira requirements
- **Tools**: 
  - `extract_and_generate_bdd_test_cases`: RAG-based tool for test case generation
- **Features**:
  - Chain-of-thought prompting
  - Few-shot examples
  - ReAct methodology for structured thinking
  - Gherkin syntax compliance

#### QA Automation Agent (Web Tester)
- **Purpose**: Execute automated web tests based on generated BDD scenarios
- **Tools**:
  - `open_browser`: Start Chrome browser session
  - `navigate_to_url`: Navigate to specified URLs
  - `click_action`: Click web elements
  - `set_value_action`: Fill form fields
  - `get_page_source`: Retrieve page HTML
  - `wait_for_displayed/enabled`: Wait for element states
  - `scroll_to_element`: Scroll to elements
  - `get_text`: Extract element text
  - `reset_browser/close_browser`: Manage browser sessions

#### QA Manager Agent (Supervisor)
- **Purpose**: Coordinate task assignment between QA and automation agents
- **Features**:
  - Sequential task execution (no parallel calls)
  - Intelligent agent routing
  - Full history tracking
  - Handoff back messages for communication


## Example Output

### Generated BDD Test Case Example:
```gherkin
Feature: User Authentication
  Scenario: Successful user login with valid credentials
    Given the user is on the login page
    When the user enters valid username and password
    And the user clicks the login button
    Then the user should be redirected to the dashboard
    And the user should see a welcome message
```

### Automation Agent Execution Report:
```
Actions Performed:
1. ✅ Browser opened successfully
2. ✅ Navigated to login page (https://example.com/login)
3. ✅ Entered username in field #username
4. ✅ Entered password in field #password
5. ✅ Clicked login button #login-btn
6. ✅ Verified redirect to dashboard (/dashboard)
7. ❌ Welcome message not found - BUG DETECTED

Test Result: FAILED
Issue: Welcome message element not visible on dashboard
```

## Troubleshooting

### Common Issues:

1. **Ollama Connection Error**
   ```bash
   # Ensure Ollama is running
   ollama serve
   # Pull required model
   ollama pull nomic-embed-text:v1.5
   ```

2. **WebdriverIO Server Not Starting**
   ```bash
   # Check if port 3000 is available
   lsof -i :3000
   # Kill existing process if needed
   kill -9 <PID>
   ```

3. **Chrome Browser Issues**
   ```bash
   # Update Chrome to latest version
   # Ensure chromedriver is compatible
   npm install -g chromedriver
   ```

4. **Jira API Authentication**
   - Verify API token is correct
   - Check if user has permission to access the story
   - Ensure JIRA_URL format is correct (https://domain.atlassian.net)

5. **OpenAI API Errors**
   - **DEPRECATED**: This project now uses AWS Bedrock instead of OpenAI
   - For Bedrock issues: Verify AWS credentials and model access
   - Check AWS region supports Bedrock service
   - Ensure Claude model access is granted in Bedrock console

## Project Structure

```
multi-agent-ai-langgraph/
├── multi-agent-qa-ai-system.ipynb    # Main Jupyter notebook
├── server.js                         # WebdriverIO automation server
├── test_case_db/                     # Chroma vector database storage
│   ├── chroma.sqlite3               # SQLite database file
│   └── collections/                 # Vector embeddings storage
├── README.md                        # Project documentation
└── .env                            # Environment variables (create this)
```

## Customization Options

### Adding New Tools to Agents

**For QA Agent:**
```python
@tool
def custom_test_validator(test_case: str) -> str:
    """Validate test case completeness and quality."""
    # Your custom validation logic
    return validation_result

# Add to QA agent tools
qa_agent = create_react_agent(
    model=llm,
    tools=[extract_and_generate_bdd_test_cases, custom_test_validator],
    # ... rest of configuration
)
```

**For Automation Agent:**
```python
@tool
def take_screenshot(filename: str) -> str:
    """Take screenshot during test execution."""
    # Screenshot logic using WebdriverIO
    return screenshot_result

# Add to automation agent tools
```

### Modifying Prompts

Update agent prompts to change behavior:
```python
qa_agent = create_react_agent(
    model=llm,
    tools=[...],
    prompt="Custom prompt for specialized test case generation...",
    name="qa_agent",
)
```

### Adding New Agent Types

Create additional specialized agents:
```python
# Security testing agent
security_agent = create_react_agent(
    model=llm,
    tools=[security_scan_tool, vulnerability_check_tool],
    prompt="You are a security testing specialist...",
    name="security_agent",
)

# Add to supervisor
qa_manager_agent = create_supervisor(
    model=llm,
    agents=[qa_agent, qa_automation_agent, security_agent],
    # ... configuration
)
```

### Integration with Other Systems

- **Jenkins/CI Integration**: Add webhook endpoints to trigger tests
- **Slack Notifications**: Integrate Slack API for test result notifications
- **Database Integration**: Store test results in external databases
- **Custom Reporting**: Generate detailed test reports in various formats

## Contributing

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Changes and Test**
4. **Submit a Pull Request**

### Development Guidelines:
- Follow Python PEP 8 style guide
- Add docstrings to all functions
- Include unit tests for new features
- Update README.md for significant changes

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review LangGraph and LangChain documentation

## Quick Reference

### File Structure Overview
```
multi-agent-ai-langgraph/
├── 📓 multi-agent-qa-ai-system.ipynb    # Main workflow notebook
├── 🌐 server.js                         # WebdriverIO automation server
├── ⚡ setup.sh                          # Automated setup script
├── 🔍 validate_setup.py                 # Setup validation script
├── 📋 requirements.txt                  # Python dependencies
├── 📦 package.json                      # Node.js dependencies
├── 🔧 .env.example                      # Environment template
├── 📚 README.md                         # This documentation
├── 🗃️ test_case_db/                     # Vector database storage
└── 🚫 .gitignore                        # Git ignore rules
```

### Essential Commands
```bash
# Initial setup
./setup.sh                           # Automated setup
python3 validate_setup.py           # Validate configuration

# Running the system
npm start                            # Start WebdriverIO server
jupyter notebook multi-agent-qa-ai-system.ipynb  # Open notebook

# Ollama commands
ollama serve                         # Start Ollama service
ollama pull nomic-embed-text:v1.5   # Download embedding model

# AWS CLI setup
aws configure                        # Configure AWS credentials
aws bedrock list-foundation-models  # Check available models
```

### Environment Variables Quick Reference
```env
# AWS Bedrock Configuration
AWS_REGION=us-east-1                # AWS region for Bedrock
AWS_ACCESS_KEY_ID=AKIA...          # AWS access key
AWS_SECRET_ACCESS_KEY=...          # AWS secret key

# Jira Configuration  
JIRA_URL=https://company.atlassian.net  # Jira instance URL
JIRA_USER=user@company.com          # Jira username/email
JIRA_API_TOKEN=...                  # Jira API token
STORY_KEY=PROJ-123                  # Jira story key to process
```

### Agent Workflow Summary
1. **Jira Integration** → Fetch user story requirements
2. **Text Processing** → Chunk and embed content using Ollama
3. **Vector Storage** → Store in Chroma database for RAG
4. **QA Agent** → Generate BDD test cases using Claude 3 Sonnet
5. **Automation Agent** → Execute tests via WebdriverIO
6. **Manager Agent** → Orchestrate and coordinate workflow

### Key Technologies
- **🤖 LangGraph**: Multi-agent orchestration framework
- **🔗 LangChain**: LLM application framework  
- **☁️ AWS Bedrock**: Enterprise LLM service with Claude models
- **📊 Ollama**: Local embedding model server
- **🗄️ Chroma**: Vector database for RAG
- **🌐 WebdriverIO**: Browser automation framework
- **📋 Jira API**: Requirements and story management

### Migration Benefits
- **💰 Cost Savings**: ~70% reduction in LLM costs vs OpenAI
- **🔒 Enhanced Security**: Data stays within your AWS account
- **📏 Higher Limits**: 200k token context window with Claude
- **🏢 Enterprise Ready**: Better compliance and audit trails

---

## Acknowledgments

- **LangChain/LangGraph**: For the multi-agent framework
- **OpenAI**: For GPT-4 language model
- **Ollama**: For local embedding models
- **WebdriverIO**: For browser automation capabilities
- **Chroma**: For vector database functionality
