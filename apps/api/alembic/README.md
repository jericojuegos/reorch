# Database Migrations with Alembic

This directory contains Alembic migrations for the REORCH API database schema.

## Running Migrations

### Via Docker (Recommended)

```bash
# Start the database
cd docker
docker-compose up -d postgres

# Run migrations inside the API container
docker-compose run --rm api alembic upgrade head
```

### Locally (if Python is installed)

```bash
cd apps/api

# Upgrade to latest
alembic upgrade head

# Downgrade one revision
alembic downgrade -1

# View migration history
alembic history

# View current revision
alembic current
```

## Creating New Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration
alembic revision -m "Description of changes"
```

## Initial Setup

The initial migration (`001_initial_schema.py`) creates:
- `projects` table
- `tracks` table  
- `jobs` table
- `jobstatus` enum type

## Important Notes

- **Never** use `Base.metadata.create_all()` - Alembic manages the schema
- Always run migrations before starting the API
- Migrations run automatically in CI/CD pipelines
- Use `alembic upgrade head` in production deployments
