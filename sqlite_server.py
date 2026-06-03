from flask import Flask, request, jsonify
import sqlite3
import time

DB_PATH = "benchmark.db"
app = Flask(__name__)


def run_query(query, params=None, fetch=False, many=False):
    params = params or []
    start = time.perf_counter()

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        if many:
            cur.executemany(query, params)
            conn.commit()
            rows = []
        else:
            cur.execute(query, params)
            rows = cur.fetchall() if fetch else []
            conn.commit()

    elapsed_ms = (time.perf_counter() - start) * 1000
    return rows, elapsed_ms


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/execute")
def execute():
    data = request.get_json(force=True)
    query = data.get("query")
    params = data.get("params", [])
    fetch = bool(data.get("fetch", False))

    rows, elapsed_ms = run_query(query, params=params, fetch=fetch, many=False)
    return jsonify({"rows": rows, "elapsed_ms": elapsed_ms})


@app.post("/executemany")
def executemany():
    data = request.get_json(force=True)
    query = data.get("query")
    params = data.get("params", [])

    rows, elapsed_ms = run_query(query, params=params, fetch=False, many=True)
    return jsonify({"rows": rows, "elapsed_ms": elapsed_ms})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)