# Mikroteenused

Mikroteenuste arhitektuuris on **iga funktsionaalsus eraldi teenuses** — kasutajad, tooted, tellimused ja arvustused jooksevad eraldi konteinerites, eraldi portidel, ja suhtlevad omavahel HTTP kaudu.

---

## Enne alustamist

Veendu et oled repo juurkaustas ja monoliit on peatatud:

```bash
# Mac / Linux
cd ~/Tarkvaraarendus-lab

# Windows
cd ~\Tarkvaraarendus-lab
```

```bash
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
| epood-gateway | 5070 | Veebileht — see on mida kasutaja näeb |
| epood-users | 5051 | Kasutajate teenus |
| epood-products | 5052 | Toodete teenus |
| epood-orders | 5053 | Tellimuste teenus |
| epood-reviews | 5054 | Arvustuste teenus |

Ava brauseris: **http://localhost:5070**

Lehel on **teenuste staatus** — näed reaalajas kas iga teenus töötab.

---

## 2. Tutvu rakendusega

1. Loo tellimus läbi veebi
2. Pane tähele — gateway saadab päringu → orders → users + products → tagasi

**Testi terminalist:**

```bash
curl http://localhost:5051/users
curl http://localhost:5052/products
curl -X POST http://localhost:5070/api/orders -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 2, \"quantity\": 3}"
```

---

## 3. Mis juhtub kui teenus kukub?

See on mikroteenuste kõige olulisem õppetund.

**Peata toodete teenus:**

```bash
docker stop epood-products
```

**Vaata brauseris** (värskenda F5):
- Toodete teenuse staatus → **OFFLINE** 🔴
- Tooted kaovad lehelt
- Proovi luua tellimus — saad veateate

> **Küsimus:** Kas monoliidis saaks sama juhtuda?

**Taasta teenus:**

```bash
docker start epood-products
```

---

## 4. Vaata logisid — näe kuidas teenused suhtlevad

Ava **kolm terminali akent**:

```bash
# Aken 1
docker logs -f epood-orders

# Aken 2
docker logs -f epood-users

# Aken 3
docker logs -f epood-products
```

Loo brauseris tellimus ja jälgi kõiki kolme akent korraga.

> **Küsimus:** Kummas on lihtsam probleeme leida?

---

## 5. Ülesanne: Lisa uus toode

Lisa toode: **Monitor**, hind **349.99**, emoji **🖥️**

**Mida muudame failis `microservices/products/app.py`:**

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
python3 patches/05-micro-add-product.py
```

> **Küsimus:** Muutsid ainult `products/app.py`. Ühtegi teist teenust ei puudutatud. Monoliidis muutsid sama faili kus on KÕIK. Mis vahe on 10-liikmelises meeskonnas?

---

## 6. Ülesanne: Lisa uus kasutaja

Lisa kasutaja: **Kati Kask**, email **kati@example.com**

**Mida muudame failis `microservices/users/app.py`:**

```diff
 users = [
     {"id": 1, "name": "Mari Maasikas", "email": "mari@example.com"},
     {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},
+    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},
 ]
```

**Tee see automaatselt:**

```bash
python3 patches/06-micro-add-user.py
```

---

## 7. Ülesanne: Lisa otsingu endpoint

**Mida muudame failis `microservices/products/app.py`:**

```diff
-from flask import Flask, jsonify
+from flask import Flask, jsonify, request

+@app.route("/products/search", methods=["GET"])
+def search_products():
+    query = request.args.get("name", "").lower()
+    if not query:
+        return jsonify({"error": "Lisa parameeter ?name=otsingusona"}), 400
+    results = [p for p in products if query in p["name"].lower()]
+    return jsonify({"results": results, "count": len(results)})
+
 @app.route("/products/<int:product_id>", methods=["GET"])
```

**Tee see automaatselt:**

```bash
python3 patches/07-micro-add-search.py
```

**Testi pärast skripti lõppu:**

```bash
curl "http://localhost:5052/products/search?name=hiir"
```

