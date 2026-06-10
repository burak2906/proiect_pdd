"""
client_postgresql.py
PostgreSQL benchmark client.
Uses psycopg2 (DB-API 2.0).
"""

import psycopg2
import psycopg2.extras
from metrics import Timer, ScenarioResult, ResourceMonitor, measure_connection

PG_CONFIG = {
    "host":     "127.0.0.1",
    "port":     5432,
    "user":     "benchmark_user",
    "password": "benchmark_pass",
    "dbname":   "benchmark_db",
}

DB = "postgresql"


def _connect():
    return psycopg2.connect(**PG_CONFIG)


def measure_connection_overhead() -> float:
    elapsed, conn = measure_connection(_connect)
    conn.close()
    return elapsed


def bench_bulk_insert(rows: list, batch_size: int = 1000) -> ScenarioResult:
    n = len(rows)
    result = ScenarioResult(db=DB, scenario=f"bulk_insert_{n}")
    conn = _connect()
    conn.autocommit = False
    cur  = conn.cursor()

    with ResourceMonitor() as rm:
        for _ in range(5):
            cur.execute("DELETE FROM orders WHERE ctid IN "
                        "(SELECT ctid FROM orders LIMIT %s)", (n,))
            conn.commit()
            with Timer() as t:
                psycopg2.extras.execute_batch(
                    cur,
                    "INSERT INTO orders (user_id, product_id, quantity, order_date) "
                    "VALUES (%s,%s,%s,%s)",
                    rows,
                    page_size=batch_size,
                )
                conn.commit()
            result.runs.append(t.elapsed_ms)

    result.cpu_percent = rm.cpu_percent
    result.memory_delta_mb = rm.memory_delta_mb
    cur.close()
    conn.close()
    return result


def bench_select_where() -> ScenarioResult:
    result = ScenarioResult(db=DB, scenario="select_where")
    conn = _connect()
    cur  = conn.cursor()

    with ResourceMonitor() as rm:
        for _ in range(5):
            with Timer() as t:
                cur.execute(
                    "SELECT id, name, email FROM users "
                    "WHERE created_at >= '2023-01-01' LIMIT 1000"
                )
                cur.fetchall()
            result.runs.append(t.elapsed_ms)

    result.cpu_percent = rm.cpu_percent
    result.memory_delta_mb = rm.memory_delta_mb
    cur.close()
    conn.close()
    return result


def bench_complex_join() -> ScenarioResult:
    result = ScenarioResult(db=DB, scenario="complex_join")
    conn = _connect()
    cur  = conn.cursor()

    with ResourceMonitor() as rm:
        for _ in range(5):
            with Timer() as t:
                cur.execute("""
                    SELECT u.name, p.name AS product, o.quantity, o.order_date
                    FROM orders o
                    JOIN users    u ON o.user_id    = u.id
                    JOIN products p ON o.product_id = p.id
                    LIMIT 1000
                """)
                cur.fetchall()
            result.runs.append(t.elapsed_ms)

    result.cpu_percent = rm.cpu_percent
    result.memory_delta_mb = rm.memory_delta_mb
    cur.close()
    conn.close()
    return result


def bench_aggregation() -> ScenarioResult:
    result = ScenarioResult(db=DB, scenario="aggregation")
    conn = _connect()
    cur  = conn.cursor()

    with ResourceMonitor() as rm:
        for _ in range(5):
            with Timer() as t:
                cur.execute("""
                    SELECT p.category,
                           COUNT(*)        AS total_orders,
                           SUM(o.quantity) AS total_qty,
                           AVG(o.quantity) AS avg_qty
                    FROM orders o
                    JOIN products p ON o.product_id = p.id
                    GROUP BY p.category
                """)
                cur.fetchall()
            result.runs.append(t.elapsed_ms)

    result.cpu_percent = rm.cpu_percent
    result.memory_delta_mb = rm.memory_delta_mb
    cur.close()
    conn.close()
    return result


def bench_update_delete() -> ScenarioResult:
    result = ScenarioResult(db=DB, scenario="update_delete")
    conn = _connect()
    conn.autocommit = False
    cur  = conn.cursor()

    with ResourceMonitor() as rm:
        for _ in range(5):
            with Timer() as t:
                cur.execute(
                    "UPDATE orders SET quantity = quantity + 1 "
                    "WHERE quantity < 3"
                )
                cur.execute(
                    "DELETE FROM orders "
                    "WHERE order_date < '2022-01-01'"
                )
                conn.commit()
            result.runs.append(t.elapsed_ms)

    result.cpu_percent = rm.cpu_percent
    result.memory_delta_mb = rm.memory_delta_mb
    cur.close()
    conn.close()
    return result