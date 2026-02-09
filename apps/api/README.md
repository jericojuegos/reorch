# REORCH API

FastAPI backend for the REORCH music re-orchestration platform.

## Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Unix)
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

## Development

```bash
# Run dev server
uvicorn main:app --reload --port 8000

# Run tests
pytest

# Lint
ruff check .
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Swagger UI documentation
