"""
DataHub Custom Transformers

A collection of custom DataHub transformers for various metadata enhancement tasks.
"""

__version__ = "0.2.1"
__author__ = "Abdullah Tariq"

# Import all available transformers
from .domain_structured_properties import (
    SimpleAddDatasetDomainStructuredPropertiesConfig,
    SimpleAddDatasetDomainStructuredPropertiesTransformer,
)

# Registry of all available transformers
TRANSFORMERS = {
    "simple_add_dataset_domain_structured_properties": SimpleAddDatasetDomainStructuredPropertiesTransformer,
}

__all__ = [
    # Domain Structured Properties
    "SimpleAddDatasetDomainStructuredPropertiesTransformer",
    "SimpleAddDatasetDomainStructuredPropertiesConfig",
    # Registry
    "TRANSFORMERS",
]
