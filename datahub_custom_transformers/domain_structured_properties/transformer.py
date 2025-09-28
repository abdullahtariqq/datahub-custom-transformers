"""
Simple DataHub transformer for adding domain-type structured properties to ALL datasets.

Adds the same structured properties to every dataset ingested by the recipe.
Useful for organizational data classification (environment, team, department, etc.).

Prerequisites:
- Structured properties must be pre-defined in DataHub with type "domain"
- Domain entities must exist in DataHub
"""

import logging
from typing import Any, cast

from datahub.configuration.common import TransformerSemanticsConfigModel
from datahub.emitter.mce_builder import Aspect
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.transformer.dataset_transformer import DatasetTransformer
from datahub.metadata.schema_classes import (
    StructuredPropertiesClass,
    StructuredPropertyValueAssignmentClass,
)
from datahub.utilities.urns._urn_base import Urn
from datahub.utilities.urns.domain_urn import DomainUrn
from pydantic import Field

log = logging.getLogger(__name__)


class SimpleAddDatasetDomainStructuredPropertiesConfig(TransformerSemanticsConfigModel):
    """Configuration for adding domain structured properties to all datasets"""

    properties: dict[str, str] = Field(
        description="Map of structured property names to domain qualified names"
    )


class SimpleAddDatasetDomainStructuredPropertiesTransformer(DatasetTransformer):
    """
    Adds domain-type structured properties to ALL datasets in the ingestion.

    Example configuration:
    ```yaml
    transformers:
      - type: "simple_add_dataset_domain_structured_properties"
        config:
          properties:
            environment: "production_environment"
            team: "data_engineering_team"
    ```
    """

    def __init__(
        self,
        config: SimpleAddDatasetDomainStructuredPropertiesConfig,
        ctx: PipelineContext,
    ):
        super().__init__()  # type: ignore
        self.config = config
        self.ctx = ctx

    @classmethod
    def create(
        cls, config_dict: dict[str, Any], ctx: PipelineContext
    ) -> "SimpleAddDatasetDomainStructuredPropertiesTransformer":
        config = SimpleAddDatasetDomainStructuredPropertiesConfig.parse_obj(config_dict)
        return cls(config, ctx)

    def aspect_name(self) -> str:
        return "structuredProperties"

    def transform_aspect(
        self, entity_urn: str, aspect_name: str, aspect: Aspect | None
    ) -> Aspect | None:
        _ = aspect_name  # Mark as used to avoid linter warning

        # Get existing structured properties or create new
        structured_props: StructuredPropertiesClass
        if aspect is not None and isinstance(aspect, StructuredPropertiesClass):
            structured_props = aspect
        else:
            structured_props = StructuredPropertiesClass(properties=[])

        properties_dict = {
            prop.propertyUrn: prop for prop in structured_props.properties
        }

        # Add each configured property
        for prop_name, domain_qualified_name in self.config.properties.items():
            prop_urn = Urn.make_structured_property_urn(prop_name)
            domain_urn = str(DomainUrn(domain_qualified_name))

            properties_dict[prop_urn] = StructuredPropertyValueAssignmentClass(
                propertyUrn=prop_urn, values=[domain_urn]
            )
            log.info(f"Added {prop_name}='{domain_qualified_name}' to {entity_urn}")

        structured_props.properties = list(properties_dict.values())
        return cast(Aspect, structured_props)
