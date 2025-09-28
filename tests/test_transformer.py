"""
Unit tests for the SimpleAddDatasetDomainStructuredPropertiesTransformer
"""

from unittest.mock import Mock, patch

import pytest
from datahub.ingestion.api.common import PipelineContext
from datahub.metadata.schema_classes import (
    StructuredPropertiesClass,
    StructuredPropertyValueAssignmentClass,
)

from datahub_custom_transformers.domain_structured_properties.transformer import (
    SimpleAddDatasetDomainStructuredPropertiesConfig,
    SimpleAddDatasetDomainStructuredPropertiesTransformer,
)


class TestSimpleAddDatasetDomainStructuredPropertiesTransformer:
    """Test suite for the simple domain structured properties transformer"""

    @pytest.fixture
    def mock_ctx(self) -> Mock:
        """Mock PipelineContext for testing"""
        return Mock(spec=PipelineContext)

    @pytest.fixture
    def basic_config(self) -> SimpleAddDatasetDomainStructuredPropertiesConfig:
        """Basic configuration for testing"""
        return SimpleAddDatasetDomainStructuredPropertiesConfig(
            properties={
                "environment": "test_environment",
                "team": "test_team"
            }
        )

    @pytest.fixture
    def transformer(
        self,
        basic_config: SimpleAddDatasetDomainStructuredPropertiesConfig,
        mock_ctx: Mock,
    ) -> SimpleAddDatasetDomainStructuredPropertiesTransformer:
        """Basic transformer instance for testing"""
        return SimpleAddDatasetDomainStructuredPropertiesTransformer(basic_config, mock_ctx)

    def test_transformer_creation(self, mock_ctx: Mock) -> None:
        """Test transformer can be created with valid configuration"""
        config = SimpleAddDatasetDomainStructuredPropertiesConfig(
            properties={"environment": "test_environment"}
        )
        transformer = SimpleAddDatasetDomainStructuredPropertiesTransformer(config, mock_ctx)

        assert transformer.config == config
        assert transformer.ctx == mock_ctx
        assert transformer.aspect_name() == "structuredProperties"

    def test_create_factory_method(self, mock_ctx: Mock) -> None:
        """Test the create factory method works correctly"""
        config_dict = {
            "properties": {
                "environment": "test_environment",
                "team": "test_team"
            }
        }

        transformer = SimpleAddDatasetDomainStructuredPropertiesTransformer.create(config_dict, mock_ctx)

        assert isinstance(transformer, SimpleAddDatasetDomainStructuredPropertiesTransformer)
        assert transformer.config.properties == config_dict["properties"]

    def test_property_assignment(
        self, transformer: SimpleAddDatasetDomainStructuredPropertiesTransformer
    ) -> None:
        """Test properties are added to datasets"""
        entity_urn = "urn:li:dataset:(urn:li:dataPlatform:postgres,db.schema.table,PROD)"

        # Mock the URN utility functions
        with (
            patch(
                'datahub_custom_transformers.domain_structured_properties.'
                'transformer.Urn.make_structured_property_urn'
            ) as mock_sp_urn,
            patch(
                'datahub_custom_transformers.domain_structured_properties.'
                'transformer.DomainUrn'
            ) as mock_domain_urn,
        ):

            mock_sp_urn.side_effect = lambda x: f"urn:li:structuredProperty:{x}"
            mock_domain_urn.side_effect = lambda x: f"urn:li:domain:{x}"

            result = transformer.transform_aspect(entity_urn, "structuredProperties", None)

            assert isinstance(result, StructuredPropertiesClass)
            assert len(result.properties) == 2

            # Check assignments by URN
            prop_urns = {prop.propertyUrn: prop for prop in result.properties}

            environment_prop_urn = "urn:li:structuredProperty:environment"
            assert environment_prop_urn in prop_urns
            environment_assignment = prop_urns[environment_prop_urn]
            assert isinstance(environment_assignment, StructuredPropertyValueAssignmentClass)
            assert environment_assignment.values == ["urn:li:domain:test_environment"]

            team_prop_urn = "urn:li:structuredProperty:team"
            assert team_prop_urn in prop_urns
            team_assignment = prop_urns[team_prop_urn]
            assert team_assignment.values == ["urn:li:domain:test_team"]

    def test_existing_properties_preserved(
        self, transformer: SimpleAddDatasetDomainStructuredPropertiesTransformer
    ) -> None:
        """Test that existing structured properties are preserved"""
        entity_urn = "urn:li:dataset:(urn:li:dataPlatform:postgres,db.schema.table,PROD)"

        # Create existing structured properties
        existing_props = StructuredPropertiesClass(properties=[
            StructuredPropertyValueAssignmentClass(
                propertyUrn="urn:li:structuredProperty:existing_prop",
                values=["existing_value"]
            )
        ])

        with (
            patch(
                'datahub_custom_transformers.domain_structured_properties.'
                'transformer.Urn.make_structured_property_urn'
            ) as mock_sp_urn,
            patch(
                'datahub_custom_transformers.domain_structured_properties.'
                'transformer.DomainUrn'
            ) as mock_domain_urn,
        ):

            mock_sp_urn.side_effect = lambda x: f"urn:li:structuredProperty:{x}"
            mock_domain_urn.side_effect = lambda x: f"urn:li:domain:{x}"

            result = transformer.transform_aspect(entity_urn, "structuredProperties", existing_props)

            # Should preserve existing property and add new ones
            assert result is not None
            assert isinstance(result, StructuredPropertiesClass)
            prop_urns = {prop.propertyUrn: prop for prop in result.properties}
            assert "urn:li:structuredProperty:existing_prop" in prop_urns
            assert "urn:li:structuredProperty:environment" in prop_urns
            assert "urn:li:structuredProperty:team" in prop_urns
            assert len(result.properties) == 3

    def test_empty_configuration(self, mock_ctx: Mock) -> None:
        """Test transformer with empty properties"""
        config = SimpleAddDatasetDomainStructuredPropertiesConfig(properties={})
        transformer = SimpleAddDatasetDomainStructuredPropertiesTransformer(config, mock_ctx)

        entity_urn = "urn:li:dataset:(urn:li:dataPlatform:postgres,db.schema.table,PROD)"
        result = transformer.transform_aspect(entity_urn, "structuredProperties", None)

        # Should return structured properties object but with no properties
        assert isinstance(result, StructuredPropertiesClass)
        assert len(result.properties) == 0

    def test_single_property(self, mock_ctx: Mock) -> None:
        """Test transformer with single property"""
        config = SimpleAddDatasetDomainStructuredPropertiesConfig(
            properties={"environment": "single_environment"}
        )
        transformer = SimpleAddDatasetDomainStructuredPropertiesTransformer(config, mock_ctx)

        entity_urn = "urn:li:dataset:(urn:li:dataPlatform:postgres,db.schema.table,PROD)"

        with (
            patch(
                'datahub_custom_transformers.domain_structured_properties.'
                'transformer.Urn.make_structured_property_urn'
            ) as mock_sp_urn,
            patch(
                'datahub_custom_transformers.domain_structured_properties.'
                'transformer.DomainUrn'
            ) as mock_domain_urn,
        ):

            mock_sp_urn.side_effect = lambda x: f"urn:li:structuredProperty:{x}"
            mock_domain_urn.side_effect = lambda x: f"urn:li:domain:{x}"

            result = transformer.transform_aspect(entity_urn, "structuredProperties", None)

            assert result is not None
            assert len(result.properties) == 1
            prop_urns = {prop.propertyUrn: prop for prop in result.properties}
            environment_prop_urn = "urn:li:structuredProperty:environment"
            assert environment_prop_urn in prop_urns
            assert prop_urns[environment_prop_urn].values == ["urn:li:domain:single_environment"]


if __name__ == "__main__":
    pytest.main([__file__])
