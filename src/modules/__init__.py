"""
Marketing Modules Package
"""
from .customer_acquisition import CustomerAcquisitionModule
from .customer_retention import CustomerRetentionModule
from .digital_marketing import DigitalMarketingModule
from .instore_marketing import InStoreMarketingModule

__all__ = [
    "CustomerAcquisitionModule",
    "CustomerRetentionModule",
    "DigitalMarketingModule",
    "InStoreMarketingModule"
]
