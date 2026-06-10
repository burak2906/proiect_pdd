"""
metrics.py
Timing and statistics utilities for the benchmark.
"""

import time
import statistics
from dataclasses import dataclass, field
from typing import List, Optional
import psutil
import os

@dataclass
class ScenarioResult:
    db: str
    scenario: str
    runs: List[float] = field(default_factory=list)
    cpu_percent: Optional[float] = None
    memory_delta_mb: Optional[float] = None

    @property
    def mean(self) -> float:
        return statistics.mean(self.runs) if self.runs else 0.0

    @property
    def stdev(self) -> float:
        return statistics.stdev(self.runs) if len(self.runs) > 1 else 0.0

    @property
    def min_ms(self) -> float:
        return min(self.runs) if self.runs else 0.0

    @property
    def max_ms(self) -> float:
        return max(self.runs) if self.runs else 0.0

    @property
    def p95(self) -> float:
        if len(self.runs) < 2:
            return self.runs[0] if self.runs else 0.0
        return statistics.quantiles(self.runs, n=20)[18]  # 95th percentile

    @property
    def p99(self) -> float:
        if len(self.runs) < 2:
            return self.runs[0] if self.runs else 0.0
        return statistics.quantiles(self.runs, n=100)[98]  # 99th percentile

    @property
    def throughput(self) -> float:
        try:
            n = int(self.scenario.split("_")[-1])
            return n / (self.mean / 1000) if self.mean > 0 else 0.0
        except (ValueError, ZeroDivisionError):
            return 0.0

    def __str__(self):
        return (f"[{self.db.upper():12s}] {self.scenario:<30s} "
                f"mean={self.mean:9.2f}ms  std={self.stdev:7.2f}ms  "
                f"p95={self.p95:8.2f}ms  cpu={self.cpu_percent or 0:.1f}%  "
                f"mem={self.memory_delta_mb or 0:.1f}MB")


class Timer:
    def __init__(self):
        self.elapsed_ms: float = 0.0

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_):
        self.elapsed_ms = (time.perf_counter() - self._start) * 1000


class ResourceMonitor:
    """Measures CPU and memory around a benchmark scenario."""

    def __init__(self):
        self._process = psutil.Process(os.getpid())
        self.cpu_percent: float = 0.0
        self.memory_delta_mb: float = 0.0

    def __enter__(self):
        self._process.cpu_percent(interval=None)  # reset counter
        self._mem_before = self._process.memory_info().rss
        return self

    def __exit__(self, *_):
        self.cpu_percent = self._process.cpu_percent(interval=None)
        mem_after = self._process.memory_info().rss
        self.memory_delta_mb = (mem_after - self._mem_before) / (1024 * 1024)


def measure_connection(connect_fn):
    with Timer() as t:
        conn = connect_fn()
    return t.elapsed_ms, conn