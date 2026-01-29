# Retail Marketing Agent - Examples

This directory contains example scripts demonstrating various features and use cases of the Retail Marketing Agent.

## Examples Overview

### 1. Basic Usage (`basic_usage.py`)
**Purpose**: Introduction to the core functionality of the agent.

**What it demonstrates**:
- Initializing the Retail Marketing Agent
- Setting a marketing goal
- Creating an execution plan
- Executing a goal
- Getting status reports

**Run it**:
```bash
python examples/basic_usage.py
```

### 2. Advanced Campaign (`advanced_campaign.py`)
**Purpose**: Complete end-to-end marketing campaign setup.

**What it demonstrates**:
- Using multiple marketing modules together
- Creating promotional campaigns
- Generating social media content
- Designing in-store merchandising
- Planning influencer campaigns
- Campaign management and tracking
- Setting multiple coordinated goals

**Run it**:
```bash
python examples/advanced_campaign.py
```

### 3. Analytics Example (`analytics_example.py`)
**Purpose**: Customer insights and performance analysis.

**What it demonstrates**:
- Sales data analysis
- Customer segmentation
- Shopping pattern analysis
- Customer feedback processing
- Customer lifetime value prediction
- Performance reporting

**Run it**:
```bash
python examples/analytics_example.py
```

## Prerequisites

Before running the examples, ensure you have:

1. Installed all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`

3. (Optional) For examples to run with actual AI-generated content:
   ```python
   import os
   os.environ["OPENAI_API_KEY"] = "your-actual-api-key"
   ```

## Understanding the Output

Each example will display:
- Step-by-step progress indicators (✓)
- Generated marketing plans and strategies
- Campaign details and metrics
- Analytics insights and recommendations
- Status reports and summaries

## Customizing the Examples

You can modify the examples to fit your specific retail business:

### Change Store Details
```python
agent = RetailMarketingAgent(
    client_name="Your Store Name",
    store_type="your_type",  # fashion, electronics, grocery, etc.
    has_online_store=True,
    location="Your Location"
)
```

### Adjust Campaign Parameters
```python
promo_campaign = acquisition_module.create_promotion_campaign(
    target_audience="Your specific audience",
    campaign_type="seasonal",  # or "clearance", "new_product", etc.
    budget=5000,  # Your budget
    duration_days=30,  # Campaign length
    store_context=store_context
)
```

### Set Different Goals
```python
goal = agent.set_goal(
    goal_type="customer_retention",  # or any other GoalType
    target="Your specific target",
    timeframe="60 days",
    metrics={"your_metric": value}
)
```

## Next Steps

After running these examples, you can:

1. **Create your own campaigns**: Use the modules to build custom marketing campaigns
2. **Integrate with your data**: Connect real sales and customer data for analysis
3. **Automate workflows**: Schedule regular campaign creation and analysis
4. **Extend functionality**: Add new modules or customize existing ones

## Need Help?

- Check the main README.md for detailed documentation
- Review the source code in `src/` directory
- See inline comments in example files for additional guidance

## Example Data

The examples use sample/mock data for demonstration. In production:
- Replace with actual sales data from your POS system
- Connect to your customer database
- Integrate with your analytics platform
- Use real campaign performance metrics
