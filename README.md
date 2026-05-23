# Tarkvaraarenduse labor: Monoliit vs Mikroteenused

Selles laboris võrdled kahte arhitektuurimudelit — **monoliitset** ja **mikroteenuste** põhist rakendust. Mõlemad teevad sama asja (lihtne e-poe rakendus), aga on üles ehitatud erinevalt.

---

## Eeldused

- Docker ja Docker Compose on paigaldatud
- Terminal/käsurida on tuttav
- Git on paigaldatud

---

## 1. Repo kloonimine ja ülevaade

### 1.1 Klooni repo

```bash
git clone https://github.com/svnder/Tarkvaraarendus-lab.git
cd Tarkvaraarendus-lab
```

### 1.2 Projekti struktuur

```
Tarkvaraarendus-lab/
├── monolith/                          # MONOLIIT — kõik ühes
│   ├── app.py                         # Kogu rakendus ühes failis
│   ├── templates/index.html           # Veebileht
│   ├── static/style.css               # Stiilid
│   ├── requirements.txt
│   └── Dockerfile
├── microservices/                     # MIKROTEENUSED — eraldi teenused
│   ├── users/                         # Kasutajate teenus (port 5051)
│   ├── products/                      # Toodete teenus (port 5052)
│   ├── orders/                        # Tellimuste teenus (port 5053)
│   ├── reviews/                       # Arvustuste teenus (port 5054)
│   └── gateway/                       # API Gateway — veebileht (port 5070)
├── docker-compose.monolith.yml
└── docker-compose.microservices.yml
```

---

## 2. Monoliidi käivitamine

### 2.1 Käivita monoliit

```bash
docker compose -f docker-compose.monolith.yml up --build
```

Oota kuni näed:
```
epood-monolith  |  * Running on all addresses (0.0.0.0)
```

### 2.2 Ava brauseris

Mine aadressile: **http://localhost:5050**

### 2.3 Testi rakendust

1. Vaata tooteid ja kasutajaid lehel
2. Loo tellimus — vali kasutaja ID, toote ID ja kogus, vajuta "Loo tellimus"
3. Vaata kuidas tellimus ilmub tellimuste nimekirja

### 2.4 Testi terminalist (valikuline)

```bash
curl http://localhost:5050/api/users
curl http://localhost:5050/api/products
curl -X POST http://localhost:5050/api/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 2, "quantity": 3}'
```

### 2.5 Peata monoliit

```bash
docker compose -f docker-compose.monolith.yml down
```

---

## 3. Mikroteenuste käivitamine

### 3.1 Käivita mikroteenused

```bash
docker compose -f docker-compose.microservices.yml up --build
```

See käivitab **5 eraldi konteinerit**:
- `epood-gateway` — veebileht (port 5070)
- `epood-users` — kasutajate teenus (port 5051)
- `epood-products` — toodete teenus (port 5052)
- `epood-orders` — tellimuste teenus (port 5053)
- `epood-reviews` — arvustuste teenus (port 5054)

### 3.2 Ava brauseris

Mine aadressile: **http://localhost:5070**

### 3.3 Peata mikroteenused

```bash
docker compose -f docker-compose.microservices.yml down
```

---

## 4. Ülesanne: Mis juhtub kui teenus kukub?

### 4.1 Käivita mikroteenused

```bash
docker compose -f docker-compose.microservices.yml up --build
```

### 4.2 Peata toodete teenus

```bash
docker stop epood-products
```

### 4.3 Vaata mis juhtub

1. Värskenda lehte (F5) brauseris
2. Toodete teenuse staatus peaks olema **OFFLINE** 🔴
3. Proovi luua tellimus — saad veateate

### 4.4 Taasta teenus

```bash
docker start epood-products
```

> **Küsimus:** Kas monoliidis saaks sama asi juhtuda — et ainult üks osa rakendusest lakkab töötamast?

---

## 5. Ülesanne: Lisa uus toode

Lisa mõlemale rakendusele uus toode: **Monitor**, hind **349.99**, emoji **🖥️**.

### 5.1 Monoliidis

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
sed -i '' 's/{"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},/{"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},\
    {"id": 4, "name": "Monitor", "price": 349.99, "emoji": "🖥️"},/' monolith/app.py
```

Rebuild:

```bash
docker compose -f docker-compose.monolith.yml up --build
```

### 5.2 Mikroteenustes

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
sed -i '' 's/{"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},/{"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},\
    {"id": 4, "name": "Monitor", "price": 349.99, "emoji": "🖥️"},/' microservices/products/app.py
```

Rebuild:

```bash
docker compose -f docker-compose.microservices.yml up --build
```

> **Küsimus:** Kummas oli muudatus lihtsam? Mõlemas muutsid üht faili — aga mis vahe on 10-liikmelises meeskonnas?

---

## 6. Ülesanne: Lisa uus kasutaja

Lisa uus kasutaja: **Kati Kask**, email **kati@example.com**.

### 6.1 Monoliidis

