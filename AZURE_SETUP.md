# Azure OpenAI Setup - Quick Start

Your Retail Marketing Agent is now configured to use **Azure OpenAI**! 🎉

## ✅ Configuration Complete

Your `.env` file has been updated with Azure OpenAI credentials:
- Azure API Key: ✓ Configured
- Azure Endpoint: ✓ Configured  
- Deployment: gpt-4o

## 🧪 Test Your Setup

Run this command to verify everything works:

```bash
python test_azure_config.py
```

This will:
1. Check your configuration
2. Test the Azure OpenAI connection
3. Make a sample API call
4. Confirm everything is working

## 🚀 Quick Start Example

```python
from src.agents import RetailMarketingAgent

# Initialize the agent (it will automatically use Azure OpenAI)
agent = RetailMarketingAgent(
    client_name="Fashion Forward Boutique",
    store_type="fashion",
    has_online_store=True,
    location="Seattle, WA"
)

# Set a marketing goal
goal = agent.set_goal(
    goal_type="customer_acquisition",
    target="Increase foot traffic by 25%",
    timeframe="30 days"
)

# The agent will use Azure OpenAI to create a plan
plan = agent.plan(goal)

# Execute the plan
results = agent.execute(goal)
print(results)
```

## 📝 What Changed

1. **Configuration (`src/config/settings.py`)**
   - Added Azure OpenAI support
   - Automatically detects Azure vs OpenAI
   - Uses Azure if credentials are present

2. **LLM Helper (`src/utils/llm_helper.py`)**
   - New utility to get configured LLM
   - Supports both Azure and OpenAI
   - Used by all modules

3. **All Modules Updated**
   - Customer Acquisition Module
   - Customer Retention Module
   - Digital Marketing Module
   - In-Store Marketing Module
   - Analytics Module
   - Main Agent

## 🎯 Next Steps

### 1. Test the Configuration
```bash
python test_azure_config.py
```

### 2. Run Basic Example
```bash
python examples/basic_usage.py
```

### 3. Try Advanced Campaign
```bash
python examples/advanced_campaign.py
```

### 4. Explore Analytics
```bash
python examples/analytics_example.py
```

## ⚙️ Your Environment Variables

Current configuration in `.env`:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=sWUV0J...7w3AAAAACOG8cVj
AZURE_OPENAI_ENDPOINT=https://medisummarize-openai.cognitiveservices.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_API_VERSION=2024-02-15-preview

# Store Information (Customize these!)
STORE_NAME=Fashion Forward Boutique
STORE_TYPE=fashion
STORE_LOCATION=Downtown Seattle
HAS_ONLINE_STORE=true
```

## 🔧 Customizing Store Information

Edit the `.env` file to match your retail business:

```env
STORE_NAME=Your Store Name
STORE_TYPE=fashion  # or electronics, grocery, beauty, etc.
STORE_LOCATION=Your City, State
HAS_ONLINE_STORE=true  # or false
WEBSITE_URL=https://yourstore.com
```

## 🆘 Troubleshooting

### Error: "Unauthorized" or "401"
- Check your Azure API key is correct
- Verify the endpoint URL
- Ensure your Azure subscription is active

### Error: "Deployment not found"
- Verify `AZURE_OPENAI_DEPLOYMENT` matches your deployment name in Azure
- Check the deployment is in the same region as your endpoint

### Error: "Rate limit exceeded"
- Your Azure deployment may have rate limits
- Wait a moment and try again
- Consider upgrading your Azure OpenAI tier

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 📚 Additional Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [LangChain Azure Integration](https://python.langchain.com/docs/integrations/llms/azure_openai)
- Project documentation in `docs/` directory

## 🎉 Ready to Go!

Your Retail Marketing Agent is now powered by Azure OpenAI and ready to:
- Generate marketing campaigns
- Create social media content
- Design promotional strategies
- Analyze customer data
- Plan seasonal campaigns
- And much more!

Run the test script to get started:
```bash
python test_azure_config.py
```
