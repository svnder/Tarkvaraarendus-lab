import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# ============================================
# ARVUSTUSTE TEENUS (Microservice)
# Vastutab tootearvustuste eest
# Suhtleb toodete ja kasutajate teenusega
# Port: 5004
# ============================================

USERS_SERVICE = "http://users:5001"
PRODUCTS_SERVICE = "http://products:5002"

reviews = []
next_review_id = 1


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Arvustuste teenus",
        "port": 5004,
        "depends_on": ["users:5001", "products:5002"]
    })


@app.route("/reviews", methods=["GET"])
def get_reviews():
    return jsonify({"reviews": reviews})


@app.route("/reviews/product/<int:product_id>", methods=["GET"])
def get_product_reviews(product_id):
    product_reviews = [r for r in reviews if r["product_id"] == product_id]
    return jsonify({"reviews": product_reviews, "count": len(product_reviews)})


@app.route("/reviews", methods=["POST"])
def create_review():
    global next_review_id
    data = request.get_json()

    if not data or "user_id" not in data or "product_id" not in data or "rating" not in data:
        return jsonify({"error": "Vajalikud väljad: user_id, product_id, rating, comment"}), 400

    if not 1 <= data["rating"] <= 5:
        return jsonify({"error": "Hinne peab olema 1-5"}), 400

    # Kontrollime kasutajat
    try:
        user_resp = requests.get(f"{USERS_SERVICE}/users/{data['user_id']}")
        if user_resp.status_code != 200:
            return jsonify({"error": "Kasutajat ei leitud"}), 404
        user = user_resp.json()
    except requests.ConnectionError:
        return jsonify({"error": "Kasutajate teenus ei ole kättesaadav!"}), 503

    # Kontrollime toodet
    try:
        product_resp = requests.get(f"{PRODUCTS_SERVICE}/products/{data['product_id']}")
        if product_resp.status_code != 200:
            return jsonify({"error": "Toodet ei leitud"}), 404
        product = product_resp.json()
    except requests.ConnectionError:
        return jsonify({"error": "Toodete teenus ei ole kättesaadav!"}), 503

    review = {
        "id": next_review_id,
        "user": user["name"],
        "product": product["name"],
        "product_id": data["product_id"],
        "rating": data["rating"],
        "comment": data.get("comment", ""),
        "stars": "⭐" * data["rating"]
    }
    reviews.append(review)
    next_review_id += 1

    return jsonify({"message": "Arvustus lisatud!", "review": review}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
