# Mikroteenused

Mikroteenuste arhitektuuris on **iga funktsionaalsus eraldi teenuses** — kasutajad, tooted, tellimused ja arvustused jooksevad eraldi konteinerites, eraldi portidel ja suhtlevad omavahel HTTP kaudu.

---

## Enne alustamist

Veendu et oled repo juurkaustas ja monoliit on peatatud:

```bash
cd ~/Tarkvaraarendus-lab
docker compose -f docker-compose.monolith.yml down
```

---

## 1. Käivitamine

```bash
docker compose -f docker-compose.microservices.yml up --build
```

See käivitab **5 eraldi konteinerit**:

| Konteiner | Port | Ülesanne |
|---|---|---|
| epood-gateway | 5070 | Veebileht ja API Gateway |
| epood-users | 5051 | Kasutajate teenus |
| epood-products | 5052 | Toodete teenus |
| epood-orders | 5053 | Tellimuste teenus |
| epood-reviews | 5054 | Arvustuste teenus |

Ava brauseris: **http://localhost:5070**

Pane tähele — lehel on **teenuste staatus**. Näed reaalajas kas iga teenus töötab.

---

## 2. Testi rakendust

1. Loo tellimus läbi veebi — see käivitab ketireaktsiooni:
   - Gateway → Tellimuste teenus
   - Tellimuste teenus → Kasutajate teenus (pärib kasutaja info)
   - Tellimuste teenus → Toodete teenus (pärib toote info)
   - Vastus tuleb tagasi läbi keti

---

## 3. Ülesanne: Mis juhtub kui teenus kukub?

See on mikroteenuste kõige olulisem õppetund.

**Peata toodete teenus:**

```bash
docker stop epood-products
```

Värskenda lehte (F5) brauseris:
- Toodete teenuse staatus → **OFFLINE** 🔴
- Tooted kaovad lehelt
- Proovi luua tellimus — saad veateate

> **Küsimus:** Kas monoliidis saaks sama asi juhtuda — et ainult üks osa rakendusest lakkab töötamast?

**Taasta teenus:**

```bash
docker start epood-products
```

---

## 4. Vaata logisid — näed kuidas teenused suhtlevad

Ava **kolm terminali akent kõrvuti** (Cmd+T):

```bash
# Aken 1 — tellimuste teenus
docker logs -f epood-orders

# Aken 2 — kasutajate teenus
docker logs -f epood-users

# Aken 3 — toodete teenus
docker logs -f epood-products
```

Loo brauseris tellimus ja jälgi kõiki kolme akent — näed kuidas `orders` küsib `users`-ilt ja `products`-ilt andmeid.

> **Küsimus:** Kummas on lihtsam probleeme leida — monoliidi üks log vs mikroteenuste mitu logi?

---

## 5. Ülesanne: Lisa uus toode

Lisa uus toode: **Monitor**, hind **349.99**, emoji **🖥️**.

**Muudatus failis** `microservices/products/app.py`:

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
git apply patches/05-micro-add-product.patch
```

Rebuild:

```bash
docker compose -f docker-compose.microservices.yml up --build
```

> **Küsimus:** Muutsid ainult `products/app.py` — ühtegi teist teenust ei puudutatud. Monoliidis muutsid sama faili kus on KÕIK. Mis vahe on 10-liikmelises meeskonnas?

---

## 6. Ülesanne: Lisa uus kasutaja

Lisa kasutaja: **Kati Kask**, email **kati@example.com**.

**Muudatus failis** `microservices/users/app.py`:

```diff
 users = [
     {"id": 1, "name": "Mari Maasikas", "email": "mari@example.com"},
     {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},
+    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},
 ]
```

Või käsuga:

```bash
git apply patches/06-micro-add-user.patch
```

Rebuild:

```bash
docker compose -f docker-compose.microservices.yml up --build
```

---

## 7. Ülesanne: Lisa otsingu endpoint

Lisa toodete otsimine nime järgi.

**Muudatus failis** `microservices/products/app.py`:

```diff
-from flask import Flask, jsonify
+from flask import Flask, jsonify, request

