"""
Customer Retention Module
Handles loyalty programs, email campaigns, and retention strategies
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

from ..utils.llm_helper import get_llm


class CustomerRetentionModule:
    """Module for customer retention strategies"""
    
    def __init__(self):
        self.llm = get_llm()
    
    def design_loyalty_program(
        self,
        program_type: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Design a comprehensive loyalty program
        
        Args:
            program_type: Type of loyalty program (points, tiers, cashback, etc.)
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in customer loyalty and retention strategies.
            Design a loyalty program that keeps customers coming back."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Program Type: {program_type}
            
            Design a complete loyalty program including:
            1. Program name and branding
            2. How customers earn rewards (points, purchases, actions)
            3. Reward tiers or levels (if applicable)
            4. Redemption options and value proposition
            5. Exclusive perks for loyal customers
            6. Program communication strategy
            7. Technology/tools needed
            8. Expected impact on customer lifetime value
            
            Make it engaging and valuable for customers.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "program_type": program_type
        })
        
        loyalty_program = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "loyalty_program": loyalty_program,
            "program_type": program_type,
            "status": "designed",
            "created_at": datetime.now().isoformat()
        }
    
    def create_email_campaign(
        self,
        campaign_goal: str,
        customer_segment: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create an email marketing campaign
        
        Args:
            campaign_goal: Goal of the campaign (re-engagement, new product, sale, etc.)
            customer_segment: Target customer segment
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert email marketer specializing in retail.
            Create email campaigns that drive engagement and sales."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Campaign Goal: {campaign_goal}
            Customer Segment: {customer_segment}
            
            Create a complete email campaign including:
            1. Email sequence (3-5 emails)
            2. Subject lines for each email
            3. Email content and structure
            4. Personalization elements
            5. Call-to-action for each email
            6. Timing and frequency
            7. A/B testing suggestions
            8. Success metrics
            
            Make emails engaging and conversion-focused.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "campaign_goal": campaign_goal,
            "customer_segment": customer_segment
        })
        
        email_campaign = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "email_campaign": email_campaign,
            "campaign_goal": campaign_goal,
            "customer_segment": customer_segment,
            "status": "created",
            "created_at": datetime.now().isoformat()
        }
    
    def create_win_back_campaign(
        self,
        inactive_period: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a campaign to win back inactive customers
        
        Args:
            inactive_period: How long customers have been inactive
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in customer re-engagement and win-back strategies.
            Create campaigns that bring inactive customers back."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Customer Inactive Period: {inactive_period}
            
            Create a win-back campaign including:
            1. Campaign messaging ("We miss you" approach)
            2. Special incentives to return (exclusive offers)
            3. Multi-channel approach (email, SMS, direct mail)
            4. Personalization based on past purchase history
            5. Timeline for the campaign
            6. Success metrics and goals
            
            Make the campaign emotionally resonant and valuable.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "inactive_period": inactive_period
        })
        
        winback_campaign = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "winback_campaign": winback_campaign,
            "inactive_period": inactive_period,
            "status": "created",
            "created_at": datetime.now().isoformat()
        }
    
    def create_vip_experience(
        self,
        vip_criteria: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create VIP customer experience and perks
        
        Args:
            vip_criteria: Criteria for VIP status (spend, frequency, etc.)
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in luxury retail and VIP customer experiences.
            Design exclusive experiences that make top customers feel valued."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            VIP Criteria: {vip_criteria}
            
            Create a VIP experience program including:
            1. VIP tier name and branding
            2. Qualification criteria
            3. Exclusive perks and benefits
            4. Early access to sales and new products
            5. Personal shopping or concierge services
            6. Special events for VIP customers
            7. Communication strategy
            8. How to make VIPs feel special
            
            Make it luxurious and aspirational.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "vip_criteria": vip_criteria
        })
        
        vip_experience = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "vip_experience": vip_experience,
            "vip_criteria": vip_criteria,
            "status": "created",
            "created_at": datetime.now().isoformat()
        }
