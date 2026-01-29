"""
Customer Acquisition Module
Handles promotional campaigns, targeting, and new customer acquisition strategies
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from langchain_core.prompts import ChatPromptTemplate

from ..utils.llm_helper import get_llm


class CustomerAcquisitionModule:
    """Module for customer acquisition strategies"""
    
    def __init__(self):
        self.llm = get_llm()
    
    def create_promotion_campaign(
        self,
        target_audience: str,
        campaign_type: str,
        budget: float,
        duration_days: int,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a promotional campaign to acquire new customers
        
        Args:
            target_audience: Description of target customer segment
            campaign_type: Type of campaign (seasonal, clearance, new_product, etc.)
            budget: Campaign budget
            duration_days: Campaign duration in days
            store_context: Store information (name, type, location)
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert retail marketing strategist specializing in customer acquisition.
            Create a comprehensive promotional campaign that will attract new customers."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Location: {location}
            
            Campaign Details:
            - Target Audience: {target_audience}
            - Campaign Type: {campaign_type}
            - Budget: ${budget}
            - Duration: {duration_days} days
            
            Create a detailed campaign including:
            1. Campaign name and tagline
            2. Key promotional offers (discounts, bundles, incentives)
            3. Marketing channels to use (social media, email, local ads, etc.)
            4. Content ideas for each channel
            5. Call-to-action strategy
            6. Budget allocation across channels
            7. Success metrics to track
            
            Format the response as a structured campaign plan.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "location": store_context.get("location", "Local"),
            "target_audience": target_audience,
            "campaign_type": campaign_type,
            "budget": budget,
            "duration_days": duration_days
        })
        
        campaign_plan = response.content if hasattr(response, 'content') else str(response)
        
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)
        
        return {
            "campaign_plan": campaign_plan,
            "target_audience": target_audience,
            "campaign_type": campaign_type,
            "budget": budget,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "status": "planned",
            "created_at": datetime.now().isoformat()
        }
    
    def design_first_purchase_incentive(
        self,
        incentive_type: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Design incentives for first-time customers
        
        Args:
            incentive_type: Type of incentive (discount, gift, points, etc.)
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in customer acquisition and loyalty programs.
            Design an attractive first-purchase incentive that will convert new customers."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            
            Incentive Type: {incentive_type}
            
            Design a first-purchase incentive including:
            1. Offer details (percentage off, dollar amount, gift, etc.)
            2. Terms and conditions
            3. How to communicate it (welcome email, social media, in-store signage)
            4. Follow-up strategy after first purchase
            5. Expected conversion rate improvement
            
            Make it compelling and easy to understand.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "incentive_type": incentive_type
        })
        
        incentive_design = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "incentive_design": incentive_design,
            "incentive_type": incentive_type,
            "status": "designed",
            "created_at": datetime.now().isoformat()
        }
    
    def create_referral_program(
        self,
        reward_structure: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a customer referral program
        
        Args:
            reward_structure: How referrers and referees are rewarded
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in referral marketing and viral growth strategies.
            Create a referral program that incentivizes existing customers to bring in new ones."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            
            Reward Structure: {reward_structure}
            
            Create a complete referral program including:
            1. Program name and description
            2. Rewards for referrer (existing customer)
            3. Rewards for referee (new customer)
            4. How the referral process works
            5. Tracking mechanism
            6. Promotion strategy for the program
            7. Terms and conditions
            8. Expected virality and growth metrics
            
            Make it simple, attractive, and easy to participate in.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "reward_structure": reward_structure
        })
        
        referral_program = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "referral_program": referral_program,
            "reward_structure": reward_structure,
            "status": "created",
            "created_at": datetime.now().isoformat()
        }
    
    def generate_targeted_ad_copy(
        self,
        platform: str,
        target_segment: str,
        product_category: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate ad copy for different platforms and target segments
        
        Args:
            platform: Advertising platform (facebook, instagram, google, etc.)
            target_segment: Customer segment to target
            product_category: Product category being promoted
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert copywriter specializing in retail advertising.
            Create compelling ad copy that drives clicks and conversions."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Platform: {platform}
            Target Segment: {target_segment}
            Product Category: {product_category}
            
            Create 3 variations of ad copy including:
            1. Headline (attention-grabbing)
            2. Body text (benefit-focused)
            3. Call-to-action
            4. Visual recommendations
            
            Each variation should be optimized for {platform} and appeal to {target_segment}.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "platform": platform,
            "target_segment": target_segment,
            "product_category": product_category
        })
        
        ad_copy = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "ad_copy": ad_copy,
            "platform": platform,
            "target_segment": target_segment,
            "product_category": product_category,
            "created_at": datetime.now().isoformat()
        }
