# Tarkvaraarenduse labor: Monoliit vs Mikroteenused

Selles laboris uurid kahte erinevat arhitektuurimudelit. Mõlemad rakendused teevad sama asja — lihtne e-poe rakendus kasutajate, toodete ja tellimustega — aga on üles ehitatud täiesti erinevalt.

---

## Eeldused

- Docker ja Docker Compose on paigaldatud
- Git on paigaldatud
- Python 3 on paigaldatud

---

## Repo kloonimine

```bash
git clone https://github.com/svnder/Tarkvaraarendus-lab.git
cd Tarkvaraarendus-lab
```

---

## Projekti struktuur

```
Tarkvaraarendus-lab/
├── monolith/                        # Monoliit — kõik ühes rakenduses
│   ├── app.py                       # Kogu rakendus ühes failis
│   ├── templates/index.html
│   ├── static/style.css
│   ├── requirements.txt
│   └── Dockerfile
├── microservices/                   # Mikroteenused — eraldi teenused
│   ├── users/                       # Kasutajate teenus (port 5051)
│   ├── products/                    # Toodete teenus (port 5052)
│   ├── orders/                      # Tellimuste teenus (port 5053)
│   ├── reviews/                     # Arvustuste teenus (port 5054)
│   └── gateway/                     # Veebileht ja sisend (port 5070)
├── patches/                         # Skriptid koodi muutmiseks
├── docker-compose.monolith.yml
├── docker-compose.microservices.yml
├── MONOLIIT.md                      ← Monoliidi juhend
└── MIKROTEENUSED.md                 ← Mikroteenuste juhend
```

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

## Alusta siit

👉 **[MONOLIIT.md](MONOLIIT.md)** — käivita ja uuri monoliitset rakendust

👉 **[MIKROTEENUSED.md](MIKROTEENUSED.md)** — käivita ja uuri mikroteenuseid

---

## Alusta nullist

Kui midagi läks valesti, taasta kõik algse seisu:

```bash
# Mac / Linux
docker compose -f docker-compose.monolith.yml down
docker compose -f docker-compose.microservices.yml down
docker system prune -f
git checkout -- .

# Windows (PowerShell)
docker compose -f docker-compose.monolith.yml down
docker compose -f docker-compose.microservices.yml down
docker system prune -f
git checkout -- .
```

Seejärel käivita uuesti valitud juhendi järgi.

---

## Probleemide lahendamine

**Veendu alati et oled repo juurkaustas:**

```bash
# Mac / Linux
cd ~/Tarkvaraarendus-lab

# Windows
cd ~\Tarkvaraarendus-lab
```

**Port on hõivatud:**

```bash
# Mac / Linux
lsof -i :5050

# Windows
netstat -ano | findstr :5050
```

**Muudatused ei kajastu pärast koodi muutmist:**

```bash
docker compose -f docker-compose.monolith.yml down
docker compose -f docker-compose.monolith.yml up --build
```

**Teenuse logid (veateate leidmiseks):**

```bash
docker logs epood-monolith
docker logs epood-orders
docker logs epood-products
```
