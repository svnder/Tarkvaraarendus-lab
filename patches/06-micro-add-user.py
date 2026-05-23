"""
Ülesanne: Lisa uus kasutaja mikroteenuste rakendusse.

Mida see skript teeb sinu eest:
  1. Avab faili microservices/users/app.py (AINULT kasutajate teenus!)
  2. Lisab uue kasutaja (Kati Kask)
  3. Käivitab Docker rebuildi (taustal)
  4. Ootab kuni rakendus on valmis
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import run_rebuild, wait_for_service

FILE = os.path.join("microservices", "users", "app.py")
COMPOSE = "docker-compose.microservices.yml"

OLD = '    {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},'
NEW = '    {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},\n    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},'

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if "Kati Kask" in content:
    print("ℹ️  Kati Kask on juba lisatud — jätan koodimuudatuse vahele.")
else:
    content = content.replace(OLD, NEW)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Kati Kask lisatud faili microservices/users/app.py")

if run_rebuild(COMPOSE):
    if wait_for_service("http://localhost:5070"):
        print("")
        print("🎉 Valmis! Mine brauserisse: http://localhost:5070")
        print("   Peaksid nägema 3 kasutajat.")
