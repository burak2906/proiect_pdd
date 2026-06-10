"""
benchmark.py
Orchestrates all benchmark scenarios across MySQL, PostgreSQL, and SQLite.
Generates sample INSERT rows, runs each scenario 5 times per DB,
prints results, and saves them to results.csv.
"""

import random
import csv
import os
from datetime import datetime, timedelta

import client_mysql
import client_postgresql
import client_sqlite
from metrics import ScenarioResult, measure_connection

random.seed(42)

# ---------------------------------------------------------------------------
# Generate sample rows for INSERT benchmarks
# ---------------------------------------------------------------------------

def _make_rows(n: int, max_user=100_000, max_product=50_000):
    base = datetime(2023, 1, 1)
    rows = []
    for _ in range(n):
        rows.append((
            random.randint(1, max_user),
            random.randint(1, max_product),
            random.randint(1, 10),
            base + timedelta(days=random.randint(0, 730)),
        ))
    return rows

ROWS_1K   = _make_rows(1_000)
ROWS_10K  = _make_rows(10_000)
ROWS_100K = _make_rows(100_000)

# ---------------------------------------------------------------------------
# Connection overhead
# ---------------------------------------------------------------------------

def measure_all_connections():
    print("\\n=== Connection Overhead (5 measurements each) ===")
    results = {}
    for name, client in [("mysql", client_mysql),
                         ("postgresql", client_postgresql),
                         ("sqlite", client_sqlite)]:
        times = []
        for _ in range(5):
            elapsed, conn = measure_connection(
                client._connect if hasattr(client, "_connect") else client._connect
            )
            conn.close()
            times.append(elapsed)
        import statistics
        mean = statistics.mean(times)
        std  = statistics.stdev(times)
        print(f"  {name:<12s}  mean={mean:7.2f}ms  std={std:6.2f}ms")
        results[name] = {"mean": mean, "std": std}
    return results

# ---------------------------------------------------------------------------
# Run all scenarios
# ---------------------------------------------------------------------------

def run_benchmarks():
    all_results: list[ScenarioResult] = []

    clients = [
        ("MySQL",      client_mysql),
        ("PostgreSQL", client_postgresql),
        ("SQLite",     client_sqlite),
    ]

    for label, client in clients:
        print(f"\\n=== {label} ===")

        # INSERT 1K
        print(f"  bulk_insert_1000 ...")
        all_results.append(client.bench_bulk_insert(ROWS_1K,   batch_size=500))

        # INSERT 10K
        print(f"  bulk_insert_10000 ...")
        all_results.append(client.bench_bulk_insert(ROWS_10K,  batch_size=1000))

        # INSERT 100K
        print(f"  bulk_insert_100000 ...")
        all_results.append(client.bench_bulk_insert(ROWS_100K, batch_size=5000))

        # SELECT
        print(f"  select_where ...")
        all_results.append(client.bench_select_where())

        # JOIN
        print(f"  complex_join ...")
        all_results.append(client.bench_complex_join())

        # AGGREGATION
        print(f"  aggregation ...")
        all_results.append(client.bench_aggregation())

        # UPDATE/DELETE
        print(f"  update_delete ...")
        all_results.append(client.bench_update_delete())

        print(f"  {label} done ✓")

    return all_results

# ---------------------------------------------------------------------------
# Save to CSV
# ---------------------------------------------------------------------------

def save_csv(results: list[ScenarioResult], path="results.csv"):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "db", "scenario",
            "run_1", "run_2", "run_3", "run_4", "run_5",
            "mean_ms", "std_ms", "min_ms", "max_ms",
            "p95_ms", "p99_ms",
            "throughput_rows_per_sec",
            "cpu_percent", "memory_delta_mb"
        ])
        for r in results:
            runs = r.runs + [None] * (5 - len(r.runs))
            writer.writerow([
                r.db, r.scenario,
                *[f"{x:.3f}" if x is not None else "" for x in runs],
                f"{r.mean:.3f}",
                f"{r.stdev:.3f}",
                f"{r.min_ms:.3f}",
                f"{r.max_ms:.3f}",
                f"{r.p95:.3f}",
                f"{r.p99:.3f}",
                f"{r.throughput:.1f}",
                f"{r.cpu_percent or 0:.1f}",
                f"{r.memory_delta_mb or 0:.2f}",
            ])
    print(f"\\nResults saved to {path}")

# ---------------------------------------------------------------------------
# Print summary table
# ---------------------------------------------------------------------------

def print_summary(results: list[ScenarioResult]):
    print("\\n" + "="*80)
    print(f"{'DB':<14} {'Scenario':<22} {'Mean (ms)':>10} {'Std (ms)':>10} {'Runs':>6}")
    print("="*80)
    for r in results:
        print(f"{r.db:<14} {r.scenario:<22} {r.mean:>10.2f} {r.stdev:>10.2f} {len(r.runs):>6}")
    print("="*80)

# ---------------------------------------------------------------------------
# Print scalability information
# ---------------------------------------------------------------------------

def print_scalability(results: list[ScenarioResult]):
    print("\n=== Scalability Factor (INSERT latency growth) ===")
    for db in ["MySQL", "PostgreSQL", "SQLite"]:
        r1k   = next((r for r in results if r.db.lower() == db.lower() 
                      and r.scenario == "bulk_insert_1000"), None)
        r10k  = next((r for r in results if r.db.lower() == db.lower() 
                      and r.scenario == "bulk_insert_10000"), None)
        r100k = next((r for r in results if r.db.lower() == db.lower() 
                      and r.scenario == "bulk_insert_100000"), None)
        if r1k and r10k and r100k:
            f1  = r10k.mean  / r1k.mean   # 1K → 10K (10x data)
            f2  = r100k.mean / r10k.mean  # 10K → 100K (10x data)
            print(f"  {db:<14s}  1K→10K: {f1:.2f}x  |  10K→100K: {f2:.2f}x  "
                  f"(linear would be 10.00x)")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Starting benchmark suite...")
    print("Databases: MySQL 8.0 | PostgreSQL 18 | SQLite 3.45")
    print("Scenarios: INSERT(1K/10K/100K) | SELECT | JOIN | AGGREGATION | UPDATE/DELETE")
    print("Runs per scenario: 5\\n")

    measure_all_connections()
    results = run_benchmarks()
    print_summary(results)
    print_scalability(results)
    save_csv(results)
    print("\\nDone! Run report.py to generate charts.")