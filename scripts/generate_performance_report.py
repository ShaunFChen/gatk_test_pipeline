#!/usr/bin/env python3
"""Generate comprehensive performance report from Snakemake benchmarks.

This script analyzes benchmark data from pipeline runs and creates
an HTML report with performance metrics, visualizations, and recommendations.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend


def parse_benchmark_file(filepath: Path) -> dict:
    """Parse Snakemake benchmark file.

    Args:
        filepath: Path to benchmark file

    Returns:
        Dictionary with parsed metrics
    """
    if not filepath.exists():
        return {
            "runtime": 0,
            "max_rss": 0,
            "max_vms": 0,
            "max_uss": 0,
            "max_pss": 0,
            "io_in": 0,
            "io_out": 0,
            "mean_load": 0,
            "cpu_time": 0,
        }

    # Read benchmark file
    df = pd.read_csv(filepath, sep="\t")

    # Get the most recent run (last row)
    if len(df) > 0:
        latest = df.iloc[-1]
        return {
            "runtime": float(latest.get("s", 0)),
            "max_rss": float(latest.get("max_rss", 0)),
            "max_vms": float(latest.get("max_vms", 0)),
            "max_uss": float(latest.get("max_uss", 0)),
            "max_pss": float(latest.get("max_pss", 0)),
            "io_in": float(latest.get("io_in", 0)),
            "io_out": float(latest.get("io_out", 0)),
            "mean_load": float(latest.get("mean_load", 0)),
            "cpu_time": float(latest.get("cpu_time", 0)),
        }

    return {}


def format_memory(bytes_val: float) -> str:
    """Format memory value in human-readable format."""
    if bytes_val == 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB"]
    power = 0
    while bytes_val >= 1024 and power < len(units) - 1:
        bytes_val /= 1024
        power += 1

    return f"{bytes_val:.2f} {units[power]}"


def format_time(seconds: float) -> str:
    """Format time in human-readable format."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.2f} hours"


def create_performance_visualization(variant_metrics: dict, bisulfite_metrics: dict, output_dir: Path) -> list[str]:
    """Create performance visualizations and return list of created files."""

    created_files = []

    # Memory usage comparison
    plt.figure(figsize=(10, 6))
    pipelines = ["Variant Calling", "Bisulfite Analysis"]
    memory_usage = [
        variant_metrics.get("max_rss", 0) / (1024**2),  # Convert to MB
        bisulfite_metrics.get("max_rss", 0) / (1024**2),
    ]

    bars = plt.bar(pipelines, memory_usage, color=["#FF6B6B", "#4ECDC4"])
    plt.title("Peak Memory Usage Comparison")
    plt.ylabel("Memory Usage (MB)")
    plt.grid(axis="y", alpha=0.3)

    # Add value labels on bars
    for bar, value in zip(bars, memory_usage):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(memory_usage) * 0.01,
            f"{value:.1f} MB",
            ha="center",
            va="bottom",
        )

    memory_plot = output_dir / "memory_usage.png"
    plt.savefig(memory_plot, dpi=150, bbox_inches="tight")
    plt.close()
    created_files.append(memory_plot)

    # Runtime comparison
    plt.figure(figsize=(10, 6))
    runtime_data = [variant_metrics.get("runtime", 0), bisulfite_metrics.get("runtime", 0)]

    bars = plt.bar(pipelines, runtime_data, color=["#FF6B6B", "#4ECDC4"])
    plt.title("Pipeline Runtime Comparison")
    plt.ylabel("Runtime (seconds)")
    plt.grid(axis="y", alpha=0.3)

    # Add value labels on bars
    for bar, value in zip(bars, runtime_data):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(runtime_data) * 0.01,
            f"{value:.1f}s",
            ha="center",
            va="bottom",
        )

    runtime_plot = output_dir / "runtime_comparison.png"
    plt.savefig(runtime_plot, dpi=150, bbox_inches="tight")
    plt.close()
    created_files.append(runtime_plot)

    # CPU efficiency
    plt.figure(figsize=(10, 6))
    cpu_efficiency = []
    for metrics in [variant_metrics, bisulfite_metrics]:
        cpu_time = metrics.get("cpu_time", 0)
        runtime = metrics.get("runtime", 1)  # Avoid division by zero
        efficiency = (cpu_time / runtime) * 100 if runtime > 0 else 0
        cpu_efficiency.append(efficiency)

    bars = plt.bar(pipelines, cpu_efficiency, color=["#FF6B6B", "#4ECDC4"])
    plt.title("CPU Efficiency")
    plt.ylabel("CPU Efficiency (%)")
    plt.ylim(0, 110)
    plt.grid(axis="y", alpha=0.3)

    # Add value labels on bars
    for bar, value in zip(bars, cpu_efficiency):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f"{value:.1f}%",
            ha="center",
            va="bottom",
        )

    cpu_plot = output_dir / "cpu_efficiency.png"
    plt.savefig(cpu_plot, dpi=150, bbox_inches="tight")
    plt.close()
    created_files.append(cpu_plot)

    return created_files


