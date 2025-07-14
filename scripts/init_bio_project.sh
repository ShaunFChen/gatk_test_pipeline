#!/bin/bash
# Modern bioinformatics project initializer
# Usage: ./init_bio_project.sh <project_name>

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <project_name>"
  echo "Creates a bioinformatics project with modern Python tooling"
  exit 1
fi

PROJECT_NAME="$1"

echo "🧬 Initializing bioinformatics project: $PROJECT_NAME"

# Create project directory
mkdir -p "$PROJECT_NAME" && cd "$PROJECT_NAME"

# Essential directory structure
mkdir -p data notebooks src tests .github/workflows
touch data/.gitkeep notebooks/.gitkeep

# README
cat <<EOF > README.md
# $PROJECT_NAME

A bioinformatics analysis project using modern Python tooling.

## Quick Start

\`\`\`bash
# Setup environment
uv venv --python 3.10
uv sync --group dev

# Run quality checks
make quality-check

# Start analysis
uv run jupyter lab
\`\`\`

## Structure

- \`data/\` - Input datasets
- \`notebooks/\` - Jupyter analysis notebooks  
- \`src/\` - Reusable Python modules
- \`tests/\` - Unit tests

## Development

- \`make test\` - Run tests
- \`make lint\` - Run linting  
- \`make format\` - Format code
- \`make quality-check\` - Run all quality checks
- \`make clean\` - Clean cache files
EOF

# Modern pyproject.toml with specific versions
cat <<EOF > pyproject.toml
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "Bioinformatics analysis project"
authors = [{ name = "Your Name", email = "you@example.com" }]
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "pandas>=2.3.0",
    "numpy>=2.2.0",
    "matplotlib>=3.10.0",
    "seaborn>=0.13.0",
    "scipy>=1.15.0",
    "pysam>=0.23.0",
    "pyfaidx>=0.8.0",
    "plotly>=6.2.0",
    "biopython>=1.85",
    "tqdm>=4.66.0",
]

[dependency-groups]
dev = [
    "jupyter>=1.1.0",
    "jupyterlab>=4.4.0",
    "ruff>=0.12.0",
    "pytest>=8.4.0",
    "mypy>=1.16.0"
]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["ALL", "E", "F", "B"]
ignore = [
    "D100",  # Missing docstring in public module
    "D101",  # Missing docstring in public class
    "COM812",  # Conflicts with formatter
    "D203",  # Incompatible with D211
    "D213",  # Incompatible with D212
    "S101",  # Assert usage (acceptable in tests)
    "S311",  # Random number usage (acceptable for scientific simulations)
    "S602",  # shell=True usage (needed for bioinformatics tools)
    "PLR2004",  # Magic numbers (scientific constants are acceptable)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
EOF

# Comprehensive bioinformatics .gitignore
cat <<'EOF' > .gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Testing
.pytest_cache/
.coverage
htmlcov/
*.cover
*.py,cover
.hypothesis/

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb~

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Bioinformatics data files
*.fastq
*.fastq.gz
*.fq
*.fq.gz
*.fasta
*.fa
*.fna
*.fas
*.sam
*.bam
*.bai
*.vcf
*.vcf.gz
*.gff
*.gff3
*.gtf
*.bed
*.wig
*.bigwig
*.bw

# Analysis outputs
results/
output/
logs/
plots/
figures/
reports/

# Tool-specific outputs
gatk_logs/
multiqc_data/
.nextflow/
.snakemake/
work/
EOF

# Essential Makefile
cat <<'EOF' > Makefile
.PHONY: install test lint format quality-check clean

install:
	@echo "📦 Installing dependencies..."
	uv sync --group dev

test:
	@echo "🧪 Running tests..."
	uv run pytest tests/ -v --tb=short

lint:
	@echo "🔍 Running linting..."
	uv run ruff check .

format:
	@echo "🎨 Formatting code..."
	uv run ruff format .

quality-check: lint
	@echo "🔍 Checking code formatting..."
	uv run ruff format --check .
	@echo "🧪 Running tests..."
	uv run pytest tests/ -v --tb=short
	@echo "🎯 All quality checks passed!"
	@echo "✅ Ready to push to GitHub"

clean:
	@echo "🧹 Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/
	@echo "✅ Cache cleaned"
EOF

# Simple CI workflow
mkdir -p .github/workflows
cat <<'EOF' > .github/workflows/test.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Install uv
      uses: astral-sh/setup-uv@v3
      with:
        version: "latest"
    
    - name: Set up Python 3.10
      run: uv python install 3.10
    
    - name: Install dependencies
      run: |
        uv sync --group dev
    
    - name: Run linting
      run: |
        uv run ruff check .
    
    - name: Run format check
      run: |
        uv run ruff format --check .
    
    - name: Run tests
      run: |
        uv run pytest tests/ -v --tb=short
    
    - name: Run type checking
      run: |
        uv run mypy src/ --ignore-missing-imports
    
    - name: Check package can be built
      run: |
        uv build
EOF

# Basic test file
cat <<EOF > tests/__init__.py
"""Test suite for $PROJECT_NAME."""
EOF

cat <<EOF > tests/test_basic.py
"""Basic tests for $PROJECT_NAME."""

import pytest


def test_basic_math():
    """Test basic functionality."""
    assert 1 + 1 == 2


def test_imports():
    """Test that basic scientific libraries can be imported."""
    import numpy as np
    import pandas as pd
    
    # Basic operations
    assert np.array([1, 2, 3]).sum() == 6
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    assert len(df) == 2
EOF

# Basic utility module
cat <<EOF > src/__init__.py
"""$PROJECT_NAME utilities."""
EOF

cat <<EOF > src/utils.py
"""Basic utilities for $PROJECT_NAME."""

import logging
from pathlib import Path
from typing import Union


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Configured logger
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


def create_output_dir(path: Union[str, Path]) -> Path:
    """Create output directory if it doesn't exist.
    
    Args:
        path: Directory path to create
        
    Returns:
        Path object of created directory
    """
    output_path = Path(path)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def validate_file_exists(file_path: Union[str, Path]) -> Path:
    """Validate that a file exists.
    
    Args:
        file_path: Path to file
        
    Returns:
        Path object if file exists
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path
EOF

echo ""
echo "✅ Project '$PROJECT_NAME' created successfully!"
echo ""
echo "🚀 Next steps:"
echo "   cd $PROJECT_NAME"
echo "   uv venv --python 3.10"
echo "   uv sync --group dev"
echo "   make quality-check"
echo ""
echo "🎯 Start coding:"
echo "   uv run jupyter lab"
echo ""

