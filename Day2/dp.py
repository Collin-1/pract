import sqlite3
from pathlib import Path

DB_PATH =Path("store.db")

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # results behave like dicts
    # Enforce foreing keys in SQLite
    conn.execute("PRAGMA foreing_keys = ON;")
    return conn

def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()

    # --- Tables ---
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('user','admin'))
    );

    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        price_cents INTEGER NOT NULL CHECK(price_cents >= 0),
        stock INTEGER NOT NULL CHECK(stock >= 0),
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','checked_out')),
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS cart_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        qty INTEGER NOT NULL CHECK(qty > 0),
        UNIQUE(cart_id, product_id),
        FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id)
    );

    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        cart_id INTEGER NOT NULL UNIQUE,
        total_cents INTEGER NOT NULL CHECK(total_cents >= 0),
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (cart_id) REFERENCES carts(id)
    );
""")
    
def seed_db() -> None:
    """Idempotent-ish seed: inserts only if tables are empty."""
    conn = get_conn()
    cur = conn.cursor()

    users_count = cur.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
    products_count = cur.execute("SELECT COUNT(*) AS c FROM products").fetchone()["c"]

    if users_count == 0:
        cur.execute(
            "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
            ("admin@example.com", "demo_hash_admin", "admin")
        )
        cur.execute(
            "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
            ("collin@example.com", "demo_hash_user", "user")
        )

    if products_count == 0:
        cur.executemany(
            "INSERT INTO products (sku, name, price_cents, stock) VALUES (?, ?, ?, ?)",
            [
                ("SKU-001", "Sneaker", 99900, 10),
                ("SKU-002", "Jacket", 149900, 5),
                ("SKU-003", "T-Shirt", 19900, 50),
                ("SKU-004", "Cap", 15900, 25),
            ]
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_db()
    print("✅ Database initialised and seeded: store.db")
