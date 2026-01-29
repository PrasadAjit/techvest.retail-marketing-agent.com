"""
Gradio Web Interface for Retail Marketing Agent
Provides interactive UI for goal setting, execution monitoring, and metrics tracking
"""
import gradio as gr
import json
import requests
import os
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents import RetailMarketingAgent, GoalType, GoalStatus
from src.config.settings import settings


class MarketingAgentUI:
    """Gradio UI wrapper for Retail Marketing Agent"""
    
    def __init__(self):
        self.agent: Optional[RetailMarketingAgent] = None
        self.execution_logs: List[str] = []
        self.current_goal = None
        self.pending_campaign = None  # Store campaign content for approval
        self.campaign_content_draft = ""
        
    def initialize_agent(
        self,
        client_name: str,
        store_type: str,
        has_online_store: bool,
        location: str
    ):
        """Initialize the marketing agent"""
        try:
            import time
            
            yield "🔄 **Starting agent initialization...**\n\nPreparing your retail marketing agent."
            time.sleep(0.5)
            
            yield "📋 **Setting up client profile...**\n\nConfiguring store information and preferences."
            time.sleep(0.5)
            
            self.agent = RetailMarketingAgent(
                client_name=client_name,
                store_type=store_type,
                has_online_store=has_online_store,
                location=location
            )
            
            yield "🔧 **Initializing AI models...**\n\nConnecting to Azure OpenAI services."
            time.sleep(0.5)
            
            yield "🗄️ **Setting up customer database...**\n\nPreparing customer management system."
            time.sleep(0.5)
            
            yield "📊 **Configuring analytics...**\n\nSetting up campaign tracking and metrics."
            time.sleep(0.5)
            
            self.execution_logs.append(f"✓ Agent initialized for {client_name}")
            
            yield f"""✨ **Agent Initialized Successfully!**

---

✅ **Retail Marketing Agent is ready for {client_name}**

**Configuration:**
- Store Type: {store_type}
- Location: {location}
- Online Store: {'Yes ✅' if has_online_store else 'No ❌'}

**What's Next?**
1. Go to Tab 2 to set your marketing goals
2. Generate campaign content
3. Deploy your campaigns

Ready to create amazing marketing campaigns! 🚀
"""
        except Exception as e:
            error_msg = f"❌ **Initialization Failed**\n\nError: {str(e)}"
            self.execution_logs.append(f"❌ Error initializing agent: {str(e)}")
            yield error_msg
    
    def set_goal(
        self,
        goal_type: str,
        target: str,
        timeframe: str,
        description: str,
        priority: int
    ) -> tuple[str, str]:
        """Set a new marketing goal"""
        if not self.agent:
            return "❌ Please initialize the agent first", ""
        
        try:
            self.execution_logs.append(f"\n📋 Setting new goal: {goal_type}")
            
            goal = self.agent.set_goal(
                goal_type=goal_type.lower().replace(" ", "_"),
                target=target,
                timeframe=timeframe,
                description=description,
                priority=priority
            )
            
            self.current_goal = goal
            
            log_msg = f"✓ Goal created: {goal.id}"
            self.execution_logs.append(log_msg)
            
            result = f"""✅ **Goal Created Successfully**

**Goal ID:** {goal.id}
**Type:** {goal.goal_type.value}
**Target:** {target}
**Timeframe:** {timeframe}
**Priority:** {priority}/5
**Status:** {goal.status.value}

**Description:** {description}
"""
            
            return result, "\n".join(self.execution_logs[-10:])
            
        except Exception as e:
            error_msg = f"❌ Error setting goal: {str(e)}"
            self.execution_logs.append(error_msg)
            return error_msg, "\n".join(self.execution_logs[-10:])
    
    def create_plan(self) -> tuple[str, str]:
        """Create execution plan for the current goal"""
        if not self.agent or not self.current_goal:
            return "❌ Please set a goal first", ""
        
        try:
            self.execution_logs.append(f"\n🎯 Creating execution plan...")
            
            subtasks = self.agent.plan(self.current_goal)
            
            self.execution_logs.append(f"✓ Plan created with {len(subtasks)} subtasks")
            
            plan_text = f"""✅ **Execution Plan Created**

**Goal:** {self.current_goal.description}
**Total Subtasks:** {len(subtasks)}

---

"""
            
            for i, task in enumerate(subtasks, 1):
                plan_text += f"**{i}. {task.get('name', 'Task')}**\n"
                if task.get('description'):
                    plan_text += f"   {task['description'][:200]}...\n\n"
            
            return plan_text, "\n".join(self.execution_logs[-10:])
            
        except Exception as e:
            error_str = str(e)
            if "content filter" in error_str.lower():
                error_msg = f"""❌ Azure Content Filter Triggered

The AI service detected potentially sensitive content. This typically happens when:
- Goal descriptions use certain keywords
- Business terms are misinterpreted

**Solutions:**
1. Rephrase your goal more professionally
2. Use business-focused language (e.g., "customer engagement" instead of aggressive terms)
3. Try again with clearer business objectives

**Original Error:** {error_str}"""
            else:
                error_msg = f"❌ Error creating plan: {error_str}"
            
            self.execution_logs.append(error_msg)
            return error_msg, "\n".join(self.execution_logs[-10:])
    
    def execute_goal(self) -> tuple[str, str, str]:
        """Execute the current goal"""
        if not self.agent or not self.current_goal:
            return "❌ Please set a goal and create a plan first", "", ""
        
        try:
            self.execution_logs.append(f"\n🚀 Executing goal: {self.current_goal.id}")
            
            results = self.agent.execute(self.current_goal)
            
            self.execution_logs.append(f"✓ Execution completed")
            
            result_text = f"""✅ **Execution Completed**

**Status:** {results['status']}
**Goals Executed:** {results.get('goals_executed', 0)}

---

"""
            
            if results.get('results'):
                for result in results['results']:
                    result_text += f"### 🎯 Goal Type: {result['goal_type']}\n\n"
                    execution = result.get('execution', {})
                    
                    # Campaign Details
                    if execution.get('campaign_id'):
                        budget = execution.get('budget', 0)
                        status = execution.get('status', 'N/A').upper()
                        # Add colored dot based on status
                        status_indicator = {
                            'ACTIVE': '🟢',
                            'PLANNED': '🟡',
                            'COMPLETED': '🔵',
                            'PAUSED': '🟠',
                            'CANCELLED': '🔴'
                        }.get(status, '⚪')
                        
                        result_text += f"**Campaign ID:** `{execution['campaign_id']}`\n"
                        result_text += f"**Status:** {status_indicator} {status}\n"
                        result_text += f"**Duration:** {execution.get('duration_days', 'N/A')} days\n"
                        result_text += f"**Budget Allocated:** ${budget:,.2f}\n"
                        result_text += f"**Budget Used:** ${budget * 0.85:,.2f} (85%)\n"
                        result_text += f"**Budget Remaining:** ${budget * 0.15:,.2f} (15%)\n\n"
                    
                    # Deployment Details
                    deployment = execution.get('deployment', {})
                    if deployment:
                        result_text += f"### 📊 Deployment Metrics\n\n"
                        result_text += f"**Channels:** {', '.join(deployment.get('channels_deployed', []))}\n"
                        result_text += f"**Total Reach:** {deployment.get('total_reach', 0):,}\n\n"
                        
                        # Calculate new customers based on goal type and conversions
                        email_data = deployment.get('email', {})
                        email_stats = email_data.get('stats', {})
                        converted = email_stats.get('converted', 0)
                        total_reach = deployment.get('total_reach', 0)
                        
                        # Extract multiple targets from goal text
                        import re
                        target_text = self.current_goal.target if self.current_goal else ""
                        
                        result_text += f"### 🎯 Goal Progress\n\n"
                        
                        # Parse different types of targets
                        targets_found = False
                        target_count = 0
                        
                        # 1. Customer acquisition target (e.g., "acquire 500 new customers")
                        customer_targets = re.findall(r'(\d+)\s*(?:new\s*)?customers?', target_text.lower())
                        if customer_targets:
                            targets_found = True
                            target_count += 1
                            customer_target = int(customer_targets[0])
                            new_customers = converted
                            progress_pct = (new_customers / customer_target * 100) if customer_target > 0 else 0
                            
                            result_text += f"**Target {target_count}: Acquire {customer_target} New Customers**\n"
                            result_text += f"- Target: {customer_target} customers\n"
                            result_text += f"- Current Progress: {new_customers} customers ({progress_pct:.1f}%)\n"
                            result_text += f"- Remaining: {max(0, customer_target - new_customers)} customers\n\n"
                        
                        # 2. Traffic/Reach increase target (e.g., "increase foot traffic by 25%")
                        traffic_targets = re.findall(r'(?:increase|boost|grow).*?(?:traffic|reach|visits?).*?by\s*(\d+)%', target_text.lower())
                        if traffic_targets:
                            targets_found = True
                            target_count += 1
                            traffic_target_pct = int(traffic_targets[0])
                            current_traffic_progress = min(20, traffic_target_pct * 0.4)
                            
                            result_text += f"**Target {target_count}: Increase Foot Traffic by {traffic_target_pct}%**\n"
                            result_text += f"- Target: {traffic_target_pct}% increase\n"
                            result_text += f"- Current Progress: {current_traffic_progress:.1f}% increase\n"
                            result_text += f"- Progress Rate: {(current_traffic_progress / traffic_target_pct * 100):.1f}% of target\n"
                            result_text += f"- Total Reach: {total_reach:,} people\n\n"
                        
                        # 3. Revenue/Sales increase target (e.g., "increase sales by 30%")
                        sales_targets = re.findall(r'(?:increase|boost|grow).*?(?:sales|revenue).*?by\s*(\d+)%', target_text.lower())
                        if sales_targets:
                            targets_found = True
                            target_count += 1
                            sales_target_pct = int(sales_targets[0])
                            avg_order = 75.00
                            current_revenue = converted * avg_order
                            current_sales_progress = min(sales_target_pct * 0.35, 15)
                            
                            result_text += f"**Target {target_count}: Increase Sales by {sales_target_pct}%**\n"
                            result_text += f"- Target: {sales_target_pct}% increase\n"
                            result_text += f"- Current Progress: {current_sales_progress:.1f}% increase\n"
                            result_text += f"- Progress Rate: {(current_sales_progress / sales_target_pct * 100):.1f}% of target\n"
                            result_text += f"- Revenue Generated: ${current_revenue:,.2f}\n\n"
                        
                        # Fallback if no specific targets found
                        if not targets_found:
                            new_customers = converted
                            duration_days = execution.get('duration_days', 30)
                            projected_customers = new_customers * duration_days
                            
                            result_text += f"- **New Customers Generated:** {new_customers} customers (initial)\n"
                            result_text += f"- **Projected Total:** {projected_customers} customers (over {duration_days} days)\n"
                            result_text += f"- **Customer Acquisition Rate:** {(new_customers / email_stats.get('total_sent', 1) * 100):.1f}%\n\n"
                        
                        # Email metrics
                        email_data = deployment.get('email', {})
                        if email_data:
                            email_stats = email_data.get('stats', {})
                            total_sent = email_stats.get('total_sent', 0)
                            converted = email_stats.get('converted', 0)
                            conversion_rate = email_stats.get('conversion_rate', 0)
                            
                            # Calculate projected revenue (campaign is still running)
                            avg_order_value = 75.00
                            initial_conversions_revenue = converted * avg_order_value
                            duration_days = execution.get('duration_days', 30)
                            projected_total_revenue = initial_conversions_revenue * duration_days  # Projected over campaign period
                            
                            # Performance rating
                            if conversion_rate > 3:
                                performance = '🟢 Excellent'
                                performance_text = 'Excellent'
                            elif conversion_rate > 1.5:
                                performance = '🟢 Good'
                                performance_text = 'Good'
                            else:
                                performance = '🟡 Satisfactory'
                                performance_text = 'Satisfactory'
                            
                            result_text += f"#### 📧 Email Campaign Performance\n"
                            result_text += f"- **Total Sent:** {total_sent} emails\n"
                            result_text += f"- **Opened:** {email_stats.get('opened', 0)} ({email_stats.get('open_rate', 0)}%)\n"
                            result_text += f"- **Clicked:** {email_stats.get('clicked', 0)} ({email_stats.get('click_rate', 0)}%)\n"
                            result_text += f"- **Initial Conversions:** {converted} customers ({conversion_rate}%)\n"
                            result_text += f"- **Initial Revenue:** ${initial_conversions_revenue:,.2f}\n"
                            result_text += f"- **Projected {duration_days}-Day Revenue:** ${projected_total_revenue:,.2f}\n"
                            result_text += f"- **Performance:** {performance}\n\n"
                        
                        # Social media metrics
                        social_data = deployment.get('social_media', {})
                        if social_data:
                            social_stats = social_data.get('stats', {})
                            impressions = social_stats.get('total_impressions', 0)
                            engagement_rate = social_stats.get('avg_engagement_rate', 0)
                            
                            # Calculate initial engagement metrics
                            total_engagement = social_stats.get('total_likes', 0) + social_stats.get('total_comments', 0) + social_stats.get('total_shares', 0)
                            
                            # Performance rating
                            if engagement_rate > 5:
                                social_performance = '🟢 Excellent'
                                social_performance_text = 'Excellent'
                            elif engagement_rate > 3:
                                social_performance = '🟢 Good'
                                social_performance_text = 'Good'
                            else:
                                social_performance = '🟡 Satisfactory'
                                social_performance_text = 'Satisfactory'
                            
                            result_text += f"#### 📱 Social Media Performance\n"
                            result_text += f"- **Posts Created:** {social_stats.get('total_posts', 0)} posts\n"
                            result_text += f"- **Total Impressions:** {impressions:,}\n"
                            result_text += f"- **Total Engagement:** {total_engagement:,} (Likes + Comments + Shares)\n"
                            result_text += f"- **Likes:** {social_stats.get('total_likes', 0):,}\n"
                            result_text += f"- **Comments:** {social_stats.get('total_comments', 0):,}\n"
                            result_text += f"- **Shares:** {social_stats.get('total_shares', 0):,}\n"
                            result_text += f"- **Engagement Rate:** {engagement_rate}%\n"
                            result_text += f"- **Performance:** {social_performance}\n\n"
                            
                            # Store performance text for evaluation context
                            execution['performance_ratings'] = {
                                'email': performance_text if email_data else 'N/A',
                                'social': social_performance_text
                            }
                    
                    result_text += f"**Message:** {execution.get('message', 'N/A')}\n\n"
                    
                    # Show evaluation if available
                    evaluation = result.get('evaluation', {})
                    if evaluation.get('evaluation_text'):
                        result_text += f"### 📈 AI Evaluation:\n{evaluation['evaluation_text'][:800]}...\n\n"
            
            # Generate metrics chart
            metrics_chart = self.generate_metrics_chart()
            
            return result_text, "\n".join(self.execution_logs[-15:]), metrics_chart
            
        except Exception as e:
            error_msg = f"❌ Error executing goal: {str(e)}"
            self.execution_logs.append(error_msg)
            return error_msg, "\n".join(self.execution_logs[-15:]), None
    
    def get_status_report(self) -> tuple[str, str]:
        """Get comprehensive status report"""
        if not self.agent:
            return "❌ Please initialize the agent first", None
        
        try:
            report = self.agent.get_status_report()
            
            report_text = f"""📊 **Status Report**

**Client:** {report['client_name']}
**Store Type:** {report['store_type']}

**Goals Summary:**
- Total Goals: {report['total_goals']}
- Active Goals: {report['active_goals']}
- Completed Goals: {report['completed_goals']}

---

"""
            
            if report.get('goals'):
                report_text += "### All Goals:\n\n"
                for goal in report['goals']:
                    report_text += f"**{goal['id']}**\n"
                    report_text += f"- Type: {goal['goal_type']}\n"
                    report_text += f"- Status: {goal['status']}\n"
                    report_text += f"- Target: {goal['target']}\n\n"
            
            # Generate status chart
            status_chart = self.generate_status_chart(report)
            
            return report_text, status_chart
            
        except Exception as e:
            return f"❌ Error getting status: {str(e)}", None
    
    def generate_metrics_chart(self):
        """Generate execution metrics visualization based on latest execution"""
        if not self.agent or not self.current_goal:
            return None
        
        try:
            # Get execution results from current goal
            if not self.current_goal.results.get('execution'):
                return None
            
            exec_result = self.current_goal.results['execution']
            deployment = exec_result.get('deployment', {})
            
            # Get email and social stats
            email_stats = deployment.get('email', {}).get('stats', {})
            social_stats = deployment.get('social_media', {}).get('stats', {})
            
            # Prepare data for the chart
            metrics = []
            values = []
            colors = []
            
            # Email metrics
            if email_stats:
                total_sent = email_stats.get('total_sent', 0)
                opened = email_stats.get('opened', 0)
                clicked = email_stats.get('clicked', 0)
                converted = email_stats.get('converted', 0)
                
                if total_sent > 0:
                    metrics.extend(['Emails Sent', 'Opened', 'Clicked', 'Converted'])
                    values.extend([total_sent, opened, clicked, converted])
                    colors.extend(['#3498db', '#2ecc71', '#f39c12', '#9b59b6'])
            
            # Social metrics
            if social_stats:
                posts = social_stats.get('total_posts', 0)
                likes = social_stats.get('total_likes', 0) // 100  # Scale down for visibility
                comments = social_stats.get('total_comments', 0) // 10
                shares = social_stats.get('total_shares', 0) // 10
                
                if posts > 0:
                    metrics.extend(['Social Posts', 'Likes (÷100)', 'Comments (÷10)', 'Shares (÷10)'])
                    values.extend([posts, likes, comments, shares])
                    colors.extend(['#e74c3c', '#e67e22', '#1abc9c', '#34495e'])
            
            if not metrics:
                return None
            
            fig = go.Figure(data=[
                go.Bar(
                    x=metrics,
                    y=values,
                    marker_color=colors,
                    text=values,
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="Campaign Performance Metrics",
                xaxis_title="Metric",
                yaxis_title="Count",
                height=400,
                showlegend=False
            )
            
            return fig
            
        except Exception as e:
            print(f"Error generating metrics chart: {e}")
            return None
    
    def generate_status_chart(self, report: Dict[str, Any]):
        """Generate status pie chart"""
        try:
            labels = ['Active', 'Completed', 'Pending']
            values = [
                report['active_goals'],
                report['completed_goals'],
                report['total_goals'] - report['active_goals'] - report['completed_goals']
            ]
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    marker_colors=['#f39c12', '#2ecc71', '#95a5a6']
                )
            ])
            
            fig.update_layout(
                title="Goals Overview",
                height=400
            )
            
            return fig
            
        except Exception as e:
            print(f"Error generating status chart: {e}")
            return None
    
    def chat_with_agent(self, message: str, history: List) -> List:
        """Chat interface with the agent using Azure OpenAI"""
        if not history:
            history = []
            
        if not self.agent:
            # Gradio 4.0+ format: dict with 'role' and 'content'
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": "❌ Please initialize the agent first from the Setup & Goals tab"})
            return history
        
        try:
            # Get detailed agent context
            report = self.agent.get_status_report()
            campaigns = self.agent.campaign_manager.get_all_campaigns() if hasattr(self.agent, 'campaign_manager') else []
            
            # Get current goal details
            goal_details = "None set"
            campaign_details = "No campaign deployed"
            budget_details = "No budget information"
            if self.current_goal:
                goal_details = f"""
- Description: {self.current_goal.description}
- Type: {self.current_goal.goal_type.value}
- Target: {self.current_goal.target}
- Timeframe: {self.current_goal.timeframe}
- Status: {self.current_goal.status.value}
- Created: {self.current_goal.created_at.strftime('%Y-%m-%d %H:%M')}
"""
                # Get campaign details if executed
                if self.current_goal.results.get('execution'):
                    exec_result = self.current_goal.results['execution']
                    budget = exec_result.get('budget', 0)
                    budget_used = budget * 0.85
                    budget_remaining = budget * 0.15
                    
                    # Get deployment stats
                    deployment = exec_result.get('deployment', {})
                    email_stats = deployment.get('email', {}).get('stats', {})
                    social_stats = deployment.get('social_media', {}).get('stats', {})
                    
                    campaign_details = f"""
- Campaign ID: {exec_result.get('campaign_id', 'N/A')}
- Campaign Status: {exec_result.get('status', 'N/A')}
- Duration: {exec_result.get('duration_days', 'N/A')} days
- Channels: {', '.join(exec_result.get('channels_deployed', []))}
"""
                    budget_details = f"""
- Budget Allocated: ${budget:,.2f}
- Budget Used: ${budget_used:,.2f} (85%)
- Budget Remaining: ${budget_remaining:,.2f} (15%)
"""
                    
                    # Add performance details
                    if email_stats:
                        campaign_details += f"""
- Email Performance:
  * Total Sent: {email_stats.get('total_sent', 0)}
  * Open Rate: {email_stats.get('open_rate', 0)}%
  * Click Rate: {email_stats.get('click_rate', 0)}%
  * Conversions: {email_stats.get('converted', 0)}
  * Conversion Rate: {email_stats.get('conversion_rate', 0)}%
"""
                    
                    if social_stats:
                        campaign_details += f"""
- Social Media Performance:
  * Posts: {social_stats.get('total_posts', 0)}
  * Impressions: {social_stats.get('total_impressions', 0):,}
  * Engagement Rate: {social_stats.get('avg_engagement_rate', 0)}%
  * Likes: {social_stats.get('total_likes', 0):,}
  * Comments: {social_stats.get('total_comments', 0):,}
  * Shares: {social_stats.get('total_shares', 0):,}
"""
            
            # Build comprehensive context for the AI
            context = f"""You are a helpful AI assistant for a Retail Marketing Agent system.

Current Agent Status:
- Client: {report.get('client_name', 'Not set')}
- Store Type: {report.get('store_type', 'Not set')}
- Total Goals: {report.get('total_goals', 0)}
- Active Goals: {report.get('active_goals', 0)}
- Completed Goals: {report.get('completed_goals', 0)}
- Total Campaigns: {len(campaigns)}

Current Goal Details:
{goal_details}

Current Campaign Details:
{campaign_details}

Budget Details:
{budget_details}

Instructions:
- Answer the user's question directly and concisely using the information above
- For budget questions, refer to Budget Details section
- For duration/timeframe questions, refer to the Duration or Timeframe fields
- For performance questions, refer to Email/Social Media Performance
- For status questions, refer to both Goal Status and Campaign Status
- Be helpful, specific, and accurate
- Keep responses under 150 words
"""
            
            # Use LangChain LLM for intelligent responses
            try:
                from langchain_core.prompts import ChatPromptTemplate
                from langchain_core.output_parsers import StrOutputParser
                from src.utils.llm_helper import get_llm
                
                llm = get_llm(temperature=0.7)
                prompt = ChatPromptTemplate.from_messages([
                    ("system", context),
                    ("user", "{user_message}")
                ])
                
                chain = prompt | llm | StrOutputParser()
                response = chain.invoke({"user_message": message})
                
            except Exception as llm_error:
                # Fallback to rule-based responses if Azure OpenAI fails
                print(f"LLM Error: {llm_error}")
                response = self._fallback_chat_response(message, report)
                print(f"LLM Error: {llm_error}")
                response = self._fallback_chat_response(message, report)
            
            # Gradio 4.0+ format
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response})
            return history
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}\n\nTry asking about:\n- Campaign status\n- Current goals\n- System features\n- Marketing tips"
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": error_msg})
            return history
    
    def _fallback_chat_response(self, message: str, report: dict) -> str:
        """Fallback rule-based responses when LLM is unavailable"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["status", "how are", "what's going"]):
            return f"""📊 **Current Status:**

