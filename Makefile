# Makefile for GATK Test Pipeline - Local Quality Verification
# Run this before pushing to avoid GitHub Actions failures

.PHONY: help install test lint format check-format quality-check clean build jupyter notebooks-execute ci-check

# Default target
help:
	@echo "🛠️  GATK Test Pipeline - Local Quality Verification"
	@echo "=================================================="
	@echo "Core targets:"
	@echo "  install            - Install dependencies with uv"
	@echo "  test               - Run all tests"
	@echo "  lint               - Run linting with ruff"
	@echo "  format             - Format code with ruff"
	@echo "  check-format       - Check code formatting (CI mode)"
	@echo "  quality-check      - Run all quality checks (lint + format + test)"
	@echo "  clean              - Clean build artifacts"
	@echo "  build              - Build the package"
	@echo ""
	@echo "Notebook targets:"
	@echo "  notebooks-execute  - Convert and execute all .py notebooks to .ipynb with outputs"
	@echo "  jupyter            - Start Jupyter Lab"
	@echo ""
	@echo "CI/Testing:"
	@echo "  ci-check           - Run exactly what GitHub Actions will run"
	@echo ""
	@echo "🚀 Quick workflow:"
	@echo "  make install && make quality-check"
	@echo ""
	@echo "📓 Notebook workflow:"
	@echo "  make notebooks-execute && make jupyter"
	@echo "  # Then open notebooks/executed_ipynb/ in Jupyter"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	uv sync --group dev
	@echo "✅ Dependencies installed"

# Run all tests
test:
	@echo "🧪 Running tests..."
	uv run python -m pytest tests/ -v --tb=short
	@echo "✅ All tests passed"

# Run linting
lint:
	@echo "🔍 Running linting..."
	uv run ruff check .
	@echo "✅ Linting completed"

# Format code
format:
	@echo "🎨 Formatting code..."
	uv run ruff format .
	@echo "✅ Code formatted"

# Check code formatting (CI mode)
check-format:
	@echo "🔍 Checking code formatting..."
	uv run ruff format --check .
	@echo "✅ Code formatting is correct"

# Run all quality checks
quality-check: lint check-format test
	@echo "🎯 All quality checks passed!"
	@echo "✅ Ready to push to GitHub"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ __pycache__/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf notebooks/executed_ipynb/*.ipynb
	@echo "✅ Cleanup completed"

# Build the package
build: clean
	@echo "📦 Building package..."
	uv build
	@echo "✅ Package built"

# Start Jupyter Lab
jupyter:
	@echo "📓 Starting Jupyter Lab..."
	uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
	@echo "✅ Jupyter Lab stopped"

# Convert and execute notebooks to generate outputs with executed cells
notebooks-execute:
	@echo "🔄 Converting and executing all notebooks with outputs..."
	mkdir -p notebooks/executed_ipynb
	@echo "🔍 Finding all .py notebook files in notebooks/..."
	@for notebook in notebooks/*.py; do \
		if [ -f "$$notebook" ] && grep -q "# %%" "$$notebook"; then \
			basename=$$(basename "$$notebook" .py); \
			echo "🔄 Converting $$basename.py..."; \
			uv run --with jupytext jupytext --to notebook "$$notebook" --output "notebooks/executed_ipynb/$$basename.ipynb"; \
			echo "🔄 Executing $$basename.ipynb..."; \
			uv run papermill "notebooks/executed_ipynb/$$basename.ipynb" "notebooks/executed_ipynb/$$basename.ipynb" -k python3; \
		fi; \
	done
	@echo "✅ All notebooks converted and executed with outputs"
	@echo "📂 Executed notebook files saved to notebooks/executed_ipynb/"
	@echo "💡 Open with: jupyter lab notebooks/executed_ipynb/"
	@echo "🚀 These files can be committed to git for sharing results"

# CI simulation - run exactly what GitHub Actions will run
ci-check:
	@echo "🤖 Running CI checks (simulating GitHub Actions)..."
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📦 Installing dependencies..."
	@uv sync --group dev
	@echo "🔍 Running linting..."
	@uv run ruff check .
	@echo "🔍 Checking format..."
	@uv run ruff format --check .
	@echo "🧪 Running tests..."
	@uv run python -m pytest tests/ -v
	@echo "🔄 Testing package build..."
	@uv build >/dev/null
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ CI checks completed successfully!"
	@echo "🎯 Your code will pass GitHub Actions" 