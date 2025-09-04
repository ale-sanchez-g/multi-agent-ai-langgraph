#!/usr/bin/env python3
"""
AWS Bedrock Connection Validation Script
This script validates the AWS Bedrock setup for the Multi-Agent QA System.
"""

import os
import sys
from dotenv import load_dotenv

def check_environment_variables():
    """Check if required environment variables are set."""
    print("🔍 Checking environment variables...")
    
    load_dotenv()
    
    required_vars = {
        'AWS_REGION': os.getenv('AWS_REGION'),
        'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'JIRA_URL': os.getenv('JIRA_URL'),
        'JIRA_USER': os.getenv('JIRA_USER'),
        'JIRA_API_TOKEN': os.getenv('JIRA_API_TOKEN')
    }
    
    missing_vars = []
    for var_name, var_value in required_vars.items():
        if not var_value:
            missing_vars.append(var_name)
        else:
            print(f"  ✅ {var_name}: {'*' * min(len(var_value), 20)}")
    
    if missing_vars:
        print(f"  ❌ Missing variables: {', '.join(missing_vars)}")
        return False
    
    print("  ✅ All environment variables are set!")
    return True

def check_aws_credentials():
    """Check AWS credentials and Bedrock access."""
    print("\n🔐 Checking AWS credentials...")
    
    try:
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError
        
        # Test basic AWS connection
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if not credentials:
            print("  ❌ No AWS credentials found!")
            print("  💡 Run 'aws configure' or set environment variables")
            return False
        
        print(f"  ✅ AWS credentials found for region: {session.region_name or 'default'}")
        
        # Test Bedrock access and list available models
        bedrock_client = boto3.client('bedrock', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        try:
            print("  🔍 Checking Bedrock model access...")
            models = bedrock_client.list_foundation_models()
            
            # Show all available models
            all_models = models['modelSummaries']
            print(f"  📊 Total models available in region: {len(all_models)}")
            
            # Check for Claude models specifically
            claude_models = [m for m in all_models if 'anthropic.claude' in m['modelId']]
            
            if claude_models:
                print(f"  ✅ Found {len(claude_models)} Claude models:")
                for model in claude_models[:5]:  # Show first 5
                    print(f"    - {model['modelId']}")
                if len(claude_models) > 5:
                    print(f"    ... and {len(claude_models) - 5} more")
                return True
            else:
                print("  ❌ No Claude models found!")
                print("  💡 You need to request access to Claude models")
                print("  🌐 Go to: https://console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess")
                return False
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                print("  ❌ Access denied to Bedrock service")
                print("  💡 Add bedrock:* permissions to your IAM user/role")
            else:
                print(f"  ❌ Bedrock error: {error_code}")
            return False
            
    except ImportError:
        print("  ❌ boto3 not installed")
        print("  💡 Run: pip install boto3")
        return False
    except NoCredentialsError:
        print("  ❌ AWS credentials not configured")
        print("  💡 Run 'aws configure' or set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY")
        return False
    except Exception as e:
        print(f"  ❌ AWS connection error: {str(e)}")
        return False

def check_langchain_aws():
    """Check if langchain-aws is installed and working."""
    print("\n📦 Checking LangChain AWS integration...")
    
    try:
        from langchain_aws import ChatBedrock
        print("  ✅ langchain-aws imported successfully")
        
        # Try to initialize ChatBedrock (without invoking)
        try:
            llm = ChatBedrock(
                model_id="anthropic.claude-3-haiku-20240307-v1:0",
                model_kwargs={"max_tokens": 100, "temperature": 0.1},
                region_name=os.getenv('AWS_REGION', 'us-east-1')
            )
            print("  ✅ ChatBedrock initialized successfully")
            return True
        except Exception as e:
            print(f"  ❌ ChatBedrock initialization failed: {str(e)}")
            return False
            
    except ImportError as e:
        print(f"  ❌ langchain-aws import failed: {str(e)}")
        print("  💡 Run: pip install langchain-aws")
        return False

def test_bedrock_invoke():
    """Test actual Bedrock model invocation."""
    print("\n🧠 Testing Bedrock model invocation...")
    
    # List of models to try in order of preference
    models_to_try = [
        "anthropic.claude-3-haiku-20240307-v1:0",    # Fastest, cheapest
        "anthropic.claude-3-sonnet-20240229-v1:0",   # Good balance
        "anthropic.claude-instant-v1",               # Legacy fallback
    ]
    
    try:
        from langchain_aws import ChatBedrock
        
        for model_id in models_to_try:
            print(f"  🔍 Trying model: {model_id}")
            try:
                llm = ChatBedrock(
                    model_id=model_id,
                    model_kwargs={"max_tokens": 50, "temperature": 0.1},
                    region_name=os.getenv('AWS_REGION', 'us-east-1')
                )
                
                test_message = "Respond with exactly: 'Bedrock connection successful'"
                response = llm.invoke(test_message)
                
                print(f"  ✅ Model response: {response.content}")
                print(f"  🎉 Bedrock invocation test passed with model: {model_id}")
                return True
                
            except Exception as e:
                if "You don't have access to the model" in str(e):
                    print(f"  ⚠️  No access to model: {model_id}")
                    continue
                else:
                    print(f"  ❌ Error with model {model_id}: {str(e)}")
                    continue
        
        # If we get here, none of the models worked
        print("  ❌ None of the Claude models are accessible")
        print("  🚨 ACTION REQUIRED: Request model access in AWS Bedrock Console")
        print("  🌐 Direct link: https://console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess")
        print("\n  📋 Steps to request access:")
        print("     1. Click the link above")
        print("     2. Find 'Anthropic' in the provider list")
        print("     3. Select Claude models (Haiku, Sonnet, Opus)")
        print("     4. Click 'Request model access'")
        print("     5. Wait for approval (usually instant)")
        return False
        
    except Exception as e:
        print(f"  ❌ Bedrock invocation failed: {str(e)}")
        return False

def main():
    """Run all validation checks."""
    print("🚀 AWS Bedrock Migration Validation")
    print("=" * 50)
    
    checks = [
        check_environment_variables,
        check_aws_credentials,
        check_langchain_aws,
        test_bedrock_invoke
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check in checks:
        try:
            if check():
                passed_checks += 1
        except KeyboardInterrupt:
            print("\n\n❌ Validation interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"  ❌ Unexpected error in {check.__name__}: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Validation Results: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 All checks passed! Your AWS Bedrock setup is ready!")
        print("\n🚀 Next steps:")
        print("  1. Start WebdriverIO server: node server.js")
        print("  2. Open notebook: jupyter notebook multi-agent-qa-ai-system.ipynb")
        print("  3. Run the cells to test your migrated system")
        return True
    else:
        print("❌ Some checks failed. Most likely you need to request Claude model access.")
        print("\n🔧 Quick fix:")
        print("  1. Go to: https://console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess")
        print("  2. Find 'Anthropic' and request access to Claude models")
        print("  3. Run this script again: python3 validate_bedrock_setup.py")
        print("\n📚 Helpful resources:")
        print("  - AWS Bedrock setup: https://docs.aws.amazon.com/bedrock/")
        print("  - Migration guide: ./BEDROCK_MIGRATION.md")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)