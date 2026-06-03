"""
metrics.py
Timing and statistics utilities for the benchmark.
"""

import time
import statistics
from dataclasses import dataclass, field
from typing import List


@dataclass
class ScenarioResult:
    db: str           # "mysql" | "postgresql" | "sqlite"
    scenario: str     # e.g. "bulk_insert_1000"
    runs: List[float] = field(default_factory=list)  # raw times in ms

    @property
    def mean(self) -> float:
        return statistics.mean(self.runs) if self.runs else 0.0

    @property
    def stdev(self) -> float:
        return statistics.stdev(self.runs) if len(self.runs) > 1 else 0.0

    @property
    def throughput(self) -> float:
        """Operations per second (only meaningful for INSERT scenarios)."""
        # extract row count from scenario name e.g. bulk_insert_1000
        try:
            n = int(self.scenario.split("_")[-1])
            return n / (self.mean / 1000) if self.mean > 0 else 0.0
        except (ValueError, ZeroDivisionError):
            return 0.0

    def __str__(self):
        return (f"[{self.db.upper():12s}] {self.scenario:<30s} "
                f"mean={self.mean:9.2f}ms  std={self.stdev:7.2f}ms  "
                f"runs={len(self.runs)}")


class Timer:
    """Context manager that records elapsed time in milliseconds."""

    def __init__(self):
        self.elapsed_ms: float = 0.0

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_):
        self.elapsed_ms = (time.perf_counter() - self._start) * 1000


def measure_connection(connect_fn) -> float:
    """
    Measure time (ms) to establish a fresh DB connection.
    connect_fn must return a live connection object.
    Returns elapsed ms and the connection so the caller can reuse it.
    """
    with Timer() as t:
        conn = connect_fn()
    return t.elapsed_ms, conn