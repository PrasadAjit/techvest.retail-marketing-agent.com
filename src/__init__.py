"""
Retail Marketing Agent Package
"""
from .agents import RetailMarketingAgent, Goal, GoalType, GoalStatus
from .modules import (
    CustomerAcquisitionModule,
    CustomerRetentionModule,
    DigitalMarketingModule,
    InStoreMarketingModule
)
from .analytics import CustomerAnalyticsModule
from .campaigns import Campaign, CampaignManager, CampaignStatus, CampaignType
from .config import settings

__version__ = "1.0.0"

__all__ = [
    "RetailMarketingAgent",
    "Goal",
    "GoalType",
    "GoalStatus",
    "CustomerAcquisitionModule",
    "CustomerRetentionModule",
    "DigitalMarketingModule",
    "InStoreMarketingModule",
    "CustomerAnalyticsModule",
    "Campaign",
    "CampaignManager",
    "CampaignStatus",
    "CampaignType",
    "settings"
]
