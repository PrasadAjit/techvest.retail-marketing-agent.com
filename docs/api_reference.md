# API Reference

## Core Classes

### RetailMarketingAgent

Main agent class for orchestrating marketing activities.

#### Constructor

```python
RetailMarketingAgent(
    client_name: str,
    store_type: str = "general",
    has_online_store: bool = True,
    location: Optional[str] = None
)
```

**Parameters**:
- `client_name`: Name of the retail client
- `store_type`: Type of store (fashion, electronics, grocery, etc.)
- `has_online_store`: Whether the store has an online presence
- `location`: Physical location of the store

**Example**:
```python
agent = RetailMarketingAgent(
    client_name="Fashion Boutique",
    store_type="fashion",
    has_online_store=True,
    location="New York, NY"
)
```

#### Methods

##### `set_goal()`

Create and add a new marketing goal.

```python
set_goal(
    goal_type: str,
    target: str,
    timeframe: str,
    description: Optional[str] = None,
    metrics: Optional[Dict[str, Any]] = None,
    priority: int = 1
) -> Goal
```

**Parameters**:
- `goal_type`: Type of goal (customer_acquisition, customer_retention, etc.)
- `target`: Specific target to achieve
- `timeframe`: Time period for goal completion
- `description`: Detailed description (optional)
- `metrics`: Success metrics dictionary (optional)
- `priority`: Priority level 1-5 (1 is highest)

**Returns**: Goal object

**Example**:
```python
goal = agent.set_goal(
    goal_type="customer_acquisition",
    target="Increase foot traffic by 25%",
    timeframe="30 days",
    metrics={"target_customers": 500}
)
```

##### `plan()`

Create an execution plan for a goal.

```python
plan(goal: Goal) -> List[Dict[str, Any]]
```

**Parameters**:
- `goal`: Goal object to create plan for

**Returns**: List of subtask dictionaries

##### `execute()`

Execute one or all active goals.

```python
execute(goal: Optional[Goal] = None) -> Dict[str, Any]
```

**Parameters**:
- `goal`: Specific goal to execute (optional, executes all if None)

**Returns**: Dictionary with execution results

##### `get_status_report()`

Get comprehensive status of all goals and activities.

```python
get_status_report() -> Dict[str, Any]
```

**Returns**: Status report dictionary

---

## Marketing Modules

### CustomerAcquisitionModule

#### `create_promotion_campaign()`

