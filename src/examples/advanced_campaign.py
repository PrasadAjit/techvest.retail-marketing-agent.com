"""
Advanced Example: Complete Marketing Campaign
"""
import os
from datetime import datetime, timedelta
from src.agents import RetailMarketingAgent
from src.modules import (
    CustomerAcquisitionModule,
    DigitalMarketingModule,
    InStoreMarketingModule
)
from src.campaigns import CampaignManager, CampaignType


def main():
    print("=" * 80)
    print("Advanced Example: Complete Holiday Marketing Campaign")
    print("=" * 80)
    
    # Initialize agent and modules
    print("\n1. Initializing components...")
    agent = RetailMarketingAgent(
        client_name="TechStyle Electronics",
        store_type="electronics",
        has_online_store=True,
        location="San Francisco Bay Area"
    )
    
    acquisition_module = CustomerAcquisitionModule()
    digital_module = DigitalMarketingModule()
    instore_module = InStoreMarketingModule()
    campaign_manager = CampaignManager()
    
    print("✓ All components initialized")
    
    # Create store context
    store_context = {
        "name": agent.client_name,
        "type": agent.store_type,
        "location": agent.location
    }
    
    # 1. Create a promotional campaign
    print("\n2. Creating Black Friday promotional campaign...")
    promo_campaign = acquisition_module.create_promotion_campaign(
        target_audience="Tech enthusiasts aged 25-45 with mid-to-high income",
        campaign_type="seasonal",
        budget=15000,
        duration_days=14,
        store_context=store_context
    )
    print("✓ Promotional campaign created")
    print(f"  Budget: ${promo_campaign['budget']}")
    print(f"  Duration: {promo_campaign['start_date']} to {promo_campaign['end_date']}")
    
    # 2. Create social media content
    print("\n3. Creating social media content...")
    social_content = digital_module.create_social_media_content(
        platform="instagram",
        content_type="product_showcase",
        theme="Black Friday Tech Deals",
        num_posts=7,
        store_context=store_context
    )
    print(f"✓ {social_content['num_posts']} Instagram posts created")
    print(f"  Theme: {social_content['theme']}")
    
    # 3. Design in-store displays
    print("\n4. Designing in-store visual merchandising...")
    merchandising = instore_module.design_visual_merchandising(
        season="Black Friday / Holiday",
        focus_products="Latest smartphones, laptops, and smart home devices",
        store_context=store_context
    )
    print("✓ Visual merchandising strategy designed")
    
    # 4. Create influencer campaign
    print("\n5. Creating influencer marketing campaign...")
    influencer_campaign = digital_module.create_influencer_campaign(
        campaign_goal="Drive awareness and foot traffic for Black Friday",
        influencer_tier="micro",
        budget=5000,
        store_context=store_context
    )
    print("✓ Influencer campaign created")
    print(f"  Budget: ${influencer_campaign['budget']}")
    print(f"  Tier: {influencer_campaign['influencer_tier']}")
    
    # 5. Register campaign with campaign manager
    print("\n6. Registering campaign in campaign manager...")
    start_date = datetime.now() + timedelta(days=7)
    end_date = start_date + timedelta(days=14)
    
    campaign = campaign_manager.create_campaign(
        name="Black Friday 2026 Tech Sale",
        campaign_type="seasonal",
        description="Comprehensive Black Friday campaign with in-store and digital promotion",
        start_date=start_date,
        end_date=end_date,
        budget=20000,
        target_metrics={
            "target_revenue": 100000,
            "target_customers": 1000,
            "target_impressions": 50000,
            "target_roi": 400
        }
    )
    
    # Add channels and assets
    campaign.add_channel("instagram")
    campaign.add_channel("facebook")
    campaign.add_channel("in_store")
    campaign.add_channel("influencer")
    
    campaign.add_asset("social_media_posts", social_content)
    campaign.add_asset("merchandising_plan", merchandising)
    campaign.add_asset("influencer_brief", influencer_campaign)
    
    campaign.update_status(campaign_manager.CampaignStatus.PLANNED)
    
    print("✓ Campaign registered and planned")
    print(f"  Campaign ID: {campaign.id}")
    print(f"  Name: {campaign.name}")
    print(f"  Duration: {campaign.get_duration_days()} days")
    print(f"  Budget: ${campaign.budget}")
    print(f"  Channels: {', '.join(campaign.channels)}")
    
    # 6. Set multiple goals for the agent
    print("\n7. Setting comprehensive marketing goals...")
    
    # Customer acquisition goal
    goal1 = agent.set_goal(
        goal_type="customer_acquisition",
        target="Acquire 1000 new customers during Black Friday period",
        timeframe="14 days",
        priority=1
    )
    print(f"✓ Goal 1: {goal1.goal_type.value}")
    
    # Digital presence goal
    goal2 = agent.set_goal(
        goal_type="digital_presence",
        target="Achieve 50,000 impressions and 5,000 engagements on social media",
        timeframe="14 days",
        priority=1
    )
    print(f"✓ Goal 2: {goal2.goal_type.value}")
    
    # In-store marketing goal
    goal3 = agent.set_goal(
        goal_type="instore_marketing",
        target="Create compelling displays that increase foot traffic by 40%",
        timeframe="14 days",
        priority=2
    )
    print(f"✓ Goal 3: {goal3.goal_type.value}")
    
    # 7. Create execution plans for all goals
    print("\n8. Creating execution plans...")
    for goal in agent.get_active_goals():
        plan = agent.plan(goal)
        print(f"✓ Plan created for {goal.goal_type.value}: {len(plan)} subtasks")
    
    # 8. Get comprehensive status report
    print("\n9. Generating status report...")
    status = agent.get_status_report()
    print("=" * 80)
    print("CAMPAIGN STATUS REPORT")
    print("=" * 80)
    print(f"Client: {status['client_name']}")
    print(f"Store Type: {status['store_type']}")
    print(f"\nGoals Overview:")
    print(f"  Total Goals: {status['total_goals']}")
    print(f"  Active Goals: {status['active_goals']}")
    print(f"  Completed Goals: {status['completed_goals']}")
    
    print(f"\nCampaign Summary:")
    campaign_summary = campaign_manager.get_campaign_summary()
    print(f"  Total Campaigns: {campaign_summary['total_campaigns']}")
    print(f"  Active Campaigns: {campaign_summary['active_campaigns']}")
    print(f"  Total Budget: ${campaign_summary['total_budget']}")
    
    print("\n" + "=" * 80)
    print("Advanced example completed successfully!")
    print("Campaign is ready for execution on:", start_date.strftime("%B %d, %Y"))
    print("=" * 80)


if __name__ == "__main__":
    main()
