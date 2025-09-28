# DataHub Custom Transformers

A collection of custom DataHub transformers for various metadata enhancement tasks.

## Installation

```bash
uv add datahub-custom-transformers
```

## Available Transformers

### 1. Domain Structured Properties Transformer

Adds domain-type structured properties to **all** datasets ingested by a recipe.

**Usage:**
```yaml
transformers:
  - type: "simple_add_dataset_domain_structured_properties"
    config:
      properties:
        environment: "production_environment"
        team: "data_engineering_team"
```

**Prerequisites:**
- Create structured properties in DataHub with type "urn" and domain type qualifiers
- Create domain entities in DataHub

## Quick Start

### 1. Install Package

```bash
uv add datahub-custom-transformers
```

### 2. Use in Recipe

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

## Adding New Transformers

This package is designed to be extensible. To add new transformers:

1. Create a new directory under `datahub_custom_transformers/`
2. Implement your transformer following DataHub patterns
3. Add entry point in `pyproject.toml`
4. Update the main `__init__.py` to include your transformer

Example structure:
```
datahub_custom_transformers/
├── __init__.py                    # Main package
├── domain_structured_properties/  # Domain transformer
│   ├── __init__.py
│   └── transformer.py
└── your_new_transformer/         # Your new transformer
    ├── __init__.py
    └── transformer.py
```

## Development

```bash
# Install in development mode
uv sync --dev

# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Run type checking
uv run mypy datahub_custom_transformers

# Build and publish
uv build
uv publish
```

## License

MIT License - see [LICENSE](LICENSE) file.