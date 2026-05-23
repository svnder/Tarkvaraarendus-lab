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
# Vaata kasutajaid
curl http://localhost:5050/api/users

# Vaata tooteid
curl http://localhost:5050/api/products

# Loo tellimus
curl -X POST http://localhost:5050/api/orders -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 2, \"quantity\": 3}"
```

---

## 3. Vaata koodi

Ava fail `monolith/app.py`. Pane tähele — **kõik on ühes failis**:
- Kasutajate andmed ja endpointid
- Toodete andmed ja endpointid
- Tellimuste loogika ja endpointid

> **Küsimus:** Kui 10 arendajat töötavad korraga selle ühe faili kallal, mis probleemid tekivad?

---

## 4. Lisa uus toode

Lisa toode: **Monitor**, hind **349.99**, emoji **🖥️**

**Samm 1 — muuda koodi:**

```bash
python3 patches/01-monolith-add-product.py
```

**Samm 2 — käivita uuesti:**

```bash
docker compose -f docker-compose.monolith.yml up --build
```

**Samm 3 — kontrolli brauserist** http://localhost:5050 — Monitor peaks ilmuma toodete nimekirja.

---

## 5. Lisa uus kasutaja

Lisa kasutaja: **Kati Kask**, email **kati@example.com**

**Samm 1 — muuda koodi:**

```bash
python3 patches/02-monolith-add-user.py
```

**Samm 2 — käivita uuesti:**

```bash
docker compose -f docker-compose.monolith.yml up --build
```

**Samm 3 — kontrolli:**

```bash
curl http://localhost:5050/api/users
```

---

## 6. Lisa otsingu endpoint

Lisa toote otsimine nime järgi.

**Samm 1 — muuda koodi:**

```bash
python3 patches/03-monolith-add-search.py
```

**Samm 2 — käivita uuesti:**

```bash
docker compose -f docker-compose.monolith.yml up --build
```

**Samm 3 — testi:**

```bash
curl "http://localhost:5050/api/products/search?name=hiir"
```

---

## 7. Lisa allahindlus

Lisa loogika: **kogus 5 või rohkem → 10% allahindlus**.

**Samm 1 — muuda koodi:**

```bash
python3 patches/04-monolith-add-discount.py
```

**Samm 2 — käivita uuesti:**

```bash
docker compose -f docker-compose.monolith.yml up --build
```

**Samm 3 — testi** (telli 5 toodet):

```bash
curl -X POST http://localhost:5050/api/orders -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 2, \"quantity\": 5}"
```

Kontrolli brauserist — tellimusel peaks olema allahindluse summa näha.

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

```bash
for i in 1 2 3 4 5; do time curl -s -X POST http://localhost:5050/api/orders -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 1, \"quantity\": 1}" > /dev/null; done
```

Pane kirja keskmine `real` väärtus — võrdled hiljem mikroteenustega.

---

## 10. Peata monoliit

```bash
docker compose -f docker-compose.monolith.yml down
```

Jätka: **[MIKROTEENUSED.md](MIKROTEENUSED.md)**
