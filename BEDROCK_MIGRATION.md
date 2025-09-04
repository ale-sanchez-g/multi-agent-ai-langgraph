# AWS Bedrock Migration Guide

This document outlines the migration from OpenAI to AWS Bedrock for the Multi-Agent QA System.

## Changes Made

### 1. Dependencies Updated
- Replaced `langchain-openai` with `langchain-aws`
- Added `boto3` for AWS SDK support
- Updated `requirements.txt` accordingly

### 2. LLM Configuration
- Replaced `ChatOpenAI` with `ChatBedrock`
- Changed from GPT-4 to Claude 3 Sonnet (`anthropic.claude-3-sonnet-20240229-v1:0`)
- Updated model parameters to match Bedrock's API

### 3. Environment Variables
- Removed `OPENAI_API_KEY` requirement
- Added AWS credentials configuration:
  - `AWS_REGION`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`

### 4. Model Comparison

| Feature | OpenAI GPT-4 | AWS Bedrock Claude 3 Sonnet |
|---------|--------------|------------------------------|
| Context Window | 8k-128k tokens | 200k tokens |
| Temperature | 0-2 | 0-1 |
| Max Tokens | 4096 | 4096 |
| Cost | $0.03/1k input, $0.06/1k output | $0.003/1k input, $0.015/1k output |

## Setup Instructions

### 1. AWS Account Setup
1. Create an AWS account if you don't have one
2. Set up IAM user with Bedrock permissions
3. Request access to Claude models in Bedrock console

### 2. AWS CLI Configuration
```bash
aws configure
```
Enter your AWS credentials when prompted.

### 3. Environment Variables
Update your `.env` file with AWS credentials:
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Verify Bedrock Access
Run this test to ensure Bedrock is accessible:
```python
from langchain_aws import ChatBedrock

llm = ChatBedrock(model_id="anthropic.claude-3-sonnet-20240229-v1:0")
response = llm.invoke("Hello, world!")
print(response.content)
```

## Benefits of Migration

1. **Cost Efficiency**: Lower per-token costs compared to OpenAI
2. **Higher Context Limits**: 200k tokens vs GPT-4's variable limits
3. **AWS Integration**: Better integration with other AWS services
4. **Data Privacy**: Data stays within your AWS account
5. **Enterprise Features**: Better compliance and security controls

## Available Models

You can switch between different Claude models by changing the `model_id`:

- `anthropic.claude-3-sonnet-20240229-v1:0` (recommended for balance)
- `anthropic.claude-3-haiku-20240307-v1:0` (faster, cheaper)
- `anthropic.claude-3-opus-20240229-v1:0` (highest capability)

## Troubleshooting

### Common Issues

1. **Model Access Denied**: Request access in Bedrock console
2. **Credentials Error**: Verify AWS CLI configuration
3. **Region Issues**: Ensure Bedrock is available in your selected region
4. **Import Errors**: Make sure `langchain-aws` is installed

### Testing Connection
```python
import boto3
client = boto3.client('bedrock-runtime', region_name='us-east-1')
print("Bedrock connection successful")
```

## Migration Validation

After migration, verify that:
- [ ] All agents initialize correctly
- [ ] BDD test case generation works
- [ ] QA automation agent functions properly
- [ ] Manager agent orchestrates tasks correctly
- [ ] Cost monitoring is set up in AWS