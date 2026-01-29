"""
Mock Social Media Service
Simulates posting to Facebook, Instagram, Twitter with engagement tracking
"""
import random
import requests
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
try:
    from ..utils.llm_helper import get_llm
    from ..config.settings import settings
except ImportError:
    from src.utils.llm_helper import get_llm
    from src.config.settings import settings
import openai

# Setup logger
logger = logging.getLogger(__name__)


class Platform(Enum):
    """Social media platforms"""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"


@dataclass
class MockSocialPost:
    """Represents a social media post"""
    id: str
    campaign_id: str
    platform: str
    content: str
    image_url: Optional[str]
    hashtags: List[str]
    posted_at: str
    impressions: int
    likes: int
    comments: int
    shares: int
    clicks: int
    engagement_rate: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class MockSocialComment:
    """Represents a comment on a social post"""
    id: str
    post_id: str
    author_name: str
    content: str
    sentiment: str  # positive, neutral, negative
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class MockSocialMediaService:
    """Simulates social media posting and engagement"""
    
    POSITIVE_COMMENTS = [
        "Love this! 😍",
        "Great deal! Thanks for sharing!",
        "Just ordered mine! 🎉",
        "This is amazing! 💯",
        "Can't wait to visit!",
        "Awesome! When does this start?",
        "Perfect timing! Just what I needed!",
        "Your store is the best! ❤️",
        "This looks great! 👍",
        "Definitely checking this out!"
    ]
    
    NEUTRAL_COMMENTS = [
        "What are the store hours?",
        "Is this available online?",
        "Do you ship?",
        "More info please?",
        "Interesting...",
        "How long is this offer valid?",
        "What colors do you have?",
        "Is this still available?",
        "Where is your location?",
        "Can I use this with other offers?"
    ]
    
    NEGATIVE_COMMENTS = [
        "Wish the prices were better",
        "Out of stock again? 😞",
        "Shipping takes too long",
        "Had a bad experience last time",
        "Too expensive",
        "Not interested",
        "Meh...",
        "Already have this",
        "Seen better elsewhere"
    ]
    
    COMMENT_AUTHORS = [
        "Sarah Johnson", "Mike Williams", "Emily Davis", "James Brown", "Jessica Miller",
        "David Wilson", "Ashley Taylor", "Chris Anderson", "Amanda Thomas", "Ryan Martinez",
        "Jennifer Lopez", "Kevin Garcia", "Laura Rodriguez", "Brian Lee", "Nicole White"
    ]
    
    def __init__(self):
        self.posts: Dict[str, MockSocialPost] = {}
        self.comments: Dict[str, List[MockSocialComment]] = {}  # post_id -> comments
        self.campaigns: Dict[str, List[str]] = {}  # campaign_id -> post_ids
        self._post_counter = 0
        self._comment_counter = 0
        self.campaign_images: Dict[str, Dict[str, str]] = {}  # campaign_id -> {platform: image_url}
    
    def generate_campaign_image(
        self,
        platform: str,
        campaign_context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate AI image for social media post using DALL-E or gpt-image-1
        
        Args:
            platform: Social media platform (facebook, instagram, twitter)
            campaign_context: Campaign details for image generation
        
        Returns:
            Image URL or None if generation fails
        """
        try:
            # Extract campaign-specific details
            store_name = campaign_context.get("store_name", "retail store")
            store_type = campaign_context.get("store_type", "retail")
            campaign_type = campaign_context.get("campaign_type", "promotion")
            goal = campaign_context.get("goal", "attract customers")
            offers = campaign_context.get("offers", "")
            target_audience = campaign_context.get("target_audience", "customers")
            location = campaign_context.get("location", "")
            
            # Build product-focused scene description (not store-focused)
            # Map store types to product categories
            product_category = store_type
            
            # Customize scene based on actual campaign content - PRODUCT FOCUSED
            if "acquisition" in campaign_type.lower() or "new customer" in goal.lower():
                scene = f"attractive {product_category} products being used by happy customers in lifestyle setting"
                theme = "inviting, energetic, and discovery-focused"
                mood = "excitement and curiosity"
            elif "retention" in campaign_type.lower() or "loyalty" in goal.lower():
                scene = f"premium {product_category} products showcased in elegant setting with satisfied customers"
                theme = "luxurious, exclusive, and rewarding"
                mood = "satisfaction and appreciation"
            elif "sale" in offers.lower() or "discount" in offers.lower() or "promotion" in campaign_type.lower():
                scene = f"eye-catching collection of {product_category} products with special offer highlights"
                theme = "energetic, value-focused, and compelling"
                mood = "excitement and urgency"
            elif "seasonal" in goal.lower() or "holiday" in goal.lower():
                scene = f"festive display of {product_category} products with seasonal decorations and happy people"
                theme = "seasonal, festive, and celebratory"
                mood = "joy and celebration"
            else:
                scene = f"beautiful {product_category} products in modern lifestyle context with people enjoying them"
                theme = "contemporary, appealing, and lifestyle-focused"
                mood = "comfort and satisfaction"
            
            # Add location context if provided
            location_context = f" for {location} market" if location else ""
            
            # Platform-specific style guidance
            platform_styles = {
                "facebook": "warm lifestyle photography with community feel, people using products naturally",
                "instagram": "aesthetically stunning with bold colors, high-fashion editorial quality, Instagram-worthy product showcase",
                "twitter": "dynamic candid moment with energy and movement, photojournalistic authenticity"
            }
            
            style = platform_styles.get(platform, "professional commercial photography")
            
            # Create highly detailed, product-focused DALL-E prompt
            image_prompt = f"""Professional product photography for {product_category} marketing campaign{location_context}.

SCENE: {scene}
Campaign Focus: {goal}
Target Audience: {target_audience}

VISUAL STYLE: {style}
Atmosphere: {theme}
Emotional Tone: {mood}

MAIN FOCUS: {product_category} products (NOT stores or buildings)
Show products being:
- Used, worn, or enjoyed by people in real-life scenarios
- Displayed attractively in lifestyle context
- Featured as the hero/main subject of the image

ELEMENTS TO INCLUDE:
- {product_category} products as the primary focus and hero element
- People actively using, wearing, or enjoying the products
- Lifestyle setting that shows product benefits and usage
- Natural environment or contextual background (NOT retail stores)
- Diverse people (various ages, ethnicities) authentically engaged with products

VISUAL REQUIREMENTS:
- High-quality 4K commercial product photography
- Natural lighting with professional color grading
- Lifestyle photography aesthetic showing product in use
- Brand-appropriate composition with products as hero
- NO text, NO words, NO letters, NO price tags, NO signs
- NO store interiors, NO shopping carts, NO cash registers
- Pure photographic content focused on products and their lifestyle use

MOOD & FEELING: {mood}, aspirational lifestyle that makes viewers want to own and use these {product_category} products."""
            
            print(f"\n🎨 Generating campaign-specific image for {platform}...")
            print(f"   Campaign: {campaign_type}")
            print(f"   Goal: {goal[:50]}...")
            print(f"   Store: {store_type}")
            
            # Try DALL-E 3 image generation with REST API
            try:
                # Priority 1: Use DALL-E REST API endpoint (configured in .env)
                if settings.openai.dalle_api_key and settings.openai.dalle_api_endpoint:
                    print(f"   🔹 Using DALL-E 3 REST API (configured endpoint)...")
                    print(f"   🌐 Endpoint: {settings.openai.dalle_api_endpoint}")
                    
                    # Prepare REST API request
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {settings.openai.dalle_api_key}"
                    }
                    
                    # Check if it's Azure OpenAI endpoint (different format)
                    if "azure.com" in settings.openai.dalle_api_endpoint.lower():
                        headers = {
                            "Content-Type": "application/json",
                            "api-key": settings.openai.dalle_api_key
                        }
                        print(f"   🔹 Detected Azure OpenAI endpoint format")
                    
                    payload = {
                        "prompt": image_prompt,
                        "n": 1,
                        "size": "1024x1024"
                    }
                    
                    # Add model parameter if not Azure endpoint
                    if "azure.com" not in settings.openai.dalle_api_endpoint.lower():
                        payload["model"] = settings.openai.dalle_model
                        payload["quality"] = "standard"
                    
                    try:
                        print(f"   🔹 Making REST API call to DALL-E 3...")
                        response = requests.post(
                            settings.openai.dalle_api_endpoint,
                            headers=headers,
                            json=payload,
                            timeout=60
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            image_url = result["data"][0]["url"]
                            print(f"   ✅ Successfully generated image with DALL-E 3 (REST API)")
                            return image_url
                        elif response.status_code == 429:
                            # Rate limit exceeded - use stock images
                            error_msg = response.json() if 'application/json' in response.headers.get('content-type', '') else response.text
                            print(f"   ⚠️ DALL-E 3 Rate Limit Reached (Status 429)")
                            print(f"   💡 Azure pricing tier limit exceeded - falling back to stock images")
                            print(f"   📸 Using high-quality curated stock images instead...")
                            return self._get_stock_image(platform, campaign_context)
                        else:
                            error_msg = response.json() if 'application/json' in response.headers.get('content-type', '') else response.text
                            print(f"   ⚠️ DALL-E 3 REST API failed (Status {response.status_code}): {str(error_msg)[:200]}")
                            print(f"   📸 Falling back to stock images...")
                            return self._get_stock_image(platform, campaign_context)
                    except requests.exceptions.Timeout:
                        print(f"   ⚠️ DALL-E 3 REST API timeout (60s exceeded)")
                        print(f"   📸 Using stock images instead...")
                        return self._get_stock_image(platform, campaign_context)
                    except Exception as rest_error:
                        print(f"   ⚠️ DALL-E 3 REST API error: {str(rest_error)[:200]}")
                        print(f"   📸 Using stock images instead...")
                        return self._get_stock_image(platform, campaign_context)
                
                # Priority 2: Try Azure OpenAI SDK
                elif settings.openai.use_azure and settings.openai.azure_api_key:
                    print(f"   🔹 Using Azure OpenAI SDK for image generation...")
                    
                    # Create Azure OpenAI client
                    from openai import AzureOpenAI
                    client = AzureOpenAI(
                        api_key=settings.openai.azure_api_key,
                        api_version=settings.openai.azure_api_version,
                        azure_endpoint=settings.openai.azure_endpoint
                    )
                    
                    # Try GPT-image-1 model (as requested by user)
                    try:
                        print(f"   🔹 Attempting GPT-image-1 with Azure OpenAI...")
                        response = client.images.generate(
                            model="gpt-image-1",
                            prompt=image_prompt,
                            size="1024x1024",
                            n=1
                        )
                        image_url = response.data[0].url
                        print(f"   ✅ Successfully generated image with GPT-image-1 (Azure)")
                        return image_url
                    except Exception as gpt_img_error:
                        print(f"   ⚠️ GPT-image-1 (Azure) failed: {str(gpt_img_error)[:150]}")
                        
                        # Try DALL-E 3 with Azure as fallback
                        try:
                            print(f"   🔹 Attempting DALL-E 3 with Azure OpenAI...")
                            response = client.images.generate(
                                model="dall-e-3",
                                prompt=image_prompt,
                                size="1024x1024",
                                quality="standard",
                                n=1
                            )
                            image_url = response.data[0].url
                            print(f"   ✅ Successfully generated image with DALL-E 3 (Azure)")
                            return image_url
                        except Exception as dalle_azure_error:
                            print(f"   ⚠️ DALL-E 3 (Azure) failed: {str(dalle_azure_error)[:150]}")
                            print(f"   📸 Azure OpenAI image generation not available in your region")
                            print(f"   📸 Using high-quality curated stock images...")
                            return self._get_stock_image(platform, campaign_context)
                
                # Try standard OpenAI if Azure not configured
                elif settings.openai.api_key:
                    print(f"   🔹 Using standard OpenAI for image generation...")
                    client = openai.OpenAI(api_key=settings.openai.api_key)
                    
                    # Try DALL-E 3 first (best quality)
                    try:
                        print(f"   🔹 Attempting DALL-E 3...")
                        response = client.images.generate(
                            model="dall-e-3",
                            prompt=image_prompt,
                            size="1024x1024",
                            quality="standard",
                            n=1
                        )
                        image_url = response.data[0].url
                        print(f"   ✅ Successfully generated image with DALL-E 3")
                        return image_url
                    except Exception as dalle_error:
                        print(f"   ⚠️ DALL-E 3 failed: {str(dalle_error)[:100]}")
                        
                        # Try gpt-image-1 as fallback
                        try:
                            print(f"   🔹 Attempting gpt-image-1 fallback...")
                            response = client.images.generate(
                                model="gpt-image-1",
                                prompt=image_prompt,
                                size="1024x1024",
                                n=1
                            )
                            image_url = response.data[0].url
                            print(f"   ✅ Successfully generated image with gpt-image-1")
                            return image_url
                        except Exception as gpt_img_error:
                            print(f"   ⚠️ gpt-image-1 failed: {str(gpt_img_error)[:100]}")
                            
                            # Try DALL-E 2 as last resort
                            try:
                                print(f"   🔹 Attempting DALL-E 2 fallback...")
                                response = client.images.generate(
                                    model="dall-e-2",
                                    prompt=image_prompt[:1000],  # DALL-E 2 has shorter prompt limit
                                    size="1024x1024",
                                    n=1
                                )
                                image_url = response.data[0].url
                                print(f"   ✅ Successfully generated image with DALL-E 2")
                                return image_url
                            except Exception as dalle2_error:
                                print(f"   ⚠️ DALL-E 2 failed: {str(dalle2_error)[:100]}")
                                raise dalle2_error
                else:
                    print(f"   ⚠️ No OpenAI API key found")
                    print(f"   📸 Using high-quality curated stock images...")
                    return self._get_stock_image(platform, campaign_context)
                    
            except Exception as api_error:
                print(f"   ❌ All image generation models failed, using stock images")
                return self._get_stock_image(platform, campaign_context)
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Image generation error for {platform}: {error_msg}")
            
            # Return high-quality stock images instead of text placeholders
            return self._get_stock_image(platform, campaign_context)
    
    def _get_stock_image(self, platform: str, campaign_context: Dict[str, Any]) -> str:
        """Get a high-quality stock image URL as fallback - RANDOMIZED for variety"""
        import hashlib
        import time
        
        store_type = campaign_context.get("store_type", "retail").lower()
        campaign_type = campaign_context.get("campaign_type", "").lower()
        goal = campaign_context.get("goal", "")
        offers = campaign_context.get("offers", "")
        
        # Determine the best image category based on context
        if "clothing" in store_type or "fashion" in store_type or "apparel" in store_type:
            category = "fashion"
            image_pool = [1, 15, 16, 21, 24, 27, 33, 40, 48, 49, 52, 56, 60, 64, 65, 82, 91]
        elif "food" in store_type or "grocery" in store_type or "restaurant" in store_type:
            category = "food"
            image_pool = [2, 10, 30, 42, 51, 59, 70, 96, 162, 163, 225, 292, 326, 431, 436]
        elif "electronics" in store_type or "tech" in store_type:
            category = "technology"
            image_pool = [0, 3, 20, 77, 119, 152, 180, 249, 250, 326, 367, 487]
        elif "beauty" in store_type or "cosmetic" in store_type:
            category = "beauty"
            image_pool = [8, 26, 36, 47, 54, 61, 63, 103, 177, 200, 240, 314, 349]
        elif "home" in store_type or "furniture" in store_type:
            category = "home"
            image_pool = [7, 14, 17, 19, 101, 106, 112, 152, 175, 181, 398, 447, 502]
        else:
            category = "retail"
            image_pool = [1, 2, 3, 10, 15, 20, 30, 42, 48, 52, 56, 60, 70, 82, 91, 96]
        
        # Create a unique seed based on campaign details + timestamp to ensure variation
        seed_string = f"{platform}{store_type}{campaign_type}{goal}{offers}{time.time()}"
        seed_hash = hashlib.md5(seed_string.encode()).hexdigest()
        seed_number = int(seed_hash[:8], 16)
        
        # Select an image ID from the pool based on the seed
        image_id = image_pool[seed_number % len(image_pool)]
        
        print(f"   📸 Selected image ID: {image_id} from {category} category ({len(image_pool)} options)")
        
        # Return social media sized image (600x400 - perfect for posts)
        return f"https://picsum.photos/id/{image_id}/600/400"
    
    def create_post(
        self,
        platform: str,
        content: str,
        campaign_id: str,
        image_url: Optional[str] = None,
        hashtags: Optional[List[str]] = None
    ) -> MockSocialPost:
        """
        Create a social media post
        
        Args:
            platform: Social media platform (facebook, instagram, twitter)
            content: Post content/caption
            campaign_id: Associated campaign ID
            image_url: Optional image URL
            hashtags: Optional list of hashtags
        
        Returns:
            MockSocialPost object
        """
        self._post_counter += 1
        post_id = f"{platform.upper()}{self._post_counter:06d}"
        
        # Generate realistic engagement based on platform
        if platform == "facebook":
            base_impressions = random.randint(1000, 5000)
            engagement_multiplier = 0.05  # 5% engagement rate
        elif platform == "instagram":
            base_impressions = random.randint(2000, 8000)
            engagement_multiplier = 0.08  # 8% engagement rate
        else:  # twitter
            base_impressions = random.randint(500, 3000)
            engagement_multiplier = 0.03  # 3% engagement rate
        
        impressions = base_impressions
        total_engagements = int(impressions * engagement_multiplier)
        
        # Distribute engagements
        likes = int(total_engagements * random.uniform(0.6, 0.75))
        comments_count = int(total_engagements * random.uniform(0.05, 0.15))
        shares = int(total_engagements * random.uniform(0.05, 0.15))
        clicks = int(total_engagements * random.uniform(0.10, 0.25))
        
        engagement_rate = round((likes + comments_count + shares) / impressions * 100, 2)
        
        post = MockSocialPost(
            id=post_id,
            campaign_id=campaign_id,
            platform=platform,
            content=content,
            image_url=image_url,
            hashtags=hashtags or [],
            posted_at=datetime.now().isoformat(),
            impressions=impressions,
            likes=likes,
            comments=comments_count,
            shares=shares,
            clicks=clicks,
            engagement_rate=engagement_rate
        )
        
        self.posts[post_id] = post
        
        # Track by campaign
        if campaign_id not in self.campaigns:
            self.campaigns[campaign_id] = []
        self.campaigns[campaign_id].append(post_id)
        
        # Generate some mock comments
        self._generate_comments(post_id, comments_count)
        
        return post
    
    def _generate_comments(self, post_id: str, count: int):
        """Generate mock comments for a post"""
        self.comments[post_id] = []
        
        for _ in range(count):
            self._comment_counter += 1
            comment_id = f"COMMENT{self._comment_counter:06d}"
            
            # Random sentiment distribution: 60% positive, 30% neutral, 10% negative
            sentiment_choice = random.random()
            if sentiment_choice < 0.6:
                sentiment = "positive"
                content = random.choice(self.POSITIVE_COMMENTS)
            elif sentiment_choice < 0.9:
                sentiment = "neutral"
                content = random.choice(self.NEUTRAL_COMMENTS)
            else:
                sentiment = "negative"
                content = random.choice(self.NEGATIVE_COMMENTS)
            
            comment = MockSocialComment(
                id=comment_id,
                post_id=post_id,
                author_name=random.choice(self.COMMENT_AUTHORS),
                content=content,
                sentiment=sentiment,
                created_at=datetime.now().isoformat()
            )
            
            self.comments[post_id].append(comment)
    
    def get_post(self, post_id: str) -> Optional[MockSocialPost]:
        """Get post by ID"""
        return self.posts.get(post_id)
    
    def get_post_comments(self, post_id: str) -> List[MockSocialComment]:
        """Get comments for a post"""
        return self.comments.get(post_id, [])
    
    def get_campaign_posts(self, campaign_id: str) -> List[MockSocialPost]:
        """Get all posts for a campaign"""
        post_ids = self.campaigns.get(campaign_id, [])
        return [self.posts[pid] for pid in post_ids if pid in self.posts]
    
    def get_campaign_stats(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign social media statistics"""
        posts = self.get_campaign_posts(campaign_id)
        
        if not posts:
            return {
                "total_posts": 0,
                "total_impressions": 0,
                "total_likes": 0,
                "total_comments": 0,
                "total_shares": 0,
                "total_clicks": 0,
                "avg_engagement_rate": 0.0,
                "by_platform": {}
            }
        
        total_impressions = sum(p.impressions for p in posts)
        total_likes = sum(p.likes for p in posts)
        total_comments = sum(p.comments for p in posts)
        total_shares = sum(p.shares for p in posts)
        total_clicks = sum(p.clicks for p in posts)
        avg_engagement = round(sum(p.engagement_rate for p in posts) / len(posts), 2)
        
        # Stats by platform
        by_platform = {}
        for platform in ["facebook", "instagram", "twitter"]:
            platform_posts = [p for p in posts if p.platform == platform]
            if platform_posts:
                by_platform[platform] = {
                    "posts": len(platform_posts),
                    "impressions": sum(p.impressions for p in platform_posts),
                    "engagement_rate": round(
                        sum(p.engagement_rate for p in platform_posts) / len(platform_posts), 2
                    )
                }
        
        return {
            "total_posts": len(posts),
            "total_impressions": total_impressions,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "total_clicks": total_clicks,
            "avg_engagement_rate": avg_engagement,
            "by_platform": by_platform
        }
    
    def get_all_posts(self) -> List[MockSocialPost]:
        """Get all posts"""
        return list(self.posts.values())
    
    def update_post_image(self, post_id: str, image_url: str) -> bool:
        """Update the image URL for a specific post"""
        if post_id in self.posts:
            self.posts[post_id].image_url = image_url
            return True
        return False
    
    def get_recent_posts(self, limit: int = 50) -> List[MockSocialPost]:
        """Get most recent posts"""
        return sorted(
            self.posts.values(),
            key=lambda p: p.posted_at,
            reverse=True
        )[:limit]
    
    def get_sentiment_analysis(self, campaign_id: str) -> Dict[str, Any]:
        """Analyze sentiment of comments for a campaign"""
        posts = self.get_campaign_posts(campaign_id)
        all_comments = []
        
        for post in posts:
            all_comments.extend(self.get_post_comments(post.id))
        
        if not all_comments:
            return {
                "total_comments": 0,
                "positive": 0,
                "neutral": 0,
                "negative": 0,
                "positive_percent": 0.0,
                "negative_percent": 0.0
            }
        
        positive = len([c for c in all_comments if c.sentiment == "positive"])
        neutral = len([c for c in all_comments if c.sentiment == "neutral"])
        negative = len([c for c in all_comments if c.sentiment == "negative"])
        total = len(all_comments)
        
        return {
            "total_comments": total,
            "positive": positive,
            "neutral": neutral,
            "negative": negative,
            "positive_percent": round(positive / total * 100, 2),
            "negative_percent": round(negative / total * 100, 2)
        }