+@app.route("/products/search", methods=["GET"])
+def search_products():
+    query = request.args.get("name", "").lower()
+    if not query:
+        return jsonify({"error": "Lisa parameeter ?name=otsingusõna"}), 400
+    results = [p for p in products if query in p["name"].lower()]
+    return jsonify({"results": results, "count": len(results)})
+
 @app.route("/products/<int:product_id>", methods=["GET"])
```

Või käsuga:

```bash
git apply patches/07-micro-add-search.patch
```

Rebuild ja testi:

```bash
docker compose -f docker-compose.microservices.yml up --build
curl "http://localhost:5052/products/search?name=hiir"
```

> **Küsimus:** Miks on endpointid erinevad? Monoliidis `/api/products/search`, mikroteenustes `/products/search`. Sest mikroteenuse teenus EI TEA teistest teenustest — tal pole vaja `/api/` prefiksit.

---

## 8. Ülesanne: Lisa allahindlus

Lisa loogika: kogus >= 5 → 10% allahindlus.

**Muudatus failis** `microservices/orders/app.py`:

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
git apply patches/08-micro-add-discount.patch
```

Rebuild ja testi:

```bash
docker compose -f docker-compose.microservices.yml up --build
curl -X POST http://localhost:5053/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 2, "quantity": 5}'
```

---

## 9. Kiiruse võrdlus

```bash
for i in 1 2 3 4 5; do
  time curl -s -X POST http://localhost:5070/api/orders \
    -H "Content-Type: application/json" \
    -d '{"user_id": 1, "product_id": 1, "quantity": 1}' > /dev/null
done
```

Võrdle monoliidi tulemusega:

| | Monoliit | Mikroteenused |
|---|---|---|
| Keskmine aeg | ___ ms | ___ ms |

> **Küsimus:** Mikroteenused on aeglasemad — miks? Kas see on alati oluline?

---

## 10. Ülesanne: Skaleeri üht teenust

```bash
docker compose -f docker-compose.microservices.yml up --scale products=3 -d
docker compose -f docker-compose.microservices.yml ps
```

Näed kolm `epood-products` konteinerit! Kasutajate ja tellimuste teenused jäid samaks.

**Taasta normaalolek:**

```bash
docker compose -f docker-compose.microservices.yml up --scale products=1 -d
```

> **Küsimus:** Black Friday ajal saab toodete teenus 100x rohkem liiklust. Mikroteenustes skaleerid ainult toodete teenust. Monoliidis pead skaleerima kogu rakendust. Mis on rahaline mõju pilves?

---

## 11. Ülesanne: Testi arvustuste teenust

```bash
# Lisa arvustus
curl -X POST http://localhost:5054/reviews \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 1, "rating": 5, "comment": "Väga hea sülearvuti!"}'

# Lisa veel üks
curl -X POST http://localhost:5054/reviews \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2, "product_id": 1, "rating": 3, "comment": "Aku võiks kauem kesta"}'

# Vaata kõiki arvustusi
curl http://localhost:5054/reviews

# Vaata konkreetse toote arvustusi
curl http://localhost:5054/reviews/product/1
```

Vaata kuidas teenus on tehtud:

```bash
cat microservices/reviews/app.py
```

> **Küsimus:** Arvustuste teenuse lisamiseks ei muudetud **ühtegi olemasolevat faili**. Monoliidis peaksid muutma `app.py` faili kus on juba kõik muu. Kumba eelistad 50-liikmelises meeskonnas?

---

## 12. Peata mikroteenused

```bash
docker compose -f docker-compose.microservices.yml down
```

---

## 13. Kokkuvõte ja arutelu

1. **Millal eelistaksid monoliiti?** Millal mikroteenuseid?
2. **Mis on mikroteenuste suurim eelis?** Suurim puudus?
3. **Kui sul oleks 2-liikmeline tiim ja 2 nädalat aega**, kumma valiksid?
4. **Kiiruse vahe** — kas see on alati oluline?
5. **Skaleerimine** — mis on rahaline erinevus pilves?
6. **Uue teenuse lisamine** — kumb viis oli puhtam?
