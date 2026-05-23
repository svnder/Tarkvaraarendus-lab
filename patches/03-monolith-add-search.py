import os

FILE = os.path.join("monolith", "app.py")
MARKER = '@app.route("/api/products/<int:product_id>"'
NEW_FUNC = '''@app.route("/api/products/search", methods=["GET"])
def search_products():
    query = request.args.get("name", "").lower()
    if not query:
        return jsonify({"error": "Lisa parameeter ?name=otsingusona"}), 400
    results = [p for p in products if query in p["name"].lower()]
    return jsonify({"results": results, "count": len(results)})


'''

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if "search_products" in content:
    print("✅ Otsingu endpoint on juba lisatud!")
else:
    content = content.replace(MARKER, NEW_FUNC + MARKER)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Otsingu endpoint lisatud! Käivita: docker compose -f docker-compose.monolith.yml up --build")
