import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

USERS_SERVICE = "http://users:5001"
PRODUCTS_SERVICE = "http://products:5002"

orders = []
next_order_id = 1


@app.route("/", methods=["GET"])
def index():
    return jsonify({"service": "Tellimuste teenus", "port": 5003})


@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify({"orders": orders})


@app.route("/orders", methods=["POST"])
def create_order():
    global next_order_id
    data = request.get_json()

    if not data or "user_id" not in data or "product_id" not in data:
        return jsonify({"error": "Vajalikud väljad: user_id, product_id, quantity"}), 400

    try:
        user_resp = requests.get(f"{USERS_SERVICE}/users/{data['user_id']}")
        if user_resp.status_code != 200:
            return jsonify({"error": "Kasutajat ei leitud"}), 404
        user = user_resp.json()
    except requests.ConnectionError:
        return jsonify({"error": "Kasutajate teenus ei ole kättesaadav!"}), 503

    try:
        product_resp = requests.get(f"{PRODUCTS_SERVICE}/products/{data['product_id']}")
        if product_resp.status_code != 200:
            return jsonify({"error": "Toodet ei leitud"}), 404
        product = product_resp.json()
    except requests.ConnectionError:
        return jsonify({"error": "Toodete teenus ei ole kättesaadav!"}), 503

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
    app.run(host="0.0.0.0", port=5003, debug=True)