> **Küsimus:** Miks aadress on `localhost:5052` mitte `localhost:5070`? Sest otsing on toodete teenuse funktsioon — küsid otse toodete teenuselt.

---

## 8. Ülesanne: Lisa allahindlus

Lisa loogika: **kogus 5 või rohkem → 10% allahindlus**.

**Mida muudame failis `microservices/orders/app.py`:**

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
python3 patches/08-micro-add-discount.py
```

**Testi brauserist** — telli 5+ toodet ja vaata allahindluse summat.

---

## 9. Kiiruse võrdlus

```bash
for i in 1 2 3 4 5; do time curl -s -X POST http://localhost:5070/api/orders -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 1, \"quantity\": 1}" > /dev/null; done
```

Võrdle monoliidi tulemusega:

| | Monoliit | Mikroteenused |
|---|---|---|
| Keskmine aeg | ___ ms | ___ ms |

> **Küsimus:** Mikroteenused on aeglasemad — miks? Kas see on alati oluline?

---

## 10. Skaleeri üht teenust

Kujuta ette et on Black Friday ja toodete teenus saab 100x rohkem liiklust. Mikroteenustes saad käivitada toodete teenusest mitu koopiat — teised teenused jäävad puutumata.

Skaleerimiseks peame products teenuselt eemaldama fikseeritud pordi ja konteineri nime — mitu koopiat ei saa sama porti ega nime jagada.

**Mida muudame failis `docker-compose.microservices.yml`:**

```diff
   products:
     build: ./microservices/products
-    ports:
-      - "5052:5002"
-    container_name: epood-products
```

**Samm 1 — eemalda port ja konteineri nimi:**

```bash
sed -i '' '/container_name: epood-products/d' docker-compose.microservices.yml
sed -i '' '/5052:5002/d' docker-compose.microservices.yml
```

**Samm 2 — käivita uuesti:**

```bash
docker compose -f docker-compose.microservices.yml down
docker compose -f docker-compose.microservices.yml up --build -d
```

**Samm 3 — skaleeri 3 koopiani:**

```bash
docker compose -f docker-compose.microservices.yml up --scale products=3 -d
```

**Samm 4 — kontrolli:**

```bash
docker compose -f docker-compose.microservices.yml ps
```

Näed kolm products konteinerit! Teised teenused jäid 1 koopiana. Rakendus töötab endiselt läbi gateway `http://localhost:5070`.

**Monoliidis** ei saaks nii teha — skaleerimiseks peaksid käivitama kogu rakenduse 3 koopiana, kuigi probleem oli ainult toodete juures. Pilves (AWS, Azure) maksad iga konteineri eest — see vahe on rahaline.

**Taasta normaalolek:**

```bash
docker compose -f docker-compose.microservices.yml up --scale products=1 -d
```

> **Küsimus:** Mitu eurot kuus säästaksid pilves kui pead skaleerima ainult toodete teenust vs kogu monoliiti?

---

## 11. Testi arvustuste teenust

```bash
curl -X POST http://localhost:5054/reviews -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 1, \"rating\": 5, \"comment\": \"Vaga hea!\"}"
curl http://localhost:5054/reviews
```

> **Küsimus:** Arvustuste teenuse lisamiseks ei muudetud ühtegi olemasolevat faili. Kumba eelistad 50-liikmelises meeskonnas?

---

## 12. Peata mikroteenused

```bash
docker compose -f docker-compose.microservices.yml down
```

---

## Kokkuvõte ja arutelu

1. **Millal eelistaksid monoliiti?** Millal mikroteenuseid?
2. **Mis on mikroteenuste suurim eelis?** Suurim puudus?
3. **2-liikmeline tiim, 2 nädalat** — kumba valid?
4. **Teenuse kukukumine** — eelis või puudus?
5. **Kiiruse vahe** — kas alati oluline?
6. **Skaleerimine** — mis on rahaline erinevus pilves?
7. **Uue teenuse lisamine** — kumb viis oli puhtam?
