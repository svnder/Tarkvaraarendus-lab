from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# ============================================
# MONOLIITNE RAKENDUS
# Kõik on ühes failis: kasutajad, tooted, tellimused
# ============================================

users = [
    {"id": 1, "name": "Mari Maasikas", "email": "mari@example.com"},
    {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},
]

products = [
    {"id": 1, "name": "Sülearvuti", "price": 899.99, "emoji": "💻"},
    {"id": 2, "name": "Hiir", "price": 29.99, "emoji": "🖱️"},
    {"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},
]

orders = []
next_order_id = 1


@app.route("/")
def index():
    return render_template("index.html", users=users, products=products, orders=orders)


@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify({"users": users})


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "Kasutajat ei leitud"}), 404
    return jsonify(user)


@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify({"products": products})


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Toodet ei leitud"}), 404
    return jsonify(product)


@app.route("/api/orders", methods=["GET"])
def get_orders():
    return jsonify({"orders": orders})


@app.route("/api/orders", methods=["POST"])
def create_order():
    global next_order_id
    data = request.get_json()

    if not data or "user_id" not in data or "product_id" not in data:
        return jsonify({"error": "Vajalikud väljad: user_id, product_id, quantity"}), 400

    user = next((u for u in users if u["id"] == data["user_id"]), None)
    if not user:
        return jsonify({"error": "Kasutajat ei leitud"}), 404

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
        "total": round(total, 2),
        "status": "created"
    }
    orders.append(order)
    next_order_id += 1

    return jsonify({"message": "Tellimus loodud!", "order": order}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
