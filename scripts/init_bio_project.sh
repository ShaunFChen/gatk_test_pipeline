#!/bin/bash
# Comprehensive bioinformatics project initializer
# Usage: ./init_bio_project.sh <project_name>

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <project_name>"
  echo "Creates a comprehensive bioinformatics project structure with modern tooling"
  exit 1
fi

PROJECT_NAME="$1"

echo "🧬 Initializing bioinformatics project: $PROJECT_NAME"

# Create project directory
mkdir -p "$PROJECT_NAME" && cd "$PROJECT_NAME"

# Basic directory structure
mkdir -p data notebooks src tests .github/workflows
touch data/.gitkeep notebooks/.gitkeep

# Basic README
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

# Run analysis
uv run jupyter lab
\`\`\`

## Structure

- \`data/\` - Input datasets
- \`notebooks/\` - Jupyter analysis notebooks  
- \`src/\` - Reusable Python modules
- \`tests/\` - Unit tests
- \`.github/workflows/\` - CI/CD configuration

## Development

- \`make test\` - Run tests
- \`make lint\` - Run linting
- \`make format\` - Format code
- \`make quality-check\` - Run all quality checks
- \`make clean\` - Clean cache files

EOF

# Modern Python project configuration
cat <<EOF > pyproject.toml
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "Bioinformatics analysis project"
requires-python = ">=3.10"
dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "matplotlib>=3.6.0",
    "seaborn>=0.12.0",
    "scipy>=1.10.0",
    "biopython>=1.80",
    "pysam>=0.21.0",
    "pyfaidx>=0.7.0",
    "plotly>=5.15.0",
]

[dependency-groups]
dev = [
    "jupyter>=1.0.0",
    "jupyterlab>=4.0.0",
    "ruff>=0.1.0",
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.5.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "pre-commit>=3.0.0",
]

[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 100
target-version = "py310"
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "C901",  # too complex
]

[tool.ruff.per-file-ignores]
"tests/*" = ["S101"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
    "--tb=short",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
ignore_missing_imports = true

[tool.black]
line-length = 100
target-version = ['py310']
include = '\.pyi?$'
extend-exclude = '''
/(
    \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 100
EOF

# Comprehensive gitignore for bioinformatics projects
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

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# pdm
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
.idea/

# VS Code
.vscode/settings.json
.vscode/launch.json
.vscode/extensions.json
.vscode/tasks.json

# Spyder
.spyderproject
.spyproject

# Rope
.ropeproject

# OS-specific files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Ruff cache
.ruff_cache/

# Bioinformatics specific
*.bam
*.bai
*.sam
*.vcf
*.vcf.gz
*.vcf.idx
*.bed
*.fasta
*.fa
*.fastq
*.fq
*.gz
*.tbi
*.csi
*.gff
*.gff3
*.gtf
*.wig
*.bigwig
*.bw
*.bedgraph
*.maf
*.psl
*.chain
*.2bit
*.dict
*.fai
*.amb
*.ann
*.bwt
*.pac
*.sa
*.sai
*.bt2
*.bt2l
*.bowtie2
*.bam.bai
*.sam.bai
*.fasta.fai
*.fa.fai
*.fq.gz
*.fastq.gz
*_R1_*.fastq*
*_R2_*.fastq*
*_1.fastq*
*_2.fastq*
*_trimmed*
*_filtered*
*_sorted*
*_marked*
*_recalibrated*
*_variants*
*_annotated*
gatk_logs/
trimmomatic_logs/
bowtie2_logs/
bwa_logs/
star_logs/
salmon_logs/
kallisto_logs/
picard_logs/
multiqc_data/
multiqc_report.html
fastqc_results/
*.html
*.zip
temp/
tmp/
scratch/
work/
results/
output/
logs/
benchmarks/
profiles/
dag.pdf
dag.png
dag.svg
report.html
timeline.html
trace.txt
execution_trace.txt
execution_report.html
*.lsf
*.pbs
*.slurm
*.out
*.err
*.log
*.e*
*.o*
*.pe*
*.po*
.nextflow/
.nextflow.log*
nextflow.config
.snakemake/
Snakefile.orig
*.sif
*.img
singularity_cache/
apptainer_cache/
conda_cache/
mamba_cache/
EOF

# Comprehensive Makefile
cat <<'EOF' > Makefile
.PHONY: help install test lint format type-check quality-check clean docker-build docker-run docker-test ci-check

help:
	@echo "Available commands:"
	@echo "  install        Install dependencies"
	@echo "  test           Run tests"
	@echo "  lint           Run linting"
	@echo "  format         Format code"
	@echo "  type-check     Run type checking"
	@echo "  quality-check  Run all quality checks"
	@echo "  clean          Clean cache files"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-run     Run Docker container"
	@echo "  docker-test    Test Docker environment"
	@echo "  ci-check       Run CI checks locally"

install:
	@echo "Installing dependencies..."
	uv sync --group dev

test:
	@echo "Running tests..."
	uv run pytest tests/ -v

lint:
	@echo "Running linting..."
	uv run ruff check .

format:
	@echo "Formatting code..."
	uv run ruff format .

type-check:
	@echo "Running type checking..."
	uv run mypy src/ --ignore-missing-imports

quality-check: lint format type-check test
	@echo "All quality checks passed!"

clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".coverage" -delete 2>/dev/null || true
	@echo "Cache files cleaned!"

docker-build:
	@echo "Building Docker image..."
	docker build -t ${PROJECT_NAME} .

docker-run:
	@echo "Running Docker container..."
	docker run -it --rm -v $(PWD):/workspace ${PROJECT_NAME}

docker-test:
	@echo "Testing Docker environment..."
	docker run --rm ${PROJECT_NAME} python -c "import pysam; import pandas; print('Docker environment working')"

ci-check: clean install quality-check
	@echo "CI checks completed successfully!"
EOF

# GitHub Actions workflow
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
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Install uv
      uses: astral-sh/setup-uv@v3
      with:
        version: "latest"
    
    - name: Set up Python ${{ matrix.python-version }}
      run: uv python install ${{ matrix.python-version }}
    
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

  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Install uv
      uses: astral-sh/setup-uv@v3
      with:
        version: "latest"
    
    - name: Set up Python
      run: uv python install 3.10
    
    - name: Install dependencies
      run: |
        uv sync --group dev
    
    - name: Check notebooks can be executed
      run: |
        uv run jupyter nbconvert --to notebook --execute notebooks/*.ipynb --inplace || true
    
    - name: Generate documentation
      run: |
        echo "Documentation generation placeholder"

  docker:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Build Docker image
      run: |
        docker build -t ${PROJECT_NAME} .
    
    - name: Test Docker image
      run: |
        docker run --rm ${PROJECT_NAME} python -c "import pysam; import pandas; print('Docker environment working')"
EOF

# VS Code settings for automatic Python configuration
mkdir -p .vscode
cat <<EOF > .vscode/settings.json
{
    "python.defaultInterpreterPath": "\${workspaceFolder}/.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.analysis.extraPaths": ["src"],
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/.ruff_cache": true,
        "**/*.egg-info": true,
        "**/.mypy_cache": true
    }
}
EOF

# Python version file
echo "3.10" > .python-version

# Basic sample module
mkdir -p src
cat <<EOF > src/__init__.py
"""${PROJECT_NAME} - Bioinformatics analysis project."""

__version__ = "0.1.0"
EOF

# Basic test
mkdir -p tests
cat <<EOF > tests/test_basic.py
"""Basic tests for ${PROJECT_NAME}."""

import pytest


def test_basic():
    """Test basic functionality."""
    assert True


def test_imports():
    """Test that required packages can be imported."""
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import scipy
    import Bio
    import pysam
    
    assert pd.__version__
    assert np.__version__
    print("All imports successful!")
EOF

echo "✅ Project '$PROJECT_NAME' initialized successfully!"
echo ""
echo "🔧 Next steps:"
echo "  cd $PROJECT_NAME"
echo "  uv venv --python 3.10"
echo "  uv sync --group dev"
echo "  make quality-check"
echo "  uv run jupyter lab"
echo ""
echo "🧪 Development commands:"
echo "  make test          # Run tests"
echo "  make lint          # Run linting"
echo "  make format        # Format code"
echo "  make quality-check # Run all quality checks"
echo "  make clean         # Clean cache files"
echo ""
echo "�� Happy analyzing!"

