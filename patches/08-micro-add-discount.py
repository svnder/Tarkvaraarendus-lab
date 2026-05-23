"""
Ülesanne: Lisa allahindlus mikroteenuste tellimuste loogikale.
Kui kogus on 5 või rohkem, kehtib 10% allahindlus.

Mida see skript teeb sinu eest:
  1. Avab faili microservices/orders/app.py (AINULT tellimuste teenus!)
  2. Lisab allahindluse loogika create_order funktsiooni
  3. Käivitab Docker rebuildi (taustal)
  4. Ootab kuni rakendus on valmis

PANE TÄHELE: ainult ÜKS fail muutus — orders/app.py.
Toodete ja kasutajate teenused jäid puutumata!
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import run_rebuild, wait_for_service

FILE = os.path.join("microservices", "orders", "app.py")
COMPOSE = "docker-compose.microservices.yml"

OLD = '    quantity = data.get("quantity", 1)\n    total = product["price"] * quantity\n\n    order = {'
NEW = '    quantity = data.get("quantity", 1)\n    total = product["price"] * quantity\n\n    discount = 0\n    if quantity >= 5:\n        discount = total * 0.10\n        total = total - discount\n\n    order = {'

OLD2 = '        "total": round(total, 2),\n        "status": "created"\n    }'
NEW2 = '        "total": round(total, 2),\n        "status": "created",\n        "discount": round(discount, 2)\n    }'

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if "discount" in content:
    print("ℹ️  Allahindlus on juba lisatud — jätan koodimuudatuse vahele.")
else:
    content = content.replace(OLD, NEW)
    content = content.replace(OLD2, NEW2)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Allahindlus (10% kogusele 5+) lisatud faili microservices/orders/app.py")

if run_rebuild(COMPOSE):
    if wait_for_service("http://localhost:5070"):
        print("")
        print("🎉 Valmis! Mine brauserisse: http://localhost:5070")
        print("   Telli 5+ toodet ja vaata allahindluse summat!")
