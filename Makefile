# Makefile for TheThinkle.ai Newsletter System
# Provides convenient commands for development, testing, and maintenance

.PHONY: help test test-unit test-integration test-config test-coverage test-verbose clean lint format install dev-install

# Default target
help:
	@echo "Available commands:"
	@echo "  test              - Run all tests"
	@echo "  test-unit         - Run unit tests only"
	@echo "  test-integration  - Run integration tests only"
	@echo "  test-config       - Run config-related tests only"
	@echo "  test-coverage     - Run tests with coverage report"
	@echo "  test-verbose      - Run tests with verbose output"
	@echo "  test-fast         - Run tests excluding slow ones"
	@echo "  lint              - Run linting (flake8)"
	@echo "  format            - Format code (black)"
	@echo "  format-check      - Check code formatting without changes"
	@echo "  install           - Install production dependencies"
	@echo "  dev-install       - Install development dependencies"
	@echo "  clean             - Clean up generated files"
	@echo "  clean-cache       - Clean Python cache files"
	@echo "  clean-coverage    - Clean coverage reports"
	@echo "  studio            - Launch LangGraph Studio (langgraph dev)"

# Testing commands
test:
	pytest

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-config:
	pytest -m config -v

test-coverage:
	pytest --cov=. --cov-report=html --cov-report=term-missing

test-verbose:
	pytest -v -s

test-fast:
	pytest -m "not slow" -v

test-watch:
	pytest-watch --clear

# Code quality commands
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

format:
	black .

format-check:
	black --check --diff .

# Installation commands
install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install pytest-cov pytest-watch pytest-xdist

# Cleanup commands
clean: clean-cache clean-coverage
	@echo "Cleaned up generated files"

clean-cache:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

clean-coverage:
	rm -rf htmlcov/
	rm -f .coverage
	rm -f coverage.xml

# Development commands
run-example:
	python config/config_parser.py

validate-config:
	python -c "from config import load_config; config = load_config(); print('✅ Configuration is valid!')"

# CI/CD commands (for future use)
ci-test:
	pytest --cov=. --cov-report=xml --junitxml=test-results.xml

# Docker commands (for future use)
docker-test:
	docker run --rm -v $(PWD):/app -w /app python:3.11 make test

# Performance testing
test-performance:
	pytest tests/ -k "performance" -v

# Security testing (for future use)
security-check:
	bandit -r . -f json -o security-report.json || true

# Documentation generation (for future use)
docs:
	@echo "Documentation generation not yet implemented"

# Database commands (for future use if needed)
db-test:
	@echo "Database testing not yet implemented"

# Environment setup
setup-dev: dev-install
	@echo "Development environment setup complete"
	@echo "Run 'make test' to verify everything works"

# Quick development cycle
dev: format lint test-fast
	@echo "Development cycle complete"

# Full validation (for CI)
validate: format-check lint test-coverage
	@echo "Full validation complete"

# LangGraph Studio
studio:
	langgraph dev | cat
