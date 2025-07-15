#!/usr/bin/env python3
"""
Generate sample data for GATK and bisulfite analysis notebooks.
Creates realistic but small datasets for demonstration purposes.
"""

import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import bisulfite_utils as bu


def create_sample_reference(output_path: str, length: int = 50000) -> str:
    """Create a sample reference genome sequence."""
    print(f"Creating reference sequence ({length:,} bp)...")

    # Create a more realistic sequence with some structure
    sequence = ""

    # Add some CpG islands (higher GC content)
    for i in range(0, length, 1000):
        if i % 5000 == 0:  # Every 5kb, add a CpG island
            # CpG island: higher GC content, more CpG dinucleotides
            island_length = min(500, length - i)
            island_seq = ""
            for _ in range(island_length):
                if random.random() < 0.6:  # 60% GC content
                    if random.random() < 0.5:
                        island_seq += "C"
                    else:
                        island_seq += "G"
                else:
                    if random.random() < 0.5:
                        island_seq += "A"
                    else:
                        island_seq += "T"
            sequence += island_seq
        else:
            # Regular sequence: ~40% GC content
            chunk_length = min(1000, length - len(sequence))
            chunk_seq = ""
            for _ in range(chunk_length):
                rand = random.random()
                if rand < 0.2:
                    chunk_seq += "C"
                elif rand < 0.4:
                    chunk_seq += "G"
                elif rand < 0.7:
                    chunk_seq += "A"
                else:
                    chunk_seq += "T"
            sequence += chunk_seq

        if len(sequence) >= length:
            break

    sequence = sequence[:length]

    # Write FASTA file
    with open(output_path, "w") as f:
        f.write(">chr22_sample\n")
        # Write sequence in 80-character lines
        for i in range(0, len(sequence), 80):
            f.write(sequence[i : i + 80] + "\n")

    print(f"Reference written to {output_path}")
    return sequence


def create_sample_variants(reference_seq: str, output_path: str, num_variants: int = 100) -> pd.DataFrame:
    """Create sample variants in VCF format."""
    print(f"Creating {num_variants} sample variants...")

    variants = []
    used_positions = set()

    for i in range(num_variants):
        # Random position
        pos = random.randint(1, len(reference_seq) - 10)
        while pos in used_positions:
            pos = random.randint(1, len(reference_seq) - 10)
        used_positions.add(pos)

        ref_base = reference_seq[pos - 1]  # 0-based indexing

        # Create different types of variants
        variant_type = random.choice(["SNP", "SNP", "SNP", "INS", "DEL"])  # Mostly SNPs

        if variant_type == "SNP":
            # Single nucleotide polymorphism
            alt_base = random.choice([b for b in "ATCG" if b != ref_base])
            ref_allele = ref_base
            alt_allele = alt_base
        elif variant_type == "INS":
            # Insertion
            insert_seq = "".join(random.choices("ATCG", k=random.randint(1, 5)))
            ref_allele = ref_base
            alt_allele = ref_base + insert_seq
        else:  # DEL
            # Deletion
            del_len = random.randint(1, 3)
            ref_allele = reference_seq[pos - 1 : pos - 1 + del_len + 1]
            alt_allele = reference_seq[pos - 1]

        # Generate realistic quality scores and info
        qual = random.randint(30, 60)
        depth = random.randint(10, 100)

        variants.append(
            {
                "CHROM": "chr22_sample",
                "POS": pos,
                "ID": f"variant_{i:03d}",
                "REF": ref_allele,
                "ALT": alt_allele,
                "QUAL": qual,
                "FILTER": "PASS",
                "INFO": f"DP={depth}",
                "FORMAT": "GT:DP",
                "SAMPLE": f"0/1:{depth}",
            }
        )

    # Sort by position
    variants.sort(key=lambda x: x["POS"])

    # Write VCF file
    with open(output_path, "w") as f:
        # VCF header
        f.write("##fileformat=VCFv4.2\n")
        f.write("##contig=<ID=chr22_sample>\n")
        f.write('##INFO=<ID=DP,Number=1,Type=Integer,Description="Total read depth">\n')
        f.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
        f.write('##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">\n')
        f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n")

        # Write variants
        for var in variants:
            f.write(
                f"{var['CHROM']}\t{var['POS']}\t{var['ID']}\t{var['REF']}\t{var['ALT']}\t"
                f"{var['QUAL']}\t{var['FILTER']}\t{var['INFO']}\t{var['FORMAT']}\t{var['SAMPLE']}\n"
            )

    print(f"VCF written to {output_path}")
    return pd.DataFrame(variants)