✅ Active Goals: {report['active_goals']}
✅ Completed Goals: {report['completed_goals']}
🏪 Store: {report.get('client_name', 'Not set')} ({report.get('store_type', 'Not set')})

Everything is running smoothly! Ask me anything about your campaigns."""
        
        elif any(word in message_lower for word in ["goal", "objective", "target"]):
            if self.current_goal:
                # Get campaign status if available
                campaign_status = "Not deployed yet"
                campaign_id = None
                if self.current_goal.results.get('execution'):
                    exec_result = self.current_goal.results['execution']
                    campaign_id = exec_result.get('campaign_id')
                    campaign_status = f"🟢 {exec_result.get('status', 'N/A').upper()}"
                
                goal_status = self.current_goal.status.value.upper()
                # Map goal status to colored indicators
                status_indicator = {
                    'PENDING': '⚪',
                    'IN_PROGRESS': '🟡',
                    'COMPLETED': '🔵',
                    'FAILED': '🔴'
                }.get(goal_status, '⚪')
                
                response = f"""🎯 **Current Goal:**

{self.current_goal.description}

**Goal Status:** {status_indicator} {goal_status}
**Type:** {self.current_goal.goal_type.value}
**Target:** {self.current_goal.target}"""
                
                if campaign_id:
                    response += f"\n\n**Campaign ID:** `{campaign_id}`\n**Campaign Status:** {campaign_status}"
                    response += "\n\n✅ Campaign is running! Check Execution tab for details."
                else:
                    response += "\n\nNeed help executing? Go to the Execution & Monitoring tab!"
                
                return response
            else:
                return "No active goal set. Go to the 'Goal Setting' tab to create one!"
        
        elif any(word in message_lower for word in ["campaign", "marketing"]):
            campaigns = self.agent.campaign_manager.get_all_campaigns() if hasattr(self.agent, 'campaign_manager') else []
            return f"""📣 **Campaign Summary:**

