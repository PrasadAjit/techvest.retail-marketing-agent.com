"""
Mock Customer Database
Generates and manages dummy customer data for simulation
"""
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict


@dataclass
class MockCustomer:
    """Represents a mock customer"""
    id: str
    name: str
    email: str
    phone: str
    segment: str  # new, occasional, frequent, vip
    location: str
    age_group: str  # 18-25, 26-35, 36-45, 46-55, 56+
    interests: List[str]
    purchase_history: int  # number of purchases
    total_spent: float
    last_purchase_date: Optional[str]
    email_opt_in: bool
    sms_opt_in: bool
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class MockCustomerDatabase:
    """Manages mock customer data"""
    
    FIRST_NAMES = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
        "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
        "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
        "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa",
        "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca", "Jason", "Sharon"
    ]
    
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell"
    ]
    
    LOCATIONS = [
        "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ",
        "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA",
        "Austin, TX", "Jacksonville, FL", "Fort Worth, TX", "Columbus, OH", "Charlotte, NC",
        "San Francisco, CA", "Indianapolis, IN", "Seattle, WA", "Denver, CO", "Boston, MA"
    ]
    
    INTERESTS = [
        "fashion", "electronics", "home_decor", "sports", "books", "beauty", "fitness",
        "food", "travel", "photography", "gaming", "music", "art", "gardening", "pets",
        "outdoor", "technology", "health", "cooking", "crafts"
    ]
    
    def __init__(self, num_customers: int = 500):
        """
        Initialize mock customer database
        
        Args:
            num_customers: Number of mock customers to generate
        """
        self.customers: Dict[str, MockCustomer] = {}
        self._generate_customers(num_customers)
    
    def _generate_customers(self, count: int):
        """Generate mock customers"""
        for i in range(count):
            customer_id = f"CUST{i+1:05d}"
            first_name = random.choice(self.FIRST_NAMES)
            last_name = random.choice(self.LAST_NAMES)
            
            # Determine segment and corresponding behavior
            segment = random.choices(
                ["new", "occasional", "frequent", "vip"],
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]
            
            if segment == "new":
                purchase_history = 0
                total_spent = 0.0
                last_purchase = None
            elif segment == "occasional":
                purchase_history = random.randint(1, 5)
                total_spent = round(random.uniform(50, 500), 2)
                last_purchase = (datetime.now() - timedelta(days=random.randint(30, 180))).isoformat()
            elif segment == "frequent":
                purchase_history = random.randint(6, 20)
                total_spent = round(random.uniform(500, 2000), 2)
                last_purchase = (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat()
            else:  # vip
                purchase_history = random.randint(21, 100)
                total_spent = round(random.uniform(2000, 10000), 2)
                last_purchase = (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            
            customer = MockCustomer(
                id=customer_id,
                name=f"{first_name} {last_name}",
                email=f"{first_name.lower()}.{last_name.lower()}@email.com",
                phone=f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                segment=segment,
                location=random.choice(self.LOCATIONS),
                age_group=random.choice(["18-25", "26-35", "36-45", "46-55", "56+"]),
                interests=random.sample(self.INTERESTS, k=random.randint(2, 5)),
                purchase_history=purchase_history,
                total_spent=total_spent,
                last_purchase_date=last_purchase,
                email_opt_in=random.random() > 0.15,  # 85% opt-in
                sms_opt_in=random.random() > 0.40,   # 60% opt-in
                created_at=datetime.now().isoformat()
            )
            
            self.customers[customer_id] = customer
    
    def get_customer(self, customer_id: str) -> Optional[MockCustomer]:
        """Get customer by ID"""
        return self.customers.get(customer_id)
    
    def get_all_customers(self) -> List[MockCustomer]:
        """Get all customers"""
        return list(self.customers.values())
    
    def get_customers_by_segment(self, segment: str) -> List[MockCustomer]:
        """Get customers by segment"""
        return [c for c in self.customers.values() if c.segment == segment]
    
    def get_customers_with_email_opt_in(self) -> List[MockCustomer]:
        """Get customers who opted in to email"""
        return [c for c in self.customers.values() if c.email_opt_in]
    
    def get_customers_by_interests(self, interests: List[str]) -> List[MockCustomer]:
        """Get customers with specific interests"""
        return [
            c for c in self.customers.values()
            if any(interest in c.interests for interest in interests)
        ]
    
    def get_customers_by_location(self, location: str) -> List[MockCustomer]:
        """Get customers by location"""
        return [c for c in self.customers.values() if location.lower() in c.location.lower()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        total = len(self.customers)
        return {
            "total_customers": total,
            "by_segment": {
                "new": len(self.get_customers_by_segment("new")),
                "occasional": len(self.get_customers_by_segment("occasional")),
                "frequent": len(self.get_customers_by_segment("frequent")),
                "vip": len(self.get_customers_by_segment("vip"))
            },
            "email_opt_in": len(self.get_customers_with_email_opt_in()),
            "sms_opt_in": len([c for c in self.customers.values() if c.sms_opt_in]),
            "total_revenue": round(sum(c.total_spent for c in self.customers.values()), 2),
            "average_spent": round(
                sum(c.total_spent for c in self.customers.values()) / total if total > 0 else 0, 2
            )
        }
