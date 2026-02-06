# Contributing

## Development Setup

```bash
git clone https://github.com/vindicta-platform/Vindicta-Core.git
cd Vindicta-Core
uv venv
uv pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/ -v
```

## Code Style

- Ruff for linting and formatting
- Type hints required
- 80% test coverage minimum

## Pull Requests

1. Fork the repository
2. Create a feature branch
3. Write tests first
4. Submit PR with clear description

## 🔗 Pre-Commit Hooks (Required)

All developers **must** install and run pre-commit hooks before committing. This ensures:
- All markdown links are validated
- Code quality standards are enforced

### Setup

```bash
uv pip install pre-commit
pre-commit install
```

## License

MIT License
