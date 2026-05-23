import os

FILE = os.path.join("microservices", "products", "app.py")
MARKER = '@app.route("/products/<int:product_id>"'
NEW_FUNC = '@app.route("/products/search", methods=["GET"])\ndef search_products():\n    query = request.args.get("name", "").lower()\n    if not query:\n        return jsonify({"error": "Lisa parameeter ?name=otsingusona"}), 400\n    results = [p for p in products if query in p["name"].lower()]\n    return jsonify({"results": results, "count": len(results)})\n\n\n'

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if "search_products" in content:
    print("✅ Otsingu endpoint on juba lisatud!")
else:
    # Lisa request import
    content = content.replace(
        "from flask import Flask, jsonify\n",
        "from flask import Flask, jsonify, request\n"
    )
    content = content.replace(MARKER, NEW_FUNC + MARKER)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Otsingu endpoint lisatud microservices/products/app.py faili!")
    print("")
    print("Järgmine samm — käivita teenused uuesti:")
    print("  docker compose -f docker-compose.microservices.yml up --build")
    print("")
    print("Testi pärast käivitamist:")
    print('  curl "http://localhost:5052/products/search?name=hiir"')
