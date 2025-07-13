FROM continuumio/miniconda3:latest

ENV PATH=/opt/conda/bin:$PATH
ENV PYENV_ROOT=/root/.pyenv
ENV PATH=$PYENV_ROOT/bin:$PATH

# Install Linux system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    openjdk-17-jre-headless \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-gnutls-dev \
    libssl-dev \
    git \
    vim

# Install bioinformatics tools
RUN conda install -c bioconda -c conda-forge -y \
    gatk4 \
    bwa \
    samtools \
    bcftools \
    fastqc \
    multiqc \
    rtg-tools

# Install pyenv
RUN curl https://pyenv.run | bash

# Activate pyenv in shell
RUN echo 'eval "$(pyenv init --path)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Install Python 3.10 via pyenv
RUN pyenv install 3.10.13 && pyenv global 3.10.13

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv ~/.cargo/bin/uv /usr/local/bin/

WORKDIR /project

COPY . /project

RUN uv venv && \
    source .venv/bin/activate && \
    uv pip install -r requirements.txt

CMD ["/bin/bash"]
