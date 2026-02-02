# API Reference

## vindicta_core.config

### PlatformSettings

Pydantic-based settings with environment variable support.

```python
class PlatformSettings(BaseSettings):
    environment: str = "development"
    debug: bool = False
    database_url: str = "sqlite:///vindicta.db"
    log_level: str = "INFO"
```

## vindicta_core.models

### BaseEntity

Base class for all domain entities.

```python
class BaseEntity(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
```

## vindicta_core.interfaces

### IRepository

Abstract base for data access.

```python
class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def get(self, id: UUID) -> T | None: ...
    
    @abstractmethod
    async def save(self, entity: T) -> T: ...
```
