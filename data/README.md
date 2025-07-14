# Sample Data for GATK Test Pipeline

This directory contains sample genomic data files generated for demonstrating bioinformatics workflows in the notebooks.

## Files Overview

### Generated Data Files
- **`chr22_sample.fa`** - Sample reference genome
  - Simulated chromosome 22 subset with realistic GC content
  - Includes CpG islands and varying sequence composition
  - FASTA format compatible with standard bioinformatics tools

- **`bisulfite_sample.fastq`** - Bisulfite sequencing reads
  - Simulated bisulfite-converted DNA sequences
  - Realistic read length with quality scores
  - Realistic conversion efficiency and methylation patterns

### Data Subdirectories
- **`alignments/`** - BAM/SAM alignment files and indices
- **`giab/`** - GIAB (Genome in a Bottle) benchmark data
- **`reference/`** - Reference genome files and indices

### Metadata Files
- **`DATA_MANIFEST.md`** - Detailed inventory of all data files
- **`README.md`** - This documentation file

## Data Generation

The sample data is generated using:
```bash
uv run python scripts/generate_sample_data.py
```

This creates realistic but appropriately-sized datasets suitable for:
- Educational purposes
- Testing bioinformatics workflows
- Interview demonstrations
- Method validation

## Usage in Notebooks

The data files are automatically loaded by the notebooks:

### Variant Calling Pipeline (`01_variant_calling_pipeline.py`)
- Loads and analyzes reference sequences
- Demonstrates alignment and variant calling workflows
- Calculates variant quality metrics
- Shows coverage analysis and validation

### Bisulfite Conversion Analysis (`02_bisulfite_conversion_efficiency.py`)
- Processes FASTQ reads for bisulfite analysis
- Calculates conversion efficiency metrics
- Performs quality control analysis
- Compares with simulated data

## Data Characteristics

The generated data includes realistic characteristics:

### Reference Genome
- Chromosome 22 subset with appropriate length
- Realistic GC content (~42%)
- Contains CpG islands at appropriate intervals
- Standard FASTA format

### Bisulfite Reads
- Quality reads with appropriate length
- High conversion efficiency (>95%)
- Realistic methylation patterns
- CpG, CHG, CHH contexts included
- Standard FASTQ format with quality scores

### Alignment Data
- BAM/SAM files with proper headers
- Realistic alignment statistics
- Index files for efficient access

## File Formats

All files use standard bioinformatics formats:
- **FASTA**: Reference sequences
- **FASTQ**: Sequencing reads with quality scores
- **BAM/SAM**: Binary/text alignment format
- **VCF**: Variant call format
- **Markdown**: Documentation and manifests

## Git Configuration

Large data files are managed according to the project's `.gitignore` configuration. Sample data files are regenerated as needed using the generation scripts to maintain repository efficiency.

## Production Notes

In production environments, you would replace these sample files with:
- Real reference genomes (e.g., GRCh38/hg38)
- Actual sequencing data from your experiments
- Real alignment and variant calling results
- Proper sample metadata and batch information

The analysis workflows demonstrated with this sample data scale directly to production datasets with real genomic data. 