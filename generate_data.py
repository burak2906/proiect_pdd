"""
generate_data.py
Generates synthetic e-commerce data using Faker and loads it into
MySQL, PostgreSQL, and SQLite databases.

Schema (from paper Table 2):
  users    -> 100,000 records
  products ->  50,000 records
  orders   -> 1,000,000 records (FK to users and products)
"""

import random
import time
import sqlite3
import os
from faker import Faker
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
NUM_USERS    = 100_000
NUM_PRODUCTS =  50_000
NUM_ORDERS   = 1_000_000

SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark.db")

MYSQL_CONFIG = {
    "host":     "127.0.0.1",
    "port":     3306,
    "user":     "benchmark_user",
    "password": "benchmark_pass",
    "database": "benchmark_db",
}

PG_CONFIG = {
    "host":     "127.0.0.1",
    "port":     5432,
    "user":     "benchmark_user",
    "password": "benchmark_pass",
    "dbname":   "benchmark_db",
}

BATCH_SIZE = 5_000   # rows per executemany call

fake = Faker()
Faker.seed(42)
random.seed(42)

# ---------------------------------------------------------------------------
# Data generation helpers
# ---------------------------------------------------------------------------

def gen_users(n: int):
    """Yield (name, email, created_at) tuples."""
    for _ in range(n):
        created = fake.date_time_between(start_date="-5y", end_date="now")
        yield (fake.name(), fake.unique.email(), created)

def gen_products(n: int):
    """Yield (name, price, category) tuples."""
    categories = ["Electronics", "Books", "Clothing", "Home", "Sports",
                  "Beauty", "Toys", "Food", "Garden", "Automotive"]
    for _ in range(n):
        yield (
            fake.catch_phrase()[:120],
            round(random.uniform(0.99, 999.99), 2),
            random.choice(categories),
        )

def gen_orders(n: int, max_user_id: int, max_product_id: int):
    """Yield (user_id, product_id, quantity, order_date) tuples."""
    for _ in range(n):
        yield (
            random.randint(1, max_user_id),
            random.randint(1, max_product_id),
            random.randint(1, 10),
            fake.date_time_between(start_date="-3y", end_date="now"),
        )

# ---------------------------------------------------------------------------
# DDL helpers
# ---------------------------------------------------------------------------

