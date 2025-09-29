# DataHub Custom Transformers

[![PyPI version](https://badge.fury.io/py/datahub-custom-transformers.svg)](https://badge.fury.io/py/datahub-custom-transformers)
[![Python Support](https://img.shields.io/pypi/pyversions/datahub-custom-transformers.svg)](https://pypi.org/project/datahub-custom-transformers/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A collection of custom DataHub transformers for various metadata enhancement tasks.

## Features

- 🏗️ **Modular Design**: Easy to add new transformers
- 🔧 **Production Ready**: Tested and documented transformers
- 🔌 **Auto-Discovery**: Transformers are automatically registered with DataHub

## Installation

```bash
uv add datahub-custom-transformers
```

## Available Transformers

### Domain Structured Properties Transformer

Adds domain-type structured properties to all datasets in an ingestion.

**Use Case**: Organizational data classification where all datasets from a source belong to the same environment, team, or department.

```yaml
transformers:
  - type: "simple_add_dataset_domain_structured_properties"
    config:
      properties:
        environment: "production_environment"
        team: "data_engineering_team"
        department: "engineering_department"
```

## Quick Start

### 1. Prerequisites

Create structured properties in DataHub:

```yaml
# structured_properties.yaml
- id: department
  type: urn
  description: "Data environment assignment"
  display_name: "Environment"
  entity_types: [dataset]
  cardinality: SINGLE
  type_qualifier:
    allowed_types: ["urn:li:entityType:datahub.domain"]
```

Create domain entities:
- `production_environment`
- `data_engineering_team`

### 2. Use in Ingestion Recipe

```yaml
source:
  type: postgres
  config:
    host_port: "localhost:5432"
    database: "analytics_db"

transformers:
  - type: "simple_add_dataset_domain_structured_properties"
    config:
      properties:
        environment: "production_environment"
        team: "data_engineering_team"

sink:
  type: datahub-rest
  config:
    server: "http://localhost:8080"
```

### 3. Run Ingestion

```bash
datahub ingest -c config.yaml
```

## Result

All datasets will have structured properties:

```json
{
  "structuredProperties": {
    "properties": [
      {
        "propertyUrn": "urn:li:structuredProperty:environment",
        "values": ["urn:li:domain:production_environment"]
      },
      {
        "propertyUrn": "urn:li:structuredProperty:team",
        "values": ["urn:li:domain:data_engineering_team"]
      }
    ]
  }
}
```

## Supported DataHub Sources

Works with all DataHub sources:
- BigQuery, Snowflake, PostgreSQL, MySQL, Redshift
- dbt, Airflow, Kafka, S3
- And many more...

## Requirements

- Python 3.11+
- acryl-datahub >= 0.12.0

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your transformer with tests
4. Submit a pull request

## Support

- 📖 [Documentation](https://github.com/your-org/datahub-custom-transformers#readme)
- 🐛 [Issues](https://github.com/your-org/datahub-custom-transformers/issues)
- 💬 [Discussions](https://github.com/your-org/datahub-custom-transformers/discussions)

## License

MIT License - see [LICENSE](LICENSE) file.