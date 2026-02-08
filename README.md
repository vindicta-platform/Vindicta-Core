# Vindicta-Core

Shared primitives, settings, and interface contracts for the Vindicta Platform.

## Overview

Vindicta-Core provides the foundational building blocks shared across all Vindicta Platform modules, including configuration management, base models, and platform-wide interfaces.

## Features

- **Configuration Management**: Pydantic-based settings with environment variable support
- **Base Models**: Shared data models and schemas
- **Interface Contracts**: Abstract base classes for cross-module communication
- **State Management**: Platform-wide state primitives

## Installation

Install from source using uv:

```bash
uv pip install git+https://github.com/vindicta-platform/Vindicta-Core.git
```

Or clone and install locally:

```bash
git clone https://github.com/vindicta-platform/Vindicta-Core.git
cd Vindicta-Core
uv pip install -e .
```

## Usage

```python
from vindicta_core import PlatformSettings, BaseModel

settings = PlatformSettings()
print(f"Environment: {settings.environment}")
```

## Module Structure

```
vindicta_core/
├── config/      # Configuration and settings
├── models/      # Base data models
├── interfaces/  # Abstract contracts
└── state/       # State management
```

## Related Repositories

| Repository | Relationship |
|------------|-------------|
| [platform-core](https://github.com/vindicta-platform/platform-core) | Integration layer |
| [Vindicta-API](https://github.com/vindicta-platform/Vindicta-API) | Depends on Core |
| [Vindicta-CLI](https://github.com/vindicta-platform/Vindicta-CLI) | Depends on Core |

## Platform Documentation

> **📌 Important:** All cross-cutting decisions, feature proposals, and platform-wide architecture documentation live in [**Platform-Docs**](https://github.com/vindicta-platform/Platform-Docs).
>
> Any decision affecting multiple repos **must** be recorded there before implementation.

- 📋 [Feature Proposals](https://github.com/vindicta-platform/Platform-Docs/tree/main/docs/proposals)
- 🏗️ [Architecture Decisions](https://github.com/vindicta-platform/Platform-Docs/tree/main/docs)
- 📖 [Contributing Guide](https://github.com/vindicta-platform/Platform-Docs/blob/main/CONTRIBUTING.md)

## License

MIT License - See [LICENSE](./LICENSE) for details.
