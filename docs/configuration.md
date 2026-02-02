# Configuration

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VINDICTA_ENV` | `development` | Environment name |
| `VINDICTA_DEBUG` | `false` | Enable debug mode |
| `DATABASE_URL` | `sqlite:///vindicta.db` | Database connection |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

## .env File

Create a `.env` file in your project root:

```bash
VINDICTA_ENV=production
VINDICTA_DEBUG=false
DATABASE_URL=postgresql://user:pass@localhost/vindicta
LOG_LEVEL=WARNING
```

## Programmatic Override

```python
from vindicta_core import PlatformSettings

settings = PlatformSettings(
    environment="testing",
    debug=True
)
```
