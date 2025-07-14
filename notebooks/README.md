# Notebooks Directory

This directory contains Python scripts that implement comprehensive bioinformatics analyses for technical interviews and educational purposes. The scripts are organized with proper cell separators (`# %%`) for easy conversion to Jupyter notebooks.

## Files

- `01_variant_calling_pipeline.py` - Complete GATK Best Practices implementation
- `02_bisulfite_conversion_efficiency.py` - Comprehensive bisulfite analysis pipeline

## Executing Notebooks

### Recommended: Using Make Target
```bash
# Convert and execute notebooks with outputs (from project root)
make notebooks-execute
```

This command:
- Converts `.py` files to `.ipynb` format using jupytext
- Executes the notebooks with papermill
- Saves executed notebooks with outputs to `output/notebooks/`

### Alternative: Using Jupyter Lab
```bash
# Start Jupyter Lab (from project root)
make jupyter
```

Then navigate to the notebooks directory within Jupyter Lab.

### Manual Conversion Options

#### Option 1: Using jupytext
```bash
# Convert to notebook format
uv run --with jupytext jupytext --to notebook *.py

# Execute converted notebooks
uv run --with jupyter jupyter nbconvert --execute --inplace *.ipynb
```

#### Option 2: Using papermill directly
```bash
# Convert and execute in one step
uv run --with jupytext --with papermill \
  jupytext --to notebook 01_variant_calling_pipeline.py | \
  papermill --kernel python3 - output_notebook.ipynb
```

## Features

Both scripts include:
- ✅ Robust project import system that works in IDE and execution environments
- ✅ Comprehensive tech test content integration  
- ✅ Performance analysis and visualization
- ✅ Real data integration capabilities
- ✅ Senior-level technical challenge solutions
- ✅ Production-ready implementations
- ✅ Automatic dependency checking and project environment detection

## Content Overview

### 01_variant_calling_pipeline.py
**Tech Test Question**: Develop a variant-calling pipeline using GATK best practices with performance optimization.

**Implementation includes**:
- GATK Best Practices workflow
- Performance monitoring and optimization strategies
- Quality control metrics (Ti/Tv ratio, coverage analysis)
- Real genomic data processing
- Validation against benchmark datasets
- Memory and parallelization optimization

### 02_bisulfite_conversion_efficiency.py  
**Tech Test Question**: Design experimental/computational pipeline for measuring bisulfite conversion efficiency.

**Implementation includes**:
- Bisulfite sequencing data simulation
- Conversion efficiency calculation methods
- Lambda DNA control analysis
- Context-specific methylation analysis (CpG, CHG, CHH)
- Quality control frameworks
- Interactive visualization and reporting

## Project Integration

The notebooks integrate seamlessly with the project structure:
- **Data**: Automatically loads sample data from `../data/`
- **Utilities**: Imports functions from `src/` modules
- **Output**: Saves results to `../output/`
- **Environment**: Detects and adapts to execution context (IDE vs notebook execution)

## Development Notes

### IDE Usage
The notebooks include automatic project path detection that works when:
- Running cells in VS Code/Cursor Python extension
- Executing from any directory in the project
- Using different Python interpreters

### Execution Context
The import system automatically handles:
- Finding project root via `pyproject.toml`
- Adding project root to Python path
- Importing from `src/` package
- Dependency validation and environment detection

### Output Generation
When executed via `make notebooks-execute`:
- Creates `.ipynb` files with all cell outputs
- Includes plots, tables, and analysis results
- Saves to `output/notebooks/` directory
- Preserves execution timing and metadata
