# Getting Started Guide

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- OpenAI API key

### Step 1: Clone or Download

Download the Retail Marketing Agent project to your local machine.

### Step 2: Install Dependencies

```bash
cd "Retail Marketing Agent"
pip install -r requirements.txt
```

This will install all required packages including:
- OpenAI and LangChain for AI capabilities
- Pandas and NumPy for data processing
- Various API clients for social media and email

### Step 3: Configure Environment

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your configuration:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   STORE_NAME=Your Store Name
   STORE_TYPE=your_store_type
   STORE_LOCATION=Your City, State
   ```

### Step 4: Verify Installation

Run a simple test:

```python
from src.agents import RetailMarketingAgent

agent = RetailMarketingAgent(
    client_name="Test Store",
    store_type="retail"
)
print("✓ Installation successful!")
```

---

## Quick Start

### Your First Marketing Goal

```python
from src.agents import RetailMarketingAgent

# Initialize agent
agent = RetailMarketingAgent(
    client_name="Fashion Boutique",
    store_type="fashion",
    has_online_store=True,
    location="Los Angeles, CA"
)

# Set a goal
goal = agent.set_goal(
    goal_type="customer_acquisition",
    target="Increase new customer signups by 30%",
    timeframe="30 days"
)

# Create execution plan
plan = agent.plan(goal)

# Execute
results = agent.execute(goal)

# View results
print(results)
```

---

## Core Concepts

### 1. Goals

Goals are the foundation of the agent's work. Each goal has:
- **Type**: What kind of marketing activity (acquisition, retention, etc.)
- **Target**: Specific measurable outcome
- **Timeframe**: When to achieve it
- **Metrics**: Success indicators

**Example Goal Types**:
- `customer_acquisition`: Get new customers
- `customer_retention`: Keep existing customers
- `digital_presence`: Improve online visibility
- `instore_marketing`: Enhance physical store experience
- `seasonal_campaign`: Holiday or event-based campaigns

### 2. Modules

Specialized modules handle different marketing activities:

- **CustomerAcquisitionModule**: New customer campaigns
- **CustomerRetentionModule**: Loyalty and retention
- **DigitalMarketingModule**: Social media and online
- **InStoreMarketingModule**: Physical store marketing
- **CustomerAnalyticsModule**: Data analysis and insights

### 3. Campaigns

Campaigns organize multiple marketing activities:

```python
from datetime import datetime, timedelta
from src.campaigns import CampaignManager

manager = CampaignManager()

campaign = manager.create_campaign(
    name="Summer Sale 2026",
    campaign_type="seasonal",
    description="Major summer promotion",
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=30),
    budget=10000,
    target_metrics={"revenue": 50000}
)
```

---

## Common Use Cases

### Use Case 1: Launch a Promotional Campaign

```python
from src.modules import CustomerAcquisitionModule

acquisition = CustomerAcquisitionModule()

campaign = acquisition.create_promotion_campaign(
    target_audience="Young professionals 25-35",
    campaign_type="seasonal",
    budget=5000,
    duration_days=14,
    store_context={
        "name": "Your Store",
        "type": "fashion",
        "location": "NYC"
    }
)

print(campaign['campaign_plan'])
```

### Use Case 2: Create Social Media Content

```python
from src.modules import DigitalMarketingModule

digital = DigitalMarketingModule()

content = digital.create_social_media_content(
    platform="instagram",
    content_type="product_showcase",
    theme="Spring Collection Launch",
    num_posts=7,
    store_context={
        "name": "Your Store",
        "type": "fashion"
    }
)

print(content['social_content'])
```

### Use Case 3: Analyze Customer Data

```python
from src.analytics import CustomerAnalyticsModule

analytics = CustomerAnalyticsModule()

# Analyze sales
analysis = analytics.analyze_sales_data(
    sales_data={
        "total_revenue": 100000,
        "transactions": 1000,
        "avg_basket": 100
    },
    time_period="Q1 2026",
    store_context={"name": "Your Store", "type": "retail"}
)

print(analysis['analysis'])
```

### Use Case 4: Design In-Store Display

```python
from src.modules import InStoreMarketingModule

instore = InStoreMarketingModule()

display = instore.design_visual_merchandising(
    season="Holiday Season",
    focus_products="Gift items and festive wear",
    store_context={
        "name": "Your Store",
        "type": "retail"
    }
)

print(display['merchandising_plan'])
```

---

## Working with Store Context

Most modules require a `store_context` dictionary:

```python
store_context = {
    "name": "Your Store Name",
    "type": "fashion",  # or electronics, grocery, etc.
    "location": "City, State"
}
```

This context helps the AI generate relevant, personalized strategies.

---

## Best Practices

### 1. Start with Clear Goals
Be specific about what you want to achieve:
- ✅ "Increase foot traffic by 25% in next 30 days"
- ❌ "Get more customers"

### 2. Provide Rich Context
The more context you provide, the better the strategies:
```python
goal = agent.set_goal(
    goal_type="customer_acquisition",
    target="Acquire 500 new customers",
    timeframe="60 days",
    metrics={
        "target_customers": 500,
        "budget": 10000,
        "target_conversion": 0.15
    }
)
```

### 3. Review and Iterate
Always review AI-generated strategies and refine:
```python
# Generate plan
plan = agent.plan(goal)

# Review subtasks
for task in plan:
    print(f"Task: {task['name']}")
    # Adjust if needed

# Execute
results = agent.execute(goal)
```

### 4. Track Performance
Use the analytics module to monitor results:
```python
report = analytics.generate_performance_report(
    metrics=your_metrics,
    comparison_period="previous_month",
    store_context=store_context
)
```

---

## Troubleshooting

### Issue: OpenAI API Errors

**Problem**: API key errors or rate limits

**Solution**:
```python
# Check your API key
import os
print(os.getenv("OPENAI_API_KEY"))

# Reduce temperature for more consistent results
from src.config import settings
settings.openai.temperature = 0.5
```

### Issue: Module Import Errors

**Problem**: Cannot import modules

**Solution**:
```bash
# Ensure you're in the project root
cd "Retail Marketing Agent"

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Empty or Generic Results

**Problem**: AI generates generic content

**Solution**: Provide more specific context:
```python
# Instead of this
store_context = {"name": "Store"}

# Do this
store_context = {
    "name": "Fashion Forward Boutique",
    "type": "fashion",
    "location": "Downtown Seattle",
    "specialty": "Contemporary women's fashion",
    "target_audience": "Professional women 28-45"
}
```

---

## Next Steps

1. **Run Examples**: Try the example scripts in `examples/`
   ```bash
   python examples/basic_usage.py
   python examples/advanced_campaign.py
   python examples/analytics_example.py
   ```

2. **Explore Modules**: Experiment with different marketing modules

3. **Customize**: Adapt the agent for your specific retail business

4. **Integrate**: Connect with your existing systems and data

5. **Extend**: Add custom modules or functionality

---

## Getting Help

- **Documentation**: Check `docs/` directory
- **Examples**: Review `examples/` for patterns
- **API Reference**: See `docs/api_reference.md`
- **Architecture**: Read `docs/architecture.md` for system design

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
