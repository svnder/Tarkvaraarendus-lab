import os

FILE = os.path.join("microservices", "users", "app.py")
OLD = '    {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},'
NEW = '    {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},\n    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},'

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if "Kati Kask" in content:
    print("✅ Kati Kask on juba lisatud!")
else:
    content = content.replace(OLD, NEW)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Kati Kask lisatud! Käivita: docker compose -f docker-compose.microservices.yml up --build")
