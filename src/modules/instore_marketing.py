"""
In-Store Marketing Module
Handles visual merchandising, displays, and in-store experiences
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

from ..utils.llm_helper import get_llm


class InStoreMarketingModule:
    """Module for in-store marketing strategies"""
    
    def __init__(self):
        self.llm = get_llm()
    
    def design_visual_merchandising(
        self,
        season: str,
        focus_products: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Design visual merchandising strategy
        
        Args:
            season: Current season or campaign period
            focus_products: Products to highlight
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert visual merchandiser for retail stores.
            Create displays that attract attention and drive purchases."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Season: {season}
            Focus Products: {focus_products}
            
            Design a visual merchandising strategy including:
            1. Window display concept and theme
            2. In-store display arrangements
            3. Color schemes and lighting
            4. Product placement and grouping
            5. Signage and messaging
            6. Customer flow optimization
            7. Focal points and feature areas
            8. Seasonal decorations and props
            
            Make displays eye-catching and sales-driving.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "season": season,
            "focus_products": focus_products
        })
        
        merchandising_plan = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "merchandising_plan": merchandising_plan,
            "season": season,
            "focus_products": focus_products,
            "status": "designed",
            "created_at": datetime.now().isoformat()
        }
    
    def create_pos_displays(
        self,
        promotion_type: str,
        location: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create point-of-sale display concepts
        
        Args:
            promotion_type: Type of promotion (sale, new product, impulse buy)
            location: Display location (checkout, endcap, entrance)
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in point-of-sale marketing and impulse purchasing.
            Create POS displays that maximize last-minute sales."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Promotion Type: {promotion_type}
            Display Location: {location}
            
            Design POS displays including:
            1. Display structure and size
            2. Product selection and arrangement
            3. Messaging and signage
            4. Price point strategy
            5. Visual appeal elements
            6. Easy-to-grab packaging considerations
            7. Seasonal or themed variations
            8. Expected conversion lift
            
            Focus on impulse purchase psychology.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "promotion_type": promotion_type,
            "location": location
        })
        
        pos_design = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "pos_design": pos_design,
            "promotion_type": promotion_type,
            "location": location,
            "status": "designed",
            "created_at": datetime.now().isoformat()
        }
    
    def plan_instore_event(
        self,
        event_type: str,
        duration_hours: int,
        expected_attendance: int,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Plan an in-store event or product demonstration
        
        Args:
            event_type: Type of event (product launch, workshop, demo, sale event)
            duration_hours: Event duration in hours
            expected_attendance: Expected number of attendees
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert event planner for retail environments.
            Create engaging in-store events that drive traffic and sales."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Event Type: {event_type}
            Duration: {duration_hours} hours
            Expected Attendance: {expected_attendance} people
            
            Plan an in-store event including:
            1. Event concept and theme
            2. Schedule and timeline
            3. Activities and entertainment
            4. Product demonstrations or showcases
            5. Promotional offers for attendees
            6. Staff requirements and roles
            7. Setup and logistics
            8. Marketing and promotion plan
            9. Post-event follow-up strategy
            10. Budget estimate
            
            Make the event memorable and sales-focused.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "event_type": event_type,
            "duration_hours": duration_hours,
            "expected_attendance": expected_attendance
        })
        
        event_plan = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "event_plan": event_plan,
            "event_type": event_type,
            "duration_hours": duration_hours,
            "expected_attendance": expected_attendance,
            "status": "planned",
            "created_at": datetime.now().isoformat()
        }
    
    def create_signage_materials(
        self,
        signage_type: str,
        message: str,
        store_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create in-store signage and promotional materials
        
        Args:
            signage_type: Type of signage (sale, directional, promotional, informational)
            message: Key message to communicate
            store_context: Store information
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in retail signage and visual communication.
            Create clear, compelling signage that guides and motivates customers."""),
            ("user", """Store: {store_name}
            Store Type: {store_type}
            Signage Type: {signage_type}
            Key Message: {message}
            
            Create signage materials including:
            1. Headline and body text
            2. Visual design recommendations
            3. Size and format specifications
            4. Color scheme and branding
            5. Placement recommendations
            6. Call-to-action
            7. Variations for different store areas
            
            Make signage clear, readable, and action-oriented.""")
        ])
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "store_name": store_context.get("name", "Store"),
            "store_type": store_context.get("type", "retail"),
            "signage_type": signage_type,
            "message": message
        })
        
        signage_design = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "signage_design": signage_design,
            "signage_type": signage_type,
            "message": message,
            "status": "designed",
            "created_at": datetime.now().isoformat()
        }
