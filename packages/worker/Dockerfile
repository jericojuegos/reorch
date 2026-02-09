FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY main.py .
COPY config.py .
COPY queue_client.py .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Health check (worker is alive if process is running)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep -f "python main.py" || exit 1

# Run the worker
CMD ["python", "main.py"]
