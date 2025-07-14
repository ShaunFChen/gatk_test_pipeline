"""Unit tests for variant calling utilities."""

import sys
import tempfile
import time
from pathlib import Path

import pandas as pd

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from variant_calling_utils import (
    GATKCommandBuilder,
    PerformanceMonitor,
    ValidationMetrics,
    check_dependencies,
    create_sample_sheet,
)


class TestGATKCommandBuilder:
    """Test GATK command building functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.builder = GATKCommandBuilder(java_mem="4g", threads=2)

    def test_mark_duplicates_command(self) -> None:
        """Test MarkDuplicates command generation."""
        command = self.builder.build_mark_duplicates("test.bam", "test.dedup.bam", "test.metrics")

        assert "MarkDuplicates" in command
        assert "-I test.bam" in command
        assert "-O test.dedup.bam" in command
        assert "-M test.metrics" in command
        assert "-Xmx4g" in command

    def test_base_recalibrator_command(self) -> None:
        """Test BaseRecalibrator command generation."""
        command = self.builder.build_base_recalibrator(
            input_bam="test.bam",
            reference="ref.fasta",
            known_sites=["dbsnp.vcf"],
            output_table="recal.table",
        )

        assert "BaseRecalibrator" in command
        assert "-I test.bam" in command
        assert "-R ref.fasta" in command
        assert "--known-sites dbsnp.vcf" in command
        assert "-O recal.table" in command

    def test_haplotype_caller_command(self) -> None:
        """Test HaplotypeCaller command generation."""
        command = self.builder.build_haplotype_caller(
            input_bam="test.bam",
            reference="ref.fasta",
            output_gvcf="test.g.vcf.gz",
            sample_name="sample1",
        )

        assert "HaplotypeCaller" in command
        assert "-I test.bam" in command
        assert "-R ref.fasta" in command
        assert "-O test.g.vcf.gz" in command
        assert "--sample-name sample1" in command
        assert "-ERC GVCF" in command
        assert "--native-pair-hmm-threads 2" in command

    def test_genotype_gvcfs_command(self) -> None:
        """Test GenotypeGVCFs command generation."""
        gvcf_files = ["sample1.g.vcf.gz", "sample2.g.vcf.gz"]
        command = self.builder.build_genotype_gvcfs(
            reference="ref.fasta",
            gvcf_files=gvcf_files,
            output_vcf="cohort.vcf.gz",
        )

        assert "GenotypeGVCFs" in command
        assert "-R ref.fasta" in command
        assert "-V sample1.g.vcf.gz" in command
        assert "-V sample2.g.vcf.gz" in command
        assert "-O cohort.vcf.gz" in command


class TestPerformanceMonitor:
    """Test performance monitoring functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.monitor = PerformanceMonitor()

    def test_step_timing(self) -> None:
        """Test step timing functionality."""
        # Start and end a step
        self.monitor.start_step("test_step")
        time.sleep(0.1)  # Small delay
        self.monitor.end_step("test_step")

        # Check that timing was recorded
        summary = self.monitor.get_performance_summary()
        assert "test_step" in summary
        assert summary["test_step"] > 0.05  # Should be > 0.05 seconds

    def test_multiple_steps(self) -> None:
        """Test monitoring multiple steps."""
        steps = ["step1", "step2", "step3"]

        # Time multiple steps
        for step in steps:
            self.monitor.start_step(step)
            time.sleep(0.05)  # Small delay
            self.monitor.end_step(step)

        # Check all steps were recorded
        summary = self.monitor.get_performance_summary()
        for step in steps:
            assert step in summary
            assert summary[step] > 0


class TestValidationMetrics:
    """Test validation metrics functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.validator = ValidationMetrics()

    def test_ti_tv_ratio(self) -> None:
        """Test Ti/Tv ratio calculation."""
        # This is a placeholder test since actual implementation would parse VCF
        ratio = self.validator.calculate_ti_tv_ratio("dummy.vcf")
        assert isinstance(ratio, float)
        assert ratio > 0

    def test_sensitivity_precision(self) -> None:
        """Test sensitivity and precision calculation."""
        # This is a placeholder test since actual implementation would parse VCFs
        metrics = self.validator.calculate_sensitivity_precision("truth.vcf", "called.vcf")

        assert "sensitivity" in metrics
        assert "precision" in metrics
        assert "f1_score" in metrics

        # Check values are reasonable
        assert 0 <= metrics["sensitivity"] <= 1
        assert 0 <= metrics["precision"] <= 1
        assert 0 <= metrics["f1_score"] <= 1

    def test_dbsnp_overlap(self) -> None:
        """Test dbSNP overlap calculation."""
        # This is a placeholder test since actual implementation would parse VCFs
        overlap = self.validator.calculate_dbsnp_overlap("variants.vcf", "dbsnp.vcf")
        assert isinstance(overlap, float)
        assert 0 <= overlap <= 1


class TestUtilityFunctions:
    """Test utility functions."""

    def test_check_dependencies(self) -> None:
        """Test dependency checking."""
        status = check_dependencies()

        assert isinstance(status, dict)

        # Check that expected tools are in the status
        expected_tools = ["gatk", "bwa", "samtools", "bcftools", "fastqc"]
        for tool in expected_tools:
            assert tool in status
            assert isinstance(status[tool], bool)

    def test_create_sample_sheet(self) -> None:
        """Test sample sheet creation."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_file = Path(tmp_dir) / "samples.csv"
            samples = ["sample1", "sample2", "sample3"]

            # Create sample sheet
            df = create_sample_sheet(samples, str(output_file))

            # Check that file was created
            assert output_file.exists()

            # Check DataFrame structure
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 3
            assert "sample_name" in df.columns
            assert "fastq_r1" in df.columns
            assert "fastq_r2" in df.columns
            assert "bam_file" in df.columns
            assert "gvcf_file" in df.columns

            # Check sample names
            assert list(df["sample_name"]) == samples


class TestIntegration:
    """Integration tests for the pipeline."""

    def test_pipeline_workflow(self) -> None:
        """Test basic pipeline workflow integration."""
        # Test that all components work together
        builder = GATKCommandBuilder()
        monitor = PerformanceMonitor()

        # Mock a pipeline step
        monitor.start_step("test_integration")

        # Generate a command
        command = builder.build_mark_duplicates("input.bam", "output.bam", "metrics.txt")

        # Validate command was generated
        assert "MarkDuplicates" in command

        monitor.end_step("test_integration")

        # Check timing was recorded
        summary = monitor.get_performance_summary()
        assert "test_integration" in summary
