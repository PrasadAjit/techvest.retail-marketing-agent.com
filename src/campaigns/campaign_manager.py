"""
Campaign Manager
Handles campaign planning, execution, tracking, and optimization
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum


class CampaignStatus(Enum):
    """Campaign status types"""
    DRAFT = "draft"
    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CampaignType(Enum):
    """Campaign types"""
    ACQUISITION = "acquisition"
    RETENTION = "retention"
    SEASONAL = "seasonal"
    PRODUCT_LAUNCH = "product_launch"
    CLEARANCE = "clearance"
    EVENT = "event"
    BRAND_AWARENESS = "brand_awareness"


class Campaign:
    """Represents a marketing campaign"""
    
    def __init__(
        self,
        name: str,
        campaign_type: CampaignType,
        description: str,
        start_date: datetime,
        end_date: datetime,
        budget: float,
        target_metrics: Dict[str, Any]
    ):
        self.id = self._generate_id()
        self.name = name
        self.campaign_type = campaign_type
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.target_metrics = target_metrics
        self.status = CampaignStatus.DRAFT
        self.channels: List[str] = []
        self.assets: Dict[str, Any] = {}
        self.performance: Dict[str, Any] = {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def _generate_id(self) -> str:
        """Generate unique campaign ID"""
        return f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def add_channel(self, channel: str):
        """Add a marketing channel to the campaign"""
        if channel not in self.channels:
            self.channels.append(channel)
            self.updated_at = datetime.now()
    
    def add_asset(self, asset_type: str, asset_data: Any):
        """Add a campaign asset (creative, copy, etc.)"""
        self.assets[asset_type] = asset_data
        self.updated_at = datetime.now()
    
    def update_status(self, status: CampaignStatus):
        """Update campaign status"""
        self.status = status
        self.updated_at = datetime.now()
    
    def update_performance(self, metrics: Dict[str, Any]):
        """Update performance metrics"""
        self.performance.update(metrics)
        self.updated_at = datetime.now()
    
    def get_duration_days(self) -> int:
        """Get campaign duration in days"""
        return (self.end_date - self.start_date).days
    
    def is_active(self) -> bool:
        """Check if campaign is currently active"""
        now = datetime.now()
        return (
            self.status == CampaignStatus.ACTIVE and
            self.start_date <= now <= self.end_date
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert campaign to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "campaign_type": self.campaign_type.value,
            "description": self.description,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "duration_days": self.get_duration_days(),
            "budget": self.budget,
            "target_metrics": self.target_metrics,
            "status": self.status.value,
            "channels": self.channels,
            "assets": self.assets,
            "performance": self.performance,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class CampaignManager:
    """Manages marketing campaigns"""
    
    def __init__(self):
        self.campaigns: Dict[str, Campaign] = {}
    
    def create_campaign(
        self,
        name: str,
        campaign_type: str,
        description: str,
        start_date: datetime,
        end_date: datetime,
        budget: float,
        target_metrics: Dict[str, Any]
    ) -> Campaign:
        """
        Create a new campaign
        
        Args:
            name: Campaign name
            campaign_type: Type of campaign
            description: Campaign description
            start_date: Campaign start date
            end_date: Campaign end date
            budget: Campaign budget
            target_metrics: Target metrics (impressions, conversions, etc.)
        
        Returns:
            Created Campaign object
        """
        campaign_type_enum = CampaignType[campaign_type.upper()]
        
        campaign = Campaign(
            name=name,
            campaign_type=campaign_type_enum,
            description=description,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            target_metrics=target_metrics
        )
        
        self.campaigns[campaign.id] = campaign
        return campaign
    
    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """Get a campaign by ID"""
        return self.campaigns.get(campaign_id)
    
    def get_active_campaigns(self) -> List[Campaign]:
        """Get all active campaigns"""
        return [c for c in self.campaigns.values() if c.is_active()]
    
    def get_campaigns_by_type(self, campaign_type: CampaignType) -> List[Campaign]:
        """Get campaigns by type"""
        return [c for c in self.campaigns.values() if c.campaign_type == campaign_type]
    
    def get_campaigns_by_status(self, status: CampaignStatus) -> List[Campaign]:
        """Get campaigns by status"""
        return [c for c in self.campaigns.values() if c.status == status]
    
    def launch_campaign(self, campaign_id: str) -> bool:
        """Launch a campaign"""
        campaign = self.get_campaign(campaign_id)
        if campaign and campaign.status == CampaignStatus.PLANNED:
            campaign.update_status(CampaignStatus.ACTIVE)
            return True
        return False
    
    def pause_campaign(self, campaign_id: str) -> bool:
        """Pause an active campaign"""
        campaign = self.get_campaign(campaign_id)
        if campaign and campaign.status == CampaignStatus.ACTIVE:
            campaign.update_status(CampaignStatus.PAUSED)
            return True
        return False
    
    def complete_campaign(self, campaign_id: str) -> bool:
        """Mark a campaign as completed"""
        campaign = self.get_campaign(campaign_id)
        if campaign:
            campaign.update_status(CampaignStatus.COMPLETED)
            return True
        return False
    
    def calculate_roi(self, campaign_id: str, revenue: float) -> Optional[float]:
        """Calculate campaign ROI"""
        campaign = self.get_campaign(campaign_id)
        if campaign and campaign.budget > 0:
            roi = (revenue - campaign.budget) / campaign.budget * 100
            return round(roi, 2)
        return None
    
    def get_campaign_summary(self) -> Dict[str, Any]:
        """Get summary of all campaigns"""
        return {
            "total_campaigns": len(self.campaigns),
            "active_campaigns": len(self.get_active_campaigns()),
            "total_budget": sum(c.budget for c in self.campaigns.values()),
            "campaigns_by_type": {
                ct.value: len(self.get_campaigns_by_type(ct))
                for ct in CampaignType
            },
            "campaigns_by_status": {
                cs.value: len(self.get_campaigns_by_status(cs))
                for cs in CampaignStatus
            }
        }
    
    def get_all_campaigns(self) -> List[Dict[str, Any]]:
        """Get all campaigns as dictionaries"""
        return [c.to_dict() for c in self.campaigns.values()]
