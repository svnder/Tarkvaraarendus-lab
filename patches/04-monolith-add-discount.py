import os

FILE = os.path.join("monolith", "app.py")
OLD = '    quantity = data.get("quantity", 1)\n    total = product["price"] * quantity\n\n    order = {'
NEW = '    quantity = data.get("quantity", 1)\n    total = product["price"] * quantity\n\n    discount = 0\n    if quantity >= 5:\n        discount = total * 0.10\n        total = total - discount\n\n    order = {'

OLD2 = '        "total": round(total, 2),\n        "status": "created"\n    }'
NEW2 = '        "total": round(total, 2),\n        "status": "created",\n        "discount": round(discount, 2)\n    }'

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if "discount" in content:
    print("✅ Allahindlus on juba lisatud!")
else:
    content = content.replace(OLD, NEW)
    content = content.replace(OLD2, NEW2)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Allahindlus (10% kogusele 5+) lisatud monolith/app.py faili!")
    print("")
    print("Järgmine samm — käivita rakendus uuesti:")
    print("  docker compose -f docker-compose.monolith.yml up --build")
    print("")
    print("Testi pärast käivitamist — telli 5+ toodet:")
    print('  curl -X POST http://localhost:5050/api/orders -H "Content-Type: application/json" -d "{\\"user_id\\": 1, \\"product_id\\": 2, \\"quantity\\": 5}"')
