# Tarkvaraarenduse labor: Monoliit vs Mikroteenused

Selles laboris võrdled kahte arhitektuurimudelit — **monoliitset** ja **mikroteenuste** põhist rakendust. Mõlemad teevad sama asja (lihtne e-poe rakendus), aga on üles ehitatud täiesti erinevalt.

---

## Eeldused

- Docker ja Docker Compose on paigaldatud
- Terminal on tuttav
- Git on paigaldatud

---

## Projekti struktuur

```
Tarkvaraarendus-lab/
├── monolith/                        # MONOLIIT — kõik ühes rakenduses
│   ├── app.py                       # Kogu rakendus ühes failis
│   ├── templates/index.html         # Veebileht
│   ├── static/style.css             # Stiilid
│   ├── requirements.txt
│   └── Dockerfile
├── microservices/                   # MIKROTEENUSED — eraldi teenused
│   ├── users/                       # Kasutajate teenus (port 5051)
│   ├── products/                    # Toodete teenus (port 5052)
│   ├── orders/                      # Tellimuste teenus (port 5053)
│   ├── reviews/                     # Arvustuste teenus (port 5054)
│   └── gateway/                     # Veebileht ja API Gateway (port 5070)
├── patches/                         # Koodimuudatused ülesannete jaoks
├── docker-compose.monolith.yml
├── docker-compose.microservices.yml
├── MONOLIIT.md                      # Monoliidi ülesanded
└── MIKROTEENUSED.md                 # Mikroteenuste ülesanded
```

---

## Kuidas alustada?

Vali kumba soovid uurida:

- 👉 **[MONOLIIT.md](MONOLIIT.md)** — kõik ühes rakenduses, üks server, üks port
- 👉 **[MIKROTEENUSED.md](MIKROTEENUSED.md)** — eraldi teenused, eraldi konteinerid, eraldi pordid

---

## Alusta nullist

Kui midagi läks valesti ja tahad kõik taastada algse seisu:

```bash
cd ~/Tarkvaraarendus-lab
docker compose -f docker-compose.monolith.yml down
docker compose -f docker-compose.microservices.yml down
docker system prune -f
git checkout -- .
```

Seejärel käivita uuesti valitud juhendi järgi.

---

## Pordid

| Rakendus | Port | Aadress |
|---|---|---|
| Monoliit | 5050 | http://localhost:5050 |
| Gateway (mikroteenused) | 5070 | http://localhost:5070 |
| Kasutajate teenus | 5051 | http://localhost:5051 |
| Toodete teenus | 5052 | http://localhost:5052 |
| Tellimuste teenus | 5053 | http://localhost:5053 |
| Arvustuste teenus | 5054 | http://localhost:5054 |

---

## Vihjed probleemide korral

**Veendu et oled alati repo juurkaustas:**
```bash
cd ~/Tarkvaraarendus-lab
pwd
# Peaks näitama: /Users/sander/Tarkvaraarendus-lab
```

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

**Teenus jookseb kokku:**
```bash
docker logs epood-monolith
docker logs epood-orders
docker logs epood-products
```
