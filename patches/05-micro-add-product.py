import os

FILE = os.path.join("microservices", "products", "app.py")
OLD = '    {"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},'
NEW = '    {"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},\n    {"id": 4, "name": "Monitor", "price": 349.99, "emoji": "🖥️"},'

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if '"id": 4' in content:
    print("✅ Monitor on juba lisatud!")
else:
    content = content.replace(OLD, NEW)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Monitor lisatud microservices/products/app.py faili!")
    print("")
    print("Järgmine samm — käivita teenused uuesti:")
    print("  docker compose -f docker-compose.microservices.yml up --build")
