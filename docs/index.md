# Vindicta Core

**The foundation layer for the Vindicta ecosystem.**

Vindicta Core provides shared primitives, configuration management, and interface contracts used across all Vindicta Platform modules.

---

## Why Vindicta Core?

Building a modular platform requires a stable foundation. Vindicta Core is that foundation:

- **Zero Dependencies on Other Modules** — Core depends on nothing else
- **Stable Interfaces** — Breaking changes require major version bumps
- **Minimal Surface Area** — Only essential utilities exposed

## Installation

```bash
uv pip install git+https://github.com/vindicta-platform/Vindicta-Core.git
```

## Quick Example

```python
from vindicta_core import PlatformSettings

settings = PlatformSettings()
print(f"Environment: {settings.environment}")
print(f"Debug Mode: {settings.debug}")
```

## What's Included

| Module | Purpose |
|--------|---------|
| `config` | Pydantic-based settings management |
| `models` | Shared data models and schemas |
| `interfaces` | Abstract contracts for cross-module communication |
| `state` | Platform-wide state primitives |

---

## Part of the Vindicta Platform

Vindicta Core is one module in the larger [Vindicta Platform](https://vindicta-platform.github.io/mkdocs/). Use it standalone, or as part of the full ecosystem.
