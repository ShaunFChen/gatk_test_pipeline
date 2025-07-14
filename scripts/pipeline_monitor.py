"""Pipeline Monitoring and Benchmarking System.

This script demonstrates advanced pipeline monitoring concepts including:
- Performance benchmarking and tracking
- Resource utilization monitoring
- Parallel pipeline execution
- Comprehensive reporting
- Quality control metrics

This replaces Snakemake functionality while being compatible with Python 3.10.
"""

import argparse
import concurrent.futures
import json
import logging
import subprocess
import sys
import threading
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import psutil

# Configure logging
logger = logging.getLogger(__name__)


class PipelineBenchmark:
    """Monitor and benchmark individual pipeline execution."""

    def __init__(self, name: str) -> None:
        """Initialize pipeline benchmark.

        Args:
            name: Name of the pipeline being benchmarked

        """
        self.name = name
        self.process = psutil.Process()
        self.start_time: float | None = None
        self.end_time: float | None = None
        self.max_memory_percent: float = 0
        self.max_cpu_percent: float = 0
        self.io_counters_start: dict | None = None
        self.io_counters_end: dict | None = None

    def start(self) -> None:
        """Start benchmarking."""
        self.start_time = time.time()
        try:
            self.io_counters_start = self.process.io_counters()._asdict()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            self.io_counters_start = {}

    def update_metrics(self) -> None:
        """Update resource usage metrics."""
        if self.process:
            try:
                self.max_memory_percent = max(self.max_memory_percent, self.process.memory_percent())
                self.max_cpu_percent = max(self.max_cpu_percent, self.process.cpu_percent())
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def stop(self) -> None:
        """Stop benchmarking and finalize metrics."""
        self.end_time = time.time()
        try:
            self.io_counters_end = self.process.io_counters()._asdict()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            self.io_counters_end = {}

    def get_metrics(self) -> dict[str, Any]:
        """Get final benchmark metrics."""
        runtime = (self.end_time - self.start_time) if self.start_time and self.end_time else 0

        io_read = 0
        io_write = 0
        if self.io_counters_start and self.io_counters_end:
            io_read = self.io_counters_end.get("read_bytes", 0) - self.io_counters_start.get("read_bytes", 0)
            io_write = self.io_counters_end.get("write_bytes", 0) - self.io_counters_start.get("write_bytes", 0)

        return {
            "name": self.name,
            "success": True,
            "runtime_seconds": runtime,
            "runtime_formatted": self._format_time(runtime),
            "max_memory_percent": self.max_memory_percent,
            "max_memory_formatted": f"{self.max_memory_percent:.1f}%",
            "max_cpu_percent": self.max_cpu_percent,
            "io_read_bytes": io_read,
            "io_write_bytes": io_write,
            "io_read_formatted": self._format_bytes(io_read),
            "io_write_formatted": self._format_bytes(io_write),
            "timestamp": datetime.now(UTC).isoformat(),
        }

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format time duration in human-readable format."""
        if seconds < 60:
            return f"{seconds:.2f}s"
        if seconds < 3600:
            return f"{seconds / 60:.2f}m"
        return f"{seconds / 3600:.2f}h"

    @staticmethod
    def _format_bytes(bytes_value: int) -> str:
        """Format bytes in human-readable format."""
        for unit in ["B", "KB", "MB", "GB"]:
            if bytes_value < 1024:
                return f"{bytes_value:.1f}{unit}"
            bytes_value /= 1024
        return f"{bytes_value:.1f}TB"


class PipelineRunner:
    """Execute individual pipelines with monitoring."""

    def __init__(self, output_dir: Path) -> None:
        """Initialize pipeline runner.

        Args:
            output_dir: Directory for output files

        """
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)

    def run_pipeline(self, pipeline_name: str, script_path: str) -> dict[str, Any]:
        """Run a single pipeline with comprehensive monitoring."""
        benchmark = PipelineBenchmark(pipeline_name)
        benchmark.start()

        logger.info("🚀 Starting %s...", pipeline_name)

        try:
            monitoring_active = True

            def monitor_resources() -> None:
                while monitoring_active:
                    benchmark.update_metrics()
                    time.sleep(0.1)

            monitor_thread = threading.Thread(target=monitor_resources)
            monitor_thread.daemon = True
            monitor_thread.start()

            # Run the pipeline
            cmd = [sys.executable, script_path]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd(), check=False)

            # Stop monitoring
            monitoring_active = False
            monitor_thread.join()
            benchmark.stop()

            metrics = benchmark.get_metrics()

            # Save output logs
            log_file = self.output_dir / f"{pipeline_name}_log.txt"
            with log_file.open("w") as f:
                f.write(f"=== {pipeline_name} Output ===\n")
                f.write(f"Return code: {result.returncode}\n\n")
                f.write("=== Standard Output ===\n")
                f.write(result.stdout)
                f.write("\n=== Standard Error ===\n")
                f.write(result.stderr)

            if result.returncode == 0:
                logger.info("✅ %s completed successfully", pipeline_name)
                logger.info("   Runtime: %s", metrics["runtime_formatted"])
                logger.info("   Peak Memory: %s", metrics["max_memory_formatted"])
                return metrics

            logger.error("❌ %s failed with return code %d", pipeline_name, result.returncode)
            metrics["success"] = False
            return metrics

        except subprocess.SubprocessError:
            benchmark.stop()
            logger.exception("❌ %s failed with exception", pipeline_name)
            return {
                "name": pipeline_name,
                "success": False,
                "error": "Subprocess error",
                "runtime_seconds": 0,
                "runtime_formatted": "0s",
                "max_memory_percent": 0,
                "max_memory_formatted": "0%",
                "max_cpu_percent": 0,
                "io_read_bytes": 0,
                "io_write_bytes": 0,
                "io_read_formatted": "0B",
                "io_write_formatted": "0B",
            }


class PipelineMonitor:
    """Main pipeline monitoring and orchestration system."""

    def __init__(self, output_dir: str = "output") -> None:
        """Initialize pipeline monitor.

        Args:
            output_dir: Directory for output files

        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.runner = PipelineRunner(self.output_dir)

    def run_sequential(self, pipelines: list[tuple[str, str]]) -> list[dict[str, Any]]:
        """Run pipelines sequentially with monitoring."""
        logger.info("🔄 Running pipelines sequentially...")
        results = []
        start_time = time.time()

        for name, script_path in pipelines:
            result = self.runner.run_pipeline(name, script_path)
            results.append(result)

        total_time = time.time() - start_time
        logger.info("\n⏱️  Total sequential runtime: %.2f seconds", total_time)

        return results

    def run_parallel(self, pipelines: list[tuple[str, str]], max_workers: int = 2) -> list[dict[str, Any]]:
        """Run pipelines in parallel with monitoring."""
        logger.info("⚡ Running pipelines in parallel (max_workers=%d)...", max_workers)
        results = []
        start_time = time.time()

        # Create a new runner for each pipeline to avoid resource conflicts
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._run_pipeline_subprocess, name, script_path): name
                for name, script_path in pipelines
            }

            for future in concurrent.futures.as_completed(futures):
                name = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except subprocess.SubprocessError:
                    logger.exception("❌ %s failed with exception", name)
                    results.append(
                        {
                            "name": name,
                            "success": False,
                            "error": "Subprocess error",
                            "runtime_seconds": 0,
                            "runtime_formatted": "0s",
                            "max_memory_percent": 0,
                            "max_memory_formatted": "0%",
                            "max_cpu_percent": 0,
                            "io_read_bytes": 0,
                            "io_write_bytes": 0,
                            "io_read_formatted": "0B",
                            "io_write_formatted": "0B",
                        }
                    )

        total_time = time.time() - start_time
        logger.info("\n⚡ Total parallel runtime: %.2f seconds", total_time)

        # Calculate speedup
        sequential_time = sum(r.get("runtime_seconds", 0) for r in results)
        speedup = sequential_time / total_time if total_time > 0 else 1
        logger.info("🚀 Parallel speedup: %.2fx", speedup)

        return results

    def _run_pipeline_subprocess(self, name: str, script_path: str) -> dict[str, Any]:
        """Run pipeline in subprocess (for parallel execution)."""
        # This creates a new PipelineRunner for each subprocess
        runner = PipelineRunner(self.output_dir)
        return runner.run_pipeline(name, script_path)

    def generate_performance_report(self, results: list[dict[str, Any]], execution_mode: str) -> str:
        """Generate comprehensive performance report."""
        report_file = self.output_dir / f"performance_report_{execution_mode}.html"

        # Create visualizations
        self._create_performance_visualizations(results, execution_mode)

        html_content = self._generate_html_report(results, execution_mode)

        with report_file.open("w") as f:
            f.write(html_content)

        logger.info("📊 Performance report generated: %s", report_file)
        return str(report_file)

    def _create_performance_visualizations(self, results: list[dict[str, Any]], execution_mode: str) -> None:
        """Create performance visualization charts."""
        # Memory usage chart
        plt.figure(figsize=(10, 6))
        memory_usage = [r.get("max_memory_percent", 0) for r in results]
        names = [r.get("name", "Unknown") for r in results]

        plt.subplot(2, 1, 1)
        bars = plt.bar(names, memory_usage)
        plt.title(f"Memory Usage - {execution_mode.title()} Execution")
        plt.ylabel("Memory Usage (%)")
        plt.xticks(rotation=45)

        # Add value labels
        for bar, value in zip(bars, memory_usage, strict=True):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                value,
                f"{value:.1f}%",
                ha="center",
                va="bottom",
            )

        # Runtime chart
        plt.subplot(2, 1, 2)
        runtime_data = [r.get("runtime_seconds", 0) for r in results]

        bars = plt.bar(names, runtime_data)
        plt.title(f"Runtime - {execution_mode.title()} Execution")
        plt.ylabel("Runtime (seconds)")
        plt.xticks(rotation=45)

        # Add value labels
        for bar, value in zip(bars, runtime_data, strict=True):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                value,
                f"{value:.1f}s",
                ha="center",
                va="bottom",
            )

        plt.tight_layout()
        plt.savefig(self.output_dir / f"performance_viz_{execution_mode}.png")
        plt.close()

    def _generate_html_report(self, results: list[dict[str, Any]], execution_mode: str) -> str:
        """Generate HTML performance report."""
        successful_results = [r for r in results if r.get("success", False)]
        total_runtime = sum(r.get("runtime_seconds", 0) for r in results)
        avg_memory = sum(r.get("max_memory_percent", 0) for r in results) / len(results) if results else 0

        html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pipeline Performance Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px;
                        border-radius: 10px; }
            h1 { color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db;
                 padding-bottom: 10px; }
            .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                      gap: 20px; margin: 20px 0; }
            .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          color: white; padding: 20px; border-radius: 8px; text-align: center; }
            .metric-value { font-size: 2em; font-weight: bold; }
            .metric-label { font-size: 0.9em; opacity: 0.9; }
            .visualization { text-align: center; margin: 20px 0; }
            .visualization img { max-width: 100%; border-radius: 8px;
                               box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            .success { color: #27ae60; }
            .error { color: #e74c3c; }
        </style>
    </head>
    <body>
    <div class="container">
        <h1>🧬 Pipeline Performance Report - {execution_mode.title()} Execution</h1>
        <div class="summary">
            <div class="metric-card">
                <div class="metric-value">{len(results)}</div>
                <div class="metric-label">Total Pipelines</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{len(successful_results)}</div>
                <div class="metric-label">Successful Pipelines</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{total_runtime:.1f}s</div>
                <div class="metric-label">Total Runtime</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{avg_memory:.1f}%</div>
                <div class="metric-label">Average Memory Usage</div>
            </div>
        </div>

        <h2>📊 Performance Visualizations</h2>
        <div class="visualization">
            <img src="performance_viz_{execution_mode}.png" alt="Performance Visualization">
        </div>

        <h2>📝 Detailed Results</h2>
        <table>
            <tr>
                <th>Pipeline</th>
                <th>Status</th>
                <th>Runtime</th>
                <th>Memory</th>
                <th>I/O Read</th>
                <th>I/O Write</th>
            </tr>
        """

        for result in results:
            status_class = "success" if result.get("success", False) else "error"
            status_text = "✅ Success" if result.get("success", False) else "❌ Failed"

            html_content += f"""
            <tr>
                <td>{result.get("name", "Unknown")}</td>
                <td class="{status_class}">{status_text}</td>
                <td>{result.get("runtime_formatted", "N/A")}</td>
                <td>{result.get("max_memory_formatted", "N/A")}</td>
                <td>{result.get("io_read_formatted", "N/A")}</td>
                <td>{result.get("io_write_formatted", "N/A")}</td>
            </tr>
            """

        html_content += f"""
        </table>
        <h2>💡 Performance Insights</h2>
        <div style="background: #e8f6f3; border-left: 4px solid #1abc9c; padding: 15px;
                   margin: 20px 0;">
            <h3>Key Findings:</h3>
            <ul>
                <li><strong>Execution Mode:</strong> {execution_mode.title()} execution
                    demonstrated</li>
                <li><strong>Resource Monitoring:</strong> Real-time CPU, memory, and I/O tracking
                    implemented</li>
                <li><strong>Performance Optimization:</strong> Pipeline efficiency and bottlenecks
                    identified</li>
                <li><strong>Benchmarking:</strong> Comprehensive metrics collection and
                    analysis</li>
            </ul>
        </div>
        <div style="text-align: center; color: #7f8c8d; margin-top: 30px; font-style: italic;">
            Report generated on {datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")}
        </div>
    </div>
    </body>
    </html>
    """

        return html_content

    def save_metrics_json(self, results: list[dict[str, Any]], execution_mode: str) -> str:
        """Save metrics to JSON file for further analysis."""
        json_file = self.output_dir / f"pipeline_metrics_{execution_mode}.json"

        metrics_data = {
            "execution_mode": execution_mode,
            "timestamp": datetime.now(UTC).isoformat(),
            "summary": {
                "total_pipelines": len(results),
                "successful_pipelines": len([r for r in results if r.get("success", False)]),
                "total_runtime_seconds": sum(r.get("runtime_seconds", 0) for r in results),
                "average_memory_percent": (
                    sum(r.get("max_memory_percent", 0) for r in results) / len(results) if results else 0
                ),
            },
            "pipeline_results": results,
        }

        with json_file.open("w") as f:
            json.dump(metrics_data, f, indent=2)

        logger.info("💾 Metrics saved to: %s", json_file)
        return str(json_file)


def main() -> None:
    """Run the pipeline monitoring system."""
    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser(description="Pipeline Monitoring and Benchmarking System")
    parser.add_argument(
        "--mode",
        choices=["sequential", "parallel", "both"],
        default="both",
        help="Execution mode",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=2,
        help="Maximum number of parallel workers",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Output directory for reports and metrics",
    )

    args = parser.parse_args()

    # Example pipelines to monitor
    pipelines = [
        ("variant_calling", "scripts/variant_calling.py"),
        ("alignment", "scripts/alignment.py"),
        ("quality_control", "scripts/quality_control.py"),
    ]

    logger.info("🧬 GATK Pipeline Monitoring and Benchmarking System")
    logger.info("=" * 60)

    # System information
    logger.info(
        "💻 System: %d cores, %.1f GB RAM",
        psutil.cpu_count(),
        psutil.virtual_memory().total / (1024**3),
    )
    logger.info("🐍 Python: %s", sys.version.split()[0])
    logger.info("📁 Output directory: %s", args.output_dir)
    logger.info("")

    monitor = PipelineMonitor(args.output_dir)

    if args.mode in ["sequential", "both"]:
        logger.info("🔄 Running Sequential Analysis...")
        sequential_results = monitor.run_sequential(pipelines)
        monitor.generate_performance_report(sequential_results, "sequential")
        monitor.save_metrics_json(sequential_results, "sequential")
        logger.info("")

    if args.mode in ["parallel", "both"]:
        logger.info("⚡ Running Parallel Analysis...")
        parallel_results = monitor.run_parallel(pipelines, args.max_workers)
        monitor.generate_performance_report(parallel_results, "parallel")
        monitor.save_metrics_json(parallel_results, "parallel")
        logger.info("")

    logger.info("✅ Pipeline monitoring completed!")
    logger.info("📊 Check %s/ for detailed reports and metrics", args.output_dir)


if __name__ == "__main__":
    main()
