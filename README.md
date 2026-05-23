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
│   │   ├── app.py
│   │   └── ...
│   ├── products/                      # Toodete teenus (port 5052)
│   │   ├── app.py
│   │   └── ...
│   ├── orders/                        # Tellimuste teenus (port 5053)
│   │   ├── app.py
│   │   └── ...
│   └── gateway/                       # API Gateway — veebileht (port 5060)
│       ├── app.py
│       ├── templates/index.html
│       └── static/style.css
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

Sa peaksid nägema e-poe lehte koos toodete, kasutajate ja tellimuse vormiga.

### 2.3 Testi rakendust

1. Vaata tooteid ja kasutajaid lehel
2. Loo tellimus — vali kasutaja ID, toote ID ja kogus, vajuta "Loo tellimus"
3. Vaata kuidas tellimus ilmub tellimuste nimekirja

### 2.4 Testi terminalist (valikuline)

Ava uus terminali aken (Cmd+T / Ctrl+Shift+T):

```bash
# Vaata kasutajaid
curl http://localhost:5050/api/users

# Vaata tooteid
curl http://localhost:5050/api/products

# Loo tellimus
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

See käivitab **4 eraldi konteinerit**:
- `epood-gateway` — veebileht (port 5060)
- `epood-users` — kasutajate teenus (port 5051)
- `epood-products` — toodete teenus (port 5052)
- `epood-orders` — tellimuste teenus (port 5053)

### 3.2 Ava brauseris

Mine aadressile: **http://localhost:5060**

Pane tähele:
- Lehel on **teenuste staatus** — näed reaalajas, kas iga teenus töötab
- Leht näeb välja sarnane monoliidile, aga taustal päritakse andmed **eraldi teenustest**

### 3.3 Testi rakendust

1. Loo tellimus läbi veebi — see käivitab ketireaktsiooni:
   - Gateway saadab päringu → Tellimuste teenus
   - Tellimuste teenus pärib kasutaja infot → Kasutajate teenus
   - Tellimuste teenus pärib toote infot → Toodete teenus
   - Tulemus tuleb tagasi läbi kogu keti

### 3.4 Peata mikroteenused

```bash
docker compose -f docker-compose.microservices.yml down
```

---

## 4. Ülesanne: Mis juhtub kui teenus kukub?

See on mikroteenuste kõige olulisem õppetund.

### 4.1 Käivita mikroteenused

```bash
docker compose -f docker-compose.microservices.yml up --build
```

### 4.2 Ava brauser

Mine **http://localhost:5060** ja veendu, et kõik teenused on "ONLINE".

### 4.3 Peata toodete teenus

Ava uus terminali aken ja:

```bash
docker stop epood-products
```

### 4.4 Vaata mis juhtub

1. **Värskenda lehte** (F5) brauseris
2. Toodete teenuse staatus peaks olema **OFFLINE** 🔴
3. Tooted ei kuvata enam
4. Proovi luua tellimus — sa saad veateate, sest tellimuste teenus ei saa toodete teenusega ühendust

### 4.5 Küsimus aruteluks

> Mis juhtus? Kas monoliidis saaks sama asi juhtuda — et ainult üks osa rakendusest lakkab töötamast?

### 4.6 Taasta teenus

```bash
docker start epood-products
```

Värskenda lehte — kõik peaks taas töötama.

---

## 5. Ülesanne: Lisa uus toode

Lisa mõlemale rakendusele uus toode: **Monitor**, hind **349.99**, emoji **🖥️**.

### 5.1 Monoliidis

Ava fail `monolith/app.py` ja leia toodete nimekiri. Lisa uus toode:

```diff
 products = [
     {"id": 1, "name": "Sülearvuti", "price": 899.99, "emoji": "💻"},
     {"id": 2, "name": "Hiir", "price": 29.99, "emoji": "🖱️"},
     {"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},
+    {"id": 4, "name": "Monitor", "price": 349.99, "emoji": "🖥️"},
 ]
```

Rebuild ja käivita:

```bash
docker compose -f docker-compose.monolith.yml up --build
```

### 5.2 Mikroteenustes

Ava fail `microservices/products/app.py` ja lisa sama toode:

```diff
 products = [
     {"id": 1, "name": "Sülearvuti", "price": 899.99, "emoji": "💻"},
     {"id": 2, "name": "Hiir", "price": 29.99, "emoji": "🖱️"},
     {"id": 3, "name": "Klaviatuur", "price": 79.99, "emoji": "⌨️"},
+    {"id": 4, "name": "Monitor", "price": 349.99, "emoji": "🖥️"},
 ]
```

Rebuild ja käivita:

```bash
docker compose -f docker-compose.microservices.yml up --build
```

### 5.3 Küsimus aruteluks

> Kummas oli muudatus lihtsam? Mõlemas muutsid üht faili — aga mis vahe on? Mõtle: kui meeskonnas on 10 arendajat, siis monoliidis muudad sama faili kus on KÕIK. Mikroteenustes muudad ainult toodete teenust.

---

## 6. Ülesanne: Lisa uus kasutaja

Lisa uus kasutaja: **Kati Kask**, email **kati@example.com**.

### 6.1 Monoliidis

Ava `monolith/app.py`:

```diff
 users = [
     {"id": 1, "name": "Mari Maasikas", "email": "mari@example.com"},
     {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},
+    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},
 ]