DDL_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY {auto},
    name       VARCHAR(200) NOT NULL,
    email      VARCHAR(200) NOT NULL UNIQUE,
    created_at DATETIME     NOT NULL
);"""

DDL_PRODUCTS = """
CREATE TABLE IF NOT EXISTS products (
    id       INTEGER PRIMARY KEY {auto},
    name     VARCHAR(200) NOT NULL,
    price    DECIMAL(10,2) NOT NULL,
    category VARCHAR(100) NOT NULL
);"""

DDL_ORDERS = """
CREATE TABLE IF NOT EXISTS orders (
    id         INTEGER PRIMARY KEY {auto},
    user_id    INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity   INTEGER NOT NULL,
    order_date DATETIME NOT NULL,
    FOREIGN KEY (user_id)    REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);"""

def ddl(template: str, dialect: str) -> str:
    """Fill AUTO_INCREMENT / SERIAL / AUTOINCREMENT placeholder."""
    mapping = {
        "mysql":    "AUTO_INCREMENT",
        "postgres": "",          # SERIAL is used in column type instead
        "sqlite":   "AUTOINCREMENT",
    }
    return template.format(auto=mapping[dialect])


# ---------------------------------------------------------------------------
# SQLite
# ---------------------------------------------------------------------------

def load_sqlite():
    print("\n=== SQLite ===")
    if os.path.exists(SQLITE_DB_PATH):
        os.remove(SQLITE_DB_PATH)
        print("  Removed old database.")

    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    cur = conn.cursor()

    cur.execute(ddl(DDL_USERS, "sqlite"))
    cur.execute(ddl(DDL_PRODUCTS, "sqlite"))
    cur.execute(ddl(DDL_ORDERS, "sqlite"))
    conn.commit()
    print("  Tables created.")

    # users
    t0 = time.perf_counter()
    users_data = list(gen_users(NUM_USERS))
    for i in range(0, NUM_USERS, BATCH_SIZE):
        cur.executemany(
            "INSERT INTO users (name, email, created_at) VALUES (?,?,?)",
            users_data[i:i+BATCH_SIZE],
        )
    conn.commit()
    print(f"  users inserted:    {NUM_USERS:,}  ({time.perf_counter()-t0:.1f}s)")

    # products
    t0 = time.perf_counter()
    products_data = list(gen_products(NUM_PRODUCTS))
    for i in range(0, NUM_PRODUCTS, BATCH_SIZE):
        cur.executemany(
            "INSERT INTO products (name, price, category) VALUES (?,?,?)",
            products_data[i:i+BATCH_SIZE],
        )
    conn.commit()
    print(f"  products inserted: {NUM_PRODUCTS:,}  ({time.perf_counter()-t0:.1f}s)")

    # orders (generated in streaming chunks to save RAM)
    t0 = time.perf_counter()
    total = 0
    chunk = []
    for row in gen_orders(NUM_ORDERS, NUM_USERS, NUM_PRODUCTS):
        chunk.append(row)
        if len(chunk) == BATCH_SIZE:
            cur.executemany(
                "INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (?,?,?,?)",
                chunk,
            )
            conn.commit()
            total += len(chunk)
            chunk = []
    if chunk:
        cur.executemany(
            "INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (?,?,?,?)",
            chunk,
        )
        conn.commit()
        total += len(chunk)
    print(f"  orders inserted:   {total:,}  ({time.perf_counter()-t0:.1f}s)")

    conn.close()
    print("  SQLite done ✓")


# ---------------------------------------------------------------------------
# MySQL
# ---------------------------------------------------------------------------

def load_mysql():
    print("\n=== MySQL ===")
    try:
        import mysql.connector
    except ImportError:
        print("  mysql-connector-python not installed. Skipping.")
        return

    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cur  = conn.cursor()

    for tbl in ("orders", "products", "users"):
        cur.execute(f"DROP TABLE IF EXISTS {tbl}")
    conn.commit()

    mysql_users = """
    CREATE TABLE users (
        id         INT AUTO_INCREMENT PRIMARY KEY,
        name       VARCHAR(200) NOT NULL,
        email      VARCHAR(200) NOT NULL UNIQUE,
        created_at DATETIME     NOT NULL
    );"""
    mysql_products = """
    CREATE TABLE products (
        id       INT AUTO_INCREMENT PRIMARY KEY,
        name     VARCHAR(200) NOT NULL,
        price    DECIMAL(10,2) NOT NULL,
        category VARCHAR(100) NOT NULL
    );"""
    mysql_orders = """
    CREATE TABLE orders (
        id         INT AUTO_INCREMENT PRIMARY KEY,
        user_id    INT NOT NULL,
        product_id INT NOT NULL,
        quantity   INT NOT NULL,
        order_date DATETIME NOT NULL,
        FOREIGN KEY (user_id)    REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    );"""
    cur.execute(mysql_users)
    cur.execute(mysql_products)
    cur.execute(mysql_orders)
    conn.commit()
    print("  Tables created.")

    t0 = time.perf_counter()
    users_data = list(gen_users(NUM_USERS))
    for i in range(0, NUM_USERS, BATCH_SIZE):
        cur.executemany(
            "INSERT INTO users (name, email, created_at) VALUES (%s,%s,%s)",
            users_data[i:i+BATCH_SIZE],
        )
    conn.commit()
    print(f"  users inserted:    {NUM_USERS:,}  ({time.perf_counter()-t0:.1f}s)")

    t0 = time.perf_counter()
    products_data = list(gen_products(NUM_PRODUCTS))
    for i in range(0, NUM_PRODUCTS, BATCH_SIZE):
        cur.executemany(
            "INSERT INTO products (name, price, category) VALUES (%s,%s,%s)",
            products_data[i:i+BATCH_SIZE],
        )
    conn.commit()
    print(f"  products inserted: {NUM_PRODUCTS:,}  ({time.perf_counter()-t0:.1f}s)")

    t0 = time.perf_counter()
    total = 0
    chunk = []
    for row in gen_orders(NUM_ORDERS, NUM_USERS, NUM_PRODUCTS):
        chunk.append(row)
        if len(chunk) == BATCH_SIZE:
            cur.executemany(
                "INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (%s,%s,%s,%s)",
                chunk,
            )
            conn.commit()
            total += len(chunk)
            chunk = []
    if chunk:
        cur.executemany(
            "INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (%s,%s,%s,%s)",
            chunk,
        )
        conn.commit()
        total += len(chunk)
    print(f"  orders inserted:   {total:,}  ({time.perf_counter()-t0:.1f}s)")

    cur.close()
    conn.close()
    print("  MySQL done ✓")


# ---------------------------------------------------------------------------
# PostgreSQL
# ---------------------------------------------------------------------------

def load_postgresql():
    print("\n=== PostgreSQL ===")
    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        print("  psycopg2-binary not installed. Skipping.")
        return

    conn = psycopg2.connect(**PG_CONFIG)
    conn.autocommit = False
    cur  = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS orders")
    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("DROP TABLE IF EXISTS users")
    conn.commit()

    cur.execute("""
    CREATE TABLE users (
        id         SERIAL PRIMARY KEY,
        name       VARCHAR(200) NOT NULL,
        email      VARCHAR(200) NOT NULL UNIQUE,
        created_at TIMESTAMP    NOT NULL
    );""")
    cur.execute("""
    CREATE TABLE products (
        id       SERIAL PRIMARY KEY,
        name     VARCHAR(200) NOT NULL,
        price    NUMERIC(10,2) NOT NULL,
        category VARCHAR(100) NOT NULL
    );""")
    cur.execute("""
    CREATE TABLE orders (
        id         SERIAL PRIMARY KEY,
        user_id    INTEGER NOT NULL REFERENCES users(id),
        product_id INTEGER NOT NULL REFERENCES products(id),
        quantity   INTEGER NOT NULL,
        order_date TIMESTAMP NOT NULL
    );""")
    conn.commit()
    print("  Tables created.")

    t0 = time.perf_counter()
    users_data = list(gen_users(NUM_USERS))
    for i in range(0, NUM_USERS, BATCH_SIZE):
        psycopg2.extras.execute_batch(
            cur,
            "INSERT INTO users (name, email, created_at) VALUES (%s,%s,%s)",
            users_data[i:i+BATCH_SIZE],
            page_size=BATCH_SIZE,
        )
    conn.commit()
    print(f"  users inserted:    {NUM_USERS:,}  ({time.perf_counter()-t0:.1f}s)")

    t0 = time.perf_counter()
    products_data = list(gen_products(NUM_PRODUCTS))
    for i in range(0, NUM_PRODUCTS, BATCH_SIZE):
        psycopg2.extras.execute_batch(
            cur,
            "INSERT INTO products (name, price, category) VALUES (%s,%s,%s)",
            products_data[i:i+BATCH_SIZE],
            page_size=BATCH_SIZE,
        )
    conn.commit()
    print(f"  products inserted: {NUM_PRODUCTS:,}  ({time.perf_counter()-t0:.1f}s)")

    t0 = time.perf_counter()
    total = 0
    chunk = []
    for row in gen_orders(NUM_ORDERS, NUM_USERS, NUM_PRODUCTS):
        chunk.append(row)
        if len(chunk) == BATCH_SIZE:
            psycopg2.extras.execute_batch(
                cur,
                "INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (%s,%s,%s,%s)",
                chunk,
                page_size=BATCH_SIZE,
            )
            conn.commit()
            total += len(chunk)
            chunk = []
    if chunk:
        psycopg2.extras.execute_batch(
            cur,
            "INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (%s,%s,%s,%s)",
            chunk,
            page_size=BATCH_SIZE,
        )
        conn.commit()
        total += len(chunk)
    print(f"  orders inserted:   {total:,}  ({time.perf_counter()-t0:.1f}s)")

    cur.close()
    conn.close()
    print("  PostgreSQL done ✓")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Load benchmark data into databases.")
    parser.add_argument("--sqlite",   action="store_true", help="Load SQLite")
    parser.add_argument("--mysql",    action="store_true", help="Load MySQL")
    parser.add_argument("--postgres", action="store_true", help="Load PostgreSQL")
    parser.add_argument("--all",      action="store_true", help="Load all three")
    args = parser.parse_args()

    if not any([args.sqlite, args.mysql, args.postgres, args.all]):
        parser.print_help()
    else:
        t_start = time.perf_counter()
        if args.all or args.sqlite:
            load_sqlite()
        if args.all or args.mysql:
            load_mysql()
        if args.all or args.postgres:
            load_postgresql()
        print(f"\nTotal time: {time.perf_counter()-t_start:.1f}s")