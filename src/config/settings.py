"""
Configuration settings for Retail Marketing Agent
"""
import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class OpenAIConfig(BaseModel):
    """OpenAI API configuration"""
    # Standard OpenAI
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    # Azure OpenAI
    azure_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    azure_api_version: str = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")
    
    # DALL-E 3 REST API Configuration (for Indian region / custom endpoints)
    dalle_api_endpoint: str = os.getenv("DALLE_API_ENDPOINT", "https://api.openai.com/v1/images/generations")
    dalle_api_key: str = os.getenv("DALLE_API_KEY", "")
    dalle_model: str = os.getenv("DALLE_MODEL", "dall-e-3")
    
    # Use Azure if credentials are provided
    use_azure: bool = bool(os.getenv("AZURE_OPENAI_API_KEY"))
    
    # Common settings
    temperature: float = 0.7
    max_tokens: int = 2000


class StoreConfig(BaseModel):
    """Store information configuration"""
    name: str = os.getenv("STORE_NAME", "Retail Store")
    store_type: str = os.getenv("STORE_TYPE", "general")
    location: str = os.getenv("STORE_LOCATION", "")
    has_online_store: bool = os.getenv("HAS_ONLINE_STORE", "false").lower() == "true"
    website_url: Optional[str] = os.getenv("WEBSITE_URL")


class SocialMediaConfig(BaseModel):
    """Social media API configuration"""
    facebook_app_id: str = os.getenv("FACEBOOK_APP_ID", "")
    facebook_app_secret: str = os.getenv("FACEBOOK_APP_SECRET", "")
    instagram_username: str = os.getenv("INSTAGRAM_USERNAME", "")
    instagram_password: str = os.getenv("INSTAGRAM_PASSWORD", "")
    twitter_api_key: str = os.getenv("TWITTER_API_KEY", "")
    twitter_api_secret: str = os.getenv("TWITTER_API_SECRET", "")


class EmailConfig(BaseModel):
    """Email configuration"""
    sendgrid_api_key: str = os.getenv("SENDGRID_API_KEY", "")
    email_from: str = os.getenv("EMAIL_FROM", "marketing@store.com")


class DatabaseConfig(BaseModel):
    """Database configuration"""
    url: str = os.getenv("DATABASE_URL", "sqlite:///retail_marketing.db")


class AnalyticsConfig(BaseModel):
    """Analytics configuration"""
    google_analytics_id: str = os.getenv("GOOGLE_ANALYTICS_ID", "")


class CampaignConfig(BaseModel):
    """Default campaign configuration"""
    default_budget: float = float(os.getenv("DEFAULT_CAMPAIGN_BUDGET", "5000"))
    default_duration: int = int(os.getenv("DEFAULT_CAMPAIGN_DURATION", "30"))
    min_conversion_rate: float = float(os.getenv("MIN_CONVERSION_RATE", "0.02"))
    target_roi: float = float(os.getenv("TARGET_ROI", "3.0"))


class Settings(BaseModel):
    """Main settings class"""
    openai: OpenAIConfig = OpenAIConfig()
    store: StoreConfig = StoreConfig()
    social_media: SocialMediaConfig = SocialMediaConfig()
    email: EmailConfig = EmailConfig()
    database: DatabaseConfig = DatabaseConfig()
    analytics: AnalyticsConfig = AnalyticsConfig()
    campaign: CampaignConfig = CampaignConfig()


# Global settings instance
settings = Settings()
