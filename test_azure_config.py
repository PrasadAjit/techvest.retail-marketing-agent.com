"""
Test Azure OpenAI Configuration
Run this script to verify your Azure OpenAI setup is working correctly
"""
import os
from src.config.settings import settings
from src.utils.llm_helper import get_llm

def main():
    print("=" * 70)
    print("Azure OpenAI Configuration Test")
    print("=" * 70)
    
    # Check configuration
    print("\n1. Checking configuration...")
    print(f"   Using Azure: {settings.openai.use_azure}")
    
    if settings.openai.use_azure:
        print(f"   Azure Endpoint: {settings.openai.azure_endpoint}")
        print(f"   Azure Deployment: {settings.openai.azure_deployment}")
        print(f"   API Version: {settings.openai.azure_api_version}")
        print(f"   API Key: {'*' * 20}{settings.openai.azure_api_key[-10:]}")
    else:
        print(f"   OpenAI Model: {settings.openai.model}")
        print(f"   API Key: {'*' * 20}{settings.openai.api_key[-10:] if settings.openai.api_key else 'NOT SET'}")
    
    # Test LLM connection
    print("\n2. Testing LLM connection...")
    try:
        llm = get_llm()
        print("   ✓ LLM initialized successfully")
        
        # Test a simple query
        print("\n3. Testing AI response...")
        response = llm.invoke("Say 'Hello! Azure OpenAI is working!' in one sentence.")
        print(f"   AI Response: {response.content}")
        
        print("\n" + "=" * 70)
        print("✓ All tests passed! Your Azure OpenAI setup is working correctly.")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n   ✗ Error: {str(e)}")
        print("\n" + "=" * 70)
        print("Configuration check failed. Please verify:")
        print("1. Your .env file has correct Azure OpenAI credentials")
        print("2. AZURE_OPENAI_API_KEY is set correctly")
        print("3. AZURE_OPENAI_ENDPOINT is correct")
        print("4. AZURE_OPENAI_DEPLOYMENT matches your deployment name")
        print("=" * 70)
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