def create_bisulfite_reads(reference_seq: str, output_path: str, num_reads: int = 1000) -> list[str]:
    """Create realistic bisulfite sequencing reads."""
    print(f"Creating {num_reads} bisulfite sequencing reads...")

    # Use the bisulfite simulator
    simulator = bu.BisulfiteSimulator(conversion_efficiency=0.98, read_length=100)

    # Generate methylation pattern
    methylation_pattern = simulator.simulate_methylation_pattern(
        reference_seq,
        cpg_methylation_rate=0.70,
        chg_methylation_rate=0.05,
        chh_methylation_rate=0.02,
    )

    # Apply bisulfite conversion
    converted_seq = simulator.apply_bisulfite_conversion(reference_seq, methylation_pattern)

    # Generate reads
    reads = []
    for i in range(num_reads):
        # Random start position
        start = random.randint(0, len(converted_seq) - 100)
        read_seq = converted_seq[start : start + 100]

        # Add some sequencing errors
        error_read = simulator.add_sequencing_errors(read_seq, 0.001)

        # Create FASTQ format
        read_id = f"read_{i:04d}"
        quality = "I" * len(error_read)  # High quality scores

        reads.append(f"@{read_id}\n{error_read}\n+\n{quality}")

    # Write FASTQ file
    with open(output_path, "w") as f:
        f.write("\n".join(reads))

    print(f"Bisulfite reads written to {output_path}")
    return reads


