from flask import Flask, jsonify

app = Flask(__name__)

# ============================================
# KASUTAJATE TEENUS (Microservice)
# Vastutab AINULT kasutajate eest
# Port: 5001
# ============================================

users = [
    {"id": 1, "name": "Mari Maasikas", "email": "mari@example.com"},
    {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},
]


@app.route("/", methods=["GET"])
def index():
    return jsonify({"service": "Kasutajate teenus", "port": 5001})


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"users": users})


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "Kasutajat ei leitud"}), 404
    return jsonify(user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