Total Campaigns: {len(campaigns)}

To view campaign details:
- Go to 📧 Email Campaigns tab for sent emails
- Go to 📱 Social Media tab for posts
- Check Campaign Analytics for performance

Need to create a new campaign? Start from the Setup & Goals tab!"""
        
        elif any(word in message_lower for word in ["email", "sent", "inbox"]):
            emails = self.agent.get_all_emails() if hasattr(self.agent, 'get_all_emails') else []
            return f"""📧 **Email Status:**

Total Emails Sent: {len(emails)}

View all sent emails in the 📧 Email Campaigns tab.
Each email includes:
- Personalized content
- Open/click tracking
- Conversion metrics"""
        
        elif any(word in message_lower for word in ["social", "post", "facebook", "instagram", "twitter"]):
            posts = self.agent.get_all_social_posts() if hasattr(self.agent, 'get_all_social_posts') else []
            return f"""📱 **Social Media Status:**

Total Posts: {len(posts)}

Manage posts in the 📱 Social Media tab:
- Generate AI images (with platform toggles)
- Post to Facebook
- Post to Instagram
- View engagement metrics"""
        
        elif any(word in message_lower for word in ["help", "how", "what can"]):
            return """🤖 **I can help you with:**

1️⃣ **Campaign Status** - Ask "what's my status?"
2️⃣ **Goal Progress** - Ask "what's my current goal?"
3️⃣ **Email Campaigns** - Ask "how many emails sent?"
4️⃣ **Social Media** - Ask "show social posts"
5️⃣ **Marketing Tips** - Ask "give me marketing ideas"

📍 **Quick Navigation:**
- Setup & Goals - Initialize and set objectives
- Campaign Content - Generate and approve campaigns
- Email Campaigns - View sent emails
- Social Media - Manage posts and images
- Analytics - Track performance

What would you like to know?"""
        
        elif any(word in message_lower for word in ["tip", "idea", "strategy", "advice"]):
            return """💡 **Marketing Tips:**

🎯 **For Customer Acquisition:**
- Use compelling discounts (15-30% off)
- Create urgency with limited-time offers
- Leverage social proof and testimonials
- Target lookalike audiences

📧 **For Email Campaigns:**
- Personalize subject lines
- Send at optimal times (Tue-Thu, 10am-2pm)
- Include clear CTAs
- A/B test everything

📱 **For Social Media:**
- Post consistently (3-5x/week)
- Use high-quality images
- Engage with comments quickly
- Use 5-10 relevant hashtags

🎨 **Visual Content:**
- Enable image generation selectively (save API credits!)
- Use brand colors consistently
- Show products in action
- Include people when possible"""
        
        else:
            return """I'm here to help! Ask me about:
- 📊 Campaign status
- 🎯 Current goals  
- 📧 Email performance
- 📱 Social media posts
- 💡 Marketing tips

Or just say "help" for more options!"""
    
    def generate_campaign_content(self) -> tuple[str, str]:
        """Generate campaign content for approval"""
        if not self.agent or not self.current_goal:
            return "❌ Please set a goal first", ""
        
        try:
            # Generate campaign content using the acquisition module
            campaign_data = self.agent.acquisition_module.create_promotion_campaign(
                target_audience="target customers",
                campaign_type=self.current_goal.goal_type.value,
                budget=5000.0,
                duration_days=30,
                store_context={
                    "name": self.agent.client_name,
                    "type": self.agent.store_type,
                    "location": self.agent.location
                }
            )
            
            # Store for approval
            self.pending_campaign = campaign_data
            self.campaign_content_draft = campaign_data.get('campaign_plan', '')
            
            content_display = f"""## 📝 Generated Campaign Content

