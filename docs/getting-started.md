# Getting Started

Get Vindicta Core running in your project.

## Prerequisites

- Python 3.10+
- uv (recommended) or pip

## Installation

```bash
uv pip install git+https://github.com/vindicta-platform/Vindicta-Core.git
```

## Basic Usage

### Settings

```python
from vindicta_core import PlatformSettings

# Loads from environment variables
settings = PlatformSettings()

# Access configuration
print(settings.database_url)
print(settings.log_level)
```

### Base Models

```python
from vindicta_core.models import BaseEntity

class MyUnit(BaseEntity):
    name: str
    points: int
```

## Development Setup

```bash
git clone https://github.com/vindicta-platform/Vindicta-Core.git
cd Vindicta-Core
uv venv
uv pip install -e ".[dev]"
pytest tests/ -v
```
