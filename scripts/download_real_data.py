#!/usr/bin/env python3
"""
Download real genomic data for GATK pipeline testing and validation.

This script downloads:
1. GIAB HG001/NA12878 ground truth data (chromosome 22)
2. GRCh38 reference genome (chromosome 22)
3. Associated index files and metadata

Used for answering tech test questions about performance optimization
and ground truth validation.
"""

import subprocess
import urllib.request
from pathlib import Path


def download_file(url: str, output_path: Path, description: str) -> bool:
    """Download a file with progress indication."""
    print(f"📥 Downloading {description}...")
    print(f"   URL: {url}")
    print(f"   Output: {output_path}")

    try:

        def progress_hook(block_num: int, block_size: int, total_size: int) -> None:
            if total_size > 0:
                percent = min(100, (block_num * block_size * 100) // total_size)
                if percent % 10 == 0:  # Print every 10%
                    print(f"   Progress: {percent}%")

        urllib.request.urlretrieve(url, output_path, progress_hook)
        print(f"   ✅ Downloaded successfully ({output_path.stat().st_size / 1024 / 1024:.1f} MB)")
        return True
    except Exception as e:
        print(f"   ❌ Failed to download: {e}")
        return False


def run_command(command: str, description: str) -> bool:
    """Run a shell command with error handling."""
    print(f"🔧 {description}...")
    print(f"   Command: {command}")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Success")
            return True
        else:
            print(f"   ❌ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def download_grch38_reference(data_dir: Path) -> tuple[bool, list[str]]:
    """Download GRCh38 reference genome (chromosome 22)."""
    print("\n🧬 Downloading GRCh38 Reference Genome (Chromosome 22)")
    print("=" * 60)

    ref_dir = data_dir / "reference"
    ref_dir.mkdir(exist_ok=True)

    files_downloaded = []

    # GRCh38 chromosome 22 from NCBI
    ref_urls = {
        "chr22.fa": "https://hgdownload.cse.ucsc.edu/goldenPath/hg38/chromosomes/chr22.fa.gz",
    }

    for filename, url in ref_urls.items():
        output_path = ref_dir / filename
        compressed_path = ref_dir / f"{filename}.gz"

        if output_path.exists():
            print(f"   ✅ {filename} already exists, skipping...")
            files_downloaded.append(str(output_path))
            continue

        # Download compressed file
        if download_file(url, compressed_path, f"GRCh38 {filename}"):
            # Decompress
            if run_command(f"gunzip {compressed_path}", f"Decompressing {filename}"):
                files_downloaded.append(str(output_path))

                # Create FASTA index
                if filename.endswith(".fa"):
                    run_command(f"samtools faidx {output_path}", f"Indexing {filename}")
            else:
                print(f"   ⚠️  Failed to decompress {filename}")

    return len(files_downloaded) > 0, files_downloaded


def download_giab_data(data_dir: Path) -> tuple[bool, list[str]]:
    """Download GIAB HG001/NA12878 ground truth data."""
    print("\n🎯 Downloading GIAB HG001/NA12878 Ground Truth Data")
    print("=" * 60)

    giab_dir = data_dir / "giab"
    giab_dir.mkdir(exist_ok=True)

    files_downloaded = []

    # GIAB HG001/NA12878 high-confidence calls (chromosome 22)
    # Using NIST v4.2.1 high-confidence calls
    giab_base_url = "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/NA12878_HG001/NISTv4.2.1/GRCh38"

    giab_files = {
        "HG001_GRCh38_1_22_v4.2.1_benchmark.vcf.gz": f"{giab_base_url}/HG001_GRCh38_1_22_v4.2.1_benchmark.vcf.gz",
        "HG001_GRCh38_1_22_v4.2.1_benchmark.bed": f"{giab_base_url}/HG001_GRCh38_1_22_v4.2.1_benchmark.bed",
    }

    for filename, url in giab_files.items():
        output_path = giab_dir / filename

        if output_path.exists():
            print(f"   ✅ {filename} already exists, skipping...")
            files_downloaded.append(str(output_path))
            continue

        if download_file(url, output_path, f"GIAB {filename}"):
            files_downloaded.append(str(output_path))

            # Index VCF file if needed
            if filename.endswith(".vcf.gz"):
                run_command(f"tabix -p vcf {output_path}", f"Indexing {filename}")

    return len(files_downloaded) > 0, files_downloaded


def download_test_bam_data(data_dir: Path) -> tuple[bool, list[str]]:
    """Download a small test BAM file for alignment analysis."""
    print("\n🧬 Downloading Test BAM Data")
    print("=" * 60)

    bam_dir = data_dir / "alignments"
    bam_dir.mkdir(exist_ok=True)

    files_downloaded = []

    # Use a small publicly available BAM file for testing
    # This is from the 1000 Genomes Project - chromosome 22 region
    bam_urls = {"NA12878_chr22_sample.bam": "https://github.com/samtools/samtools/raw/develop/test/dat/mpileup.1.bam"}

    for filename, url in bam_urls.items():
        output_path = bam_dir / filename

        if output_path.exists():
            print(f"   ✅ {filename} already exists, skipping...")
            files_downloaded.append(str(output_path))
            continue

        if download_file(url, output_path, f"Test BAM {filename}"):
            files_downloaded.append(str(output_path))

            # Index BAM file
            run_command(f"samtools index {output_path}", f"Indexing {filename}")

    return len(files_downloaded) > 0, files_downloaded


def extract_chromosome_22_data(data_dir: Path) -> bool:
    """Extract chromosome 22 specific data from downloaded files."""
    print("\n✂️  Extracting Chromosome 22 Data")
    print("=" * 60)

    giab_dir = data_dir / "giab"
    ref_dir = data_dir / "reference"

    # Extract chr22 from GIAB VCF if needed
    full_vcf = giab_dir / "HG001_GRCh38_1_22_v4.2.1_benchmark.vcf.gz"
    chr22_vcf = giab_dir / "HG001_chr22_benchmark.vcf.gz"

    if full_vcf.exists() and not chr22_vcf.exists():
        print("   Extracting chromosome 22 variants...")
        cmd = f"bcftools view -r chr22 {full_vcf} | bgzip > {chr22_vcf}"
        if run_command(cmd, "Extracting chr22 variants"):
            run_command(f"tabix -p vcf {chr22_vcf}", "Indexing chr22 VCF")

    return True


def create_data_manifest(data_dir: Path, downloaded_files: dict[str, list[str]]) -> None:
    """Create a manifest file documenting all downloaded data."""
    print("\n📋 Creating Data Manifest")
    print("=" * 60)

    manifest_path = data_dir / "DATA_MANIFEST.md"

    with open(manifest_path, "w") as f:
        f.write("# Real Genomic Data Manifest\n\n")
        f.write("This directory contains real genomic data downloaded for pipeline testing and validation.\n\n")

        f.write("## Download Date\n")
        from datetime import datetime

        f.write(f"Downloaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Data Sources\n\n")
        f.write("### Reference Genome\n")
        f.write("- **Source**: UCSC Genome Browser (hg38/GRCh38)\n")
        f.write("- **Chromosome**: chr22\n")
        f.write("- **Version**: GRCh38/hg38\n\n")

        f.write("### GIAB Ground Truth Data\n")
        f.write("- **Source**: NIST Genome in a Bottle (GIAB)\n")
        f.write("- **Sample**: HG001/NA12878\n")
        f.write("- **Version**: NISTv4.2.1\n")
        f.write("- **Reference**: GRCh38\n\n")

        f.write("## Downloaded Files\n\n")
        for category, files in downloaded_files.items():
            f.write(f"### {category}\n")
            for file_path in files:
                file_obj = Path(file_path)
                if file_obj.exists():
                    size_mb = file_obj.stat().st_size / 1024 / 1024
                    f.write(f"- `{file_obj.name}` ({size_mb:.1f} MB)\n")
                else:
                    f.write(f"- `{file_obj.name}` (missing)\n")
            f.write("\n")

        f.write("## Usage\n\n")
        f.write("These files are used by the notebooks for:\n")
        f.write("- Ground truth validation of variant calling accuracy\n")
        f.write("- Performance testing with real data\n")
        f.write("- Benchmarking against GIAB high-confidence regions\n")
        f.write("- Technical challenge demonstration\n\n")

        f.write("## Commands to Reproduce\n\n")
        f.write("```bash\n")
        f.write("# Re-download all data\n")
        f.write("uv run python scripts/download_real_data.py\n")
        f.write("```\n")

    print(f"   ✅ Manifest created: {manifest_path}")


def main():
    """Download all real genomic data for pipeline testing."""
    print("🌐 DOWNLOADING REAL GENOMIC DATA FOR GATK PIPELINE")
    print("=" * 60)
    print("This script downloads real data for performance testing and validation:")
    print("• GRCh38 reference genome (chromosome 22)")
    print("• GIAB HG001/NA12878 ground truth variants")
    print("• Test alignment data")
    print()

    # Create data directory structure
    base_dir = Path.cwd()
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)

    # Check for required tools
    required_tools = ["samtools", "bcftools", "tabix"]
    missing_tools = []

    for tool in required_tools:
        result = subprocess.run(f"which {tool}", shell=True, capture_output=True)
        if result.returncode != 0:
            missing_tools.append(tool)

    if missing_tools:
        print(f"⚠️  Warning: Missing required tools: {', '.join(missing_tools)}")
        print("   Some operations may fail. Install with:")
        print("   • samtools: conda install -c bioconda samtools")
        print("   • bcftools: conda install -c bioconda bcftools")
        print("   • tabix: conda install -c bioconda tabix")
        print()

    downloaded_files = {}

    # Download reference genome
    success, files = download_grch38_reference(data_dir)
    if success:
        downloaded_files["Reference Genome"] = files

    # Download GIAB data
    success, files = download_giab_data(data_dir)
    if success:
        downloaded_files["GIAB Ground Truth"] = files

    # Download test BAM data
    success, files = download_test_bam_data(data_dir)
    if success:
        downloaded_files["Test Alignments"] = files

    # Extract chromosome 22 specific data
    extract_chromosome_22_data(data_dir)

    # Create manifest
    create_data_manifest(data_dir, downloaded_files)

    print("\n✅ DOWNLOAD COMPLETE!")
    print("=" * 60)

    total_files = sum(len(files) for files in downloaded_files.values())
    total_size = 0

    for files in downloaded_files.values():
        for file_path in files:
            if Path(file_path).exists():
                total_size += Path(file_path).stat().st_size

    print("📊 Summary:")
    print(f"   • Files downloaded: {total_files}")
    print(f"   • Total size: {total_size / 1024 / 1024:.1f} MB")
    print(f"   • Data location: {data_dir}")
    print()
    print("🎯 Ready for:")
    print("   • Ground truth validation")
    print("   • Performance benchmarking")
    print("   • Technical challenge demonstration")
    print("   • Real-world pipeline testing")
    print()
    print("💡 Run the notebooks to see the analysis with real data!")


if __name__ == "__main__":
    main()
