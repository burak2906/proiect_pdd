"""
client_sqlite.py
SQLite benchmark client exposed through an HTTP wrapper server.
Keeps the same interface as client_mysql.py and client_postgresql.py
so benchmark.py does not need to change.
"""

import requests
from metrics import Timer, ScenarioResult, measure_connection
from datetime import date, datetime

DB = "sqlite"
BASE_URL = "http://127.0.0.1:5000"

def _json_safe(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat(sep=" ")
    if isinstance(value, tuple):
        return [_json_safe(v) for v in value]
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    return value


class SQLiteHTTPConnection:
    def __init__(self, base_url=BASE_URL, timeout=120):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def health(self):
        r = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def execute(self, query, params=None, fetch=False):
        payload = {
            "query": query,
            "params": _json_safe(params or []),
            "fetch": fetch
        }
        r = self.session.post(f"{self.base_url}/execute", json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def executemany(self, query, params):
        payload = {
            "query": query,
            "params": _json_safe(params)
        }
        r = self.session.post(f"{self.base_url}/executemany", json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def close(self):
        self.session.close()


def _connect():
    conn = SQLiteHTTPConnection()
    conn.health()
    return conn


def measure_connection_overhead() -> float:
    elapsed, conn = measure_connection(_connect)
    conn.close()
    return elapsed


# ── INSERT ────────────────────────────────────────────────────────────────────

def bench_bulk_insert(rows: list, batch_size: int = 1000) -> ScenarioResult:
    n = len(rows)
    result = ScenarioResult(db=DB, scenario=f"bulk_insert_{n}")
    conn = _connect()

    for _ in range(5):
        conn.execute(
            "DELETE FROM orders WHERE rowid IN (SELECT rowid FROM orders LIMIT ?)",
            [n],
            fetch=False
        )

        with Timer() as t:
            for i in range(0, n, batch_size):
                batch = rows[i:i + batch_size]
                conn.executemany(
                    "INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (?,?,?,?)",
                    batch
                )
        result.runs.append(t.elapsed_ms)

    conn.close()
    return result


# ── SELECT ────────────────────────────────────────────────────────────────────

def bench_select_where() -> ScenarioResult:
    result = ScenarioResult(db=DB, scenario="select_where")
    conn = _connect()

    for _ in range(5):
        with Timer() as t:
            conn.execute(
                "SELECT id, name, email FROM users WHERE created_at >= '2023-01-01' LIMIT 1000",
                fetch=True
            )
        result.runs.append(t.elapsed_ms)

    conn.close()
    return result


# ── JOIN ──────────────────────────────────────────────────────────────────────

def bench_complex_join() -> ScenarioResult:
    result = ScenarioResult(db=DB, scenario="complex_join")
    conn = _connect()

    query = """
        SELECT u.name, p.name AS product, o.quantity, o.order_date
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN products p ON o.product_id = p.id
        LIMIT 1000
    """

    for _ in range(5):
        with Timer() as t:
            conn.execute(query, fetch=True)
        result.runs.append(t.elapsed_ms)

    conn.close()
    return result


# ── AGGREGATION ───────────────────────────────────────────────────────────────

def bench_aggregation() -> ScenarioResult:
    result = ScenarioResult(db=DB, scenario="aggregation")
    conn = _connect()

    query = """
        SELECT p.category,
               COUNT(*) AS total_orders,
               SUM(o.quantity) AS total_qty,
               AVG(o.quantity) AS avg_qty
        FROM orders o
        JOIN products p ON o.product_id = p.id
        GROUP BY p.category
    """

    for _ in range(5):
        with Timer() as t:
            conn.execute(query, fetch=True)
        result.runs.append(t.elapsed_ms)

    conn.close()
    return result


# ── UPDATE / DELETE ───────────────────────────────────────────────────────────

def bench_update_delete() -> ScenarioResult:
    result = ScenarioResult(db=DB, scenario="update_delete")
    conn = _connect()

    for _ in range(5):
        with Timer() as t:
            conn.execute(
                "UPDATE orders SET quantity = quantity + 1 WHERE quantity < 3",
                fetch=False
            )
            conn.execute(
                "DELETE FROM orders WHERE order_date < '2022-01-01'",
                fetch=False
            )
        result.runs.append(t.elapsed_ms)

    conn.close()
    return result


def run_all() -> list:
    print("  Running SQLite benchmarks...")
    results = [
        bench_select_where(),
        bench_complex_join(),
        bench_aggregation(),
        bench_update_delete(),
    ]
    for r in results:
        print(f"    {r}")
    return results