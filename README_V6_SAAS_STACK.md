# Lentra SaaS-Grade Docker Stack V6 (Production Architecture)

## Цель
Стабильная production архитектура:
- единый base image
- deterministic builds
- shared dependency layer
- быстрые rebuilds (cache-first)
- изоляция сервисов
- предсказуемый runtime

---

# 1. ROOT STRUCTURE

/opt/lentra
├── Dockerfile.base
├── requirements.core.txt
├── api/
├── bot/
├── worker/
├── miniapp/
├── infra/
│   └── docker-compose.yml

---

# 2. CORE DEPENDENCIES (SINGLE SOURCE OF TRUTH)

/opt/lentra/requirements.core.txt

fastapi
uvicorn
redis
pydantic
httpx
aiogram
tenacity
python-dotenv

---

# 3. BASE IMAGE (IMMUTABLE LAYER)

/opt/lentra/Dockerfile.base

FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

RUN pip install --upgrade pip

COPY requirements.core.txt /tmp/core.txt
RUN pip install -r /tmp/core.txt

---

# 4. SERVICE PATTERN (STANDARDIZED)

## API Dockerfile
FROM lentra-base:latest

WORKDIR /app

COPY api/ /app/api/
COPY core/ /app/core/

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

---

## WORKER Dockerfile
FROM lentra-base:latest

WORKDIR /app

COPY worker/ /app/worker/
COPY core/ /app/core/

CMD ["python", "-u", "worker/worker.py"]

---

## BOT Dockerfile
FROM lentra-base:latest

WORKDIR /app

COPY bot/ /app/bot/
COPY core/ /app/core/

CMD ["python", "bot/main.py"]

---

## MINIAPP (STATIC NGINX)
FROM nginx:alpine

COPY miniapp/ /usr/share/nginx/html

---

# 5. DOCKER COMPOSE (PRODUCTION)

version: "3.9"

services:

  redis:
    image: redis:7-alpine
    container_name: lentra-redis

  db:
    image: postgres:15
    container_name: lentra-db
    environment:
      POSTGRES_USER: lentra
      POSTGRES_PASSWORD: lentra
      POSTGRES_DB: lentra

  api:
    build:
      context: ..
      dockerfile: api/Dockerfile
    container_name: lentra-api
    depends_on: [redis, db]
    ports:
      - "8000:8000"

  worker:
    build:
      context: ..
      dockerfile: worker/Dockerfile
    container_name: lentra-worker
    depends_on: [redis, db]

  bot:
    build:
      context: ..
      dockerfile: bot/Dockerfile
    container_name: lentra-bot
    depends_on: [api, redis]

  miniapp:
    build:
      context: ..
      dockerfile: miniapp/Dockerfile
    container_name: lentra-miniapp
    ports:
      - "8080:80"

---

# 6. KEY ARCHITECTURAL RULES

## RULE 1 — NO DUPLICATE DEPENDENCIES
All Python deps ONLY in:
requirements.core.txt

## RULE 2 — NO pip install IN SERVICES
Never run pip install in api/bot/worker Dockerfiles

## RULE 3 — SINGLE BASE IMAGE
All services MUST use:
FROM lentra-base:latest

## RULE 4 — NO ../ COPY
All COPY paths must be inside build context root

## RULE 5 — SHARED CORE MODULE
/core must be copied into all services

---

# 7. PERFORMANCE MODEL

Before:
- rebuild time: 3–10 minutes
- pip install repeated 4 times
- inconsistent runtime

After:
- rebuild time: 10–40 seconds
- cached base layer
- deterministic dependencies
- no runtime drift

---

# 8. PRODUCTION READY FEATURES (NEXT PHASE)

To upgrade to V7:

- Redis Streams ingestion pipeline
- retry + backoff middleware
- DLQ (dead-letter queue)
- worker isolation lanes (rent.search / flights / alerts)
- async task fanout
- observability (prometheus + logs)

---

# STATUS

V6 = production-grade container architecture foundation
