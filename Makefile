.PHONY: help setup install test test-unit test-integration format lint type-check spec-check clean dev docker-build docker-up docker-down

# Default target
help:
	@echo "Project Chimera - Makefile Commands"
	@echo "===================================="
	@echo "setup           - Install uv and initialize environment"
	@echo "install         - Install project dependencies"
	@echo "test            - Run all tests"
	@echo "test-unit       - Run unit tests only"
	@echo "test-integration - Run integration tests only"
	@echo "format          - Format code with black"
	@echo "lint            - Lint code with ruff"
	@echo "type-check      - Type check with mypy"
	@echo "spec-check      - Validate code against specifications"
	@echo "clean           - Remove build artifacts and caches"
	@echo "dev             - Start development environment"
	@echo "docker-build    - Build Docker images"
	@echo "docker-up       - Start Docker services"
	@echo "docker-down     - Stop Docker services"

# Setup: Install uv
setup:
	@echo "Installing uv..."
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo "uv installed successfully"
	@make install

# Install dependencies
install:
	@echo "Installing dependencies with uv..."
	uv pip install -e ".[dev]"
	@echo "Dependencies installed"

# Run all tests
test:
	@echo "Running all tests..."
	pytest tests/ -v
	@echo "Tests complete"

# Run unit tests only
test-unit:
	@echo "Running unit tests..."
	pytest tests/ -v -m unit
	@echo "Unit tests complete"

# Run integration tests
test-integration:
	@echo "Running integration tests..."
	pytest tests/ -v -m integration
	@echo "Integration tests complete"

# Format code
format:
	@echo "Formatting code with black..."
	black src/ tests/ skills/
	@echo "Code formatted"

# Lint code
lint:
	@echo "Linting with ruff..."
	ruff check src/ tests/ skills/
	@echo "Linting complete"

# Type check
type-check:
	@echo "Type checking with mypy..."
	mypy src/
	@echo "Type checking complete"

# Spec validation (placeholder - to be implemented)
spec-check:
	@echo "Validating code against specifications..."
	@echo "⚠️  Spec validation not yet implemented"
	@echo "TODO: Check API contracts, database schemas, MCP tool definitions"
	@echo "Spec check complete (manual verification required)"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	rm -rf dist/ build/
	@echo "Clean complete"

# Development environment
dev:
	@echo "Starting development environment..."
	@echo "⚠️  Development server not yet implemented"
	@echo "TODO: uvicorn src.api.main:app --reload"

# Docker commands
docker-build:
	@echo "Building Docker images..."
	docker build -t chimera:latest .
	@echo "Docker build complete"

docker-up:
	@echo "Starting Docker services..."
	docker-compose up -d
	@echo "Services started"

docker-down:
	@echo "Stopping Docker services..."
	docker-compose down
	@echo "Services stopped"

# Git helpers
commit:
	@echo "Checking code before commit..."
	@make format
	@make lint
	@make type-check
	@make test
	@echo "✅ All checks passed - ready to commit"

# Pre-commit hook setup
pre-commit:
	@echo "Setting up pre-commit hooks..."
	pre-commit install
	@echo "Pre-commit hooks installed"
