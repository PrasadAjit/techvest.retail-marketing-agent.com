"""
Mock Email Service
Simulates email sending with tracking
"""
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
try:
    from ..utils.llm_helper import get_llm
except ImportError:
    from src.utils.llm_helper import get_llm


@dataclass
class MockEmail:
    """Represents a sent email"""
    id: str
    campaign_id: str
    to_email: str
    to_name: str
    subject: str
    content: str
    sent_at: str
    opened: bool
    opened_at: Optional[str]
    clicked: bool
    clicked_at: Optional[str]
    converted: bool
    converted_at: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class MockEmailService:
    """Simulates email sending and tracking"""
    
    def __init__(self):
        self.emails: Dict[str, MockEmail] = {}
        self.campaigns: Dict[str, List[str]] = {}  # campaign_id -> email_ids
        self._email_counter = 0
        self.campaign_context: Dict[str, Dict[str, Any]] = {}  # Store campaign context for personalization
    
    def send_email(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        content: str,
        campaign_id: str
    ) -> MockEmail:
        """
        Send a mock email
        
        Args:
            to_email: Recipient email
            to_name: Recipient name
            subject: Email subject
            content: Email content/body
            campaign_id: Associated campaign ID
        
        Returns:
            MockEmail object
        """
        self._email_counter += 1
        email_id = f"EMAIL{self._email_counter:06d}"
        
        # Simulate realistic engagement rates with guaranteed conversions
        opened = random.random() < 0.45  # 45% open rate
        clicked = opened and random.random() < 0.25  # 25% click-through of opens (11.25% overall)
        converted = clicked and random.random() < 0.35  # 35% conversion of clicks
        
        email = MockEmail(
            id=email_id,
            campaign_id=campaign_id,
            to_email=to_email,
            to_name=to_name,
            subject=subject,
            content=content,
            sent_at=datetime.now().isoformat(),
            opened=opened,
            opened_at=datetime.now().isoformat() if opened else None,
            clicked=clicked,
            clicked_at=datetime.now().isoformat() if clicked else None,
            converted=converted,
            converted_at=datetime.now().isoformat() if converted else None
        )
        
        self.emails[email_id] = email
        
        # Track by campaign
        if campaign_id not in self.campaigns:
            self.campaigns[campaign_id] = []
        self.campaigns[campaign_id].append(email_id)
        
        return email
    
    def send_bulk_emails(
        self,
        recipients: List[Dict[str, str]],  # [{"email": ..., "name": ...}, ...]
        subject: str,
        content: str,
        campaign_id: str,
        campaign_context: Optional[Dict[str, Any]] = None
    ) -> List[MockEmail]:
        """
        Send bulk emails with personalized content for top 3
        
        Args:
            recipients: List of recipient dicts with 'email' and 'name'
            subject: Email subject
            content: Email content (generic template)
            campaign_id: Associated campaign ID
            campaign_context: Campaign details for personalization
        
        Returns:
            List of MockEmail objects
        """
        # Store campaign context for later retrieval
        if campaign_context:
            self.campaign_context[campaign_id] = campaign_context
        
        emails = []
        for idx, recipient in enumerate(recipients):
            # Generate personalized content for top 3 emails
            if idx < 3 and campaign_context:
                personalized_content = self._generate_personalized_email(
                    recipient_name=recipient["name"],
                    campaign_context=campaign_context,
                    base_content=content
                )
                personalized_subject = self._generate_personalized_subject(
                    recipient_name=recipient["name"],
                    campaign_context=campaign_context,
                    base_subject=subject
                )
            else:
                # Use generic content for the rest
                personalized_content = content
                personalized_subject = subject
            
            email = self.send_email(
                to_email=recipient["email"],
                to_name=recipient["name"],
                subject=personalized_subject,
                content=personalized_content,
                campaign_id=campaign_id
            )
            emails.append(email)
        
        return emails
    
    def _generate_personalized_email(
        self,
        recipient_name: str,
        campaign_context: Dict[str, Any],
        base_content: str
    ) -> str:
        """Generate personalized email content using LLM"""
        try:
            llm = get_llm(temperature=0.7)
            
            prompt = ChatPromptTemplate.from_template(
                """You are a professional email marketing copywriter. Create a personalized, engaging email for a retail marketing campaign.

Recipient Name: {recipient_name}

Campaign Details:
- Campaign Type: {campaign_type}
- Store Name: {store_name}
- Store Type: {store_type}
- Location: {location}
- Goal: {goal}
- Target Audience: {target_audience}
- Special Offers: {offers}

Base Email Template:
{base_content}

Create a warm, personalized email that:
1. Addresses {recipient_name} personally
2. Highlights the specific benefits relevant to this campaign
3. Includes a clear call-to-action
4. Matches the campaign goal and store brand
5. Is engaging and conversational
6. Keep it concise (200-300 words)

Write ONLY the email body content, no subject line:"""
            )
            
            chain = prompt | llm | StrOutputParser()
            
            personalized = chain.invoke({
                "recipient_name": recipient_name,
                "campaign_type": campaign_context.get("campaign_type", "marketing campaign"),
                "store_name": campaign_context.get("store_name", "our store"),
                "store_type": campaign_context.get("store_type", "retail"),
                "location": campaign_context.get("location", "your area"),
                "goal": campaign_context.get("goal", "engage with customers"),
                "target_audience": campaign_context.get("target_audience", "valued customers"),
                "offers": campaign_context.get("offers", "special promotions"),
                "base_content": base_content[:500]  # Limit base content length
            })
            
            return personalized.strip()
        except Exception as e:
            # Fallback to base content if LLM fails
            return f"Dear {recipient_name},\n\n{base_content}"
    
    def _generate_personalized_subject(
        self,
        recipient_name: str,
        campaign_context: Dict[str, Any],
        base_subject: str
    ) -> str:
        """Generate personalized email subject using LLM"""
        try:
            llm = get_llm(temperature=0.7)
            
            prompt = ChatPromptTemplate.from_template(
                """Create a compelling, personalized email subject line for a retail marketing campaign.

Recipient Name: {recipient_name}
Store Name: {store_name}
Campaign Type: {campaign_type}
Goal: {goal}
Base Subject: {base_subject}

Create a subject line that:
1. Is attention-grabbing and personalized
2. Includes recipient name if it fits naturally
3. Highlights key benefit or offer
4. Is 6-10 words maximum
5. Creates urgency or curiosity

Write ONLY the subject line, nothing else:"""
            )
            
            chain = prompt | llm | StrOutputParser()
            
            personalized = chain.invoke({
                "recipient_name": recipient_name,
                "store_name": campaign_context.get("store_name", "our store"),
                "campaign_type": campaign_context.get("campaign_type", "special offer"),
                "goal": campaign_context.get("goal", "exclusive deal"),
                "base_subject": base_subject
            })
            
            return personalized.strip()
        except Exception as e:
            # Fallback to base subject if LLM fails
            return f"{recipient_name}, {base_subject}"
    
    def get_email(self, email_id: str) -> Optional[MockEmail]:
        """Get email by ID"""
        return self.emails.get(email_id)
    
    def get_campaign_emails(self, campaign_id: str) -> List[MockEmail]:
        """Get all emails for a campaign"""
        email_ids = self.campaigns.get(campaign_id, [])
        return [self.emails[eid] for eid in email_ids if eid in self.emails]
    
    def get_campaign_stats(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign email statistics"""
        emails = self.get_campaign_emails(campaign_id)
        
        if not emails:
            return {
                "total_sent": 0,
                "opened": 0,
                "clicked": 0,
                "converted": 0,
                "open_rate": 0.0,
                "click_rate": 0.0,
                "conversion_rate": 0.0
            }
        
        total = len(emails)
        opened = sum(1 for e in emails if e.opened)
        clicked = sum(1 for e in emails if e.clicked)
        converted = sum(1 for e in emails if e.converted)
        
        return {
            "total_sent": total,
            "opened": opened,
            "clicked": clicked,
            "converted": converted,
            "open_rate": round(opened / total * 100, 2) if total > 0 else 0,
            "click_rate": round(clicked / total * 100, 2) if total > 0 else 0,
            "conversion_rate": round(converted / total * 100, 2) if total > 0 else 0
        }
    
    def get_all_emails(self) -> List[MockEmail]:
        """Get all sent emails"""
        return list(self.emails.values())
    
    def get_recent_emails(self, limit: int = 50) -> List[MockEmail]:
        """Get most recent emails"""
        return sorted(
            self.emails.values(),
            key=lambda e: e.sent_at,
            reverse=True
        )[:limit]
