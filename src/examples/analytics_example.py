"""
Analytics Example: Customer Insights and Performance Analysis
"""
import os
from datetime import datetime
from src.agents import RetailMarketingAgent
from src.analytics import CustomerAnalyticsModule


def main():
    print("=" * 80)
    print("Analytics Example: Customer Insights and Performance Analysis")
    print("=" * 80)
    
    # Initialize components
    print("\n1. Initializing components...")
    agent = RetailMarketingAgent(
        client_name="Style & Grace Fashion",
        store_type="fashion",
        has_online_store=True,
        location="Los Angeles, CA"
    )
    
    analytics = CustomerAnalyticsModule()
    
    store_context = {
        "name": agent.client_name,
        "type": agent.store_type,
        "location": agent.location
    }
    
    print("✓ Components initialized")
    
    # Sample sales data
    sales_data = {
        "total_revenue": 125000,
        "total_transactions": 1250,
        "average_basket_value": 100,
        "top_categories": {
            "dresses": 35000,
            "accessories": 28000,
            "shoes": 22000,
            "outerwear": 20000,
            "tops": 20000
        },
        "customer_segments": {
            "new_customers": 450,
            "returning_customers": 800
        },
        "online_vs_instore": {
            "online": 75000,
            "instore": 50000
        }
    }
    
    # 1. Analyze sales data
    print("\n2. Analyzing sales data for Q4 2025...")
    sales_analysis = analytics.analyze_sales_data(
        sales_data=sales_data,
        time_period="Q4 2025 (Oct-Dec)",
        store_context=store_context
    )
    print("✓ Sales analysis completed")
    print("\n--- SALES ANALYSIS ---")
    print(sales_analysis['analysis'][:500] + "...\n")
    
    # Sample customer data
    customer_data = [
        {"id": i, "total_purchases": (i % 10) + 1, "total_spend": (i % 10) * 150}
        for i in range(1, 501)
    ]
    
    # 2. Customer segmentation
    print("\n3. Performing customer segmentation...")
    segmentation = analytics.segment_customers(
        customer_data=customer_data,
        segmentation_criteria="RFM (Recency, Frequency, Monetary value)",
        store_context=store_context
    )
    print("✓ Customer segmentation completed")
    print(f"  Total customers analyzed: {segmentation['total_customers']}")
    print("\n--- CUSTOMER SEGMENTS ---")
    print(segmentation['segmentation'][:500] + "...\n")
    
    # Sample transaction data
    transaction_data = [
        {"transaction_id": i, "items": (i % 3) + 1, "total": (i % 5) * 75}
        for i in range(1, 1001)
    ]
    
    # 3. Shopping pattern analysis
    print("\n4. Analyzing shopping patterns...")
    patterns = analytics.analyze_shopping_patterns(
        transaction_data=transaction_data,
        store_context=store_context
    )
    print("✓ Shopping pattern analysis completed")
    print(f"  Transactions analyzed: {patterns['transactions_analyzed']}")
    print("\n--- SHOPPING PATTERNS ---")
    print(patterns['pattern_analysis'][:500] + "...\n")
    
    # Sample feedback data
    feedback_data = [
        {"rating": 5, "comment": "Great experience"},
        {"rating": 4, "comment": "Good quality"},
        {"rating": 5, "comment": "Love the collection"},
        {"rating": 3, "comment": "Average service"},
        {"rating": 4, "comment": "Nice products"}
    ] * 20
    
    # 4. Process customer feedback
    print("\n5. Processing customer feedback...")
    feedback_analysis = analytics.process_customer_feedback(
        feedback_data=feedback_data,
        feedback_type="reviews",
        store_context=store_context
    )
    print("✓ Feedback analysis completed")
    print(f"  Feedback items processed: {feedback_analysis['items_processed']}")
    print("\n--- FEEDBACK ANALYSIS ---")
    print(feedback_analysis['feedback_analysis'][:500] + "...\n")
    
    # Sample customer profile for CLV prediction
    customer_profile = {
        "id": "CUST_12345",
        "first_purchase_date": "2025-06-15",
        "total_purchases": 8,
        "total_spent": 1200,
        "average_order_value": 150,
        "last_purchase_date": "2025-12-20",
        "favorite_category": "dresses",
        "engagement_score": 0.85
    }
    
    # 5. Predict customer lifetime value
    print("\n6. Predicting customer lifetime value...")
    clv_prediction = analytics.predict_customer_lifetime_value(
        customer_profile=customer_profile,
        store_context=store_context
    )
    print("✓ CLV prediction completed")
    print(f"  Customer ID: {clv_prediction['customer_id']}")
    print("\n--- CLV PREDICTION ---")
    print(clv_prediction['prediction'][:500] + "...\n")
    
    # Performance metrics
    performance_metrics = {
        "revenue": {
            "current": 125000,
            "previous": 95000,
            "target": 150000
        },
        "customers": {
            "new": 450,
            "returning": 800,
            "total": 1250
        },
        "conversion_rate": 0.18,
        "average_order_value": 100,
        "customer_satisfaction": 4.3,
        "marketing_spend": 15000,
        "roi": 733
    }
    
    # 6. Generate performance report
    print("\n7. Generating comprehensive performance report...")
    report = analytics.generate_performance_report(
        metrics=performance_metrics,
        comparison_period="Q3 2025",
        store_context=store_context
    )
    print("✓ Performance report generated")
    print("\n" + "=" * 80)
    print("PERFORMANCE REPORT")
    print("=" * 80)
    print(report['report'][:800] + "...\n")
    
    # Set an analytics goal
    print("\n8. Setting an analytics goal...")
    goal = agent.set_goal(
        goal_type="analytics_insights",
        target="Generate actionable insights to improve customer retention by 20%",
        timeframe="30 days",
        description="Deep dive analytics to understand customer behavior and retention drivers"
    )
    print(f"✓ Analytics goal set: {goal.id}")
    
    print("\n" + "=" * 80)
    print("Analytics example completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
