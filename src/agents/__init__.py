"""
Agents package initialization
"""
from .base_agent import BaseAgent, Goal, GoalType, GoalStatus
from .retail_marketing_agent import RetailMarketingAgent

__all__ = [
    "BaseAgent",
    "Goal",
    "GoalType",
    "GoalStatus",
    "RetailMarketingAgent"
]
