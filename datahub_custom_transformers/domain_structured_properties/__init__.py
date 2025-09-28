"""
Domain Structured Properties Transformer

Adds domain-type structured properties to all datasets in an ingestion.
"""

from .transformer import (
    SimpleAddDatasetDomainStructuredPropertiesConfig,
    SimpleAddDatasetDomainStructuredPropertiesTransformer,
)

__all__ = [
    "SimpleAddDatasetDomainStructuredPropertiesTransformer",
    "SimpleAddDatasetDomainStructuredPropertiesConfig",
]
