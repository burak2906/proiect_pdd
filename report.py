"""
report.py
Final clean chart generator for benchmark results.
Generates charts for all metrics including CPU, memory, scalability factor.
"""

import os
import json
import pandas as pd
import plotly.graph_objects as go

RESULTS_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.csv")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

DB_LABELS = {
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "sqlite": "SQLite",
}

DB_COLORS = {
    "mysql": "#3b82f6",
    "postgresql": "#f59e0b",
    "sqlite": "#14b8a6",
}


def load_results() -> pd.DataFrame:
    df = pd.read_csv(RESULTS_CSV)
    for col in ["mean_ms", "std_ms", "min_ms", "max_ms",
                "p95_ms", "p99_ms", "throughput_rows_per_sec",
                "cpu_percent", "memory_delta_mb"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def save_fig(fig, filename: str, caption: str, description: str):
    out = os.path.join(OUTPUT_DIR, filename)
    fig.write_image(out)
    with open(out + ".meta.json", "w") as f:
        json.dump({"caption": caption, "description": description}, f)
    print(f"  Saved: {filename}")


def add_grouped_bars(fig, subset: pd.DataFrame, order: list,
                     y_col: str = "mean_ms", err_col: str = "std_ms",
                     show_text: bool = False):
    for db in ["mysql", "postgresql", "sqlite"]:
        rows = subset[subset["db"] == db].copy()
        rows["scenario"] = pd.Categorical(rows["scenario"], categories=order, ordered=True)
        rows = rows.sort_values("scenario")

        err = rows[err_col].tolist() if err_col and err_col in rows.columns else None

        kwargs = {
            "name": DB_LABELS[db],
            "x": rows["scenario"],
            "y": rows[y_col],
            "marker_color": DB_COLORS[db],
            "cliponaxis": False,
        }
        if err:
            kwargs["error_y"] = dict(type="data", array=err, visible=True)
        if show_text:
            kwargs["text"] = [f"{v:.1f}" for v in rows[y_col]]
            kwargs["textposition"] = "outside"

        fig.add_trace(go.Bar(**kwargs))


def apply_layout(fig, title: str, x_title: str, y_title: str, log_y: bool = False):
    fig.update_layout(
        title=title,
        barmode="group",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
    )
    fig.update_xaxes(title_text=x_title)
    fig.update_yaxes(title_text=y_title, type="log" if log_y else "linear")


def chart_insert(df: pd.DataFrame):
    order = ["bulk_insert_1000", "bulk_insert_10000", "bulk_insert_100000"]
    subset = df[df["scenario"].isin(order)]
    fig = go.Figure()
    add_grouped_bars(fig, subset, order, show_text=True)
    apply_layout(fig, "INSERT Performance", "Insert load", "Time (ms)", log_y=True)
    save_fig(fig, "chart_insert.png", "INSERT benchmark",
             "Grouped bar chart comparing INSERT performance on a logarithmic scale.")


def chart_query(df: pd.DataFrame):
    order = ["select_where", "complex_join", "aggregation"]
    subset = df[df["scenario"].isin(order)]
    fig = go.Figure()
    add_grouped_bars(fig, subset, order, show_text=True)
    apply_layout(fig, "Read Query Performance", "Query type", "Time (ms)", log_y=True)
    save_fig(fig, "chart_query.png", "Read query benchmark",
             "Grouped bar chart comparing SELECT, JOIN and aggregation latency on a logarithmic scale.")


def chart_update_delete(df: pd.DataFrame):
    order = ["update_delete"]
    subset = df[df["scenario"].isin(order)]
    fig = go.Figure()
    add_grouped_bars(fig, subset, order, show_text=True)
    apply_layout(fig, "UPDATE + DELETE Performance", "Scenario", "Time (ms)")
    save_fig(fig, "chart_update_delete.png", "Update/delete benchmark",
             "Grouped bar chart comparing UPDATE and DELETE scenario latency.")


def chart_summary(df: pd.DataFrame):
    order = ["bulk_insert_1000", "bulk_insert_10000", "bulk_insert_100000",
             "select_where", "complex_join", "aggregation", "update_delete"]
    subset = df[df["scenario"].isin(order)]
    fig = go.Figure()
    add_grouped_bars(fig, subset, order)
    apply_layout(fig, "Full Benchmark Summary", "Scenario", "Time (ms)", log_y=True)
    save_fig(fig, "chart_summary.png", "Full benchmark summary",
             "Overview of all benchmark scenarios on a logarithmic scale.")



def chart_p95_p99(df: pd.DataFrame):
    """P95 and P99 latency for all scenarios."""
    order = ["bulk_insert_1000", "bulk_insert_10000", "bulk_insert_100000",
             "select_where", "complex_join", "aggregation", "update_delete"]
    subset = df[df["scenario"].isin(order)]
    fig = go.Figure()

    for db in ["mysql", "postgresql", "sqlite"]:
        rows = subset[subset["db"] == db].copy()
        rows["scenario"] = pd.Categorical(rows["scenario"], categories=order, ordered=True)
        rows = rows.sort_values("scenario")

        fig.add_trace(go.Bar(
            name=f"{DB_LABELS[db]} P95",
            x=rows["scenario"],
            y=rows["p95_ms"],
            marker_color=DB_COLORS[db],
            marker_pattern_shape="/",
            cliponaxis=False,
        ))
        fig.add_trace(go.Bar(
            name=f"{DB_LABELS[db]} P99",
            x=rows["scenario"],
            y=rows["p99_ms"],
            marker_color=DB_COLORS[db],
            marker_pattern_shape="x",
            cliponaxis=False,
        ))

    apply_layout(fig, "P95 and P99 Latency", "Scenario", "Time (ms)", log_y=True)
    save_fig(fig, "chart_p95_p99.png", "P95/P99 latency",
             "P95 and P99 latency percentiles across all scenarios and databases.")


def chart_cpu(df: pd.DataFrame):
    """CPU usage per scenario."""
    order = ["bulk_insert_1000", "bulk_insert_10000", "bulk_insert_100000",
             "select_where", "complex_join", "aggregation", "update_delete"]
    subset = df[df["scenario"].isin(order)]
    fig = go.Figure()
    add_grouped_bars(fig, subset, order, y_col="cpu_percent", err_col=None, show_text=True)
    apply_layout(fig, "CPU Usage per Scenario", "Scenario", "CPU (%)")
    save_fig(fig, "chart_cpu.png", "CPU usage benchmark",
             "CPU usage percentage per scenario across the three databases.")


def chart_memory(df: pd.DataFrame):
    """Memory delta per scenario."""
    order = ["bulk_insert_1000", "bulk_insert_10000", "bulk_insert_100000",
             "select_where", "complex_join", "aggregation", "update_delete"]
    subset = df[df["scenario"].isin(order)]
    fig = go.Figure()
    add_grouped_bars(fig, subset, order, y_col="memory_delta_mb", err_col=None, show_text=True)
    apply_layout(fig, "Memory Usage per Scenario", "Scenario", "Memory delta (MB)")
    save_fig(fig, "chart_memory.png", "Memory usage benchmark",
             "Memory delta in MB per scenario across the three databases.")


def chart_throughput(df: pd.DataFrame):
    """Throughput (rows/sec) for INSERT scenarios only."""
    order = ["bulk_insert_1000", "bulk_insert_10000", "bulk_insert_100000"]
    subset = df[df["scenario"].isin(order)]
    fig = go.Figure()
    add_grouped_bars(fig, subset, order,
                     y_col="throughput_rows_per_sec", err_col=None, show_text=True)
    apply_layout(fig, "INSERT Throughput (rows/sec)", "Insert load", "Rows per second")
    save_fig(fig, "chart_throughput.png", "INSERT throughput",
             "Rows per second for INSERT scenarios across the three databases.")


def chart_scalability(df: pd.DataFrame):
    """Scalability factor: how latency grows as volume increases 10x."""
    insert_scenarios = ["bulk_insert_1000", "bulk_insert_10000", "bulk_insert_100000"]
    labels = ["1K → 10K (10× data)", "10K → 100K (10× data)"]
    fig = go.Figure()

    for db in ["mysql", "postgresql", "sqlite"]:
        rows = df[(df["db"] == db) & (df["scenario"].isin(insert_scenarios))].copy()
        rows["scenario"] = pd.Categorical(rows["scenario"],
                                          categories=insert_scenarios, ordered=True)
        rows = rows.sort_values("scenario").reset_index(drop=True)

        if len(rows) == 3:
            f1 = rows.loc[1, "mean_ms"] / rows.loc[0, "mean_ms"]
            f2 = rows.loc[2, "mean_ms"] / rows.loc[1, "mean_ms"]
            fig.add_trace(go.Bar(
                name=DB_LABELS[db],
                x=labels,
                y=[f1, f2],
                marker_color=DB_COLORS[db],
                text=[f"{f1:.2f}×", f"{f2:.2f}×"],
                textposition="outside",
                cliponaxis=False,
            ))

    fig.add_hline(y=10, line_dash="dash", line_color="gray",
                  annotation_text="Linear (10×)", annotation_position="right")
    apply_layout(fig, "Scalability Factor (INSERT)", "Volume step", "Latency growth factor")
    save_fig(fig, "chart_scalability.png", "Scalability factor",
             "How much latency increases when data volume grows 10×. "
             "Dashed line = perfectly linear scaling.")


# ── PRINT SUMMARY ──────────────────────────────────────────────────────────

def print_summary(df: pd.DataFrame):
    cols = ["db", "scenario", "mean_ms", "std_ms", "p95_ms", "p99_ms",
            "cpu_percent", "memory_delta_mb"]
    available = [c for c in cols if c in df.columns]
    print("\n" + "=" * 90)
    header = f"{'DB':<14} {'Scenario':<25} {'Mean':>9} {'Std':>8} "
    if "p95_ms" in available:
        header += f"{'P95':>9} {'P99':>9} "
    if "cpu_percent" in available:
        header += f"{'CPU%':>6} "
    if "memory_delta_mb" in available:
        header += f"{'Mem MB':>7}"
    print(header)
    print("=" * 90)
    for _, row in df.iterrows():
        line = f"{row['db']:<14} {row['scenario']:<25} {row['mean_ms']:>9.2f} {row['std_ms']:>8.2f} "
        if "p95_ms" in available:
            line += f"{row['p95_ms']:>9.2f} {row['p99_ms']:>9.2f} "
        if "cpu_percent" in available:
            line += f"{row['cpu_percent']:>6.1f} "
        if "memory_delta_mb" in available:
            line += f"{row['memory_delta_mb']:>7.2f}"
        print(line)
    print("=" * 90)


def print_scalability(df: pd.DataFrame):
    print("\n=== Scalability Factor (INSERT latency growth) ===")
    insert_scenarios = ["bulk_insert_1000", "bulk_insert_10000", "bulk_insert_100000"]
    for db in ["mysql", "postgresql", "sqlite"]:
        rows = df[(df["db"] == db) & (df["scenario"].isin(insert_scenarios))].copy()
        rows["scenario"] = pd.Categorical(rows["scenario"],
                                          categories=insert_scenarios, ordered=True)
        rows = rows.sort_values("scenario").reset_index(drop=True)
        if len(rows) == 3:
            f1 = rows.loc[1, "mean_ms"] / rows.loc[0, "mean_ms"]
            f2 = rows.loc[2, "mean_ms"] / rows.loc[1, "mean_ms"]
            print(f"  {db:<14}  1K→10K: {f1:.2f}×  |  10K→100K: {f2:.2f}×  "
                  f"(linear = 10.00×)")


# ── ENTRY POINT ────────────────────────────────────────────────────────────

def generate_all_charts(df: pd.DataFrame):
    print("\nGenerating charts...")
    chart_insert(df)
    chart_query(df)
    chart_update_delete(df)
    chart_summary(df)
    chart_p95_p99(df)
    chart_cpu(df)
    chart_memory(df)
    chart_throughput(df)
    chart_scalability(df)
    print("  All charts saved.")


if __name__ == "__main__":
    if not os.path.exists(RESULTS_CSV):
        print(f"ERROR: {RESULTS_CSV} not found.")
        print("Run benchmark.py first to generate results.")
        raise SystemExit(1)

    df = load_results()
    print_summary(df)
    print_scalability(df)
    generate_all_charts(df)
    print("\nDone!")