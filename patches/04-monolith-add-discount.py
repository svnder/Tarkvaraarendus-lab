import os

FILE = os.path.join("monolith", "app.py")
OLD = '    quantity = data.get("quantity", 1)\n    total = product["price"] * quantity'
NEW = '''    quantity = data.get("quantity", 1)
    total = product["price"] * quantity

    discount = 0
    if quantity >= 5:
        discount = total * 0.10
        total = total - discount'''

OLD2 = '        "status": "created"\n    }'
NEW2 = '        "status": "created",\n        "discount": round(discount, 2)\n    }'

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if "discount" in content:
    print("✅ Allahindlus on juba lisatud!")
else:
    content = content.replace(OLD, NEW)
    content = content.replace(OLD2, NEW2)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Allahindlus lisatud! Käivita: docker compose -f docker-compose.monolith.yml up --build")
