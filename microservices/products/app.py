from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {"id": 1, "name": "Sülearvuti", "price": 899.99, "emoji": "💻"},
    {"id": 2, "name": "Hiir", "price": 29.99, "emoji": "🖱️"},
    {"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},
]


@app.route("/", methods=["GET"])
def index():
    return jsonify({"service": "Toodete teenus", "port": 5002})


@app.route("/products", methods=["GET"])
def get_products():
    return jsonify({"products": products})


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Toodet ei leitud"}), 404
    return jsonify(product)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
