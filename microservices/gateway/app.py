import requests
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

USERS_SERVICE = "http://users:5001"
PRODUCTS_SERVICE = "http://products:5002"
ORDERS_SERVICE = "http://orders:5003"
REVIEWS_SERVICE = "http://reviews:5004"


@app.route("/")
def index():
    users, products, orders = [], [], []
    services = {}

    for name, url, key in [
        ("users", f"{USERS_SERVICE}/users", "users"),
        ("products", f"{PRODUCTS_SERVICE}/products", "products"),
        ("orders", f"{ORDERS_SERVICE}/orders", "orders"),
    ]:
        try:
            resp = requests.get(url, timeout=2)
            locals()[key] if False else None
            if name == "users": users = resp.json().get("users", [])
            if name == "products": products = resp.json().get("products", [])
            if name == "orders": orders = resp.json().get("orders", [])
            services[name] = "online"
        except Exception:
            services[name] = "offline"

    try:
        requests.get(f"{REVIEWS_SERVICE}/reviews", timeout=2)
        services["reviews"] = "online"
    except Exception:
        services["reviews"] = "offline"

    return render_template("index.html",
                           users=users, products=products,
                           orders=orders, services=services)


@app.route("/api/orders", methods=["POST"])
def create_order():
    try:
        resp = requests.post(f"{ORDERS_SERVICE}/orders",
                             json=request.get_json(), timeout=5)
        return jsonify(resp.json()), resp.status_code
    except requests.ConnectionError:
        return jsonify({"error": "Tellimuste teenus ei ole kättesaadav!"}), 503


@app.route("/api/orders", methods=["GET"])
def get_orders():
    try:
        resp = requests.get(f"{ORDERS_SERVICE}/orders", timeout=2)
        return jsonify(resp.json())
    except requests.ConnectionError:
        return jsonify({"orders": []})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
