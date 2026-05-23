"""
Ülesanne: Lisa uus toode monoliitsesse rakendusse.

Mida see skript teeb sinu eest:
  1. Avab faili monolith/app.py
  2. Lisab uue toote (Monitor) toodete nimekirja
  3. Käivitab Docker rebuildi (taustal)
  4. Ootab kuni rakendus on valmis
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import run_rebuild, wait_for_service

FILE = os.path.join("monolith", "app.py")
COMPOSE = "docker-compose.monolith.yml"

OLD = '    {"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},'
NEW = '    {"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},\n    {"id": 4, "name": "Monitor", "price": 349.99, "emoji": "🖥️"},'

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if '"id": 4' in content:
    print("ℹ️  Monitor on juba lisatud — jätan koodimuudatuse vahele.")
else:
    content = content.replace(OLD, NEW)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Monitor lisatud faili monolith/app.py")

if run_rebuild(COMPOSE):
    if wait_for_service("http://localhost:5050"):
        print("")
        print("🎉 Valmis! Mine brauserisse: http://localhost:5050")
        print("   Peaksid nägema 4 toodet (Monitor on viimane).")
