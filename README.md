# GATK Test Pipeline

Fully derived using agenetic coding with Claude 4 from scratch - A comprehensive bioinformatics pipeline for variant calling and bisulfite conversion analysis, designed for educational purposes.

## 🎯 Features

- **Real Working Code**: Actual implementations, not pseudocode
- **Sample Data Generation**: Creates realistic genomic data for analysis  
- **Quality Assurance**: Makefile with linting, testing, and formatting
- **Documentation**: Complete setup and troubleshooting guides
- **Portable Setup**: Works on any machine with Python 3.10+ and UV

## 📋 Project Contents

### Notebooks
- **`01_variant_calling_pipeline.py`**: Complete GATK best practices pipeline with real BAM/VCF generation
- **`02_bisulfite_conversion_efficiency.py`**: Comprehensive bisulfite analysis with quality control

### Source Code
- **`src/variant_calling_utils.py`**: GATK command builders, performance monitoring, validation metrics
- **`src/bisulfite_utils.py`**: Bisulfite simulation, efficiency analysis, quality control
- **`src/performance_analysis.py`**: Pipeline performance monitoring and reporting
- **`src/real_data_analysis.py`**: Real genomic data processing and validation

### Quality Assurance
- **Unit tests** with comprehensive test coverage (all passing)
- **Linting and formatting** with Ruff
- **Makefile** for local verification before CI
- **Docker support** for reproducible environments

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** (tested with 3.11+)
- **UV package manager** ([install from astral.sh/uv](https://astral.sh/uv))
- **Docker** (optional, for full bioinformatics tools)

### Environment Setup

#### Local Development (Python-only)
```bash
# Clone and enter directory
git clone <repository-url>
cd gatk_test_pipeline

# Create environment and install dependencies
uv venv --python 3.11
uv sync --group dev

# Verify setup
uv run python --version          # Should show Python 3.11+
uv run python -c "import pandas; print('✅ Pandas:', pandas.__version__)"
make test                        # Should pass all tests
```

#### Docker (Full Bioinformatics Tools)
```bash
# Build Docker image with all bioinformatics tools
docker build -t gatk_test_pipeline .

# Run interactive container
docker run -it --rm -v $(pwd):/project gatk_test_pipeline
```

### Bioinformatics Tools

The project includes interfaces for:
- **GATK**: Variant calling and analysis
- **BWA**: Read alignment  
- **samtools/pysam**: BAM file manipulation
- **bcftools**: VCF file processing
- **FastQC**: Quality control

**Tool Availability:**
- **Local Environment**: Python tools (pysam, pandas, matplotlib) + project environment simulation
- **Docker Environment**: Full bioinformatics suite (GATK, BWA, samtools, etc.)

The dependency checker automatically detects available tools in your environment.

### Usage

#### Development Commands
```bash
make help           # Show all available commands
make test           # Run unit tests
make quality-check  # Run linting, formatting, and tests
make lint           # Run code linting
make format         # Format code
make build          # Build the package
```

#### Notebook Execution
```bash
make notebooks-execute  # Convert .py files to executed .ipynb notebooks
make jupyter            # Start Jupyter Lab
```

The notebooks are stored as Python files with cell markers (`# %%`) and converted to Jupyter notebooks with executed outputs using the `notebooks-execute` target.

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

**Implementation**: `notebooks/01_variant_calling_pipeline.py`
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

**Implementation**: `notebooks/02_bisulfite_conversion_efficiency.py`
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
docker build -t gatk_test_pipeline .
docker run -it --rm -v $(pwd):/project gatk_test_pipeline
```

The Docker image includes all bioinformatics tools (GATK, BWA, samtools, etc.) and Python dependencies for a complete execution environment.

---

## 📁 Project Structure

```
gatk_test_pipeline/
├── .venv/                 # Virtual environment
├── .vscode/              # VS Code configuration
├── data/                 # Input data and sample files
│   ├── alignments/       # BAM/SAM alignment files
│   ├── giab/            # GIAB benchmark data
│   ├── reference/       # Reference genome files
│   └── README.md        # Data documentation
├── notebooks/            # Analysis notebooks as Python files
│   ├── executed_ipynb/   # Executed notebooks as .ipynb files
│   ├── 01_variant_calling_pipeline.py
│   ├── 02_bisulfite_conversion_efficiency.py
│   └── README.md        # Notebook documentation
├── output/              # Generated outputs and results
│   └── notebooks/       # Executed Jupyter notebooks (.ipynb)
├── src/                 # Source code utilities
│   ├── __init__.py
│   ├── variant_calling_utils.py
│   ├── bisulfite_utils.py
│   ├── performance_analysis.py
│   └── real_data_analysis.py
├── tests/               # Unit tests
├── scripts/             # Utility scripts
│   ├── generate_sample_data.py
│   ├── download_real_data.py
│   ├── generate_performance_report.py
│   ├── pipeline_monitor.py
│   └── init_bio_project.sh
├── Dockerfile           # Container configuration
├── Makefile            # Development commands
├── pyproject.toml      # Dependencies and configuration
├── Snakefile           # Workflow definition
├── workflow_config.yaml # Workflow configuration
└── README.md           # This file
```

---

## 🛠️ Troubleshooting

### Import Errors in Notebooks
The notebooks include automatic project path detection. If you encounter import errors, ensure you're running from the project root or using the provided `make notebooks-execute` command.

### Environment Issues
```bash
# Clean reinstall
rm -rf .venv
uv venv --python 3.11
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
- Uses Homebrew Python or system Python
- May need: `xcode-select --install`

#### Linux  
- May need: `sudo apt-get install build-essential`

#### Windows
- Use PowerShell or Git Bash
- Replace `make` with `uv run` commands if needed

---

## 🔬 Workflow Execution

### Snakemake Workflow
```bash
# Run the complete pipeline
uv run snakemake --cores all

# Run specific targets
uv run snakemake variant_calling
uv run snakemake bisulfite_analysis
```

### Script Execution
```bash
# Generate sample data
uv run python scripts/generate_sample_data.py

# Download real data
uv run python scripts/download_real_data.py

# Generate performance reports
uv run python scripts/generate_performance_report.py
```

---

## 📊 Quality Metrics

The project includes comprehensive quality control:
- **Code quality**: Linting with Ruff
- **Test coverage**: Unit tests for all major components
- **Performance monitoring**: Built-in timing and resource usage tracking
- **Data validation**: Automated checks for genomic data integrity
- **Reproducibility**: Containerized environment with pinned dependencies

Run all quality checks before committing:
```bash
make quality-check
```
