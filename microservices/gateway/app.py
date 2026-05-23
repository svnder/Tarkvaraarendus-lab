import requests
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# ============================================
# API GATEWAY (Microservice)
# Serveerib veebilehte ja suunab päringud teenustele
# See on "sissepääsupunkt" mida kasutaja näeb
# Port: 5000
# ============================================

USERS_SERVICE = "http://users:5001"
PRODUCTS_SERVICE = "http://products:5002"
ORDERS_SERVICE = "http://orders:5003"


@app.route("/")
def index():
    # Kogume andmed kõigist teenustest
    users = []
    products = []
    orders = []
    services_status = {}

    try:
        resp = requests.get(f"{USERS_SERVICE}/users", timeout=2)
        users = resp.json().get("users", [])
        services_status["users"] = "online"
    except Exception:
        services_status["users"] = "offline"

    try:
        resp = requests.get(f"{PRODUCTS_SERVICE}/products", timeout=2)
        products = resp.json().get("products", [])
        services_status["products"] = "online"
    except Exception:
        services_status["products"] = "offline"

    try:
        resp = requests.get(f"{ORDERS_SERVICE}/orders", timeout=2)
        orders = resp.json().get("orders", [])
        services_status["orders"] = "online"
    except Exception:
        services_status["orders"] = "offline"

    return render_template("index.html",
                           users=users,
                           products=products,
                           orders=orders,
                           services=services_status)


# Proxy API päringuid teenustele
@app.route("/api/orders", methods=["POST"])
def create_order():
    try:
        resp = requests.post(f"{ORDERS_SERVICE}/orders",
                             json=request.get_json(),
                             timeout=5)
        return jsonify(resp.json()), resp.status_code
    except requests.ConnectionError:
        return jsonify({"error": "Tellimuste teenus ei ole kättesaadav!"}), 503


@app.route("/api/orders", methods=["GET"])
def get_orders():
    try:
        resp = requests.get(f"{ORDERS_SERVICE}/orders", timeout=2)
        return jsonify(resp.json())
    except requests.ConnectionError:
        return jsonify({"error": "Tellimuste teenus ei ole kättesaadav!"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
