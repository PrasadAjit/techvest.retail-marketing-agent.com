"""
Basic Example: Getting Started with Retail Marketing Agent
"""
import os
from datetime import datetime, timedelta
from src.agents import RetailMarketingAgent

# Set up your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def main():
    print("=" * 60)
    print("Retail Marketing Agent - Basic Example")
    print("=" * 60)
    
    # Initialize the agent
    print("\n1. Initializing Retail Marketing Agent...")
    agent = RetailMarketingAgent(
        client_name="Fashion Forward Boutique",
        store_type="fashion",
        has_online_store=True,
        location="Downtown Seattle"
    )
    print(f"✓ Agent initialized for {agent.client_name}")
    
    # Set a customer acquisition goal
    print("\n2. Setting a customer acquisition goal...")
    goal = agent.set_goal(
        goal_type="customer_acquisition",
        target="Increase foot traffic by 25% and acquire 500 new customers",
        timeframe="30 days",
        description="Holiday season customer acquisition campaign",
        metrics={
            "target_new_customers": 500,
            "target_foot_traffic_increase": 0.25,
            "target_conversion_rate": 0.15
        },
        priority=1
    )
    print(f"✓ Goal set: {goal.description}")
    print(f"  Goal ID: {goal.id}")
    print(f"  Type: {goal.goal_type.value}")
    print(f"  Status: {goal.status.value}")
    
    # Create execution plan
    print("\n3. Creating execution plan...")
    subtasks = agent.plan(goal)
    print(f"✓ Plan created with {len(subtasks)} subtasks:")
    for i, task in enumerate(subtasks, 1):
        print(f"   {i}. {task.get('name', 'Task')}")
    
    # Execute the goal
    print("\n4. Executing the goal...")
    results = agent.execute(goal)
    print(f"✓ Execution completed")
    print(f"  Status: {results['status']}")
    print(f"  Goals executed: {results['goals_executed']}")
    
    # Display execution results
    if results['results']:
        result = results['results'][0]
        print(f"\n5. Execution Results:")
        print(f"  Goal Type: {result['goal_type']}")
        execution_data = result['execution']
        print(f"  Strategy: {execution_data.get('strategy', 'N/A')}")
        print(f"  Message: {execution_data.get('message', 'N/A')}")
    
    # Get status report
    print("\n6. Status Report:")
    status = agent.get_status_report()
    print(f"  Client: {status['client_name']}")
    print(f"  Store Type: {status['store_type']}")
    print(f"  Total Goals: {status['total_goals']}")
    print(f"  Active Goals: {status['active_goals']}")
    print(f"  Completed Goals: {status['completed_goals']}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
