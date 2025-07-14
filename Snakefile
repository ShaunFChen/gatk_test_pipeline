# Snakemake Workflow for GATK Test Pipeline Monitoring and Benchmarking
# This workflow demonstrates pipeline monitoring, performance tracking, and parallelization

import os
from pathlib import Path

# Configuration
configfile: "workflow_config.yaml"

# Define output directories
OUTPUT_DIR = Path("output")
BENCHMARK_DIR = Path("benchmarks")
LOG_DIR = Path("logs")

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
BENCHMARK_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Rule to run all analyses
rule all:
    input:
        "output/variant_calling_complete.txt",
        "output/bisulfite_analysis_complete.txt",
        "output/pipeline_performance_report.html",
        "benchmarks/variant_calling.txt",
        "benchmarks/bisulfite_analysis.txt"

# Rule for variant calling pipeline with benchmarking
rule variant_calling_pipeline:
    output:
        complete="output/variant_calling_complete.txt",
        metrics="output/variant_calling_metrics.json"
    benchmark:
        "benchmarks/variant_calling.txt"
    log:
        "logs/variant_calling.log"
    threads: config.get("threads", 4)
    resources:
        mem_mb=config.get("memory_mb", 8000),
        runtime=config.get("runtime_minutes", 30)
    shell:
        """
        echo "Starting variant calling pipeline..." > {log}
        .venv/bin/python notebooks/01_variant_calling_pipeline.py >> {log} 2>&1
        
        # Generate completion marker with timestamp
        echo "Variant calling completed at $(date)" > {output.complete}
        
        # Extract performance metrics (if they exist)
        if [ -f "output/performance_metrics.json" ]; then
            cp output/performance_metrics.json {output.metrics}
        else
            echo '{{"status": "completed", "timestamp": "'$(date)'"}}' > {output.metrics}
        fi
        """

# Rule for bisulfite conversion analysis with benchmarking  
rule bisulfite_analysis:
    output:
        complete="output/bisulfite_analysis_complete.txt",
        metrics="output/bisulfite_metrics.json"
    benchmark:
        "benchmarks/bisulfite_analysis.txt"
    log:
        "logs/bisulfite_analysis.log"
    threads: config.get("threads", 2)
    resources:
        mem_mb=config.get("memory_mb", 4000),
        runtime=config.get("runtime_minutes", 15)
    shell:
        """
        echo "Starting bisulfite conversion analysis..." > {log}
        .venv/bin/python notebooks/02_bisulfite_conversion_efficiency.py >> {log} 2>&1
        
        # Generate completion marker with timestamp
        echo "Bisulfite analysis completed at $(date)" > {output.complete}
        
        # Extract performance metrics (if they exist)
        if [ -f "output/bisulfite_performance.json" ]; then
            cp output/bisulfite_performance.json {output.metrics}
        else
            echo '{{"status": "completed", "timestamp": "'$(date)'"}}' > {output.metrics}
        fi
        """

# Rule to generate comprehensive performance report
rule performance_report:
    input:
        variant_complete="output/variant_calling_complete.txt",
        bisulfite_complete="output/bisulfite_analysis_complete.txt",
        variant_benchmark="benchmarks/variant_calling.txt",
        bisulfite_benchmark="benchmarks/bisulfite_analysis.txt"
    output:
        "output/pipeline_performance_report.html"
    log:
        "logs/performance_report.log"
    shell:
        """
        .venv/bin/python scripts/generate_performance_report.py \
            --variant-benchmark {input.variant_benchmark} \
            --bisulfite-benchmark {input.bisulfite_benchmark} \
            --output {output} \
            --log {log}
        """

# Rule for parallel execution of both pipelines
rule run_parallel:
    input:
        "output/variant_calling_complete.txt",
        "output/bisulfite_analysis_complete.txt"
    output:
        "output/parallel_execution_complete.txt"
    shell:
        """
        echo "Both pipelines completed in parallel at $(date)" > {output}
        """

# Rule for resource monitoring
rule monitor_resources:
    output:
        "output/resource_usage.txt"
    shell:
        """
        echo "=== System Resource Usage ===" > {output}
        echo "Date: $(date)" >> {output}
        echo "CPU Info:" >> {output}
        sysctl -n machdep.cpu.brand_string >> {output} 2>/dev/null || echo "CPU info not available" >> {output}
        echo "Memory Info:" >> {output}
        system_profiler SPHardwareDataType | grep "Memory:" >> {output} 2>/dev/null || echo "Memory info not available" >> {output}
        echo "Available CPU cores: $(sysctl -n hw.ncpu)" >> {output} 2>/dev/null || echo "CPU core info not available" >> {output}
        """

# Rule to clean previous outputs
rule clean:
    shell:
        """
        rm -rf output/* benchmarks/* logs/*
        echo "Cleaned all output directories"
        """ 