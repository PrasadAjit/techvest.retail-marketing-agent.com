"""
Deployment Service
Orchestrates campaign deployment across all channels (email, social media)
"""
from typing import Dict, List, Any, Optional
from datetime import datetime

from .mock_customers import MockCustomerDatabase, MockCustomer
from .mock_email import MockEmailService
from .mock_social import MockSocialMediaService


class DeploymentService:
    """Coordinates campaign deployment across all channels"""
    
    def __init__(self):
        self.customer_db = MockCustomerDatabase(num_customers=500)
        self.email_service = MockEmailService()
        self.social_service = MockSocialMediaService()
    
    def deploy_customer_acquisition_campaign(
        self,
        campaign_id: str,
        campaign_content: Dict[str, Any],
        target_segment: str = "new",
        campaign_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Deploy a customer acquisition campaign
        
        Args:
            campaign_id: Campaign ID
            campaign_content: AI-generated campaign content
            target_segment: Customer segment to target (new, occasional, frequent, vip)
            campaign_context: Additional context for email personalization
        
        Returns:
            Deployment results with metrics
        """
        results = {
            "campaign_id": campaign_id,
            "deployed_at": datetime.now().isoformat(),
            "channels_deployed": [],
            "email": {},
            "social_media": {},
            "total_reach": 0
        }
        
        # Get target customers
        target_customers = self.customer_db.get_customers_by_segment(target_segment)
        email_customers = [c for c in target_customers if c.email_opt_in]
        
        # Deploy via Email
        if email_customers:
            email_results = self._deploy_email(
                campaign_id=campaign_id,
                customers=email_customers,
                subject=f"Special Offer: {campaign_content.get('campaign_type', 'Exclusive Deal')}!",
                content=campaign_content.get('campaign_plan', 'Special promotion for you!'),
                campaign_context=campaign_context
            )
            results["email"] = email_results
            results["channels_deployed"].append("email")
            results["total_reach"] += email_results["sent"]
        
        # Deploy on Social Media with campaign context for image generation
        social_results = self._deploy_social_media(
            campaign_id=campaign_id,
            campaign_content=campaign_content,
            campaign_context=campaign_context
        )
        results["social_media"] = social_results
        results["channels_deployed"].extend(["facebook", "instagram", "twitter"])
        results["total_reach"] += social_results.get("stats", {}).get("total_impressions", 0)
        
        return results
    
    def deploy_retention_campaign(
        self,
        campaign_id: str,
        campaign_content: Dict[str, Any],
        campaign_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Deploy a customer retention campaign targeting existing customers"""
        results = {
            "campaign_id": campaign_id,
            "deployed_at": datetime.now().isoformat(),
            "channels_deployed": [],
            "email": {},
            "social_media": {},
            "total_reach": 0
        }
        
        # Target occasional and frequent customers
        target_customers = (
            self.customer_db.get_customers_by_segment("occasional") +
            self.customer_db.get_customers_by_segment("frequent") +
            self.customer_db.get_customers_by_segment("vip")
        )
        email_customers = [c for c in target_customers if c.email_opt_in]
        
        # Deploy via Email
        if email_customers:
            email_results = self._deploy_email(
                campaign_id=campaign_id,
                customers=email_customers,
                subject="We Miss You! Special Offer Inside",
                content=campaign_content.get('campaign_plan', 'Come back and save!'),
                campaign_context=campaign_context
            )
            results["email"] = email_results
            results["channels_deployed"].append("email")
            results["total_reach"] += email_results["sent"]
        
        # Deploy on Social Media with campaign context for image generation
        social_results = self._deploy_social_media(
            campaign_id=campaign_id,
            campaign_content=campaign_content,
            campaign_context=campaign_context
        )
        results["social_media"] = social_results
        results["channels_deployed"].extend(["facebook", "instagram", "twitter"])
        results["total_reach"] += social_results.get("stats", {}).get("total_impressions", 0)
        
        return results
    
    def deploy_digital_campaign(
        self,
        campaign_id: str,
        campaign_content: Dict[str, Any],
        campaign_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Deploy a digital/social media focused campaign"""
        results = {
            "campaign_id": campaign_id,
            "deployed_at": datetime.now().isoformat(),
            "channels_deployed": ["facebook", "instagram", "twitter"],
            "social_media": {},
            "total_reach": 0
        }
        
        # Heavy focus on social media
        social_results = self._deploy_social_media(
            campaign_id=campaign_id,
            campaign_content=campaign_content,
            posts_per_platform=1,  # One post per platform (Facebook, Instagram, Twitter)
            campaign_context=campaign_context
        )
        results["social_media"] = social_results
        results["total_reach"] = social_results.get("stats", {}).get("total_impressions", 0)
        
        return results
    
    def _deploy_email(
        self,
        campaign_id: str,
        customers: List[MockCustomer],
        subject: str,
        content: str,
        campaign_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Deploy email campaign"""
        recipients = [
            {"email": c.email, "name": c.name}
            for c in customers
        ]
        
        emails = self.email_service.send_bulk_emails(
            recipients=recipients,
            subject=subject,
            content=content,
            campaign_id=campaign_id,
            campaign_context=campaign_context
        )
        
        stats = self.email_service.get_campaign_stats(campaign_id)
        
        return {
            "sent": len(emails),
            "stats": stats
        }
    
    def _deploy_social_media(
        self,
        campaign_id: str,
        campaign_content: Dict[str, Any],
        posts_per_platform: int = 1,
        campaign_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Deploy social media campaign - images generated on-demand via UI"""
        posts = []
        
        # DO NOT generate images automatically - user will select platforms in UI
        # This saves API costs and gives user control over which platforms get images
        
        # Create posts for each platform WITHOUT images
        for platform in ["facebook", "instagram", "twitter"]:
            for i in range(posts_per_platform):
                content = self._generate_platform_content(
                    platform=platform,
                    campaign_content=campaign_content,
                    post_number=i+1
                )
                
                # No image URL - will be generated when user selects platform in UI
                image_url = None
                
                post = self.social_service.create_post(
                    platform=platform,
                    content=content["text"],
                    campaign_id=campaign_id,
                    image_url=image_url,
                    hashtags=content.get("hashtags", [])
                )
                posts.append(post)
        
        stats = self.social_service.get_campaign_stats(campaign_id)
        
        return {
            "posts_created": len(posts),
            "stats": stats
        }
    
    def _generate_platform_content(
        self,
        platform: str,
        campaign_content: Dict[str, Any],
        post_number: int
    ) -> Dict[str, Any]:
        """Generate platform-specific content"""
        campaign_type = campaign_content.get("campaign_type", "promotion")
        
        # Platform-specific templates
        if platform == "facebook":
            text = f"🎉 Special Offer Alert! {campaign_type.title()} - Don't miss out! Visit us today for amazing deals. Limited time only!"
            hashtags = ["#Sale", "#LocalBusiness", "#Shopping", "#Deals"]
        elif platform == "instagram":
            text = f"✨ New {campaign_type} ✨\nShop the latest deals! 🛍️\nTag a friend who needs this! 👇"
            hashtags = ["#ShopLocal", "#RetailTherapy", "#InstaShop", "#MustHave", "#Shopping"]
        else:  # twitter
            text = f"🔥 {campaign_type.title()} happening NOW! Don't wait - limited time offer. Check it out!"
            hashtags = ["#Sale", "#Deal", "#Shopping"]
        
        return {
            "text": text,
            "hashtags": hashtags,
            "image_url": f"https://example.com/promo_image_{post_number}.jpg"
        }
    
    def get_campaign_overview(self, campaign_id: str) -> Dict[str, Any]:
        """Get complete overview of campaign deployment and performance"""
        email_stats = self.email_service.get_campaign_stats(campaign_id)
        social_stats = self.social_service.get_campaign_stats(campaign_id)
        sentiment = self.social_service.get_sentiment_analysis(campaign_id)
        
        # Calculate overall metrics
        total_reach = email_stats.get("total_sent", 0) + social_stats.get("total_impressions", 0)
        total_engagement = (
            email_stats.get("clicked", 0) +
            social_stats.get("total_likes", 0) +
            social_stats.get("total_comments", 0) +
            social_stats.get("total_shares", 0)
        )
        
        return {
            "campaign_id": campaign_id,
            "total_reach": total_reach,
            "total_engagement": total_engagement,
            "email": email_stats,
            "social_media": social_stats,
            "sentiment": sentiment,
            "customer_database_size": len(self.customer_db.get_all_customers())
        }
    
    def get_all_emails(self) -> List[Dict[str, Any]]:
        """Get all sent emails"""
        return [e.to_dict() for e in self.email_service.get_all_emails()]
    
    def get_all_posts(self) -> List[Dict[str, Any]]:
        """Get all social media posts"""
        return [p.to_dict() for p in self.social_service.get_all_posts()]
    
    def get_customer_stats(self) -> Dict[str, Any]:
        """Get customer database statistics"""
        return self.customer_db.get_statistics()