```python
create_promotion_campaign(
    target_audience: str,
    campaign_type: str,
    budget: float,
    duration_days: int,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Creates a promotional campaign for customer acquisition.

#### `design_first_purchase_incentive()`

```python
design_first_purchase_incentive(
    incentive_type: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Designs incentives for first-time customers.

#### `create_referral_program()`

```python
create_referral_program(
    reward_structure: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Creates a customer referral program.

#### `generate_targeted_ad_copy()`

```python
generate_targeted_ad_copy(
    platform: str,
    target_segment: str,
    product_category: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Generates ad copy for specific platforms and segments.

---

### CustomerRetentionModule

#### `design_loyalty_program()`

```python
design_loyalty_program(
    program_type: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Designs a customer loyalty program.

#### `create_email_campaign()`

```python
create_email_campaign(
    campaign_goal: str,
    customer_segment: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Creates an email marketing campaign.

#### `create_win_back_campaign()`

```python
create_win_back_campaign(
    inactive_period: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Creates campaign to win back inactive customers.

#### `create_vip_experience()`

```python
create_vip_experience(
    vip_criteria: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Creates VIP customer experience program.

---

### DigitalMarketingModule

#### `create_social_media_content()`

```python
create_social_media_content(
    platform: str,
    content_type: str,
    theme: str,
    num_posts: int,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Creates social media content for various platforms.

**Platforms**: instagram, facebook, tiktok, twitter
**Content Types**: product_showcase, behind_scenes, tips, testimonials

#### `optimize_local_seo()`

```python
optimize_local_seo(
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Creates local SEO optimization strategy.

#### `create_influencer_campaign()`

```python
create_influencer_campaign(
    campaign_goal: str,
    influencer_tier: str,
    budget: float,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Creates influencer marketing campaign.

**Influencer Tiers**: nano, micro, macro, mega

#### `create_content_calendar()`

```python
create_content_calendar(
    duration_weeks: int,
    platforms: List[str],
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Creates comprehensive content calendar.

---

### InStoreMarketingModule

#### `design_visual_merchandising()`

```python
design_visual_merchandising(
    season: str,
    focus_products: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Designs visual merchandising strategy.

#### `create_pos_displays()`

```python
create_pos_displays(
    promotion_type: str,
    location: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Creates point-of-sale display concepts.

**Locations**: checkout, endcap, entrance, aisle

#### `plan_instore_event()`

```python
plan_instore_event(
    event_type: str,
    duration_hours: int,
    expected_attendance: int,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Plans in-store events or product demonstrations.

#### `create_signage_materials()`

```python
create_signage_materials(
    signage_type: str,
    message: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Creates in-store signage and promotional materials.

---

## Analytics

### CustomerAnalyticsModule

#### `analyze_sales_data()`

```python
analyze_sales_data(
    sales_data: Dict[str, Any],
    time_period: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Analyzes sales data and provides insights.

#### `segment_customers()`

```python
segment_customers(
    customer_data: List[Dict[str, Any]],
    segmentation_criteria: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Segments customers based on behavior and characteristics.

#### `analyze_shopping_patterns()`

```python
analyze_shopping_patterns(
    transaction_data: List[Dict[str, Any]],
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Analyzes shopping patterns and basket analysis.

#### `process_customer_feedback()`

```python
process_customer_feedback(
    feedback_data: List[Dict[str, Any]],
    feedback_type: str,
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Processes and analyzes customer feedback.

#### `predict_customer_lifetime_value()`

```python
predict_customer_lifetime_value(
    customer_profile: Dict[str, Any],
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Predicts customer lifetime value and retention probability.

#### `generate_performance_report()`

```python
generate_performance_report(
    metrics: Dict[str, Any],
    comparison_period: Optional[str],
    store_context: Dict[str, Any]
) -> Dict[str, Any]
```

Generates comprehensive performance report.

---

## Campaign Management

### CampaignManager

#### `create_campaign()`

```python
create_campaign(
    name: str,
    campaign_type: str,
    description: str,
    start_date: datetime,
    end_date: datetime,
    budget: float,
    target_metrics: Dict[str, Any]
) -> Campaign
```

Creates a new marketing campaign.

#### `get_campaign()`

```python
get_campaign(campaign_id: str) -> Optional[Campaign]
```

Retrieves a campaign by ID.

#### `get_active_campaigns()`

```python
get_active_campaigns() -> List[Campaign]
```

Gets all currently active campaigns.

#### `launch_campaign()`

```python
launch_campaign(campaign_id: str) -> bool
```

Launches a planned campaign.

#### `pause_campaign()`

```python
pause_campaign(campaign_id: str) -> bool
```

Pauses an active campaign.

#### `calculate_roi()`

```python
calculate_roi(campaign_id: str, revenue: float) -> Optional[float]
```

Calculates campaign ROI.

---

## Enumerations

### GoalType
```python
class GoalType(Enum):
    CUSTOMER_ACQUISITION = "customer_acquisition"
    CUSTOMER_RETENTION = "customer_retention"
    INSTORE_MARKETING = "instore_marketing"
    DIGITAL_PRESENCE = "digital_presence"
    SEASONAL_CAMPAIGN = "seasonal_campaign"
    ANALYTICS_INSIGHTS = "analytics_insights"
    COMMUNITY_ENGAGEMENT = "community_engagement"
```

### GoalStatus
```python
class GoalStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
```

### CampaignType
```python
class CampaignType(Enum):
    ACQUISITION = "acquisition"
    RETENTION = "retention"
    SEASONAL = "seasonal"
    PRODUCT_LAUNCH = "product_launch"
    CLEARANCE = "clearance"
    EVENT = "event"
    BRAND_AWARENESS = "brand_awareness"
```

### CampaignStatus
```python
class CampaignStatus(Enum):
    DRAFT = "draft"
    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
```

---

## Utility Functions

Located in `src/utils/helpers.py`:

- `format_currency(amount, currency)`: Format amount as currency
- `calculate_percentage_change(old_value, new_value)`: Calculate % change
- `parse_timeframe(timeframe)`: Parse timeframe string to timedelta
- `get_date_range(timeframe)`: Get start/end dates
- `calculate_roi(revenue, cost)`: Calculate ROI
- `validate_email(email)`: Validate email format
- `generate_hashtags(text, max_count)`: Generate hashtags
- `format_date_range(start_date, end_date)`: Format date range
