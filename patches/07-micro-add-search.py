"""
Ülesanne: Lisa otsingu endpoint mikroteenuste toodete teenusele.

Mida see skript teeb sinu eest:
  1. Avab faili microservices/products/app.py
  2. Lisab 'request' impordi (vajalik query parameetrite jaoks)
  3. Lisab uue endpoindi /products/search ENNE /products/<id> endpointi
     (Järjekord on oluline — muidu Flask peab "search" sõna ID-ks!)
  4. Käivitab Docker rebuildi (taustal)
  5. Ootab kuni rakendus on valmis
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import run_rebuild, wait_for_service

FILE = os.path.join("microservices", "products", "app.py")
COMPOSE = "docker-compose.microservices.yml"

MARKER = '@app.route("/products/<int:product_id>"'
NEW_FUNC = '@app.route("/products/search", methods=["GET"])\ndef search_products():\n    query = request.args.get("name", "").lower()\n    if not query:\n        return jsonify({"error": "Lisa parameeter ?name=otsingusona"}), 400\n    results = [p for p in products if query in p["name"].lower()]\n    return jsonify({"results": results, "count": len(results)})\n\n\n'

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if "search_products" in content:
    print("ℹ️  Otsingu endpoint on juba lisatud — jätan koodimuudatuse vahele.")
else:
    content = content.replace(
        "from flask import Flask, jsonify\n",
        "from flask import Flask, jsonify, request\n"
    )
    content = content.replace(MARKER, NEW_FUNC + MARKER)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Otsingu endpoint lisatud faili microservices/products/app.py")

if run_rebuild(COMPOSE):
    if wait_for_service("http://localhost:5070"):
        print("")
        print("🎉 Valmis! Testi otsingut otse toodete teenuselt:")
        print('   curl "http://localhost:5052/products/search?name=hiir"')