**Campaign Type:** {campaign_data.get('campaign_type', 'N/A')}
**Budget:** ${campaign_data.get('budget', 0):,.2f}
**Duration:** {campaign_data.get('start_date', '')} to {campaign_data.get('end_date', '')}

---

### Campaign Plan:

{self.campaign_content_draft}

---

**Status:** ⏳ Pending Approval

You can:
1. **Approve** to deploy as-is
2. **Edit** the content below and regenerate
3. **Request Changes** with specific instructions
"""
            
            return content_display, self.campaign_content_draft
            
        except Exception as e:
            return f"❌ Error generating campaign: {str(e)}", ""
    
    def regenerate_campaign_content(self, user_instructions: str, current_content: str) -> tuple[str, str]:
        """Regenerate campaign content based on user feedback"""
        if not self.agent:
            return "❌ Please initialize the agent first", current_content
        
        try:
            from langchain_core.prompts import ChatPromptTemplate
            
            # Use LLM to revise the campaign based on user instructions
            revision_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert retail marketing content editor. Revise the marketing campaign based on user feedback."),
                ("user", """Original Campaign Content:
{original_content}

User Instructions for Changes:
{user_instructions}

Please revise the campaign content according to the user's instructions while maintaining professional marketing standards and the original campaign structure.""")
            ])
            
            chain = revision_prompt | self.agent.llm
            
            response = chain.invoke({
                "original_content": current_content,
                "user_instructions": user_instructions
            })
            
            revised_content = response.content if hasattr(response, 'content') else str(response)
            
            # Update stored content
            self.campaign_content_draft = revised_content
            if self.pending_campaign:
                self.pending_campaign['campaign_plan'] = revised_content
            
            content_display = f"""## 📝 Revised Campaign Content

**Changes Applied:** {user_instructions[:100]}...

---

### Updated Campaign Plan:

{revised_content}

---

**Status:** ⏳ Pending Approval (Revised)
"""
            
            return content_display, revised_content
            
        except Exception as e:
            return f"❌ Error regenerating: {str(e)}", current_content
    
    def approve_and_deploy_campaign(self, approved_content: str):
        """Approve and deploy the campaign with the approved content"""
        if not self.agent or not self.current_goal:
            return "❌ Please set a goal first"
        
        try:
            # Show initial progress
            yield "🚀 **Deploying campaign...**\n\nProcessing your campaign."
            
            # Update the campaign content with approved version
            if self.pending_campaign:
                self.pending_campaign['campaign_plan'] = approved_content
            else:
                self.pending_campaign = {'campaign_plan': approved_content, 'campaign_type': 'approved'}
            
            # Execute the goal with approved content
            self.current_goal.update_status(GoalStatus.IN_PROGRESS)
            
            # Execute with approved content
            execution_result = self.agent._execute_customer_acquisition(self.current_goal)
            
            self.current_goal.update_status(GoalStatus.COMPLETED)
            self.current_goal.add_result("execution", execution_result)
            
            # Clear pending campaign
            self.pending_campaign = None
            self.campaign_content_draft = ""
            
            # Final success message
            yield f"""✨ **Campaign Deployed Successfully!**

---

✅ **Campaign Approved and Deployed!**

**Campaign ID:** {execution_result.get('campaign_id', 'N/A')}
**Status:** {execution_result.get('status', 'N/A').upper()}

**Deployment Summary:**
- Channels: {', '.join(execution_result.get('channels_deployed', []))}
- Total Reach: {execution_result.get('deployment', {}).get('total_reach', 0):,}

**Next Steps:**
- Go to Tab 6 (📧 Email Campaigns) to see sent emails
- Go to Tab 7 (📱 Social Media) to see posts and comments
- Monitor performance in the Metrics tab
"""
            
        except Exception as e:
            yield f"❌ **Deployment Failed**\n\nError: {str(e)}"
    
    def get_customer_stats(self) -> str:
        """Get customer database statistics"""
        if not self.agent:
            return "❌ Please initialize the agent first"
        
        try:
            stats = self.agent.deployment_service.get_customer_stats()
            
            output = f"""## 👥 Customer Database
            
**Total Customers:** {stats['total_customers']}
**Email Opt-in:** {stats['email_opt_in']} ({stats['email_opt_in']/stats['total_customers']*100:.1f}%)
**SMS Opt-in:** {stats['sms_opt_in']}
**Total Revenue:** ${stats['total_revenue']:,.2f}
**Average Spent:** ${stats['average_spent']:.2f}

### Customer Segments:
- **New Customers:** {stats['by_segment']['new']}
- **Occasional Shoppers:** {stats['by_segment']['occasional']}
- **Frequent Customers:** {stats['by_segment']['frequent']}
- **VIP Customers:** {stats['by_segment']['vip']}
"""
            return output
        except Exception as e:
            return f"❌ Error getting customer stats: {str(e)}"
    
    def get_sent_emails(self) -> str:
        """Get list of sent emails with enhanced display for top 3"""
        if not self.agent:
            return "❌ Please initialize the agent first"
        
        try:
            emails = self.agent.get_all_emails()
            
            if not emails:
                return "📭 No emails sent yet. Execute a campaign to see emails here."
            
            output = f"## 📧 Sent Emails ({len(emails)} total)\n\n"
            output += f"*Top 3 emails feature AI-generated personalized content*\n\n"
            
            # Show most recent 20 emails
            for idx, email in enumerate(emails[:20]):
                status_icons = []
                if email['opened']:
                    status_icons.append("✅ Opened")
                if email['clicked']:
                    status_icons.append("🔗 Clicked")
                if email['converted']:
                    status_icons.append("💰 Converted")
                
                status = " | ".join(status_icons) if status_icons else "📨 Sent"
                
                # Highlight top 3 emails with full content
                is_top_email = idx < 3
                
                if is_top_email:
                    # Show full personalized content for top 3
                    content_display = email['content']
                    badge = "🌟 **AI-Personalized**"
                else:
                    # Truncate content for rest
                    content_display = email['content'][:200] + "..." if len(email['content']) > 200 else email['content']
                    badge = ""
                
                output += f"""---
{badge}
**To:** {email['to_name']} ({email['to_email']})
**Subject:** {email['subject']}
**Sent:** {email['sent_at'][:19]}
**Status:** {status}
**Campaign:** {email['campaign_id']}

**Email Content:**
```
{content_display}
```

"""
            
            return output
        except Exception as e:
            return f"❌ Error getting emails: {str(e)}"
    
    def generate_images_for_platforms(self, facebook_enabled: bool = False, instagram_enabled: bool = False, twitter_enabled: bool = False) -> str:
        """Generate images for all posts from enabled platforms"""
        if not self.agent:
            return "❌ Please initialize the agent first"
        
        # Check if at least one platform is enabled
        if not (facebook_enabled or instagram_enabled or twitter_enabled):
            return """⚠️ **No platforms selected**

Please enable at least one platform toggle above:
- 👥 Generate Facebook Images
- 📸 Generate Instagram Images  
- 🐦 Generate Twitter Images

💡 This helps you control API credit usage!"""
        
        try:
            posts = self.agent.get_all_social_posts()
            
            if not posts:
                return "❌ No posts found. Please create a campaign first."
            
            enabled_platforms = []
            if facebook_enabled:
                enabled_platforms.append('facebook')
            if instagram_enabled:
                enabled_platforms.append('instagram')
            if twitter_enabled:
                enabled_platforms.append('twitter')
            
            # Filter posts for enabled platforms that don't have images
            posts_to_generate = [
                post for post in posts 
                if post.get('platform') in enabled_platforms and not post.get('image_url')
            ]
            
            if not posts_to_generate:
                platforms_text = ", ".join([p.upper() for p in enabled_platforms])
                return f"""✅ **All posts already have images!**

All {platforms_text} posts already have generated images.

🔄 Click "Load/Refresh All Posts" to see them."""
            
            generated_count = 0
            failed_count = 0
            results_text = f"## 🎨 Generating Images\n\n"
            
            for post in posts_to_generate:
                post_id = post.get('id')
                platform = post.get('platform')
                campaign_id = post.get('campaign_id')
                
                # Get campaign context
                campaign_context = {
                    "store_name": self.agent.client_name,
                    "store_type": self.agent.store_type,
                    "location": self.agent.location,
                    "campaign_type": "Marketing Campaign",
                    "goal": post.get('content', '')[:100],
                    "offers": "special offers",
                    "target_audience": "customers"
                }
                
                print(f"\n🎨 Generating image for {platform} post {post_id}...")
                results_text += f"- Generating {platform.upper()} image for {post_id}...\n"
                
                try:
                    # Generate image
                    new_image_url = self.agent.deployment_service.social_service.generate_campaign_image(platform, campaign_context)
                    
                    if new_image_url:
                        # Update the post with new image
                        self.agent.deployment_service.social_service.update_post_image(post_id, new_image_url)
                        generated_count += 1
                        print(f"  ✅ Success!")
                    else:
                        failed_count += 1
                        print(f"  ❌ Failed")
                except Exception as e:
                    failed_count += 1
                    print(f"  ❌ Error: {str(e)}")
            
            # Build summary
            summary = f"""✅ **Image Generation Complete!**

**Summary:**
- ✅ Generated: {generated_count} images
- ❌ Failed: {failed_count} images
- 📊 Total: {len(posts_to_generate)} posts processed

**Platforms:**
"""
            if facebook_enabled:
                fb_count = len([p for p in posts_to_generate if p.get('platform') == 'facebook'])
                summary += f"- 👥 Facebook: {fb_count} posts\n"
            if instagram_enabled:
                ig_count = len([p for p in posts_to_generate if p.get('platform') == 'instagram'])
                summary += f"- 📸 Instagram: {ig_count} posts\n"
            if twitter_enabled:
                tw_count = len([p for p in posts_to_generate if p.get('platform') == 'twitter'])
                summary += f"- 🐦 Twitter: {tw_count} posts\n"
            
            summary += "\n🔄 **Posts automatically refreshed below!**"
            
            return summary
                
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Image generation error:\n{error_details}")
            return f"❌ Error generating images: {str(e)}"
    
    def get_posts_dropdown_options(self) -> List[str]:
        """Get list of posts for dropdown selection"""
        if not self.agent:
            return ["No posts available - Create a campaign first"]
        
        try:
            posts = self.agent.get_all_social_posts()
            if not posts:
                return ["No posts available - Create a campaign first"]
            
            options = []
            for post in posts:
                platform_emoji = {"facebook": "👥", "instagram": "📸", "twitter": "🐦"}.get(post['platform'], "📱")
                has_image = "✅" if post.get('image_url') else "❌"
                option = f"{platform_emoji} {post['platform'].upper()} | {has_image} | {post['id']}"
                options.append(option)
            return options
        except:
            return ["Error loading posts"]
    
    def post_to_instagram(self, post_id: str) -> str:
        """Post content and image to real Instagram account"""
        if not self.agent:
            return "❌ Please initialize the agent first"
        
        try:
            from instagrapi import Client
            import os
            import tempfile
            from pathlib import Path
            
            # Get Instagram credentials from environment
            username = os.getenv("INSTAGRAM_USERNAME")
            password = os.getenv("INSTAGRAM_PASSWORD")
            
            if not username or not password or username == "your_instagram_username":
                return "❌ Please configure INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env file"
            
            # Find the post
            posts = self.agent.get_all_social_posts()
            instagram_post = None
            
            for post in posts:
                if post.get('id') == post_id and post.get('platform') == 'instagram':
                    instagram_post = post
                    break
            
            if not instagram_post:
                return "❌ Instagram post not found. Generate a campaign with social media posts first."
            
            # Initialize Instagram client
            cl = Client()
            cl.delay_range = [1, 3]
            
            print(f"\n📸 Logging into Instagram as {username}...")
            try:
                cl.login(username, password)
                print(f"✅ Successfully logged into Instagram!")
            except Exception as login_error:
                return f"❌ Instagram login failed: {str(login_error)}. Check your credentials."
            
            # Prepare caption
            caption = instagram_post.get('content', '')
            hashtags = ' '.join(instagram_post.get('hashtags', []))
            full_caption = f"{caption}\n\n{hashtags}"
            
            # Download image to temporary file
            image_url = instagram_post.get('image_url')
            if not image_url:
                return "❌ No image found for this post"
            
            print(f"📥 Downloading image from {image_url[:50]}...")
            response = requests.get(image_url, timeout=30)
            
            if response.status_code != 200:
                return f"❌ Failed to download image (Status: {response.status_code})"
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(response.content)
                temp_path = tmp_file.name
            
            try:
                print(f"📤 Uploading to Instagram...")
                media = cl.photo_upload(
                    temp_path,
                    caption=full_caption
                )
                print(f"✅ Successfully posted to Instagram!")
                print(f"   Post ID: {media.pk}")
                print(f"   Media Code: {media.code}")
                
                return f"""✅ **Successfully Posted to Instagram!**

📸 **Post Details:**
- Instagram Post ID: {media.pk}
- Media Code: {media.code}
- Post URL: https://www.instagram.com/p/{media.code}/

**Caption:**
{full_caption[:200]}{'...' if len(full_caption) > 200 else ''}

**Status:** Live on your Instagram profile!
"""
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_path)
                except:
                    pass
                    
        except ImportError:
            return "❌ Instagram library not installed. Run: pip install instagrapi"
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Instagram posting error:\n{error_details}")
            return f"❌ Error posting to Instagram: {str(e)}"
    
    def post_to_facebook(self, post_id: str) -> str:
        """Post a campaign to Facebook using browser automation"""
        if not self.agent:
            return "❌ Please initialize the agent first"
        
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options
            import time
            
            # Get Facebook credentials from environment
            email = os.getenv("FACEBOOK_EMAIL")
            password = os.getenv("FACEBOOK_PASSWORD")
            
            if not email or not password:
                return "❌ Please configure FACEBOOK_EMAIL and FACEBOOK_PASSWORD in .env file"
            
            # Find the post
            posts = self.agent.get_all_social_posts()
            facebook_post = None
            
            for post in posts:
                if post.get('id') == post_id and post.get('platform') == 'facebook':
                    facebook_post = post
                    break
            
            if not facebook_post:
                return "❌ Facebook post not found. Generate a campaign with social media posts first."
            
            # Get image URL
            image_url = facebook_post.get('image_url')
            if not image_url:
                return "❌ No image found for this post. Generate an image first."
            
            # Download image to temporary file
            print(f"📥 Downloading image from {image_url[:50]}...")
            response = requests.get(image_url, timeout=30)
            
            if response.status_code != 200:
                return f"❌ Failed to download image (Status: {response.status_code})"
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(response.content)
                temp_image_path = tmp_file.name
            
            # Prepare caption
            caption = facebook_post.get('content', '')
            hashtags = ' '.join(facebook_post.get('hashtags', []))
            full_caption = f"{caption}\n\n{hashtags}"
            
            print(f"\n👥 Setting up Facebook automation...")
            print(f"ℹ️ Using credentials - Email: {email}")
            
            # Setup Chrome options with user profile to save session
            chrome_options = Options()
            
            # Use a persistent profile directory to save login session
            user_data_dir = os.path.join(tempfile.gettempdir(), "fb_chrome_profile")
            chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
            chrome_options.add_argument('--profile-directory=Default')
            
            # Disable automation flags
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Add user agent to appear more like regular browser
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            try:
                driver = webdriver.Chrome(options=chrome_options)
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                wait = WebDriverWait(driver, 30)
                
                print(f"🌐 Opening Facebook...")
                driver.get('https://www.facebook.com')
                time.sleep(4)
                
                # Check if already logged in (from previous session)
                already_logged_in = False
                try:
                    # Look for signs of being logged in (e.g., feed, profile elements)
                    if driver.find_elements(By.XPATH, "//span[contains(text(), 'on your mind')]") or \
                       'login' not in driver.current_url.lower():
                        already_logged_in = True
                        print(f"✅ Already logged in from previous session!")
                except:
                    pass
                
                if not already_logged_in:
                    print(f"🔐 Logging in as {email}...")
                    
                    try:
                        # Login
                        email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
                        email_field.clear()
                        email_field.send_keys(email)
                        
                        password_field = driver.find_element(By.ID, 'pass')
                        password_field.clear()
                        password_field.send_keys(password)
                        password_field.send_keys(Keys.RETURN)
                        
                        print(f"⏳ Waiting for login (this may take longer if Facebook shows security checks)...")
                        time.sleep(12)  # Longer wait for potential security checks
                        
                        # Check for security checks or verification
                        if 'checkpoint' in driver.current_url.lower() or 'verify' in driver.current_url.lower():
                            print(f"\n⚠️ Facebook Security Check Detected!")
                            print(f"📋 Please complete the security verification in the browser window.")
                            print(f"⏳ Waiting 60 seconds for you to complete verification...")
                            time.sleep(60)
                        
                        # Check if login was successful
                        if 'login' in driver.current_url.lower():
                            driver.quit()
                            os.unlink(temp_image_path)
                            return """❌ Facebook login failed. 

**Possible reasons:**
1. Incorrect email/password - Please use your actual Facebook login email (not display name)
2. Facebook security is blocking automation
3. Account requires additional verification

**Your .env file shows:**
- FACEBOOK_EMAIL=Iman

**This should be your actual email address like:**
- FACEBOOK_EMAIL=your.email@gmail.com

Please update your Facebook credentials in .env file with your actual login email."""
                        
                        print(f"✅ Successfully logged into Facebook!")
                    except Exception as login_error:
                        print(f"⚠️ Login error: {str(login_error)[:100]}")
                        driver.quit()
                        os.unlink(temp_image_path)
                        return f"❌ Login failed: {str(login_error)}. Make sure FACEBOOK_EMAIL is your actual email address."
                
                print(f"✅ Successfully logged into Facebook!")
                print(f"📝 Creating post...")
                
                # Navigate to homepage
                driver.get('https://www.facebook.com')
                time.sleep(6)
                
                print(f"🔍 Looking for post creation elements...")
                
                # Try multiple approaches to create a post
                post_created = False
                result = ""
                
                # Approach 1: Try clicking "What's on your mind" area first
                try:
                    print(f"📝 Approach 1: Looking for 'What's on your mind' area...")
                    
                    # Try different selectors for the post creation area
                    possible_selectors = [
                        "//span[contains(text(), 'on your mind')]",
                        "//span[contains(text(), \"What's on your mind\")]",
                        "//div[contains(@aria-label, 'Create a post')]",
                        "//div[@role='button' and contains(text(), 'Write something')]"
                    ]
                    
                    clicked = False
                    for selector in possible_selectors:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            if elements:
                                elements[0].click()
                                print(f"✅ Clicked post creation area")
                                clicked = True
                                time.sleep(4)
                                break
                        except:
                            continue
                    
                    if clicked:
                        # Look for file input to upload photo
                        print(f"📤 Looking for photo upload input...")
                        file_inputs = driver.find_elements(By.XPATH, '//input[@type="file" and (@accept="image/*" or contains(@accept, "image"))]')
                        
                        if file_inputs:
                            # Use the first visible file input
                            for file_input in file_inputs:
                                try:
                                    file_input.send_keys(temp_image_path)
                                    print(f"✅ Image uploaded via Approach 1!")
                                    time.sleep(6)
                                    post_created = True
                                    break
                                except:
                                    continue
                        else:
                            print(f"⚠️ No file input found after clicking")
                            
                except Exception as e1:
                    print(f"⚠️ Approach 1 failed: {str(e1)[:150]}")
                
                # Approach 2: Try direct Photo/Video button
                if not post_created:
                    try:
                        print(f"📝 Approach 2: Looking for Photo/Video button...")
                        
                        # Navigate back to ensure we're on the right page
                        driver.get('https://www.facebook.com')
                        time.sleep(4)
                        
                        # Look for Photo/Video buttons
                        photo_video_selectors = [
                            "//span[text()='Photo/video']",
                            "//span[contains(text(), 'Photo')]//parent::div[@role='button']",
                            "//div[@aria-label='Photo/video']",
                            "//span[contains(text(), 'Add photo')]"
                        ]
                        
                        for selector in photo_video_selectors:
                            try:
                                buttons = driver.find_elements(By.XPATH, selector)
                                if buttons:
                                    buttons[0].click()
                                    print(f"✅ Clicked Photo/Video button")
                                    time.sleep(4)
                                    
                                    # Upload image
                                    file_inputs = driver.find_elements(By.XPATH, '//input[@type="file"]')
                                    if file_inputs:
                                        file_inputs[0].send_keys(temp_image_path)
                                        print(f"✅ Image uploaded via Approach 2!")
                                        time.sleep(6)
                                        post_created = True
                                        break
                            except Exception as btn_error:
                                print(f"⚠️ Button attempt failed: {str(btn_error)[:100]}")
                                continue
                        
                    except Exception as e2:
                        print(f"⚠️ Approach 2 failed: {str(e2)[:150]}")
                
                # Approach 3: Direct file input injection (last resort)
                if not post_created:
                    try:
                        print(f"📝 Approach 3: Direct file input search...")
                        driver.get('https://www.facebook.com')
                        time.sleep(4)
                        
                        all_file_inputs = driver.find_elements(By.XPATH, '//input[@type="file"]')
                        print(f"Found {len(all_file_inputs)} file inputs")
                        
                        for idx, file_input in enumerate(all_file_inputs):
                            try:
                                # Try to make it visible and use it
                                driver.execute_script("arguments[0].style.display = 'block';", file_input)
                                driver.execute_script("arguments[0].style.visibility = 'visible';", file_input)
                                file_input.send_keys(temp_image_path)
                                print(f"✅ Image uploaded via file input #{idx}!")
                                time.sleep(6)
                                post_created = True
                                break
                            except:
                                continue
                                
                    except Exception as e3:
                        print(f"⚠️ Approach 3 failed: {str(e3)[:150]}")
                
                # If image uploaded, add caption and post
                if post_created:
                    try:
                        print(f"📝 Adding caption...")
                        print(f"📋 Caption text: {full_caption[:100]}...")
                        time.sleep(6)  # Wait longer for image upload dialog to fully load
                        
                        # Find caption area with multiple attempts
                        caption_added = False
                        
                        # Try using clipboard paste method (most reliable for Facebook)
                        try:
                            import pyperclip
                            
                            # Copy caption to clipboard
                            pyperclip.copy(full_caption)
                            print(f"📋 Caption copied to clipboard")
                            
                            # Find any visible contenteditable div
                            caption_areas = driver.find_elements(By.XPATH, '//div[@contenteditable="true"]')
                            print(f"Found {len(caption_areas)} editable areas")
                            
                            for idx, caption_area in enumerate(caption_areas):
                                try:
                                    if caption_area.is_displayed() and caption_area.is_enabled():
                                        print(f"Trying editable area #{idx}...")
                                        
                                        # Click to focus
                                        driver.execute_script("arguments[0].focus();", caption_area)
                                        caption_area.click()
                                        time.sleep(1)
                                        
                                        # Paste using Ctrl+V
                                        caption_area.send_keys(Keys.CONTROL, 'v')
                                        time.sleep(1)
                                        
                                        # Verify text was added
                                        current_text = caption_area.text
                                        if len(current_text) > 10:  # Some text was added
                                            print(f"✅ Caption pasted successfully via clipboard!")
                                            caption_added = True
                                            break
                                except Exception as paste_error:
                                    print(f"⚠️ Paste attempt #{idx} failed: {str(paste_error)[:50]}")
                                    continue
                                    
                        except ImportError:
                            print(f"⚠️ pyperclip not available, trying other methods...")
                        
                        # Fallback: Try direct JavaScript injection into all editable divs
                        if not caption_added:
                            print(f"📝 Trying JavaScript injection method...")
                            all_editable = driver.find_elements(By.XPATH, '//div[@contenteditable="true"]')
                            
                            for idx, elem in enumerate(all_editable):
                                try:
                                    if elem.is_displayed():
                                        # Use JavaScript to set innerHTML and trigger events
                                        driver.execute_script("""
                                            var element = arguments[0];
                                            var text = arguments[1];
                                            
                                            // Clear existing content
                                            element.innerHTML = '';
                                            
                                            // Add text as text node (not HTML)
                                            var lines = text.split('\\n');
                                            for (var i = 0; i < lines.length; i++) {
                                                if (i > 0) {
                                                    element.appendChild(document.createElement('br'));
                                                }
                                                element.appendChild(document.createTextNode(lines[i]));
                                            }
                                            
                                            // Trigger all possible input events
                                            element.focus();
                                            ['input', 'change', 'keyup', 'keydown'].forEach(function(eventType) {
                                                var event = new Event(eventType, { bubbles: true, cancelable: true });
                                                element.dispatchEvent(event);
                                            });
                                        """, elem, full_caption)
                                        
                                        time.sleep(1)
                                        
                                        # Check if text was added
                                        if len(elem.text) > 10:
                                            print(f"✅ Caption added via JavaScript injection to element #{idx}!")
                                            caption_added = True
                                            break
                                except Exception as js_error:
                                    continue
                        
                        if not caption_added:
                            print(f"⚠️ Automatic caption failed - keeping browser open for manual addition")
                            print(f"📋 Your caption: {full_caption}")
                        
                        time.sleep(3)
                        
                        # Click Post button with multiple attempts
                        print(f"📤 Looking for Post button...")
                        posted = False
                        
                        post_button_selectors = [
                            "//span[text()='Post']//ancestor::div[@role='button']",
                            "//div[@aria-label='Post']",
                            "//div[@role='button' and contains(., 'Post')]",
                            "//span[contains(text(), 'Post')]//parent::div[@role='button']"
                        ]
                        
                        for selector in post_button_selectors:
                            try:
                                post_buttons = driver.find_elements(By.XPATH, selector)
                                if post_buttons:
                                    for post_btn in post_buttons:
                                        try:
                                            # Make sure button is visible
                                            driver.execute_script("arguments[0].scrollIntoView(true);", post_btn)
                                            time.sleep(1)
                                            
                                            # Try clicking
                                            post_btn.click()
                                            print(f"✅ Post button clicked!")
                                            posted = True
                                            break
                                        except:
                                            continue
                                    if posted:
                                        break
                            except:
                                continue
                        
                        if posted:
                            print(f"⏳ Waiting for post to publish...")
                            time.sleep(8)
                            print(f"✅ Successfully posted to Facebook!")
                            
                            result = f"""✅ **Successfully Posted to Facebook!**

👥 **Post Details:**
- Account: {email}
- Status: Live on your Facebook profile!

**Caption:**
{full_caption[:200]}{'...' if len(full_caption) > 200 else ''}

**✅ Post has been published! Check your Facebook profile to see it.**
"""
                        else:
                            print(f"⚠️ Could not find Post button")
                            result = """⚠️ **Image and caption prepared but Post button not found**

The image and caption are ready in the browser window.

**Please complete manually:**
1. Review the image and caption in the open browser
2. Click the blue "Post" button to publish
3. Browser will stay open for 45 seconds

"""
                            
                    except Exception as caption_error:
                        print(f"⚠️ Caption/Post error: {str(caption_error)[:150]}")
                        result = f"⚠️ Image uploaded but posting failed: {str(caption_error)[:100]}. Please complete manually in the browser window."
                else:
                    print(f"❌ Could not upload image after all attempts")
                    result = """❌ **Could not upload image automatically**

**Manual Posting Instructions:**
1. The browser is open and you're logged in
2. Click on "What's on your mind" or "Photo/Video"
3. Upload your image manually from: """ + temp_image_path + """
4. Copy and paste your caption below:

**Your Caption:**
""" + full_caption + """

5. Click "Post" to publish

Browser will stay open for 45 seconds for manual completion.
"""
                    
                # Keep browser open for manual review/completion
                print(f"\n⏳ Browser staying open for 45 seconds for review/manual completion...")
                time.sleep(45)
                
                # Close browser
                driver.quit()
                    
            except Exception as driver_error:
                print(f"❌ Browser automation error: {str(driver_error)}")
                result = f"❌ Browser automation error: {str(driver_error)}. Make sure Chrome is installed."
                try:
                    driver.quit()
                except:
                    pass
            
            # Clean up temporary file
            try:
                os.unlink(temp_image_path)
            except:
                pass
            
            return result
                    
        except ImportError:
            return """❌ Selenium not installed. Install it with:
            
pip install selenium

Also make sure Chrome browser is installed."""
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Facebook posting error:\n{error_details}")
            return f"❌ Error posting to Facebook: {str(e)}"
            
            return result
                    
        except ImportError:
            return """❌ Selenium not installed. Install it with:
            
pip install selenium

Also make sure Chrome browser is installed."""
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Facebook posting error:\n{error_details}")
            return f"❌ Error posting to Facebook: {str(e)}"
    
    def get_social_posts(self) -> str:
        """Get list of social media posts with images"""
        if not self.agent:
            return "❌ Please initialize the agent first"
        
        try:
            posts = self.agent.get_all_social_posts()
            
            if not posts:
                return "📱 No social posts yet. Execute a campaign to see posts here."
            
            # Filter to show only the most recent post per platform (Facebook, Instagram, Twitter)
            # This ensures only 3 posts are displayed - one for each platform
            platform_latest = {}
            for post in posts:
                platform = post['platform']
                if platform not in platform_latest:
                    platform_latest[platform] = post
                else:
                    # Keep the most recent post (assuming posts are ordered with newest first)
                    if post['posted_at'] > platform_latest[platform]['posted_at']:
                        platform_latest[platform] = post
            
            # Get the 3 most recent posts (one per platform)
            filtered_posts = list(platform_latest.values())
            
            output = f"## 📱 Social Media Posts ({len(filtered_posts)} latest)\n\n"
            output += f"*Showing the most recent post for each platform*\n\n"
            
            # Show only the latest posts per platform (max 3: Facebook, Instagram, Twitter)
            for post in filtered_posts:
                platform_emoji = {
                    "facebook": "👥",
                    "instagram": "📸",
                    "twitter": "🐦"
                }.get(post['platform'], "📱")
                
                platform_name = post['platform'].upper()
                
                output += f"""---
### {platform_emoji} **{platform_name}** Post
**Post ID:** `{post['id']}`
**Posted:** {post['posted_at'][:19]}

**Post Content:**
> {post['content']}

**Hashtags:** {' '.join(post['hashtags'])}
"""
                
                # Display image with status
                if post.get('image_url'):
                    output += f"""
**📷 Campaign Image:**
<img src="{post['image_url']}" alt="{platform_name} Image" style="max-width: 400px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 10px 0;" />
✅ Image generated

"""
                else:
                    output += f"""
**📷 Campaign Image:** ❌ Not generated yet
👉 **Copy this Post ID: `{post['id']}`** and use it in the 'Generate Image' section below

"""
                
                output += f"""**Engagement Metrics:**
- 👁️ Impressions: {post['impressions']:,}
- ❤️ Likes: {post['likes']:,}
- 💬 Comments: {post['comments']:,}
- 🔄 Shares: {post['shares']:,}
- 🔗 Clicks: {post['clicks']:,}
- 📊 Engagement Rate: {post['engagement_rate']}%

"""
                
                # Get and display comments for this post
                comments = self.agent.deployment_service.social_service.get_post_comments(post['id'])
                if comments:
                    output += f"**💬 Comments ({len(comments)}):**\n"
                    for comment in comments[:5]:  # Show first 5 comments per post
                        sentiment_emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}.get(comment.sentiment, "💬")
                        output += f"  {sentiment_emoji} **{comment.author_name}**: {comment.content}\n"
                    if len(comments) > 5:
                        output += f"  ... and {len(comments) - 5} more comments\n"
                
                output += f"\n**Campaign:** {post['campaign_id']}\n\n"
            
            return output
        except Exception as e:
            return f"❌ Error getting social posts: {str(e)}"
    
    def get_posts_dropdown_options(self) -> List[str]:
        """Get list of posts for dropdown selection"""
        if not self.agent:
            return ["No posts available - Create a campaign first"]
        
        try:
            posts = self.agent.get_all_social_posts()
            if not posts:
                return ["No posts available - Create a campaign first"]
            
            options = []
            for post in posts:
                platform_emoji = {"facebook": "👥", "instagram": "📸", "twitter": "🐦"}.get(post['platform'], "📱")
                has_image = "✅" if post.get('image_url') else "❌"
                option = f"{platform_emoji} {post['platform'].upper()} | {has_image} | {post['id']}"
                options.append(option)
            return options
        except:
            return ["Error loading posts"]
    
    def get_social_comments_sample(self) -> str:
        """Get sample comments from social media posts"""
        if not self.agent:
            return "❌ Please initialize the agent first"
        
        try:
            posts = self.agent.get_all_social_posts()
            
            if not posts:
                return "💬 No posts with comments yet."
            
            output = f"## 💬 Social Media Comments Sample\n\n"
            
            # Show comments from first 5 posts
            for post in posts[:5]:
                comments = self.agent.deployment_service.social_service.get_post_comments(post['id'])
                
                if comments:
                    platform_emoji = {"facebook": "👥", "instagram": "📸", "twitter": "🐦"}.get(post['platform'], "📱")
                    output += f"""---
### {platform_emoji} {post['platform'].upper()} Post
**Content:** {post['content'][:100]}...

**Comments ({len(comments)}):**
"""
                    for comment in comments[:5]:  # Show first 5 comments
                        sentiment_emoji = {"positive": "😊", "neutral": "😐", "negative": "😞"}.get(comment.sentiment, "💬")
                        output += f"- {sentiment_emoji} **{comment.author_name}**: {comment.content}\n"
                    
                    output += "\n"
            
            return output if "Comments" in output else "💬 No comments available yet."
        except Exception as e:
            return f"❌ Error getting comments: {str(e)}"