def create_sample_bam_info(reference_seq: str, variants_df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    """Create sample BAM file information (simulated alignment stats)."""
    print("Creating sample BAM alignment statistics...")

    # Simulate alignment statistics
    total_reads = 10000
    aligned_reads = int(total_reads * 0.95)  # 95% alignment rate

    # Create coverage simulation
    coverage_data = []
    for i in range(0, len(reference_seq), 100):  # Every 100 bp
        pos = i + 1
        # Higher coverage around variant sites
        base_coverage = random.randint(20, 40)

        # Increase coverage near variants
        for _, variant in variants_df.iterrows():
            if abs(pos - variant["POS"]) < 200:  # Within 200bp of variant
                base_coverage += random.randint(5, 15)

        coverage_data.append(
            {
                "position": pos,
                "coverage": min(base_coverage, 100),  # Cap at 100x
            }
        )

    coverage_df = pd.DataFrame(coverage_data)

    # Create alignment stats
    alignment_stats = {
        "total_reads": total_reads,
        "aligned_reads": aligned_reads,
        "alignment_rate": aligned_reads / total_reads,
        "duplicate_rate": 0.05,
        "insert_size_mean": 350,
        "insert_size_std": 50,
        "mean_coverage": coverage_df["coverage"].mean(),
        "coverage_std": coverage_df["coverage"].std(),
    }

    # Save as JSON-like info
    with open(output_path, "w") as f:
        f.write("# Sample BAM Statistics\n")
        f.write(f"# Total reads: {alignment_stats['total_reads']:,}\n")
        f.write(f"# Aligned reads: {alignment_stats['aligned_reads']:,}\n")
        f.write(f"# Alignment rate: {alignment_stats['alignment_rate']:.3f}\n")
        f.write(f"# Duplicate rate: {alignment_stats['duplicate_rate']:.3f}\n")
        f.write(f"# Mean coverage: {alignment_stats['mean_coverage']:.1f}x\n")
        f.write("# Coverage by position:\n")
        f.write("position\tcoverage\n")
        for _, row in coverage_df.iterrows():
            f.write(f"{row['position']}\t{row['coverage']}\n")

    print(f"BAM statistics written to {output_path}")
    return coverage_df


def create_sample_bam_file(reference_seq: str, output_path: str, num_reads: int = 100) -> None:
    """Create a sample BAM file with properly formatted read names.

    Args:
        reference_seq: Reference sequence to align reads to
        output_path: Path for output BAM file
        num_reads: Number of read pairs to generate
    """
    print(f"Creating sample BAM file with {num_reads} read pairs...")

    import pysam

    # Create BAM header with proper format
    header = {
        "HD": {"VN": "1.6", "SO": "coordinate"},
        "SQ": [{"SN": "chr22_sample", "LN": len(reference_seq)}],
        "RG": [{"ID": "sample_rg", "SM": "NA12878", "LB": "lib1", "PL": "ILLUMINA", "PU": "unit1"}],
    }

    # Create properly formatted BAM file
    with pysam.AlignmentFile(output_path, "wb", header=header) as outfile:
        for i in range(num_reads):
            # Standard Illumina read name format: INSTRUMENT:RUN:FLOWCELL:LANE:TILE:X:Y
            read_name = f"SIMULATOR:1:FC123:1:1101:{1000 + i}:{2000 + i}"

            # Random position ensuring reads fit in reference
            start_pos = random.randint(0, len(reference_seq) - 150)
            read_length = 75

            # Read 1 (forward)
            read1 = pysam.AlignedSegment()
            read1.query_name = read_name
            read1.query_sequence = reference_seq[start_pos : start_pos + read_length]
            read1.flag = 99  # Properly paired, read1, mate reverse
            read1.reference_id = 0  # chr22_sample
            read1.reference_start = start_pos
            read1.mapping_quality = 60
            read1.cigartuples = [(0, read_length)]  # Perfect match (0=M)
            read1.next_reference_id = 0
            read1.next_reference_start = start_pos + 75  # Mate position
            read1.template_length = 150
            import array

            read1.query_qualities = array.array("B", [30] * read_length)  # High quality
            read1.set_tag("RG", "sample_rg")
            outfile.write(read1)

            # Read 2 (reverse)
            read2 = pysam.AlignedSegment()
            read2.query_name = read_name
            read2.query_sequence = reference_seq[start_pos + 75 : start_pos + 150]
            read2.flag = 147  # Properly paired, read2, reverse
            read2.reference_id = 0
            read2.reference_start = start_pos + 75
            read2.mapping_quality = 60
            read2.cigartuples = [(0, read_length)]
            read2.next_reference_id = 0
            read2.next_reference_start = start_pos
            read2.template_length = -150
            read2.query_qualities = array.array("B", [30] * read_length)
            read2.set_tag("RG", "sample_rg")
            outfile.write(read2)

    print(f"BAM file written to {output_path}")

    # Create BAM index
    try:
        pysam.index(output_path)
        print(f"BAM index created: {output_path}.bai")
    except Exception as e:
        print(f"Warning: Could not create BAM index: {e}")


def main():
    """Generate all sample data files."""
    print("🧬 Generating sample data for GATK and bisulfite analysis...")

    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Generate reference sequence
    reference_path = data_dir / "chr22_sample.fa"
    reference_seq = create_sample_reference(str(reference_path), length=50000)

    # Generate sample variants
    variants_path = data_dir / "sample_variants.vcf"
    variants_df = create_sample_variants(reference_seq, str(variants_path), num_variants=150)

    # Generate BAM alignment info
    bam_stats_path = data_dir / "sample_alignment_stats.txt"
    coverage_df = create_sample_bam_info(reference_seq, variants_df, str(bam_stats_path))

    # Generate bisulfite reads
    bisulfite_reads_path = data_dir / "bisulfite_sample.fastq"
    reads = create_bisulfite_reads(reference_seq, str(bisulfite_reads_path), num_reads=2000)

    # Create properly formatted BAM file with alignment data
    alignments_dir = data_dir / "alignments"
    alignments_dir.mkdir(exist_ok=True)
    bam_path = alignments_dir / "NA12878_chr22_sample_fixed.bam"
    create_sample_bam_file(reference_seq, str(bam_path), num_reads=50)

    # Create a sample sheet
    sample_sheet = pd.DataFrame(
        {
            "sample_name": ["sample_001", "sample_002", "sample_003"],
            "reference": ["chr22_sample.fa"] * 3,
            "variants": ["sample_variants.vcf"] * 3,
            "batch": ["batch_1", "batch_1", "batch_2"],
            "coverage_target": [30, 30, 40],
        }
    )

    sample_sheet_path = data_dir / "sample_sheet.csv"
    sample_sheet.to_csv(sample_sheet_path, index=False)

    print("\n✅ Sample data generation complete!")
    print(f"📁 Files created in {data_dir}:")
    print(f"   • {reference_path.name} - Reference genome ({len(reference_seq):,} bp)")
    print(f"   • {variants_path.name} - Sample variants ({len(variants_df)} variants)")
    print(f"   • {bam_stats_path.name} - Alignment statistics")
    print(f"   • {bisulfite_reads_path.name} - Bisulfite reads ({len(reads)} reads)")
    print(f"   • {bam_path.name} - Properly formatted BAM file (50 read pairs)")
    print(f"   • {sample_sheet_path.name} - Sample sheet")

    print("\n📊 Dataset Summary:")
    print(f"   • Reference length: {len(reference_seq):,} bp")
    print(f"   • Variants: {len(variants_df)} ({len(variants_df) / len(reference_seq) * 1000:.1f} per kb)")
    print(f"   • Mean coverage: {coverage_df['coverage'].mean():.1f}x")
    print(f"   • Bisulfite reads: {len(reads)}")
    print(f"   • GC content: {(reference_seq.count('G') + reference_seq.count('C')) / len(reference_seq):.1%}")

    # Calculate some quick stats
    snp_count = sum(1 for _, var in variants_df.iterrows() if len(var["REF"]) == 1 and len(var["ALT"]) == 1)
    indel_count = len(variants_df) - snp_count

    print(f"   • SNPs: {snp_count}, Indels: {indel_count}")
    print(f"   • Ti/Tv ratio: {calculate_ti_tv_ratio(variants_df):.2f}")

    print("\n💡 Ready to use in notebooks!")


def calculate_ti_tv_ratio(variants_df: pd.DataFrame) -> float:
    """Calculate Ti/Tv ratio for SNPs."""
    transitions = 0
    transversions = 0

    for _, var in variants_df.iterrows():
        if len(var["REF"]) == 1 and len(var["ALT"]) == 1:
            ref, alt = var["REF"], var["ALT"]
            if (
                (ref == "A" and alt == "G")
                or (ref == "G" and alt == "A")
                or (ref == "C" and alt == "T")
                or (ref == "T" and alt == "C")
            ):
                transitions += 1
            else:
                transversions += 1

    return transitions / transversions if transversions > 0 else 0.0


if __name__ == "__main__":
    main()
