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

**Testi terminalist** (ava uus aken):

```bash
# Kasutajate teenus otse
curl http://localhost:5051/users

# Toodete teenus otse
curl http://localhost:5052/products

# Loo tellimus läbi gateway
curl -X POST http://localhost:5070/api/orders -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 2, \"quantity\": 3}"
```

---

## 3. Mis juhtub kui teenus kukub?

See on mikroteenuste kõige olulisem õppetund.

**Samm 1 — peata toodete teenus:**

```bash
docker stop epood-products
```

**Samm 2 — vaata brauseris** (värskenda F5):
- Toodete teenuse staatus → **OFFLINE** 🔴
- Tooted kaovad lehelt
- Proovi luua tellimus — saad veateate

> **Küsimus:** Kas monoliidis saaks sama juhtuda — et ainult üks osa lakkab töötamast?

**Samm 3 — taasta teenus:**

```bash
docker start epood-products
```

---

## 4. Vaata logisid — näe kuidas teenused suhtlevad

Ava **kolm terminali akent** (Mac: Cmd+T / Windows: uus aken):

```bash
# Aken 1
docker logs -f epood-orders

# Aken 2
docker logs -f epood-users

# Aken 3
docker logs -f epood-products
```

Loo brauseris tellimus ja jälgi kõiki kolme akent korraga.

> **Küsimus:** Kummas on lihtsam probleeme leida — monoliidi üks log vs mikroteenuste mitu logi?

---

## 5. Lisa uus toode

Lisa toode: **Monitor**, hind **349.99**, emoji **🖥️**

**Samm 1 — muuda koodi** (ainult toodete teenus!):

```bash
python3 patches/05-micro-add-product.py
```

**Samm 2 — käivita uuesti:**

```bash
docker compose -f docker-compose.microservices.yml up --build
```

**Samm 3 — kontrolli brauserist** http://localhost:5070

> **Küsimus:** Muutsid ainult `microservices/products/app.py`. Ühtegi teist teenust ei puudutatud. Monoliidis muutsid sama faili kus on KÕIK. Mis vahe on 10-liikmelises meeskonnas?

---

## 6. Lisa uus kasutaja

Lisa kasutaja: **Kati Kask**, email **kati@example.com**

**Samm 1 — muuda koodi** (ainult kasutajate teenus!):

```bash
python3 patches/06-micro-add-user.py
```

**Samm 2 — käivita uuesti:**

```bash
docker compose -f docker-compose.microservices.yml up --build
```

**Samm 3 — kontrolli:**

```bash
curl http://localhost:5051/users
```

---

## 7. Lisa otsingu endpoint

Lisa toote otsimine nime järgi.

**Samm 1 — muuda koodi:**

```bash
python3 patches/07-micro-add-search.py
```

**Samm 2 — käivita uuesti:**

```bash
docker compose -f docker-compose.microservices.yml up --build
```

**Samm 3 — testi** (otse toodete teenuselt):

```bash
curl "http://localhost:5052/products/search?name=hiir"
```

> **Küsimus:** Miks on aadress `localhost:5052` mitte `localhost:5070`? Sest otsing on toodete teenuse funktsioon — küsid otse toodete teenuselt, mitte gateway kaudu.

---

## 8. Lisa allahindlus

Lisa loogika: **kogus 5 või rohkem → 10% allahindlus**.

**Samm 1 — muuda koodi** (ainult tellimuste teenus!):

```bash
python3 patches/08-micro-add-discount.py
```

**Samm 2 — käivita uuesti:**

```bash
docker compose -f docker-compose.microservices.yml up --build
```

**Samm 3 — testi** (telli 5 toodet):

```bash
curl -X POST http://localhost:5053/orders -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 2, \"quantity\": 5}"
```

Kontrolli brauserist — tellimusel peaks olema allahindluse summa näha.

---

## 9. Kiiruse võrdlus

```bash
for i in 1 2 3 4 5; do time curl -s -X POST http://localhost:5070/api/orders -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 1, \"quantity\": 1}" > /dev/null; done
```

Võrdle monoliidi tulemusega:

| | Monoliit | Mikroteenused |
|---|---|---|
| Keskmine aeg | ___ ms | ___ ms |

> **Küsimus:** Mikroteenused on aeglasemad — miks? Tellimuse loomisel teeb orders-teenus 2 HTTP päringut (users + products). Monoliidis loeb ta andmed otse mälust. Kas see on alati probleem?

---

## 10. Skaleeri üht teenust

```bash
docker compose -f docker-compose.microservices.yml up --scale products=3 -d
```

Kontrolli:

```bash
docker compose -f docker-compose.microservices.yml ps
```

Näed kolm `epood-products` konteinerit! Kasutajate ja tellimuste teenused jäid samaks.

Taasta normaalolek:

```bash
docker compose -f docker-compose.microservices.yml up --scale products=1 -d
```

> **Küsimus:** Black Friday ajal saab toodete teenus 100x rohkem liiklust. Mikroteenustes skaleerid ainult toodete teenust. Monoliidis pead skaleerima kogu rakendust. Mis on rahaline mõju pilves?

---

## 11. Testi arvustuste teenust

```bash
# Lisa arvustus
curl -X POST http://localhost:5054/reviews -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 1, \"rating\": 5, \"comment\": \"Vaga hea!\"}"

# Lisa teine arvustus
curl -X POST http://localhost:5054/reviews -H "Content-Type: application/json" -d "{\"user_id\": 2, \"product_id\": 1, \"rating\": 3, \"comment\": \"Aku voiks kauem kesta\"}"

# Vaata kõiki arvustusi
curl http://localhost:5054/reviews

# Vaata ühe toote arvustusi
curl http://localhost:5054/reviews/product/1
```

> **Küsimus:** Arvustuste teenuse lisamiseks ei muudetud ühtegi olemasolevat faili. Monoliidis peaksid muutma `app.py` faili kus on juba kõik muu. Kumba eelistad 50-liikmelises meeskonnas?

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
