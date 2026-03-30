from flask import Flask, request, jsonify
import sqlite3
from db import get_conn, init_db, seed_db

app = Flask(__name__)

@app.before_first_request
def setup():
    init_db()
    seed_db()

# -----------------------
# Helpers
# -----------------------
def row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row) if row else {}

def rows_to_list(rows) -> list[dict]:
    return [dict(r) for r in rows]

def clamp_int(value, default, min_v, max_v):
    try:
        v = int(value)
    except (TypeError, ValueError):
        v = default
    return max(min_v, min(max_v, v))

# -----------------------
# 1) Products: pagination + search + ordering
# -----------------------
@app.get("/api/products")
def list_products():
    """
    GET /api/products?page=1&page_size=10&q=sneak&sort=created_desc
    """
    page = clamp_int(request.args.get("page"), default=1, min_v=1, max_v=10_000)
    page_size = clamp_int(request.args.get("page_size"), default=10, min_v=1, max_v=50)
    q = (request.args.get("q") or "").strip()
    sort = (request.args.get("sort") or "created_desc").strip()

    offset = (page - 1) * page_size

    order_by = "created_at DESC"
    if sort == "price_asc":
        order_by = "price_cents ASC"
    elif sort == "price_desc":
        order_by = "price_cents DESC"
    elif sort == "created_asc":
        order_by = "created_at ASC"

    conn = get_conn()
    cur = conn.cursor()

    params = []
    where = ""
    if q:
        # Parameterized query prevents SQL injection
        where = "WHERE name LIKE ? OR sku LIKE ?"
        like = f"%{q}%"
        params.extend([like, like])

    total = cur.execute(
        f"SELECT COUNT(*) AS c FROM products {where}",
        params
    ).fetchone()["c"]

    rows = cur.execute(
        f"""
        SELECT id, sku, name, price_cents, stock, created_at
        FROM products
        {where}
        ORDER BY {order_by}
        LIMIT ? OFFSET ?
        """,
        params + [page_size, offset]
    ).fetchall()

    conn.close()

    return jsonify({
        "page": page,
        "page_size": page_size,
        "total": total,
        "products": rows_to_list(rows)
    }), 200

# -----------------------
# 2) Create cart for a user
# -----------------------
@app.post("/api/carts")
def create_cart():
    """
    POST /api/carts
    Body: { "user_email": "collin@example.com" }
    """
    data = request.get_json(silent=True) or {}
    email = data.get("user_email")
    if not email:
        return jsonify({"error": "user_email required"}), 400

    conn = get_conn()
    cur = conn.cursor()

    user = cur.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    cur.execute("INSERT INTO carts (user_id) VALUES (?)", (user["id"],))
    cart_id = cur.lastrowid
    conn.commit()
    conn.close()

    return jsonify({"cart_id": cart_id, "status": "open"}), 201

