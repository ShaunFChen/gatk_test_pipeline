#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <project_name>"
  exit 1
fi

PROJECT_NAME="$1"

mkdir -p "$PROJECT_NAME" && cd "$PROJECT_NAME"

# Initialize basic layout (Git initialization left to user)
mkdir -p data notebooks src tests .github/workflows .devcontainer

touch data/.gitkeep
touch notebooks/.gitkeep

cat <<EOF > README.md
# $PROJECT_NAME

Project description goes here.
EOF

cat <<EOF > .gitignore
__pycache__/
*.pyc
.venv/
.env
.ipynb_checkpoints/
.DS_Store
EOF

# pyproject.toml for uv and dependencies
cat <<EOF > pyproject.toml
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = ""
authors = [{ name = "Your Name", email = "you@example.com" }]
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "pandas",
    "numpy",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "scipy>=1.15.3",
]

[dependency-groups]
dev = [
    "jupyter",
    "ruff"
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
    "D213"   # Incompatible with D212
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
EOF

# Dockerfile with uv and bioinformatics tools
cat <<EOF > Dockerfile
FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    openjdk-17-jre-headless \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    git \
    pip \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN conda install -c bioconda -c conda-forge -y \
    gatk4 \
    bwa \
    samtools \
    bcftools \
    fastqc \
    multiqc \
    rtg-tools

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:\$PATH"

WORKDIR /project
COPY . /project

RUN uv venv \
 && curl -sS https://bootstrap.pypa.io/get-pip.py | .venv/bin/python \
 && uv pip install . \
 && uv pip install --group dev

CMD ["bash"]
EOF

# GitHub Actions CI for linting, testing, and reproducibility
cat <<EOF > .github/workflows/test.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install Python & Ruff
        run: |
          pip install ruff
      - name: Lint
        run: ruff check .
      - name: Format check
        run: ruff format --check .
EOF

# VS Code dev container configuration
cat <<EOF > .devcontainer/devcontainer.json
{
  "name": "$PROJECT_NAME",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "customizations": {
    "vscode": {
      "extensions": ["ms-python.python", "ms-python.vscode-pylance"]
    }
  },
  "mounts": [
    "source=.,target=/workspace,type=bind"
  ],
  "postCreateCommand": "curl -LsSf https://astral.sh/uv/install.sh | sh && uv venv && uv pip install . && uv pip install --group dev"
}
EOF

# Completion message
echo "✅ Project '$PROJECT_NAME' initialized."
echo "➡️  Next steps:"
echo "  cd $PROJECT_NAME"
echo "  docker build -t $PROJECT_NAME ."
echo "  docker run -it --rm -v \$(pwd):/project $PROJECT_NAME"

