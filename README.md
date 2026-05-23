# Tarkvaraarenduse labor: Monoliit vs Mikroteenused

Selles laboris võrdled kahte arhitektuurimudelit – **monoliitset** ja **mikroteenuste** põhist rakendust. Mõlemad teevad sama asja (lihtne e-poe API), aga on üles ehitatud erinevalt.

## Eeldused

- Docker ja Docker Compose on paigaldatud
- Terminal/käsurida on tuttav

## Projekti struktuur

```
├── monolith/              # Kõik ühes rakenduses
│   └── app.py             # Üks fail = kogu rakendus
├── microservices/         # Eraldi teenused
│   ├── users/             # Kasutajate teenus (port 5051)
│   ├── products/          # Toodete teenus (port 5052)
│   └── orders/            # Tellimuste teenus (port 5053)
├── docker-compose.monolith.yml
└── docker-compose.microservices.yml
```

---

## 1. osa – Monoliit

### Käivita monoliit

```bash
docker compose -f docker-compose.monolith.yml up --build
```

### Testi (uues terminali aknas)

```bash
# Vaata kõiki kasutajaid
curl http://localhost:5050/users

# Vaata kõiki tooteid
curl http://localhost:5050/products

# Loo tellimus
curl -X POST http://localhost:5050/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 2, "quantity": 3}'

# Vaata tellimusi
curl http://localhost:5050/orders
```

### Peata monoliit

```bash
docker compose -f docker-compose.monolith.yml down
```

---

## 2. osa – Mikroteenused

### Käivita mikroteenused

```bash
docker compose -f docker-compose.microservices.yml up --build
```

### Testi (uues terminali aknas)

```bash
# Kasutajate teenus (port 5051)
curl http://localhost:5051/users

# Toodete teenus (port 5052)
curl http://localhost:5052/products

# Tellimuste teenus (port 5053) - see suhtleb teiste teenustega!
curl -X POST http://localhost:5053/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 2, "quantity": 3}'

# Vaata tellimusi
curl http://localhost:5053/orders
```

### Peata mikroteenused

```bash
docker compose -f docker-compose.microservices.yml down
```

---

## Ülesanded

### Ülesanne 1: Võrdle koodi

Ava `monolith/app.py` ja võrdle seda `microservices/` kaustaga. Vasta küsimustele:
- Mitu faili on monoliidis vs mikroteenustes?
- Kus toimub tellimuse loomisel kasutaja ja toote kontrollimine kummaski variandis?

### Ülesanne 2: Mis juhtub kui teenus kukub?

Mikroteenuste variandis peata toodete teenus:
```bash
docker stop epood-products
```

Proovi nüüd luua tellimus:
```bash
curl -X POST http://localhost:5053/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 1, "quantity": 1}'
```

**Küsimus:** Mis juhtus? Kas monoliidis saaks sama asi juhtuda?

Käivita teenus uuesti:
```bash
docker start epood-products
```

### Ülesanne 3: Lisa uus toode

Lisa mõlemasse rakendusse uus toode (nt "Monitor", hind 349.99):
- Monoliidis: muuda ühte faili
- Mikroteenustes: muuda toodete teenust

**Küsimus:** Kummas oli lihtsam? Miks?

---

## Arutelu

Pärast labori lõpetamist arutle:
1. Millal eelistaksid monoliiti? Millal mikroteenuseid?
2. Mis on mikroteenuste suurim eelis? Suurim puudus?
3. Kui sul oleks 2-liikmeline tiim ja 2 nädalat aega, kumma valiksid?
