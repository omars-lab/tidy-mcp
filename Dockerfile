FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Copy all necessary files for package installation
COPY pyproject.toml .
COPY requirements.txt .
COPY LICENSE .
# Copy source code (needed for editable install)
COPY src/ ./src/

# Install dependencies first, then install package
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the HTTP server
CMD ["python", "-m", "uvicorn", "tidy_mcp.http_server:app", "--host", "0.0.0.0", "--port", "8000"]

