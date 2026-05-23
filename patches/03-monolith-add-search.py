"""
Ülesanne: Lisa otsingu endpoint monoliitsesse rakendusse.

Mida see skript teeb sinu eest:
  1. Avab faili monolith/app.py
  2. Lisab uue endpoindi /api/products/search
  3. Käivitab Docker rebuildi (taustal)
  4. Ootab kuni rakendus on valmis
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import run_rebuild, wait_for_service

FILE = os.path.join("monolith", "app.py")
COMPOSE = "docker-compose.monolith.yml"

MARKER = '@app.route("/api/products/<int:product_id>"'
NEW_FUNC = '@app.route("/api/products/search", methods=["GET"])\ndef search_products():\n    query = request.args.get("name", "").lower()\n    if not query:\n        return jsonify({"error": "Lisa parameeter ?name=otsingusona"}), 400\n    results = [p for p in products if query in p["name"].lower()]\n    return jsonify({"results": results, "count": len(results)})\n\n\n'

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if "search_products" in content:
    print("ℹ️  Otsingu endpoint on juba lisatud — jätan koodimuudatuse vahele.")
else:
    content = content.replace(MARKER, NEW_FUNC + MARKER)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Otsingu endpoint lisatud faili monolith/app.py")

if run_rebuild(COMPOSE):
    if wait_for_service("http://localhost:5050"):
        print("")
        print("🎉 Valmis! Testi otsingut:")
        print('   curl "http://localhost:5050/api/products/search?name=hiir"')
