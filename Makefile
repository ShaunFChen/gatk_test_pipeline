# Makefile for GATK Test Pipeline - Local Quality Verification
# Run this before pushing to avoid GitHub Actions failures

.PHONY: help install test lint format check-format type-check quality-check clean build docker-build docker-run

# Default target
help:
	@echo "🛠️  GATK Test Pipeline - Local Quality Verification"
	@echo "=================================================="
	@echo "Available targets:"
	@echo "  install            - Install dependencies with uv"
	@echo "  test               - Run all tests"
	@echo "  lint               - Run linting with ruff"
	@echo "  format             - Format code with ruff"
	@echo "  check-format       - Check code formatting (CI mode)"
	@echo "  type-check         - Run type checking (if mypy available)"
	@echo "  quality-check      - Run all quality checks (lint + format + test)"
	@echo "  clean              - Clean build artifacts"
	@echo "  build              - Build the package"
	@echo "  docker-build       - Build Docker image"
	@echo "  docker-run         - Run Docker container"
	@echo "  jupyter            - Start Jupyter Lab"
	@echo "  notebooks-html     - Convert .py notebooks to .ipynb format"
	@echo "  notebooks-run      - Run notebooks and save outputs"
	@echo "  notebooks-html-docker - Convert notebooks to .ipynb (Docker with tools)"
	@echo "  run-notebooks-docker - Run notebooks in Docker with bioinformatics tools"
	@echo "  snakemake-docker   - Run Snakemake workflow in Docker"
	@echo "  check-deps         - Check bioinformatics dependencies"
	@echo ""
	@echo "🚀 Quick workflow:"
	@echo "  make install && make quality-check"
	@echo ""
	@echo "🧬 Bioinformatics workflow:"
	@echo "  make docker-build && make run-notebooks-docker"
	@echo ""
	@echo "📓 Notebook workflow:"
	@echo "  make notebooks-html && make jupyter"

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

# Type checking (if mypy is available)
type-check:
	@echo "🔍 Running type checking..."
	@if uv run python -c "import mypy" 2>/dev/null; then \
		uv run mypy src/ --ignore-missing-imports; \
		echo "✅ Type checking completed"; \
	else \
		echo "ℹ️  mypy not installed, skipping type checking"; \
	fi

