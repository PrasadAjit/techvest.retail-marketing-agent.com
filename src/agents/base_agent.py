"""
Base Agent class for all marketing agents
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class GoalType(Enum):
    """Types of marketing goals"""
    CUSTOMER_ACQUISITION = "customer_acquisition"
    CUSTOMER_RETENTION = "customer_retention"
    INSTORE_MARKETING = "instore_marketing"
    DIGITAL_PRESENCE = "digital_presence"
    SEASONAL_CAMPAIGN = "seasonal_campaign"
    ANALYTICS_INSIGHTS = "analytics_insights"
    COMMUNITY_ENGAGEMENT = "community_engagement"


class GoalStatus(Enum):
    """Goal execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Goal:
    """Represents a marketing goal"""
    
    def __init__(
        self,
        goal_type: GoalType,
        description: str,
        target: str,
        timeframe: str,
        metrics: Optional[Dict[str, Any]] = None,
        priority: int = 1
    ):
        self.id = self._generate_id()
        self.goal_type = goal_type
        self.description = description
        self.target = target
        self.timeframe = timeframe
        self.metrics = metrics or {}
        self.priority = priority
        self.status = GoalStatus.PENDING
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.results: Dict[str, Any] = {}
        self.subtasks: List[Dict[str, Any]] = []
    
    def _generate_id(self) -> str:
        """Generate unique goal ID"""
        return f"goal_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def add_subtask(self, task: Dict[str, Any]):
        """Add a subtask to the goal"""
        self.subtasks.append(task)
    
    def update_status(self, status: GoalStatus):
        """Update goal status"""
        self.status = status
        if status == GoalStatus.IN_PROGRESS and not self.started_at:
            self.started_at = datetime.now()
        elif status == GoalStatus.COMPLETED:
            self.completed_at = datetime.now()
    
    def add_result(self, key: str, value: Any):
        """Add a result to the goal"""
        self.results[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert goal to dictionary"""
        return {
            "id": self.id,
            "goal_type": self.goal_type.value,
            "description": self.description,
            "target": self.target,
            "timeframe": self.timeframe,
            "metrics": self.metrics,
            "priority": self.priority,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "results": self.results,
            "subtasks": self.subtasks
        }


class BaseAgent(ABC):
    """Base class for all marketing agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.goals: List[Goal] = []
        self.memory: Dict[str, Any] = {}
    
    @abstractmethod
    def plan(self, goal: Goal) -> List[Dict[str, Any]]:
        """
        Create an execution plan for the given goal
        Returns a list of subtasks
        """
        pass
    
    @abstractmethod
    def execute(self, goal: Goal) -> Dict[str, Any]:
        """
        Execute the goal and return results
        """
        pass
    
    @abstractmethod
    def evaluate(self, goal: Goal, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the results of goal execution
        """
        pass
    
    def add_goal(self, goal: Goal):
        """Add a goal to the agent"""
        self.goals.append(goal)
    
    def get_active_goals(self) -> List[Goal]:
        """Get all active goals"""
        return [g for g in self.goals if g.status in [GoalStatus.PENDING, GoalStatus.IN_PROGRESS]]
    
    def get_completed_goals(self) -> List[Goal]:
        """Get all completed goals"""
        return [g for g in self.goals if g.status == GoalStatus.COMPLETED]
    
    def store_memory(self, key: str, value: Any):
        """Store information in agent memory"""
        self.memory[key] = value
    
    def retrieve_memory(self, key: str) -> Optional[Any]:
        """Retrieve information from agent memory"""
        return self.memory.get(key)
