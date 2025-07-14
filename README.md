# GATK Test Pipeline

A comprehensive bioinformatics pipeline for variant calling and bisulfite conversion analysis, designed for technical interviews and educational purposes.

## 🎯 Interview Ready Features

- **Real Working Code**: Actual implementations, not pseudocode
- **Sample Data Generation**: Creates realistic genomic data for analysis  
- **Quality Assurance**: Makefile with linting, testing, and formatting
- **Documentation**: Complete setup and troubleshooting guides
- **Portable Setup**: Works on any machine with Python 3.10+ and UV

## 📋 Project Contents

### Notebooks
- **`01_variant_calling_pipeline.ipynb`**: Complete GATK best practices pipeline with real BAM/VCF generation
- **`02_bisulfite_conversion_efficiency.ipynb`**: Comprehensive bisulfite analysis with quality control

### Source Code
- **`src/variant_calling_utils.py`**: GATK command builders, performance monitoring, validation metrics
- **`src/bisulfite_utils.py`**: Bisulfite simulation, efficiency analysis, quality control

### Quality Assurance
- **Unit tests** with 12 test cases (all passing)
- **Linting and formatting** with Ruff
- **Makefile** for local verification before CI
- **Docker support** for reproducible environments

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** 
- **UV package manager** ([install from astral.sh/uv](https://astral.sh/uv))
- **Docker** (optional, for full bioinformatics tools)

### Environment Options

#### Option 1: Local Development (Python-only)
```bash
# Clone and enter directory
git clone <repository-url>
cd gatk_test_pipeline

# Create environment and install dependencies
uv venv --python 3.11
uv sync --group dev

# Verify setup
uv run python --version          # Should show Python 3.11.x
uv run python -c "import pandas; print('✅ Pandas:', pandas.__version__)"
make test                        # Should pass all 12 tests
```

#### Option 2: Docker (Full Bioinformatics Tools)
```bash
# Build Docker image with all bioinformatics tools
make docker-build

# Run notebooks with full tool support
make run-notebooks-docker

# Convert notebooks to HTML with full environment
make notebooks-html-docker

# Run Snakemake workflow in Docker
make snakemake-docker
```

### Bioinformatics Tools

The project includes interfaces for:
- **GATK**: Variant calling and analysis
- **BWA**: Read alignment  
- **samtools/pysam**: BAM file manipulation
- **bcftools**: VCF file processing
- **FastQC**: Quality control

**Tool Availability:**
- **Local Environment**: Only Python tools (pysam, pandas, matplotlib)
- **Docker Environment**: Full bioinformatics suite (GATK, BWA, samtools, etc.)

Check tool availability:
```bash
make check-deps
```

### Usage

#### Local Environment
```bash
make help           # Show all available commands
make test           # Run unit tests
make jupyter        # Start Jupyter Lab
make quality-check  # Run linting, formatting, and tests
make notebooks-html # Convert notebooks to HTML
```

#### Docker Environment
```bash
make docker-build          # Build Docker image
make run-notebooks-docker  # Run notebooks with full tools
make snakemake-docker      # Run Snakemake workflow
```

---

## 🔧 IDE Configuration

### Automatic (VS Code/Cursor)
The `.vscode/settings.json` automatically configures the Python interpreter. Just restart your IDE after setup.

### Manual Configuration
1. **Find interpreter path**: `echo "$(pwd)/.venv/bin/python"`
2. **Configure IDE**:
   - **VS Code/Cursor**: `Cmd+Shift+P` → "Python: Select Interpreter" → Navigate to `.venv/bin/python`
   - **PyCharm**: Preferences → Python Interpreter → Add → Existing Environment → Select `.venv/bin/python`

### Fix Red Underlines
If you see red underlines under imports:
1. **Restart IDE** completely
2. **Reload window**: `Cmd+Shift+P` → "Developer: Reload Window"  
3. **Clear Python cache**: `Cmd+Shift+P` → "Python: Clear Cache and Reload Window"
4. **Verify interpreter**: Should be `<project-root>/.venv/bin/python`

---

## 🧪 Technical Interview Components

### 1. Variant Calling Pipeline (GATK Best Practices)
**Interview Question**: "Develop a variant-calling pipeline using GATK best practices with performance optimization."

**Implementation**: `notebooks/01_variant_calling_pipeline.ipynb`
- Real BAM file generation with pysam
- GATK command building and execution
- Performance monitoring and optimization
- Quality assessment and validation
- Visualization of results

**Key Topics**:
- GATK HaplotypeCaller workflow
- Performance bottlenecks and solutions
- Quality control metrics (Ti/Tv ratio, coverage, etc.)
- Parallelization strategies
- Memory optimization

### 2. Bisulfite Conversion Efficiency Analysis
**Interview Question**: "Analyze bisulfite conversion efficiency with quality control and computational approaches."

**Implementation**: `notebooks/02_bisulfite_conversion_efficiency.ipynb`
- Realistic bisulfite sequencing data simulation
- Conversion efficiency calculation
- Lambda DNA control analysis
- Quality control metrics
- Comprehensive visualizations

**Key Topics**:
- Bisulfite sequencing principles
- Conversion efficiency calculation methods
- Quality control strategies
- Statistical analysis approaches
- Data visualization techniques

---

## 🐳 Docker Support

### Build and Run
```bash
make docker-build
make docker-run
```

### Manual Docker Commands
```bash
docker build -t gatk-pipeline .
docker run -it --rm -v $(pwd):/project gatk-pipeline
```

The Docker image includes all bioinformatics tools (GATK, BWA, samtools, etc.) and Python dependencies.

---

## 📁 Project Structure

```
gatk_test_pipeline/
├── .venv/                 # Virtual environment
├── .vscode/              # VS Code configuration
├── data/                 # Input data (generated by notebooks)
├── notebooks/            # Jupyter notebooks with implementations
│   ├── 01_variant_calling_pipeline.ipynb
│   └── 02_bisulfite_conversion_efficiency.ipynb
├── src/                  # Source code utilities
│   ├── variant_calling_utils.py
│   └── bisulfite_utils.py
├── tests/               # Unit tests
├── scripts/             # Project initialization scripts
├── Dockerfile           # Container configuration
├── Makefile            # Development commands
├── pyproject.toml      # Dependencies and configuration
└── README.md           # This file
```

---

## 🛠️ Troubleshooting

### Import Errors in Notebooks
Add this to the first cell of notebooks:
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'src'))
```

### Environment Issues
```bash
# Clean reinstall
rm -rf .venv
uv venv --python 3.10
uv sync --group dev

