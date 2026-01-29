"""
Utility functions for the Retail Marketing Agent
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import re


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format amount as currency
    
    Args:
        amount: Amount to format
        currency: Currency code (USD, EUR, etc.)
    
    Returns:
        Formatted currency string
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    symbol = symbols.get(currency, "$")
    return f"{symbol}{amount:,.2f}"


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values
    
    Args:
        old_value: Original value
        new_value: New value
    
    Returns:
        Percentage change
    """
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100


def parse_timeframe(timeframe: str) -> timedelta:
    """
    Parse timeframe string into timedelta
    
    Args:
        timeframe: Timeframe string (e.g., "30 days", "2 weeks", "3 months")
    
    Returns:
        timedelta object
    """
    timeframe = timeframe.lower().strip()
    
    # Extract number and unit
    match = re.match(r'(\d+)\s*(day|days|week|weeks|month|months|year|years)', timeframe)
    
    if not match:
        return timedelta(days=30)  # Default
    
    value = int(match.group(1))
    unit = match.group(2)
    
    if 'day' in unit:
        return timedelta(days=value)
    elif 'week' in unit:
        return timedelta(weeks=value)
    elif 'month' in unit:
        return timedelta(days=value * 30)  # Approximate
    elif 'year' in unit:
        return timedelta(days=value * 365)  # Approximate
    
    return timedelta(days=30)


def get_date_range(timeframe: str) -> tuple[datetime, datetime]:
    """
    Get start and end dates for a timeframe
    
    Args:
        timeframe: Timeframe string
    
    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = datetime.now()
    delta = parse_timeframe(timeframe)
    start_date = end_date + delta
    
    return (end_date, start_date)


def calculate_roi(revenue: float, cost: float) -> float:
    """
    Calculate Return on Investment (ROI)
    
    Args:
        revenue: Revenue generated
        cost: Cost invested
    
    Returns:
        ROI as percentage
    """
    if cost == 0:
        return 0.0
    return ((revenue - cost) / cost) * 100


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def generate_hashtags(text: str, max_count: int = 10) -> List[str]:
    """
    Generate hashtags from text
    
    Args:
        text: Text to generate hashtags from
        max_count: Maximum number of hashtags
    
    Returns:
        List of hashtags
    """
    # Remove special characters and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter out common words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
    
    # Create hashtags
    hashtags = [f"#{word.capitalize()}" for word in filtered_words[:max_count]]
    
    return hashtags


def format_date_range(start_date: datetime, end_date: datetime) -> str:
    """
    Format a date range as a string
    
    Args:
        start_date: Start date
        end_date: End date
    
    Returns:
        Formatted date range string
    """
    start_str = start_date.strftime("%B %d, %Y")
    end_str = end_date.strftime("%B %d, %Y")
    return f"{start_str} - {end_str}"


def calculate_days_until(target_date: datetime) -> int:
    """
    Calculate days until a target date
    
    Args:
        target_date: Target date
    
    Returns:
        Number of days until target date
    """
    delta = target_date - datetime.now()
    return delta.days


def create_summary_stats(data: List[float]) -> Dict[str, float]:
    """
    Create summary statistics for a list of numbers
    
    Args:
        data: List of numbers
    
    Returns:
        Dictionary of statistics
    """
    if not data:
        return {
            "count": 0,
            "min": 0,
            "max": 0,
            "mean": 0,
            "sum": 0
        }
    
    return {
        "count": len(data),
        "min": min(data),
        "max": max(data),
        "mean": sum(data) / len(data),
        "sum": sum(data)
    }
