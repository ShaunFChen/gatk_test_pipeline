# Sample Data for GATK Test Pipeline

This directory contains sample genomic data files generated for demonstrating bioinformatics workflows in the notebooks.

## Files Overview

### Generated Data Files
- **`chr22_sample.fa`** - Sample reference genome (45,000 bp)
  - Simulated chromosome 22 subset with realistic GC content
  - Includes CpG islands and varying sequence composition
  - FASTA format compatible with standard bioinformatics tools

- **`sample_variants.vcf`** - Sample variant calls (150 variants)
  - SNPs, insertions, and deletions
  - Realistic quality scores and depth information
  - VCF 4.2 format with proper headers

- **`bisulfite_sample.fastq`** - Bisulfite sequencing reads (2,000 reads)
  - Simulated bisulfite-converted DNA sequences
  - 100bp read length with quality scores
  - Realistic conversion efficiency and methylation patterns

- **`sample_alignment_stats.txt`** - Alignment statistics
  - Coverage information across genomic positions
  - Simulated BAM file statistics
  - Used for quality control demonstrations

- **`sample_sheet.csv`** - Sample metadata
  - Sample names, batch information, and processing parameters
  - Used for batch processing demonstrations

## Data Generation

The sample data is generated using:
```bash
uv run python scripts/generate_sample_data.py
```

This creates realistic but small datasets suitable for:
- Educational purposes
- Testing bioinformatics workflows
- Interview demonstrations
- Method validation

## Usage in Notebooks

The data files are automatically loaded by the notebooks:

### Variant Calling Pipeline (`01_variant_calling_pipeline.ipynb`)
- Loads and analyzes VCF files
- Calculates variant quality metrics
- Demonstrates Ti/Tv ratio calculations
- Shows coverage analysis

### Bisulfite Conversion Analysis (`02_bisulfite_conversion_efficiency.ipynb`)
- Processes FASTQ reads
- Calculates conversion efficiency
- Performs quality control analysis
- Compares with simulated data

## Data Characteristics

### Reference Genome
- Length: 45,000 bp
- GC content: ~42%
- Contains CpG islands every 5kb
- Realistic sequence composition

### Variants
- 150 total variants (3.3 per kb)
- ~63% SNPs, ~37% indels
- Quality scores: 30-60
- Coverage: 10-100x

### Bisulfite Reads
- 2,000 reads at 100bp each
- ~98% conversion efficiency
- Realistic methylation patterns
- CpG, CHG, CHH contexts included

## File Formats

All files use standard bioinformatics formats:
- **FASTA**: Reference sequences
- **VCF**: Variant call format
- **FASTQ**: Sequencing reads with quality scores
- **CSV**: Sample metadata
- **TXT**: Analysis results and statistics

## Git Configuration

These data files are ignored by git (see `.gitignore`) to avoid committing large binary files to the repository. The data is regenerated as needed using the generation script.

## Production Notes

In production environments, you would replace these sample files with:
- Real reference genomes (e.g., GRCh38/hg38)
- Actual VCF files from variant calling pipelines
- Real bisulfite sequencing data
- Proper sample metadata and batch information

The analysis workflows demonstrated with this sample data scale directly to production datasets. 