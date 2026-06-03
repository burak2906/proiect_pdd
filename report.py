"""
report.py
Final clean chart generator for benchmark results.
Overwrites previous chart files with cleaner visuals.
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
    df["mean_ms"] = pd.to_numeric(df["mean_ms"], errors="coerce")
    df["std_ms"] = pd.to_numeric(df["std_ms"], errors="coerce")
    return df


def save_fig(fig, filename: str, caption: str, description: str):
    out = os.path.join(OUTPUT_DIR, filename)
    fig.write_image(out)
    with open(out + ".meta.json", "w") as f:
        json.dump({"caption": caption, "description": description}, f)
    print(f"  Saved: {filename}")


def add_grouped_bars(fig, subset: pd.DataFrame, order: list[str], show_text: bool = False):
    for db in ["mysql", "postgresql", "sqlite"]:
        rows = subset[subset["db"] == db].copy()
        rows["scenario"] = pd.Categorical(rows["scenario"], categories=order, ordered=True)
        rows = rows.sort_values("scenario")

        kwargs = {
            "name": DB_LABELS[db],
            "x": rows["scenario"],
            "y": rows["mean_ms"],
            "error_y": dict(type="data", array=rows["std_ms"].tolist(), visible=True),
            "marker_color": DB_COLORS[db],
            "cliponaxis": False,
        }

        if show_text:
            kwargs["text"] = [f"{v:.1f}" for v in rows["mean_ms"]]
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
    save_fig(
        fig,
        "chart_insert.png",
        "INSERT benchmark",
        "Grouped bar chart comparing INSERT performance for MySQL, PostgreSQL and SQLite on a logarithmic scale."
    )


def chart_query(df: pd.DataFrame):
    order = ["select_where", "complex_join", "aggregation"]
    subset = df[df["scenario"].isin(order)]
    fig = go.Figure()
    add_grouped_bars(fig, subset, order, show_text=True)
    apply_layout(fig, "Read Query Performance", "Query type", "Time (ms)", log_y=True)
    save_fig(
        fig,
        "chart_query.png",
        "Read query benchmark",
        "Grouped bar chart comparing SELECT, JOIN and aggregation latency across the three databases on a logarithmic scale."
    )


def chart_update_delete(df: pd.DataFrame):
    order = ["update_delete"]
    subset = df[df["scenario"].isin(order)]
    fig = go.Figure()
    add_grouped_bars(fig, subset, order, show_text=True)
    apply_layout(fig, "UPDATE + DELETE Performance", "Scenario", "Time (ms)", log_y=False)
    save_fig(
        fig,
        "chart_update_delete.png",
        "Update/delete benchmark",
        "Grouped bar chart comparing UPDATE and DELETE scenario latency across the three databases."
    )


def chart_summary(df: pd.DataFrame):
    order = [
        "bulk_insert_1000",
        "bulk_insert_10000",
        "bulk_insert_100000",
        "select_where",
        "complex_join",
        "aggregation",
        "update_delete"
    ]
    subset = df[df["scenario"].isin(order)]
    fig = go.Figure()
    add_grouped_bars(fig, subset, order, show_text=False)
    apply_layout(fig, "Full Benchmark Summary", "Scenario", "Time (ms)", log_y=True)
    save_fig(
        fig,
        "chart_summary.png",
        "Full benchmark summary",
        "Overview chart of all benchmark scenarios across MySQL, PostgreSQL and SQLite on a logarithmic scale."
    )


def print_summary(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print(f"{'DB':<14} {'Scenario':<25} {'Mean (ms)':>10} {'Std (ms)':>10}")
    print("=" * 70)
    for _, row in df.iterrows():
        print(f"{row['db']:<14} {row['scenario']:<25} {row['mean_ms']:>10.2f} {row['std_ms']:>10.2f}")
    print("=" * 70)


def generate_all_charts(df: pd.DataFrame):
    print("\nGenerating charts...")
    chart_insert(df)
    chart_query(df)
    chart_update_delete(df)
    chart_summary(df)
    print("  All charts saved.")


if __name__ == "__main__":
    if not os.path.exists(RESULTS_CSV):
        print(f"ERROR: {RESULTS_CSV} not found.")
        print("Run benchmark.py first to generate results.")
        raise SystemExit(1)

    df = load_results()
    print_summary(df)
    generate_all_charts(df)
    print("\nDone!")