```diff
 users = [
     {"id": 1, "name": "Mari Maasikas", "email": "mari@example.com"},
     {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},
+    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},
 ]
```

Või käsuga:

```bash
sed -i '' 's/{"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},/{"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},\
    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},/' monolith/app.py
```

Rebuild:

```bash
docker compose -f docker-compose.monolith.yml up --build
```

### 6.2 Mikroteenustes

```diff
 users = [
     {"id": 1, "name": "Mari Maasikas", "email": "mari@example.com"},
     {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},
+    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},
 ]
```

Või käsuga:

```bash
sed -i '' 's/{"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},/{"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},\
    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},/' microservices/users/app.py
```

Rebuild:

```bash
docker compose -f docker-compose.microservices.yml up --build
```

---

## 7. Ülesanne: Lisa otsingu endpoint

### 7.1 Monoliidis

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
python3 -c "
content = open('monolith/app.py').read()
new_func = '''
@app.route(\"/api/products/search\", methods=[\"GET\"])
def search_products():
    query = request.args.get(\"name\", \"\").lower()
    if not query:
        return jsonify({\"error\": \"Lisa parameeter ?name=otsingusona\"}), 400
    results = [p for p in products if query in p[\"name\"].lower()]
    return jsonify({\"results\": results, \"count\": len(results)})

'''
content = content.replace('@app.route(\"/api/products/<int:product_id>\"', new_func + '@app.route(\"/api/products/<int:product_id>\"')
open('monolith/app.py', 'w').write(content)
print('Valmis!')
"
```

Rebuild ja testi:

```bash
docker compose -f docker-compose.monolith.yml up --build
curl "http://localhost:5050/api/products/search?name=hiir"
```

### 7.2 Mikroteenustes

Kõigepealt lisa `request` import:

```bash
sed -i '' 's/from flask import Flask, jsonify$/from flask import Flask, jsonify, request/' microservices/products/app.py
```

Seejärel lisa search endpoint enne product_id endpointi:

```bash
python3 -c "
content = open('microservices/products/app.py').read()
new_func = '''
@app.route(\"/products/search\", methods=[\"GET\"])
def search_products():
    query = request.args.get(\"name\", \"\").lower()
    if not query:
        return jsonify({\"error\": \"Lisa parameeter ?name=otsingusona\"}), 400
    results = [p for p in products if query in p[\"name\"].lower()]
    return jsonify({\"results\": results, \"count\": len(results)})

'''
content = content.replace('@app.route(\"/products/<int:product_id>\"', new_func + '@app.route(\"/products/<int:product_id>\"')
open('microservices/products/app.py', 'w').write(content)
print('Valmis!')
"
```

Rebuild ja testi:

```bash
docker compose -f docker-compose.microservices.yml up --build
curl "http://localhost:5052/products/search?name=hiir"
```

> **Küsimus:** Pane tähele endpoindi erinevust: monoliidis `/api/products/search`, mikroteenustes `/products/search`. Miks?

---

## 8. Ülesanne: Lisa allahindlus tellimustele

Lisa loogika: kui kogus on 5 või rohkem, kehtib 10% allahindlus.

### 8.1 Monoliidis

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
python3 -c "
content = open('monolith/app.py').read()
old = '    quantity = data.get(\"quantity\", 1)\n    total = product[\"price\"] * quantity'
new = '''    quantity = data.get(\"quantity\", 1)
    total = product[\"price\"] * quantity

    discount = 0
    if quantity >= 5:
        discount = total * 0.10
        total = total - discount'''
content = content.replace(old, new)
old2 = '        \"status\": \"created\"\n    }'
new2 = '        \"status\": \"created\",\n        \"discount\": round(discount, 2)\n    }'
content = content.replace(old2, new2)
open('monolith/app.py', 'w').write(content)
print('Valmis!')
"
```

Rebuild:

```bash
docker compose -f docker-compose.monolith.yml up --build
```

### 8.2 Mikroteenustes

```bash
python3 -c "
content = open('microservices/orders/app.py').read()
old = '    quantity = data.get(\"quantity\", 1)\n    total = product[\"price\"] * quantity'
new = '''    quantity = data.get(\"quantity\", 1)
    total = product[\"price\"] * quantity

    discount = 0
    if quantity >= 5:
        discount = total * 0.10
        total = total - discount'''
content = content.replace(old, new)
old2 = '        \"status\": \"created\"\n    }'
new2 = '        \"status\": \"created\",\n        \"discount\": round(discount, 2)\n    }'
content = content.replace(old2, new2)
open('microservices/orders/app.py', 'w').write(content)
print('Valmis!')
"
```

Rebuild ja testi — telli 5+ toodet:

```bash
docker compose -f docker-compose.microservices.yml up --build
curl -X POST http://localhost:5053/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 2, "quantity": 5}'
```

---

## 9. Ülesanne: Vaata Docker logisid

### 9.1 Monoliidi logid

Käivita monoliit, ava uus terminali aken:

```bash
docker logs -f epood-monolith
```