# Verify everything works
make test
```

### IDE Python Path Issues
```bash
# Find correct path
echo "$(pwd)/.venv/bin/python"

# Alternative methods
uv run which python
realpath .venv/bin/python
```

### Platform-Specific Notes

#### macOS
- Uses Homebrew Python: `/usr/local/opt/python@3.10/bin/python3.10`
- May need: `xcode-select --install`

#### Linux  
- May need: `sudo apt-get install build-essential`

#### Windows
- Use PowerShell or Git Bash
- Replace `make` with `uv run` commands if needed

---

## 🧬 Bioinformatics Tools

The project includes interfaces for:
- **GATK**: Variant calling and analysis
- **BWA**: Read alignment  
- **samtools/pysam**: BAM file manipulation
- **bcftools**: VCF file processing
- **FastQC**: Quality control

All tools are available in the Docker container, or install locally as needed.

---

## 📊 Quality Metrics

### Test Coverage
- **12 unit tests** covering all major functionality
- **Command building**: GATK, performance monitoring
- **Data processing**: Validation metrics, utility functions
- **Integration tests**: End-to-end pipeline workflows

### Code Quality
- **Linting**: Ruff with comprehensive rules
- **Formatting**: Automatic code formatting
- **Type hints**: For better code documentation
- **Documentation**: Comprehensive docstrings

---

## 🎓 Educational Use

This project serves as:
- **Interview preparation** for data science/bioinformatics roles
- **Learning resource** for GATK best practices
- **Template** for bioinformatics projects
- **Reference implementation** of common workflows

Feel free to modify and extend for your specific needs!

---

## 📄 License

This project is for educational and interview preparation purposes. Feel free to use and modify as needed.

---

## 🔬 Snakemake Workflow Management

### Overview
This project includes a comprehensive **Snakemake workflow** for pipeline monitoring, benchmarking, and parallel execution. Snakemake provides production-ready workflow management with automatic resource tracking and performance analysis.

### Quick Start with Snakemake
```bash
# Run both pipelines with monitoring
uv run snakemake --cores 2

# View performance report
open output/pipeline_performance_report.html

# Clean outputs
uv run snakemake clean
```

### Workflow Features
- **🔄 Automatic Pipeline Orchestration**: Manages dependencies and execution order
- **📊 Performance Benchmarking**: Real-time CPU, memory, and I/O monitoring
- **⚡ Parallel Processing**: Multi-core execution with resource constraints
- **📈 Professional Reports**: HTML dashboards with performance visualizations
- **🎯 Quality Control**: Automated validation and error handling

### Workflow Architecture
```
├── Snakefile                     # Main workflow definition
├── workflow_config.yaml          # Configuration parameters
├── scripts/generate_performance_report.py  # Report generation
├── benchmarks/                   # Performance metrics
├── logs/                         # Execution logs
└── output/                       # Results and reports
```

### Configuration
Edit `workflow_config.yaml` to customize:
```yaml
# Resource allocation
threads: 4
memory_mb: 8000
runtime_minutes: 60

# Quality control thresholds
quality_thresholds:
  variant_calling:
    min_ti_tv_ratio: 2.0
    min_coverage: 10
  bisulfite:
    min_conversion_efficiency: 0.95
```

### Advanced Usage
```bash
# Run with custom resources
uv run snakemake --cores 4 --resources mem_mb=16000

# Dry run to see planned execution
uv run snakemake --dry-run

# Run specific pipeline only
uv run snakemake output/variant_calling_complete.txt

# Generate only performance report
uv run snakemake output/pipeline_performance_report.html
```

### Production Benefits
- **Scalability**: Ready for HPC/cloud deployment
- **Reproducibility**: Complete workflow versioning
- **Monitoring**: Comprehensive performance tracking
- **Quality Assurance**: Automated validation checks