def generate_html_report(
    variant_metrics: dict,
    bisulfite_metrics: dict,
    output_file: Path,
    visualization_files: list[Path],
) -> None:
    """Generate comprehensive HTML performance report."""

    total_runtime = variant_metrics.get("runtime", 0) + bisulfite_metrics.get("runtime", 0)
    total_memory = max(variant_metrics.get("max_rss", 0), bisulfite_metrics.get("max_rss", 0))

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GATK Pipeline Performance Report</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .metric-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .pipeline-section {{
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #fafafa;
        }}
        .metrics-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        .metrics-table th, .metrics-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        .metrics-table th {{
            background-color: #3498db;
            color: white;
        }}
        .visualization {{
            text-align: center;
            margin: 20px 0;
        }}
        .visualization img {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .recommendations {{
            background: #e8f6f3;
            border-left: 4px solid #1abc9c;
            padding: 15px;
            margin: 20px 0;
        }}
        .timestamp {{
            text-align: center;
            color: #7f8c8d;
            margin-top: 30px;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 GATK Pipeline Performance Report</h1>
        
        <div class="summary-grid">
            <div class="metric-card">
                <div class="metric-value">{format_time(total_runtime)}</div>
                <div class="metric-label">Total Runtime</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{format_memory(total_memory)}</div>
                <div class="metric-label">Peak Memory Usage</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">2</div>
                <div class="metric-label">Pipelines Executed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">✅</div>
                <div class="metric-label">Status</div>
            </div>
        </div>

        <h2>📊 Performance Visualizations</h2>
        <div class="visualization">
            <img src="memory_usage.png" alt="Memory Usage Comparison">
        </div>
        <div class="visualization">
            <img src="runtime_comparison.png" alt="Runtime Comparison">
        </div>
        <div class="visualization">
            <img src="cpu_efficiency.png" alt="CPU Efficiency">
        </div>

        <h2>🔬 Variant Calling Pipeline</h2>
        <div class="pipeline-section">
            <table class="metrics-table">
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Runtime</td><td>{format_time(variant_metrics.get("runtime", 0))}</td></tr>
                <tr><td>Peak Memory (RSS)</td><td>{format_memory(variant_metrics.get("max_rss", 0))}</td></tr>
                <tr><td>CPU Time</td><td>{format_time(variant_metrics.get("cpu_time", 0))}</td></tr>
                <tr><td>Mean Load</td><td>{variant_metrics.get("mean_load", 0):.2f}</td></tr>
                <tr><td>I/O Input</td><td>{format_memory(variant_metrics.get("io_in", 0))}</td></tr>
                <tr><td>I/O Output</td><td>{format_memory(variant_metrics.get("io_out", 0))}</td></tr>
            </table>
        </div>

        <h2>🧪 Bisulfite Conversion Analysis</h2>
        <div class="pipeline-section">
            <table class="metrics-table">
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Runtime</td><td>{format_time(bisulfite_metrics.get("runtime", 0))}</td></tr>
                <tr><td>Peak Memory (RSS)</td><td>{format_memory(bisulfite_metrics.get("max_rss", 0))}</td></tr>
                <tr><td>CPU Time</td><td>{format_time(bisulfite_metrics.get("cpu_time", 0))}</td></tr>
                <tr><td>Mean Load</td><td>{bisulfite_metrics.get("mean_load", 0):.2f}</td></tr>
                <tr><td>I/O Input</td><td>{format_memory(bisulfite_metrics.get("io_in", 0))}</td></tr>
                <tr><td>I/O Output</td><td>{format_memory(bisulfite_metrics.get("io_out", 0))}</td></tr>
            </table>
        </div>

        <h2>💡 Performance Recommendations</h2>
        <div class="recommendations">
            <h3>Optimization Opportunities:</h3>
            <ul>
                <li><strong>Memory Optimization:</strong> Peak memory usage was {format_memory(total_memory)}. Consider using memory-mapped files for large datasets.</li>
                <li><strong>Parallelization:</strong> Both pipelines can run in parallel for better resource utilization.</li>
                <li><strong>I/O Optimization:</strong> Monitor disk I/O patterns and consider SSD storage for better performance.</li>
                <li><strong>Resource Monitoring:</strong> Use Snakemake's built-in resource management for optimal scheduling.</li>
            </ul>
        </div>

        <div class="timestamp">
            Report generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
    </div>
</body>
</html>
"""

    with open(output_file, "w") as f:
        f.write(html_content)


def main():
    """Main function to generate performance report."""
    parser = argparse.ArgumentParser(description="Generate pipeline performance report")
    parser.add_argument("--variant-benchmark", required=True, help="Variant calling benchmark file")
    parser.add_argument("--bisulfite-benchmark", required=True, help="Bisulfite analysis benchmark file")
    parser.add_argument("--output", required=True, help="Output HTML file")
    parser.add_argument("--log", help="Log file")

    args = parser.parse_args()

    try:
        # Parse benchmark files
        variant_metrics = parse_benchmark_file(Path(args.variant_benchmark))
        bisulfite_metrics = parse_benchmark_file(Path(args.bisulfite_benchmark))

        # Create output directory
        output_file = Path(args.output)
        output_dir = output_file.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create visualizations
        visualization_files = create_performance_visualization(variant_metrics, bisulfite_metrics, output_dir)

        # Generate HTML report
        generate_html_report(variant_metrics, bisulfite_metrics, output_file, visualization_files)

        print(f"Performance report generated: {output_file}")

        # Log success
        if args.log:
            with open(args.log, "w") as f:
                f.write(f"Performance report generated successfully at {datetime.now()}\n")
                f.write(f"Output file: {output_file}\n")
                f.write(f"Visualizations created: {len(visualization_files)}\n")

    except Exception as e:
        error_msg = f"Error generating performance report: {e}"
        print(error_msg, file=sys.stderr)

        if args.log:
            with open(args.log, "w") as f:
                f.write(f"ERROR: {error_msg}\n")

        sys.exit(1)


if __name__ == "__main__":
    main()
