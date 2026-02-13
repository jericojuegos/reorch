FROM python:3.11-slim

WORKDIR /app

# Install FFmpeg for audio format conversion
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY main.py .
COPY config.py .
COPY queue_client.py .
COPY database.py .
COPY s3_client.py .
COPY pipeline/ pipeline/

# Install Python dependencies
RUN pip install --no-cache-dir ".[dev]"

# Health check (worker is alive if process is running)
COPY tests/ tests/
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep -f "python main.py" || exit 1

# Run the worker
CMD ["python", "main.py"]
