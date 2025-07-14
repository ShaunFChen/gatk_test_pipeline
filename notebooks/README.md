# Notebooks Directory

This directory contains streamlined Python scripts that implement the tech test requirements. The scripts are organized with proper cell separators (`# %%`) for easy conversion to Jupyter notebooks.

## Files

- `01_variant_calling_pipeline.py` - Complete GATK Best Practices implementation
- `02_bisulfite_conversion_efficiency.py` - Comprehensive bisulfite analysis pipeline

## Converting to Jupyter Notebooks

These Python scripts can be easily converted to Jupyter notebooks:

### Option 1: Using VSCode
1. Open the `.py` files in VSCode with Python extension
2. Click "Convert to Jupyter Notebook" or use Ctrl+Shift+P → "Jupyter: Export to HTML/PDF"

### Option 2: Using jupytext
```bash
pip install jupytext
jupytext --to notebook *.py
```

### Option 3: Using nbconvert
```bash
jupyter nbconvert --to notebook --execute *.py
```

## Features

Both scripts include:
- ✅ Proper imports from `src/` utility functions  
- ✅ Comprehensive tech test content integration
- ✅ Performance analysis and visualization
- ✅ Real data integration (GIAB benchmark data)
- ✅ Senior-level technical challenge solutions
- ✅ Production-ready implementations

## Content Integration

All content from the previous standalone `.md` files has been properly integrated:
- GATK Best Practices pipeline with optimization strategies
- Bisulfite conversion efficiency with experimental design
- Technical challenges and mitigation strategies
- Quality control frameworks and validation metrics