Loo tellimus brauseris ja vaata mis terminalis ilmub.

### 9.2 Mikroteenuste logid

Käivita mikroteenused. Ava **kolm terminali akent kõrvuti**:

```bash
# Aken 1
docker logs -f epood-orders

# Aken 2
docker logs -f epood-users

# Aken 3
docker logs -f epood-products
```

Loo brauseris tellimus ja jälgi kõiki kolme akent korraga — näed kuidas orders küsib users'ilt ja products'ilt andmeid.

> **Küsimus:** Kummas on lihtsam probleeme leida? Monoliidis on kõik ühes logis. Mikroteenustes pead vaatama mitut logi korraga.

---

## 10. Ülesanne: Kiiruse võrdlus

### 10.1 Monoliidi kiirus

```bash
for i in 1 2 3 4 5; do
  time curl -s -X POST http://localhost:5050/api/orders \
    -H "Content-Type: application/json" \
    -d '{"user_id": 1, "product_id": 1, "quantity": 1}' > /dev/null
done
```

### 10.2 Mikroteenuste kiirus

```bash
for i in 1 2 3 4 5; do
  time curl -s -X POST http://localhost:5070/api/orders \
    -H "Content-Type: application/json" \
    -d '{"user_id": 1, "product_id": 1, "quantity": 1}' > /dev/null
done
```

### 10.3 Võrdle tulemusi

| | Monoliit | Mikroteenused |
|---|---|---|
| Keskmine aeg | ___ ms | ___ ms |

> **Küsimus:** Mikroteenused on aeglasemad — miks? Kas see kiiruse vahe on alati oluline?

---

## 11. Ülesanne: Teenuse skaleerimine

### 11.1 Vaata praegust seisu

```bash
docker compose -f docker-compose.microservices.yml ps
```

### 11.2 Skaleeri toodete teenust

```bash
docker compose -f docker-compose.microservices.yml up --scale products=3 -d
```

### 11.3 Kontrolli

```bash
docker compose -f docker-compose.microservices.yml ps
```

Näed kolm `epood-products` konteinerit!

### 11.4 Taasta normaalolek

```bash
docker compose -f docker-compose.microservices.yml up --scale products=1 -d
```

> **Küsimus:** Black Friday ajal saab toodete teenus 100x rohkem liiklust. Mikroteenustes skaleerid ainult toodete teenust. Monoliidis pead skaleerima kogu rakendust. Mis on rahaline mõju pilves?

---

## 12. Ülesanne: Lisa täiesti uus teenus (arvustused)

### 12.1 Testi arvustuste teenust

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

### 12.2 Vaata kuidas teenus on tehtud

```bash
cat microservices/reviews/app.py
```

Pane tähele:
- Eraldi fail, eraldi port
- Suhtleb users ja products teenustega HTTP kaudu
- **Ühtegi olemasolevat faili ei muudetud**

### 12.3 Monoliidis vs mikroteenustes

**Monoliidis** peaksid:
1. Avama `monolith/app.py`
2. Lisama `reviews` listi kõigi teiste andmete kõrvale
3. Lisama kõik endpointid samasse faili — risk olemasolevat koodi rikkuda

**Mikroteenustes:**
1. Lõid uue kausta `reviews/`
2. Kirjutasid eraldi `app.py`
3. Lisasid ühe rea `docker-compose.yml` faili
4. **Ühtegi olemasolevat faili ei muudetud**

> **Küsimus:** 50 arendajaga meeskonnas töötab üks tiim arvustuste, teine tellimuste kallal. Monoliidis töötavad mõlemad samas failis — merge conflictid on garanteeritud. Mikroteenustes töötavad nad eraldi. Kumba eelistad?

---

## 13. Kokkuvõte ja arutelu

1. **Millal eelistaksid monoliiti?** Millal mikroteenuseid?
2. **Mis on mikroteenuste suurim eelis?** Suurim puudus?
3. **Kui sul oleks 2-liikmeline tiim ja 2 nädalat aega**, kumma valiksid?
4. **Mis juhtus kui peatasid ühe teenuse?**
5. **Kiiruse vahe** — kas see on alati oluline?
6. **Skaleerimine** — mis on rahaline erinevus pilves?
7. **Uue teenuse lisamine** — kumb viis oli puhtam?

---

## Vihjed probleemide korral

**Port on hõivatud:**
```bash
lsof -i :5050
# macOS: AirPlay kasutab porti 5000 → kasutame 5050+
# Firefox blokeerib porti 5060 → gateway on pordil 5070
```

**Muudatused ei kajastu:**
```bash
docker compose -f docker-compose.monolith.yml down
docker compose -f docker-compose.monolith.yml up --build
```

**Teenus jookseb kokku pärast koodi muutmist:**
```bash
docker logs epood-orders   # või epood-products, epood-users
```

**Skaleerimine ei tööta (port conflict):**
```bash
# Eemalda products teenuselt ports rida docker-compose.microservices.yml failist
# sest mitu konteinerit ei saa sama porti kasutada
```