# -----------------------
# 3) Add / update cart items (UPSERT)
# -----------------------
@app.post("/api/carts/<int:cart_id>/items")
def add_or_update_item(cart_id: int):
    """
    POST /api/carts/1/items
    Body: { "product_id": 1, "qty": 2 }
    """
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    qty = data.get("qty")

    if product_id is None or qty is None:
        return jsonify({"error": "product_id and qty required"}), 400
    try:
        product_id = int(product_id)
        qty = int(qty)
    except ValueError:
        return jsonify({"error": "product_id and qty must be integers"}), 400
    if qty <= 0:
        return jsonify({"error": "qty must be >= 1"}), 400

    conn = get_conn()
    cur = conn.cursor()

    cart = cur.execute("SELECT id, status FROM carts WHERE id = ?", (cart_id,)).fetchone()
    if not cart:
        conn.close()
        return jsonify({"error": "Cart not found"}), 404
    if cart["status"] != "open":
        conn.close()
        return jsonify({"error": "Cart already checked out"}), 409

    product = cur.execute("SELECT id, stock FROM products WHERE id = ?", (product_id,)).fetchone()
    if not product:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    # Upsert cart item
    cur.execute(
        """
        INSERT INTO cart_items (cart_id, product_id, qty)
        VALUES (?, ?, ?)
        ON CONFLICT(cart_id, product_id)
        DO UPDATE SET qty = excluded.qty
        """,
        (cart_id, product_id, qty)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Item set", "cart_id": cart_id, "product_id": product_id, "qty": qty}), 200

# -----------------------
# 4) View cart with JOIN (this is where JOINs become real)
# -----------------------
@app.get("/api/carts/<int:cart_id>")
def view_cart(cart_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cart = cur.execute(
        """
        SELECT c.id, c.status, u.email AS user_email, c.created_at
        FROM carts c
        JOIN users u ON u.id = c.user_id
        WHERE c.id = ?
        """,
        (cart_id,)
    ).fetchone()

    if not cart:
        conn.close()
        return jsonify({"error": "Cart not found"}), 404

    items = cur.execute(
        """
        SELECT
            ci.product_id,
            p.sku,
            p.name,
            p.price_cents,
            ci.qty,
            (p.price_cents * ci.qty) AS line_total_cents
        FROM cart_items ci
        JOIN products p ON p.id = ci.product_id
        WHERE ci.cart_id = ?
        ORDER BY p.name ASC
        """,
        (cart_id,)
    ).fetchall()

    total = sum(r["line_total_cents"] for r in items)

    conn.close()

    return jsonify({
        "cart": row_to_dict(cart),
        "items": rows_to_list(items),
        "total_cents": total
    }), 200

# -----------------------
# 5) Checkout with TRANSACTION (atomic stock update + order creation)
# -----------------------
@app.post("/api/carts/<int:cart_id>/checkout")
def checkout(cart_id: int):
    """
    This demonstrates a transaction:
    - verify stock
    - decrease stock
    - create order
    - mark cart checked_out
    If any step fails => rollback.
    """
    conn = get_conn()
    cur = conn.cursor()

    try:
        # BEGIN transaction
        conn.execute("BEGIN;")

        cart = cur.execute("SELECT id, user_id, status FROM carts WHERE id = ?", (cart_id,)).fetchone()
        if not cart:
            conn.execute("ROLLBACK;")
            conn.close()
            return jsonify({"error": "Cart not found"}), 404
        if cart["status"] != "open":
            conn.execute("ROLLBACK;")
            conn.close()
            return jsonify({"error": "Cart already checked out"}), 409

        items = cur.execute(
            """
            SELECT ci.product_id, ci.qty, p.stock, p.price_cents
            FROM cart_items ci
            JOIN products p ON p.id = ci.product_id
            WHERE ci.cart_id = ?
            """,
            (cart_id,)
        ).fetchall()

        if not items:
            conn.execute("ROLLBACK;")
            conn.close()
            return jsonify({"error": "Cart is empty"}), 400

        # 1) Verify stock
        for r in items:
            if r["stock"] < r["qty"]:
                conn.execute("ROLLBACK;")
                conn.close()
                return jsonify({
                    "error": "Insufficient stock",
                    "product_id": r["product_id"],
                    "available": r["stock"],
                    "requested": r["qty"]
                }), 409

        # 2) Deduct stock (safe because we are inside a transaction)
        for r in items:
            cur.execute(
                "UPDATE products SET stock = stock - ? WHERE id = ?",
                (r["qty"], r["product_id"])
            )

        # 3) Create order
        total_cents = sum(r["price_cents"] * r["qty"] for r in items)
        cur.execute(
            "INSERT INTO orders (user_id, cart_id, total_cents) VALUES (?, ?, ?)",
            (cart["user_id"], cart_id, total_cents)
        )
        order_id = cur.lastrowid

        # 4) Mark cart checked out
        cur.execute("UPDATE carts SET status = 'checked_out' WHERE id = ?", (cart_id,))

        # COMMIT transaction
        conn.commit()
        conn.close()

        return jsonify({"message": "Checked out", "order_id": order_id, "total_cents": total_cents}), 201

    except Exception as e:
        conn.execute("ROLLBACK;")
        conn.close()
        return jsonify({"error": "Checkout failed", "details": str(e)}), 500

# -----------------------
# 6) EXPLAIN query plan (beginner performance skill)
# -----------------------
@app.get("/debug/explain/products-search")
def explain_products_search():
    """
    GET /debug/explain/products-search?q=Sneaker
    Shows if indexes are being used.
    """
    q = (request.args.get("q") or "").strip()
    like = f"%{q}%"

    conn = get_conn()
    cur = conn.cursor()

    plan = cur.execute(
        """
        EXPLAIN QUERY PLAN
        SELECT id, sku, name FROM products
        WHERE name LIKE ? OR sku LIKE ?
        ORDER BY created_at DESC
        LIMIT 10
        """,
        (like, like)
    ).fetchall()

    conn.close()
    return jsonify({"query": "products search", "plan": [dict(r) for r in plan]}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)