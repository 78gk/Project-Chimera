# Project Chimera - Multi-stage Docker Build
# Stage 1: Base image with uv
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

WORKDIR /app

# Stage 2: Dependencies
FROM base as dependencies

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Install dependencies with uv
RUN uv pip install --system -e ".[dev]"

# Stage 3: Development
FROM dependencies as development

# Copy source code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data

# Expose ports
EXPOSE 8000

# Default command (override in docker-compose)
CMD ["python", "-m", "src.main"]

# Stage 4: Production
FROM dependencies as production

# Copy only necessary files
COPY src ./src
COPY specs ./specs
COPY skills ./skills

# Remove dev dependencies
RUN uv pip uninstall --system pytest pytest-cov pytest-asyncio black ruff mypy

# Security: Create non-root user
RUN useradd -m -u 1000 chimera && \
    chown -R chimera:chimera /app

USER chimera

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "src.main"]