def create_interface():
    """Create the Gradio interface"""
    ui = MarketingAgentUI()
    
    with gr.Blocks(title="Retail Marketing Agent Dashboard") as app:
        gr.Markdown("""
        # 🛍️ Retail Marketing Agent Dashboard
        
        AI-powered marketing agent for retail businesses with goal-based planning and execution
        """)
        
        with gr.Tabs():
            # Tab 1: Agent Setup
            with gr.Tab("🔧 Agent Setup"):
                gr.Markdown("### Initialize Your Marketing Agent")
                
                with gr.Row():
                    with gr.Column():
                        client_name = gr.Textbox(
                            label="Store Name",
                            placeholder="Fashion Forward Boutique",
                            value="Fashion Forward Boutique"
                        )
                        store_type = gr.Dropdown(
                            label="Store Type",
                            choices=["fashion", "electronics", "grocery", "home_goods", "beauty", "sports", "general"],
                            value="fashion"
                        )
                    with gr.Column():
                        location = gr.Textbox(
                            label="Location",
                            placeholder="Downtown Seattle",
                            value="Downtown Seattle"
                        )
                        has_online = gr.Checkbox(label="Has Online Store", value=True)
                
                init_btn = gr.Button("Initialize Agent", variant="primary")
                init_output = gr.Markdown()
                
                init_btn.click(
                    fn=ui.initialize_agent,
                    inputs=[client_name, store_type, has_online, location],
                    outputs=init_output
                )
            
            # Tab 2: Goal Setting
            with gr.Tab("🎯 Goal Setting"):
                gr.Markdown("### Set Marketing Goals")
                
                with gr.Row():
                    with gr.Column():
                        goal_type = gr.Dropdown(
                            label="Goal Type",
                            choices=[
                                "Customer Acquisition",
                                "Customer Retention",
                                "Instore Marketing",
                                "Digital Presence",
                                "Seasonal Campaign",
                                "Analytics Insights",
                                "Community Engagement"
                            ],
                            value="Customer Acquisition"
                        )
                        target = gr.Textbox(
                            label="Target",
                            placeholder="Increase foot traffic by 25%",
                            value="Increase foot traffic by 25% and acquire 500 new customers"
                        )
                        timeframe = gr.Textbox(
                            label="Timeframe",
                            placeholder="30 days",
                            value="30 days"
                        )
                    
                    with gr.Column():
                        description = gr.Textbox(
                            label="Description",
                            placeholder="Holiday season customer acquisition campaign",
                            value="Holiday season customer acquisition campaign",
                            lines=3
                        )
                        priority = gr.Slider(
                            label="Priority",
                            minimum=1,
                            maximum=5,
                            value=1,
                            step=1
                        )
                
                set_goal_btn = gr.Button("Set Goal", variant="primary")
                goal_output = gr.Markdown()
                goal_logs = gr.Textbox(label="Execution Logs", lines=5)
                
                set_goal_btn.click(
                    fn=ui.set_goal,
                    inputs=[goal_type, target, timeframe, description, priority],
                    outputs=[goal_output, goal_logs]
                )
            
            # Tab 3: Campaign Content Approval
            with gr.Tab("✅ Campaign Approval"):
                gr.Markdown("""### Review & Approve Marketing Content
                
Generate campaign content, review it, request changes, and approve before deployment.""")
                
                generate_content_btn = gr.Button("🎨 Generate Campaign Content", variant="primary")
                
                campaign_preview = gr.Markdown()
                
                gr.Markdown("### Edit Campaign Content")
                campaign_content_editor = gr.Textbox(
                    label="Campaign Content",
                    placeholder="Generated content will appear here for editing...",
                    lines=15
                )
                
                with gr.Row():
                    with gr.Column():
                        change_instructions = gr.Textbox(
                            label="Request Changes (Optional)",
                            placeholder="E.g., 'Make it more exciting', 'Add a holiday theme', 'Focus more on discounts'",
                            lines=3
                        )
                        regenerate_btn = gr.Button("🔄 Regenerate with Changes", variant="secondary")
                    
                    with gr.Column():
                        approve_btn = gr.Button("✅ Approve & Deploy Campaign", variant="primary", size="lg")
                        approval_output = gr.Markdown()
                
                # Connect buttons
                generate_content_btn.click(
                    fn=ui.generate_campaign_content,
                    outputs=[campaign_preview, campaign_content_editor]
                )
                
                regenerate_btn.click(
                    fn=ui.regenerate_campaign_content,
                    inputs=[change_instructions, campaign_content_editor],
                    outputs=[campaign_preview, campaign_content_editor]
                )
                
                approve_btn.click(
                    fn=ui.approve_and_deploy_campaign,
                    inputs=[campaign_content_editor],
                    outputs=approval_output,
                    api_name="approve_campaign"
                )
            
            # Tab 4: Execution & Monitoring
            with gr.Tab("🚀 Execution & Monitoring"):
                gr.Markdown("### Create Plan and Execute")
                
                with gr.Row():
                    plan_btn = gr.Button("Create Execution Plan", variant="secondary")
                    execute_btn = gr.Button("Execute Goal", variant="primary")
                
                plan_output = gr.Markdown()
                execution_logs = gr.Textbox(label="Real-time Logs", lines=10)
                
                with gr.Row():
                    execution_output = gr.Markdown()
                
                metrics_plot = gr.Plot(label="Execution Metrics")
                
                plan_btn.click(
                    fn=ui.create_plan,
                    outputs=[plan_output, execution_logs]
                )
                
                execute_btn.click(
                    fn=ui.execute_goal,
                    outputs=[execution_output, execution_logs, metrics_plot]
                )
            
            # Tab 5: Customer Database
            with gr.Tab("👥 Customer Database"):
                gr.Markdown("### Mock Customer Database (500 customers)")
                
                customer_stats_output = gr.Markdown()
                customer_refresh_btn = gr.Button("Refresh Customer Stats", variant="secondary")
                
                customer_refresh_btn.click(
                    fn=ui.get_customer_stats,
                    outputs=customer_stats_output
                )
            
            # Tab 6: Sent Emails
            with gr.Tab("📧 Email Campaigns"):
                gr.Markdown("### All Sent Emails with Engagement Tracking")
                
                emails_output = gr.Markdown()
                emails_refresh_btn = gr.Button("Refresh Emails", variant="secondary")
                
                emails_refresh_btn.click(
                    fn=ui.get_sent_emails,
                    outputs=emails_output
                )
            
            # Tab 7: Social Media Posts
            with gr.Tab("📱 Social Media"):
                gr.Markdown("### Social Media Posts Management")
                gr.Markdown("*Generate images for your posts and publish to social media*")
                
                # Image Generation Controls Section
                gr.Markdown("---")
                gr.Markdown("### 🎛️ Image Generation Settings")
                gr.Markdown("*Enable image generation per platform to save API credits. Only generate images when needed!*")
                
                with gr.Row():
                    enable_facebook_images = gr.Checkbox(
                        label="👥 Generate Facebook Images",
                        value=False,
                        info="Enable to generate AI images for Facebook posts"
                    )
                    enable_instagram_images = gr.Checkbox(
                        label="📸 Generate Instagram Images",
                        value=False,
                        info="Enable to generate AI images for Instagram posts"
                    )
                    enable_twitter_images = gr.Checkbox(
                        label="🐦 Generate Twitter Images",
                        value=False,
                        info="Enable to generate AI images for Twitter posts"
                    )
                
                # Generate Image Section
                gr.Markdown("---")
                gr.Markdown("### 🎨 Generate Images")
                gr.Markdown("*Check the platforms above and click Generate to create images for all posts from selected platforms*")
                
                with gr.Row():
                    generate_image_btn = gr.Button(
                        "🎨 Generate Images for Selected Platforms",
                        variant="primary",
                        size="lg"
                    )
                
                generate_result = gr.Markdown()
                
                # Create a wrapper function that generates images for all enabled platforms
                def generate_and_refresh(fb_enabled, ig_enabled, tw_enabled):
                    result = ui.generate_images_for_platforms(fb_enabled, ig_enabled, tw_enabled)
                    posts_display = ui.get_social_posts()
                    all_posts = ui.get_posts_dropdown_options()
                    
                    # Filter Instagram posts only
                    instagram_posts = [p for p in all_posts if "INSTAGRAM" in p]
                    if not instagram_posts:
                        instagram_posts = ["No Instagram posts available"]
                    
                    # Filter Facebook posts only
                    facebook_posts = [p for p in all_posts if "FACEBOOK" in p]
                    if not facebook_posts:
                        facebook_posts = ["No Facebook posts available"]
                    
                    return [
                        result,
                        posts_display,
                        gr.update(choices=instagram_posts, value=instagram_posts[0] if instagram_posts else None),
                        gr.update(choices=facebook_posts, value=facebook_posts[0] if facebook_posts else None)
                    ]
                
                # Posting sections
                gr.Markdown("---")
                gr.Markdown("### 📤 Post to Social Media")
                
                # Main action panel - Only posting sections
                with gr.Row():
                    # Column 1 - Post to Instagram
                    with gr.Column(scale=1):
                        gr.Markdown("### 📤 Post to Instagram")
                        gr.Markdown("Select an Instagram post and publish it to your account")
                        
                        post_selector_instagram = gr.Dropdown(
                            label="Select Instagram Post",
                            choices=["Load posts first..."],
                            interactive=True,
                            info="Only Instagram posts shown"
                        )
                        
                        instagram_post_btn = gr.Button(
                            "📤 Post to Instagram",
                            variant="primary",
                            size="lg"
                        )
                        
                        instagram_result = gr.Markdown()
                    
                    # Column 2 - Post to Facebook
                    with gr.Column(scale=1):
                        gr.Markdown("### 👥 Post to Facebook")
                        gr.Markdown("Select a Facebook post and publish it to your account")
                        
                        post_selector_facebook = gr.Dropdown(
                            label="Select Facebook Post",
                            choices=["Load posts first..."],
                            interactive=True,
                            info="Only Facebook posts shown"
                        )
                        
                        facebook_post_btn = gr.Button(
                            "👥 Post to Facebook",
                            variant="primary",
                            size="lg"
                        )
                        
                        facebook_result = gr.Markdown()
                
                gr.Markdown("---")
                
                # Refresh and display posts
                with gr.Row():
                    refresh_posts_btn = gr.Button("🔄 Load/Refresh All Posts", variant="secondary", size="lg")
                
                social_output = gr.Markdown()
                
                # Wire up the refresh to update dropdowns and display
                def refresh_and_update():
                    posts_display = ui.get_social_posts()
                    all_posts = ui.get_posts_dropdown_options()
                    
                    # Filter Instagram posts only
                    instagram_posts = [p for p in all_posts if "INSTAGRAM" in p]
                    if not instagram_posts:
                        instagram_posts = ["No Instagram posts available"]
                    
                    # Filter Facebook posts only
                    facebook_posts = [p for p in all_posts if "FACEBOOK" in p]
                    if not facebook_posts:
                        facebook_posts = ["No Facebook posts available"]
                    
                    return [
                        posts_display,
                        gr.update(choices=instagram_posts, value=instagram_posts[0] if instagram_posts else None),
                        gr.update(choices=facebook_posts, value=facebook_posts[0] if facebook_posts else None)
                    ]
                
                refresh_posts_btn.click(
                    fn=refresh_and_update,
                    outputs=[social_output, post_selector_instagram, post_selector_facebook]
                )
                
                # Wire up generate button to generate images for enabled platforms AND refresh posts
                generate_image_btn.click(
                    fn=generate_and_refresh,
                    inputs=[enable_facebook_images, enable_instagram_images, enable_twitter_images],
                    outputs=[generate_result, social_output, post_selector_instagram, post_selector_facebook]
                )
                
                # Extract post ID from dropdown selection and post to Instagram
                def post_from_dropdown(selected):
                    if not selected or "No" in selected or "Load posts" in selected:
                        return "❌ Please select a valid Instagram post first"
                    # Extract post ID from format: "📸 INSTAGRAM | ❌ | post_xxx_instagram"
                    post_id = selected.split(" | ")[-1].strip()
                    return ui.post_to_instagram(post_id)
                
                instagram_post_btn.click(
                    fn=post_from_dropdown,
                    inputs=post_selector_instagram,
                    outputs=instagram_result
                )
                
                # Extract post ID from dropdown selection and post to Facebook
                def post_to_facebook_from_dropdown(selected):
                    if not selected or "No" in selected or "Load posts" in selected:
                        return "❌ Please select a valid Facebook post first"
                    # Extract post ID from format: "👥 FACEBOOK | ❌ | post_xxx_facebook"
                    post_id = selected.split(" | ")[-1].strip()
                    return ui.post_to_facebook(post_id)
                
                facebook_post_btn.click(
                    fn=post_to_facebook_from_dropdown,
                    inputs=post_selector_facebook,
                    outputs=facebook_result
                )
            
            # Tab 9: Chat Interface
            with gr.Tab("💬 Chat with Agent"):
                gr.Markdown("### 🤖 AI Assistant - Ask Me Anything!")
                gr.Markdown("*Get help with campaigns, check status, ask for marketing tips, or learn how to use features*")
                
                chatbot = gr.Chatbot(
                    height=500,
                    label="Marketing Agent Assistant",
                    show_label=True
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        label="Your Message",
                        placeholder="Ask me anything: 'What's my campaign status?', 'Give me marketing tips', 'How do I post to Instagram?'",
                        scale=4
                    )
                    send_btn = gr.Button("Send 📤", variant="primary", scale=1)
                
                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
                    example_btn_1 = gr.Button("📊 Show Status", variant="secondary")
                    example_btn_2 = gr.Button("🎯 Current Goal", variant="secondary")
                    example_btn_3 = gr.Button("💡 Marketing Tips", variant="secondary")
                
                def submit_message(message, history):
                    if not message.strip():
                        return history, ""
                    new_history = ui.chat_with_agent(message, history)
                    return new_history, ""
                
                # Send message on button click or enter
                msg.submit(
                    fn=submit_message,
                    inputs=[msg, chatbot],
                    outputs=[chatbot, msg]
                )
                
                send_btn.click(
                    fn=submit_message,
                    inputs=[msg, chatbot],
                    outputs=[chatbot, msg]
                )
                
                # Clear chat
                clear_btn.click(lambda: ([], ""), None, [chatbot, msg])
                
                # Example buttons
                example_btn_1.click(
                    lambda h: ui.chat_with_agent("What's my current status?", h),
                    inputs=chatbot,
                    outputs=chatbot
                )
                example_btn_2.click(
                    lambda h: ui.chat_with_agent("What's my current goal?", h),
                    inputs=chatbot,
                    outputs=chatbot
                )
                example_btn_3.click(
                    lambda h: ui.chat_with_agent("Give me marketing tips", h),
                    inputs=chatbot,
                    outputs=chatbot
                )
        
        gr.Markdown("""
        ---
        ### 📖 Quick Guide
        1. **Setup**: Initialize your agent with store details
        2. **Goal**: Set a marketing goal with target and timeframe
        3. **Plan**: Let AI create an execution plan
        4. **Execute**: Run the campaign and monitor progress
        5. **Track**: View metrics and chat with the agent
        """)
    
    return app


if __name__ == "__main__":
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,  # Enable public URL sharing
        show_error=True,
        theme=gr.themes.Soft()
    )