# Run all quality checks
quality-check: lint check-format test
	@echo "🎯 All quality checks passed!"
	@echo "✅ Ready to push to GitHub"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf results/
	rm -rf data/*.fasta
	rm -rf data/*.fastq
	rm -rf data/*.vcf
	rm -rf data/*.bam
	@echo "✅ Cleanup completed"

# Build the package
build: clean
	@echo "📦 Building package..."
	uv build
	@echo "✅ Package built"

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t gatk-interview .
	@echo "✅ Docker image built"

docker-run:
	@echo "🐳 Running Docker container..."
	docker run -it --rm -v $(PWD):/project gatk-interview
	@echo "✅ Docker container stopped"

# Start Jupyter Lab
jupyter:
	@echo "📓 Starting Jupyter Lab..."
	uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
	@echo "✅ Jupyter Lab stopped"

# Convert notebooks to HTML
notebooks-html:
	@echo "📄 Converting notebooks to HTML..."
	mkdir -p output/notebooks
	@echo "🔄 Converting variant calling notebook..."
	uv run --with jupytext jupytext --to notebook notebooks/01_variant_calling_pipeline.py --output output/notebooks/01_variant_calling_pipeline.ipynb
	@echo "🔄 Converting bisulfite analysis notebook..."
	uv run --with jupytext jupytext --to notebook notebooks/02_bisulfite_conversion_efficiency.py --output output/notebooks/02_bisulfite_conversion_efficiency.ipynb
	@echo "✅ Notebooks converted to .ipynb format"
	@echo "📂 Notebook files saved to output/notebooks/"
	@echo "💡 Open with: jupyter lab output/notebooks/"

# Run notebooks and save outputs
notebooks-run:
	@echo "📓 Running notebooks to generate outputs..."
	mkdir -p output/notebooks
	@echo "🔄 Running variant calling notebook..."
	uv run python notebooks/01_variant_calling_pipeline.py > output/notebooks/01_variant_calling_output.txt 2>&1
	@echo "🔄 Running bisulfite analysis notebook..."
	uv run python notebooks/02_bisulfite_conversion_efficiency.py > output/notebooks/02_bisulfite_output.txt 2>&1
	@echo "✅ Notebook outputs saved"
	@echo "📂 Output files saved to output/notebooks/"

# Convert notebooks to executed HTML with Docker (full tools)
notebooks-html-docker:
	@echo "🐳 Converting notebooks to .ipynb format with Docker..."
	docker run --rm -v $(PWD):/project gatk-interview bash -c "cd /project && mkdir -p output/notebooks && uv run --with jupytext jupytext --to notebook notebooks/01_variant_calling_pipeline.py --output output/notebooks/01_variant_calling_pipeline.ipynb && uv run --with jupytext jupytext --to notebook notebooks/02_bisulfite_conversion_efficiency.py --output output/notebooks/02_bisulfite_conversion_efficiency.ipynb"
	@echo "✅ Notebooks converted to .ipynb format with Docker"
	@echo "📂 Notebook files saved to output/notebooks/"
	@echo "💡 Open with: jupyter lab output/notebooks/"

# Run notebooks in Docker environment
run-notebooks-docker:
	@echo "🐳 Running notebooks in Docker with full bioinformatics tools..."
	docker run --rm -v $(PWD):/project gatk-interview bash -c "cd /project && uv run python notebooks/01_variant_calling_pipeline.py && uv run python notebooks/02_bisulfite_conversion_efficiency.py"
	@echo "✅ Notebooks completed in Docker"

# Run Snakemake with Docker
snakemake-docker:
	@echo "🐳 Running Snakemake workflow in Docker..."
	docker run --rm -v $(PWD):/project gatk-interview bash -c "cd /project && uv run snakemake --cores 2"
	@echo "✅ Snakemake workflow completed in Docker"

# Check dependencies
check-deps:
	@echo "🔍 Checking bioinformatics dependencies..."
	@uv run python -c "from src.variant_calling_utils import check_dependencies; deps = check_dependencies(); print('\n'.join([f'✅ {tool}' if available else f'❌ {tool}' for tool, available in deps.items()]))"
	@echo "✅ Dependency check completed"

# Run notebook tests
test-notebooks:
	@echo "📓 Testing notebooks..."
	@echo "ℹ️  Note: This requires nbval plugin"
	@if uv run python -c "import nbval" 2>/dev/null; then \
		uv run pytest --nbval notebooks/ --ignore=notebooks/.ipynb_checkpoints; \
		echo "✅ Notebook tests passed"; \
	else \
		echo "ℹ️  nbval not installed, skipping notebook tests"; \
		echo "💡 Install with: uv add --group dev nbval"; \
	fi

# Pre-commit hook simulation
pre-commit: quality-check
	@echo "✅ Pre-commit checks passed"
	@echo "🚀 Safe to commit!"

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
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ CI checks completed successfully!"
	@echo "🎯 Your code will pass GitHub Actions"

# Development setup
dev-setup: install
	@echo "🛠️  Setting up development environment..."
	@echo "📓 Installing Jupyter kernel..."
	@uv run python -m ipykernel install --user --name=gatk-pipeline --display-name="GATK Pipeline"
	@echo "✅ Development environment ready"
	@echo "💡 Run 'make jupyter' to start Jupyter Lab"

# Show project info
info:
	@echo "📋 Project Information"
	@echo "======================"
	@echo "Project: GATK Test Pipeline"
	@echo "Purpose: Nucleix Interview Preparation"
	@echo "Python: $(shell uv run python --version)"
	@echo "UV: $(shell uv --version)"
	@echo "Git branch: $(shell git branch --show-current 2>/dev/null || echo 'Not a git repository')"
	@echo "Files:"
	@echo "  📁 src/: $(shell find src -name '*.py' | wc -l) Python files"
	@echo "  📁 tests/: $(shell find tests -name '*.py' | wc -l) Test files"
	@echo "  📁 notebooks/: $(shell find notebooks -name '*.ipynb' | wc -l) Jupyter notebooks"
	@echo "Docker image: gatk-interview"

# Performance testing
perf-test:
	@echo "⚡ Running performance tests..."
	@uv run python -c "from src.variant_calling_utils import PerformanceMonitor; m = PerformanceMonitor(); m.start_step('test'); import time; time.sleep(0.1); m.end_step('test'); print('✅ Performance monitoring works')"
	@echo "✅ Performance tests completed"

# Integration test
integration-test:
	@echo "🔗 Running integration tests..."
	@uv run python -c "import sys; sys.path.insert(0, 'src'); from variant_calling_utils import *; from bisulfite_utils import *; print('✅ All modules import successfully')"
	@echo "✅ Integration tests completed"

# Full verification (everything before push)
verify: clean install ci-check check-deps
	@echo "🎯 Full verification completed!"
	@echo "✅ Your code is ready for production"
	@echo "🚀 Safe to push to GitHub!" 