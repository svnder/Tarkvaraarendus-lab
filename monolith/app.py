from flask import Flask, jsonify, request

app = Flask(__name__)

# ============================================
# MONOLIITNE RAKENDUS
# Kõik on ühes failis: kasutajad, tooted, tellimused
# ============================================

# "Andmebaas" - lihtsuse mõttes hoiame mälus
users = [
    {"id": 1, "name": "Mari Maasikas", "email": "mari@example.com"},
    {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},
]

products = [
    {"id": 1, "name": "Sülearvuti", "price": 899.99},
    {"id": 2, "name": "Hiir", "price": 29.99},
    {"id": 3, "name": "Klaviatuur", "price": 79.99},
]

orders = []
next_order_id = 1


# ---------- KASUTAJAD ----------

@app.route("/")
def index():
    return jsonify({
        "app": "Monoliitne e-pood",
        "endpoints": {
            "kasutajad": "/users",
            "tooted": "/products",
            "tellimused": "/orders",
            "tellimuse_loomine": "POST /orders (JSON: user_id, product_id, quantity)"
        }
    })


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"users": users})


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "Kasutajat ei leitud"}), 404
    return jsonify(user)


# ---------- TOOTED ----------

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify({"products": products})


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Toodet ei leitud"}), 404
    return jsonify(product)


# ---------- TELLIMUSED ----------

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify({"orders": orders})


@app.route("/orders", methods=["POST"])
def create_order():
    global next_order_id
    data = request.get_json()

    if not data or "user_id" not in data or "product_id" not in data:
        return jsonify({"error": "Vajalikud väljad: user_id, product_id, quantity"}), 400

    # Kontrollime kasutajat
    user = next((u for u in users if u["id"] == data["user_id"]), None)
    if not user:
        return jsonify({"error": "Kasutajat ei leitud"}), 404

    # Kontrollime toodet
    product = next((p for p in products if p["id"] == data["product_id"]), None)
    if not product:
        return jsonify({"error": "Toodet ei leitud"}), 404

    quantity = data.get("quantity", 1)
    total = product["price"] * quantity

    order = {
        "id": next_order_id,
        "user": user["name"],
        "product": product["name"],
        "quantity": quantity,
        "total": total,
        "status": "created"
    }
    orders.append(order)
    next_order_id += 1

    return jsonify({"message": "Tellimus loodud!", "order": order}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
