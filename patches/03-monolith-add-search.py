import os

FILE = os.path.join("monolith", "app.py")
MARKER = '@app.route("/api/products/<int:product_id>"'
NEW_FUNC = '@app.route("/api/products/search", methods=["GET"])\ndef search_products():\n    query = request.args.get("name", "").lower()\n    if not query:\n        return jsonify({"error": "Lisa parameeter ?name=otsingusona"}), 400\n    results = [p for p in products if query in p["name"].lower()]\n    return jsonify({"results": results, "count": len(results)})\n\n\n'

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if "search_products" in content:
    print("✅ Otsingu endpoint on juba lisatud!")
else:
    content = content.replace(MARKER, NEW_FUNC + MARKER)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Otsingu endpoint lisatud monolith/app.py faili!")
    print("")
    print("Järgmine samm — käivita rakendus uuesti:")
    print("  docker compose -f docker-compose.monolith.yml up --build")
    print("")
    print("Testi pärast käivitamist:")
    print('  curl "http://localhost:5050/api/products/search?name=hiir"')
