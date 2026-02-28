from flask import Flask, request, jsonify, session
from uuid import uuid4
from functools import wraps

app = Flask(__name__)

# Needed for session (cookie signing). In production, keep this secret.
app.secret_key = "dev-secret-key-change-me"

# Fake database
USERS = [
    # Never store plaintext passwords in real life.
    {"id": "u1", "email": "collin@example.com", "password": "Password123!", "role": "user"},
    {"id": "u2", "email": "admin@example.com", "password": "Admin123!", "role": "admin"},
]

PRODUCTS = [
    {"id": "p1", "name": "Sneaker", "price": 999.0, "stock": 5},
    {"id": "p2", "name": "Jacket", "price": 1499.0, "stock": 2},
]

CARTS = {}  # cart_id -> list of items


# -------------------------
# Helpers
# -------------------------

def login_required(fn):
    """require a user to be logged in via session cookie."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized (log in first)"}), 401
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    """require admin role via session."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "Unauthorized (log in first)"}), 401
        user = next((u for u in USERS if u["id"] == user_id), None)
        if not user or user["role"] != "admin":
            return jsonify({"error": "Forbidden (admin only)"}), 403
        
        return fn(*args, **kwargs)
    return wrapper


# -------------------------
# Routes
# -------------------------
@app.get("/")
def home():
    return "Hello! Server running.", 200

# -------- Session Auth: Login / Logout / Me --------
@app.post("/auth/login")
def login():
    """
    POST /auth/login
    Body: { "email": "...", "password": "..." }

    On success:
      - server stores user_id in session
      - browser receives session cookie automatically
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password =data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"})
    
    user = next((u for u in USERS if u["email"] == email and u["password"] == password), None)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Create session
    session["user_id"] = user["id"]
    session["role"] = user["role"]

    return jsonify({"message": "Logged in", "user_id": user["id"], "role": user["role"]}), 200

@app.post("/auth/logout")
def logout():
    session.clear()
    return jsonify({"message": "logged out"}), 200

@app.get("/auth/me")
@login_required
def me():
    user_id = session["user_id"]
    user = next((u for u in USERS if u["id"] == user_id), None)
    return jsonify({"id": user["id"], "email": user["email"], "role": user["role"]}), 200

# -------- Products --------
@app.get("/api/products")
def list_products():
    return jsonify({"products": PRODUCTS}), 200

@app.get("/api/products/<product_id>")
def get_product(product_id: str):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

# Only admin can create products (demo of auth + authorization)
@app.post("/api/products")
@admin_required
def create_product():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not name or price is None or stock is None:
        return jsonify("error": "Missing required fields: name, price, stock"), 400
    
    new_id = f"p{uuid4().hex[:6]}"
    product = {"id": new_id, "name": name, "price": float(price), "stock": int(stock)}
    PRODUCTS.append(product)
    return jsonify(product), 201


# -------- Cart (requires login) --------
@app.post("/api/carts")
@login_required
def create_cart():
    cart_id=f"c{uuid4().hex[:8]}"
    CARTS[cart_id] = []
    return jsonify({"cart_id":cart_id, "items":[]}), 200

@app.post("/app/carts/<cart_id>/items")
@login_required
def add_cart_item(cart_id: str):
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    qty = int(data.get("qty", 1))

    if cart_id not in CARTS:
        return jsonify({"error": "Cart not found"}), 404
    
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    if qty <= 0:
        return jsonify({"error": "qty must be >= 1"}), 400
    
    if product["stock"] < qty:
        return jsonify({"error": "Not enough stock"}), 409
    
    CARTS[cart_id].append({"product_id": product_id, "qty": qty})
    return jsonify({"cart_id": cart_id, "items": CARTS[cart_id]}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
    

    
