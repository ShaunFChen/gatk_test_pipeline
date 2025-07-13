FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y     build-essential     wget     curl     openjdk-17-jre-headless     zlib1g-dev     libbz2-dev     liblzma-dev     libcurl4-openssl-dev     libssl-dev     git     pip     vim     && rm -rf /var/lib/apt/lists/*

RUN conda install -c bioconda -c conda-forge -y     gatk4     bwa     samtools     bcftools     fastqc     multiqc     rtg-tools

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /project
COPY . /project

RUN uv venv  && curl -sS https://bootstrap.pypa.io/get-pip.py | .venv/bin/python  && uv pip install .  && uv pip install --group dev

CMD ["bash"]
