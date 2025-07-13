# Multi-stage build for efficient bioinformatics environment
FROM continuumio/miniconda3 as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    openjdk-17-jre-headless \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install bioinformatics tools via conda
RUN conda install -c bioconda -c conda-forge -y \
    gatk4 \
    bwa \
    samtools \
    bcftools \
    fastqc \
    && conda clean -a

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /project

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Install Python dependencies
RUN uv venv && uv sync --group dev

# Set environment
ENV PATH="/project/.venv/bin:$PATH"

CMD ["bash"]
