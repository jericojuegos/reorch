# REORCH Worker

Audio processing worker that polls Redis for jobs.

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
# Run worker
python main.py

# Run tests
pytest
```

## Architecture

The worker uses a simple polling loop:
1. Poll Redis queue for jobs (BLPOP with timeout)
2. Process job (audio transformation)
3. Update job status in database
4. Repeat

## Job Format

```json
{
  "id": "uuid",
  "type": "reorchestrate",
  "input_url": "s3://bucket/input.wav",
  "preset": "ballad-to-rock",
  "created_at": "2024-01-01T00:00:00Z"
}
```
