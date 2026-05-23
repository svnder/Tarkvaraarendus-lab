# Monoliit

Monoliitses arhitektuuris on **kõik ühes rakenduses** — kasutajad, tooted ja tellimused on samas failis, samas konteineris, samal pordil.

---

## Enne alustamist

Veendu et oled repo juurkaustas:

```bash
cd ~/Tarkvaraarendus-lab
```

---

## 1. Käivitamine

```bash
docker compose -f docker-compose.monolith.yml up --build
```

Oota kuni näed:
```
epood-monolith  |  * Running on all addresses (0.0.0.0)
```

Ava brauseris: **http://localhost:5050**

---

## 2. Testi rakendust

1. Vaata tooteid ja kasutajaid lehel
2. Loo tellimus — vali kasutaja ID, toote ID ja kogus
3. Vaata kuidas tellimus ilmub nimekirja

Testi terminalist (ava uus aken Cmd+T):

```bash
curl http://localhost:5050/api/users
curl http://localhost:5050/api/products
curl -X POST http://localhost:5050/api/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 2, "quantity": 3}'
```

---

## 3. Vaata koodi struktuuri

Ava `monolith/app.py` ja pane tähele — **kõik on ühes failis**:
- Kasutajate andmed ja endpointid
- Toodete andmed ja endpointid
- Tellimuste loogika ja endpointid

> **Küsimus:** Mis juhtub kui 10 arendajat töötavad korraga selle ühe faili kallal?

---

## 4. Ülesanne: Lisa uus toode

Lisa uus toode: **Monitor**, hind **349.99**, emoji **🖥️**.

**Muudatus failis** `monolith/app.py`:

```diff
 products = [
     {"id": 1, "name": "Sülearvuti", "price": 899.99, "emoji": "💻"},
     {"id": 2, "name": "Hiir", "price": 29.99, "emoji": "🖱️"},
     {"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},
+    {"id": 4, "name": "Monitor", "price": 349.99, "emoji": "🖥️"},
 ]
```

Või käsuga:

```bash
git apply patches/01-monolith-add-product.patch
```

Rebuild:

```bash
docker compose -f docker-compose.monolith.yml up --build
```

Kontrolli brauserist — uus toode peaks ilmuma.

---

## 5. Ülesanne: Lisa uus kasutaja

Lisa kasutaja: **Kati Kask**, email **kati@example.com**.

**Muudatus failis** `monolith/app.py`:

```diff
 users = [
     {"id": 1, "name": "Mari Maasikas", "email": "mari@example.com"},
     {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},
+    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},
 ]
```

Või käsuga:

```bash
git apply patches/02-monolith-add-user.patch
```

Rebuild:

```bash
docker compose -f docker-compose.monolith.yml up --build
```

---

## 6. Ülesanne: Lisa otsingu endpoint

Lisa toodete otsimine nime järgi.

**Muudatus failis** `monolith/app.py` — lisa see kood **enne** `get_product` funktsiooni:

```diff
+@app.route("/api/products/search", methods=["GET"])
+def search_products():
+    query = request.args.get("name", "").lower()
+    if not query:
+        return jsonify({"error": "Lisa parameeter ?name=otsingusõna"}), 400
+    results = [p for p in products if query in p["name"].lower()]
+    return jsonify({"results": results, "count": len(results)})
+
 @app.route("/api/products/<int:product_id>", methods=["GET"])
```

Või käsuga:

```bash
git apply patches/03-monolith-add-search.patch
```

Rebuild ja testi:

```bash
docker compose -f docker-compose.monolith.yml up --build
curl "http://localhost:5050/api/products/search?name=hiir"
```

---

## 7. Ülesanne: Lisa allahindlus

Lisa loogika: kogus >= 5 → 10% allahindlus.

**Muudatus failis** `monolith/app.py` — leia `create_order` funktsioon:

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

Või käsuga:

```bash
git apply patches/04-monolith-add-discount.patch
```

Rebuild ja testi — telli 5+ toodet:

```bash
docker compose -f docker-compose.monolith.yml up --build
curl -X POST http://localhost:5050/api/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 2, "quantity": 5}'
```

---

## 8. Vaata logisid

Ava uus terminali aken (Cmd+T) ja:

```bash
docker logs -f epood-monolith
```

Loo brauseris tellimus — näed terminalis kõiki päringuid **ühes kohas**.

> **Küsimus:** Kas üks log on mugav või tekitab probleeme?

---

## 9. Kiiruse mõõtmine

```bash
for i in 1 2 3 4 5; do
  time curl -s -X POST http://localhost:5050/api/orders \
    -H "Content-Type: application/json" \
    -d '{"user_id": 1, "product_id": 1, "quantity": 1}' > /dev/null
done
```

Pane kirja keskmine `real` väärtus — võrdled hiljem mikroteenustega.

---

## 10. Peata monoliit

```bash
docker compose -f docker-compose.monolith.yml down
```

Järgmiseks: **[MIKROTEENUSED.md](MIKROTEENUSED.md)**
