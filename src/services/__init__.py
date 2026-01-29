"""
Services for deployment simulation
"""
from .mock_customers import MockCustomerDatabase
from .mock_email import MockEmailService
from .mock_social import MockSocialMediaService
from .deployment_service import DeploymentService

__all__ = [
    "MockCustomerDatabase",
    "MockEmailService",
    "MockSocialMediaService",
    "DeploymentService"
]
