# Monoliit

Monoliitses arhitektuuris on **kõik ühes rakenduses** — kasutajad, tooted ja tellimused on samas failis, samas konteineris, samal pordil 5050.

---

## Enne alustamist

Veendu et oled repo juurkaustas:

```bash
# Mac / Linux
cd ~/Tarkvaraarendus-lab

# Windows
cd ~\Tarkvaraarendus-lab
```

---

## 1. Käivitamine

```bash
docker compose -f docker-compose.monolith.yml up --build
```

Oota kuni terminal näitab:
```
epood-monolith  |  * Running on all addresses (0.0.0.0)
```

Ava brauseris: **http://localhost:5050**

---

## 2. Tutvu rakendusega

1. Vaata tooteid ja kasutajaid lehel
2. Loo tellimus — sisesta kasutaja ID, toote ID ja kogus
3. Vaata kuidas tellimus ilmub nimekirja

**Testi terminalist** (ava uus aken):

```bash
curl http://localhost:5050/api/users
curl http://localhost:5050/api/products
Invoke-RestMethod `
  -Method POST `
  -Uri "http://localhost:5050/api/orders" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"user_id":1,"product_id":2,"quantity":3}'
```

---

## 3. Vaata koodi

Ava fail `monolith/app.py`. Pane tähele — **kõik on ühes failis**:
- Kasutajate andmed ja endpointid
- Toodete andmed ja endpointid
- Tellimuste loogika ja endpointid

> **Küsimus:** Kui 10 arendajat töötavad korraga selle ühe faili kallal, mis probleemid tekivad?

---

## 4. Ülesanne: Lisa uus toode

Lisa toode: **Monitor**, hind **349.99**, emoji **🖥️**

**Mida muudame failis `monolith/app.py`:**

```diff
 products = [
     {"id": 1, "name": "Sülearvuti", "price": 899.99, "emoji": "💻"},
     {"id": 2, "name": "Hiir", "price": 29.99, "emoji": "🖱️"},
     {"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},
+    {"id": 4, "name": "Monitor", "price": 349.99, "emoji": "🖥️"},
 ]
```

**Tee see automaatselt:**

```bash
python3 patches/01-monolith-add-product.py
```

Skript muudab koodi, käivitab rebuildi ja ütleb kui valmis. Mine siis brauserisse vaatama.

---

## 5. Ülesanne: Lisa uus kasutaja

Lisa kasutaja: **Kati Kask**, email **kati@example.com**

**Mida muudame failis `monolith/app.py`:**

```diff
 users = [
     {"id": 1, "name": "Mari Maasikas", "email": "mari@example.com"},
     {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},
+    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},
 ]
```

**Tee see automaatselt:**

```bash
python3 patches/02-monolith-add-user.py
```

---

## 6. Ülesanne: Lisa otsingu endpoint

Lisa toote otsimine nime järgi.

**Mida muudame failis `monolith/app.py`:**

```diff
+@app.route("/api/products/search", methods=["GET"])
+def search_products():
+    query = request.args.get("name", "").lower()
+    if not query:
+        return jsonify({"error": "Lisa parameeter ?name=otsingusona"}), 400
+    results = [p for p in products if query in p["name"].lower()]
+    return jsonify({"results": results, "count": len(results)})
+
 @app.route("/api/products/<int:product_id>", methods=["GET"])
```

**Tee see automaatselt:**

```bash
python3 patches/03-monolith-add-search.py
```

**Testi pärast skripti lõppu:**

```bash
curl "http://localhost:5050/api/products/search?name=hiir"
```

---

## 7. Ülesanne: Lisa allahindlus

Lisa loogika: **kogus 5 või rohkem → 10% allahindlus**.

**Mida muudame failis `monolith/app.py`:**

```diff
     quantity = data.get("quantity", 1)
     total = product["price"] * quantity

+    discount = 0
+    if quantity >= 5:
+        discount = total * 0.10
+        total = total - discount
+
     order = {
         ...
         "total": round(total, 2),
-        "status": "created"
+        "status": "created",
+        "discount": round(discount, 2)
     }
```

**Tee see automaatselt:**

```bash
python3 patches/04-monolith-add-discount.py
```

**Testi brauserist** — telli 5+ toodet ja vaata allahindluse summat tellimuse kaardil.

---

## 8. Vaata logisid

Ava uus terminali aken ja:

```bash
docker logs -f epood-monolith
```

Loo brauseris tellimus. Näed terminalis kõiki päringuid **ühes kohas**.

> **Küsimus:** Kas üks log on mugav või tekitab probleeme suure rakenduse puhul?

---

## 9. Kiiruse mõõtmine

**Mac / Linux:**
```bash
for i in 1 2 3 4 5; do time curl -s -X POST http://localhost:5050/api/orders -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 1, \"quantity\": 1}" > /dev/null; done
```
**Windows**
``` bash
1..5 | ForEach-Object {
    Measure-Command {
        curl.exe -s -X POST "http://localhost:5050/api/orders" `
          -H "Content-Type: application/json" `
          -d "{\"user_id\":1,\"product_id\":1,\"quantity\":1}" > $null
    }
}
```

Pane kirja keskmine `real` väärtus — võrdled hiljem mikroteenustega.

---

## 10. Peata monoliit

```bash
docker compose -f docker-compose.monolith.yml down
```

Jätka: **[MIKROTEENUSED.md](MIKROTEENUSED.md)**
