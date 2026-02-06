# Project Chimera - Multi-stage Docker Build
# Day 3 Task 3.2: Enhanced for TDD and CloudOps
# "It works on my machine" is not acceptable in professional CloudOps

# Stage 1: Base image with uv
FROM python:3.11-slim as base

# Set build arguments
ARG DEBIAN_FRONTEND=noninteractive
ARG UV_VERSION=latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Verify uv installation
RUN uv --version

WORKDIR /app

# Set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Stage 2: Dependencies
FROM base as dependencies

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Install dependencies with uv
RUN uv pip install --system -e ".[dev]"

# Stage 3: Testing (for TDD - Day 3 Task 3.1)
FROM dependencies as testing

# Copy test files and source
COPY tests ./tests
COPY src ./src
COPY specs ./specs
COPY skills ./skills
COPY pyproject.toml ./
COPY conftest.py ./

# Create test output directories
RUN mkdir -p /app/test-results /app/coverage

# Set environment for testing
ENV PYTEST_ARGS="-v --tb=short --cov=src --cov-report=term-missing --cov-report=html:/app/coverage"

# Run tests by default
CMD ["pytest", "tests/", "-v", "--tb=short"]

# Stage 4: Development
FROM dependencies as development

# Copy source code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/.vscode

# Expose ports
EXPOSE 8000 5678

# Install development tools
RUN uv pip install --system debugpy ipython

# Default command (override in docker-compose)
CMD ["python", "-m", "src.main"]

# Stage 5: Production
FROM dependencies as production

# Copy only necessary files (minimize attack surface)
COPY src ./src
COPY specs ./specs
COPY skills ./skills

# Remove dev dependencies
RUN uv pip uninstall --system pytest pytest-cov pytest-asyncio pytest-mock black ruff mypy pre-commit

# Security: Create non-root user
RUN useradd -m -u 1000 chimera && \
    chown -R chimera:chimera /app

# Create runtime directories
RUN mkdir -p /app/logs /app/data && \
    chown -R chimera:chimera /app/logs /app/data

USER chimera

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Expose application port
EXPOSE 8000

# Production command
CMD ["python", "-m", "src.main"]

# Build metadata
LABEL maintainer="Chimera FDE Team <fde@chimera.dev>" \
      version="0.1.0" \
      description="Project Chimera - Autonomous AI Influencer Network" \
      org.opencontainers.image.source="https://github.com/chimera/project-chimera"