```

### 6.2 Mikroteenustes

Ava `microservices/users/app.py`:

```diff
 users = [
     {"id": 1, "name": "Mari Maasikas", "email": "mari@example.com"},
     {"id": 2, "name": "Jaan Jansen", "email": "jaan@example.com"},
+    {"id": 3, "name": "Kati Kask", "email": "kati@example.com"},
 ]
```

Rebuild mõlemat ja kontrolli brauserist, kas uus kasutaja ilmub.

---

## 7. Ülesanne: Lisa otsingu endpoint

Lisa toodete otsimise võimalus nime järgi.

### 7.1 Monoliidis

Ava `monolith/app.py` ja lisa uus endpoint peale olemasolevat `get_product` funktsiooni:

```diff
 @app.route("/api/products/<int:product_id>", methods=["GET"])
 def get_product(product_id):
     product = next((p for p in products if p["id"] == product_id), None)
     if not product:
         return jsonify({"error": "Toodet ei leitud"}), 404
     return jsonify(product)


+@app.route("/api/products/search", methods=["GET"])
+def search_products():
+    query = request.args.get("name", "").lower()
+    if not query:
+        return jsonify({"error": "Lisa parameeter ?name=otsingusõna"}), 400
+    results = [p for p in products if query in p["name"].lower()]
+    return jsonify({"results": results, "count": len(results)})
```

Testi:
```bash
curl "http://localhost:5050/api/products/search?name=hiir"
```

### 7.2 Mikroteenustes

Ava `microservices/products/app.py` ja lisa sama endpoint:

```diff
 @app.route("/products/<int:product_id>", methods=["GET"])
 def get_product(product_id):
     product = next((p for p in products if p["id"] == product_id), None)
     if not product:
         return jsonify({"error": "Toodet ei leitud"}), 404
     return jsonify(product)


+@app.route("/products/search", methods=["GET"])
+def search_products():
+    query = request.args.get("name", "").lower()
+    if not query:
+        return jsonify({"error": "Lisa parameeter ?name=otsingusõna"}), 400
+    results = [p for p in products if query in p["name"].lower()]
+    return jsonify({"results": results, "count": len(results)})
```

Testi:
```bash
curl "http://localhost:5052/products/search?name=hiir"
```

### 7.3 Küsimus aruteluks

> Pane tähele endpoindi erinevust: monoliidis on `/api/products/search`, mikroteenustes `/products/search`. Miks? Sest mikroteenustes iga teenus EI TEA teistest — tal pole vaja `/api/` prefiksit, sest tema ongi kogu API.

---

## 8. Ülesanne: Lisa allahindlus tellimustele

Lisa loogika: kui kogus on 5 või rohkem, siis kehtib 10% allahindlus.

### 8.1 Monoliidis

Ava `monolith/app.py` ja muuda `create_order` funktsiooni:

```diff
     quantity = data.get("quantity", 1)
     total = product["price"] * quantity

+    # Allahindlus: 10% kui kogus >= 5
+    discount = 0
+    if quantity >= 5:
+        discount = total * 0.10
+        total = total - discount
+
     order = {
         "id": next_order_id,
         "user": user["name"],
         "product": product["name"],
         "quantity": quantity,
         "total": round(total, 2),
-        "status": "created"
+        "status": "created",
+        "discount": round(discount, 2)
     }
```

### 8.2 Mikroteenustes

Ava `microservices/orders/app.py` ja tee sama muudatus:

```diff
     quantity = data.get("quantity", 1)
     total = product["price"] * quantity

+    # Allahindlus: 10% kui kogus >= 5
+    discount = 0
+    if quantity >= 5:
+        discount = total * 0.10
+        total = total - discount
+
     order = {
         "id": next_order_id,
         "user": user["name"],
         "product": product["name"],
         "quantity": quantity,
         "total": round(total, 2),
-        "status": "created"
+        "status": "created",
+        "discount": round(discount, 2)
     }
```

Rebuild ja testi — telli 5+ toodet ja kontrolli, kas hind on 10% väiksem.

---

## 9. Kokkuvõte ja arutelu

Pärast labori lõpetamist arutle:

1. **Millal eelistaksid monoliiti?** Millal mikroteenuseid?
2. **Mis on mikroteenuste suurim eelis?** Suurim puudus?
3. **Kui sul oleks 2-liikmeline tiim ja 2 nädalat aega**, kumma valiksid?
4. **Mis juhtus kui peatasid ühe teenuse?** Kas see on eelis või puudus?
5. **Kummas oli lihtsam koodi muuta?** Aga kummas on lihtsam aru saada, mis toimub?

---

## Vihjed probleemide korral

**Port on hõivatud:**
```bash
# Vaata mis kasutab porti
lsof -i :5050

# macOS: AirPlay kasutab porti 5000, sellepärast kasutame 5050+
```

**Docker ei käivitu:**
```bash
# Kontrolli kas Docker töötab
docker info

# Puhasta vanad konteinerid
docker compose -f docker-compose.monolith.yml down
docker compose -f docker-compose.microservices.yml down
```

**Muudatused ei kajastu:**
```bash
# Peata ja rebuildi
docker compose -f docker-compose.monolith.yml down
docker compose -f docker-compose.monolith.yml up --build
```
