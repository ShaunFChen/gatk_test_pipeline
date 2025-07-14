"""Real data analysis utilities for GATK pipeline."""

import logging
from typing import Any, TypedDict

from src.variant_calling_utils import (
    analyze_giab_ground_truth,
    analyze_reference_genome,
    validate_variant_calling_accuracy,
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class AnalysisResults(TypedDict):
    """Type definition for analysis results."""

    reference: dict[str, Any]
    giab: dict[str, Any]
    validation: dict[str, Any]


def analyze_real_data() -> AnalysisResults:
    """Analyze real data from GIAB and validate pipeline accuracy."""
    results: AnalysisResults = {
        "reference": {},
        "giab": {},
        "validation": {},
    }

    # Analyze reference genome
    logger.info("\n1. Reference Genome Analysis:")
    ref_analysis = analyze_reference_genome()
    results["reference"] = ref_analysis

    # Analyze GIAB ground truth
    logger.info("\n2. GIAB Ground Truth Analysis:")
    giab_analysis = analyze_giab_ground_truth()
    results["giab"] = giab_analysis

    # Validate pipeline accuracy
    logger.info("\n3. Pipeline Validation:")
    validation = validate_variant_calling_accuracy(
        called_vcf_path="../data/sample_variants.vcf",
        truth_vcf_path="../data/giab/HG001_chr22_benchmark.vcf.gz",
    )
    results["validation"] = validation

    return results


if __name__ == "__main__":
    results = analyze_real_data()
    logger.info("\nAnalysis Results:")
    for key, value in results.items():
        logger.info("\n%s:", key.upper())
        for k, v in value.items():
            logger.info("  %s: %s", k, v)
