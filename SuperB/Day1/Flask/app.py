from flask import Flask, request,jsonify
from uuid import uuid4

app = Flask(__name__)
# "Database"
PRODUCTS = [
    {"id": "p1", "name": "Sneaker", "price": 999.0, "stock":5},
    {"id": "p2", "name": "Jacked", "price":1499.0, "stock":2},
]

CARTS = {} # cart_id -> list of items

# ---------- Web fundamentals: request/response + routing ----------

@app.get("/")
def home():
    # This is whAt a "GET /" request triggers
    return "Hello! This server is running.", 200

# ---------- REST: GET list + GET by id ----------

@app.get("/api/products")
def list_products():
    # GET /api/products
    return jsonify({"products": PRODUCTS}), 200

@app.get("/api/products/<product_id>")
def get_proudct(product_id: str):
    # GET /api/products/p1
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


# ---------- REST: POST create (status code 201) ----------

@app.post("/api/products")
def create_product():
    # POST /api/products with JSON body
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    # Validate (client error => 400)
    if not name or price is None or stock is None:
        return jsonify({
            "error": "Missing required fields: name, price, stock"
        }), 400
    
    # Create new product
    new_id = f"p{uuid4().hex[:6]}"
    product = {"id": new_id, "name": name, "price": float(price), "stock": int(stock)}
    PRODUCTS.append(product)

    # 201 Created
    return jsonify(product), 201

# ---------- Example: simple cart flow (e-commerce thinking) ----------
@app.post("/api/carts")
def create_cart():
    # POST /api/carts -> create a new cart
    cart_id = f"c{uuid4().hex[:8]}"
    CARTS[cart_id] = []
    return jsonify({"cart_id": cart_id, "items": []}), 201

@app.post("/api/carts/<cart_id>/items")
def add_cart_item(cart_id: str):
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    qty = int(data.get("qty", 1))

    if cart_id not in CARTS:
        return jsonify({"error": "Cart not found"}), 404
    
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Produt not found"}), 404
    
    if qty <= 0:
        return jsonify({"error": "qty must be >= 1"}), 400
    
    if product["stock"] < qty:
        return jsonify({"error": "Not enough stock"}), 409 # conflict
    
    # Add to cart
    CARTS[cart_id].append({"product_id": product_id, "qty": qty})
    return jsonify({"cart_id": cart_id, "items": CARTS[cart_id]}), 200



# ---------- Debugging helpers (very interview-relevant) ----------

@app.get("/debug/request-info")
def debug_request_ingo():
    # Shows basics of HTTP request data
    return jsonify({
        "method": request.method,
        "path":request.path,
        "headers":dict(request.headers),
        "query_params":request.args.to_dict
    })


if __name__ == "__main__":
    # Run dev server
    app.run(host="127.0.0.1", port=5000, debug=True)