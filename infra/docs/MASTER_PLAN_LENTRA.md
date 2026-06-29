# LENTRA — SEA RENT INTELLIGENCE / AI PROPERTY OS

---

# 1. КОНЦЕПЦИЯ

Lentra — это AI Market Intelligence OS для аренды недвижимости в ЮВА.

Не агрегатор. Не каталог. Не доска объявлений.

Это аналитический слой поверх рынка аренды.

---

# 2. ПРОБЛЕМА РЫНКА

ЮВА рынок аренды:

- фрагментирован
- нет единого источника
- много дублей
- устаревшие объявления
- высокий риск мошенничества
- отсутствует рыночная оценка цены

---

# 3. ЦЕЛЬ ПРОДУКТА

Система должна:

- собирать объявления
- нормализовать данные
- удалять дубли
- оценивать цену относительно рынка
- считать риск
- объяснять пользователю решение

---

# 4. ЦЕЛЕВАЯ АУДИТОРИЯ

- digital nomads
- expats
- long-term travelers
- remote workers

---

# 5. АРХИТЕКТУРА

## Data Layer
- Facebook Marketplace
- Telegram groups
- local sites
- agencies

## Normalization Layer
- валюты
- структура объектов

## Dedup Engine
- поиск одинаковых квартир
- кластеризация объявлений

## Market Intelligence Layer
- средняя цена
- сегменты рынка
- отклонения

## AI Decision Layer
- risk scoring
- pricing evaluation
- ranking
- explanation engine

---

# 6. TELEGRAM ARCHITECTURE

- runtime.py = единственный вход
- aiogram polling
- dispatcher removed
- systemd конфликт устранён

---

# 7. CURRENT STATE

## WORKING
- Telegram runtime stable
- pricing engine
- risk engine
- segmentation (coastal_premium)
- confidence scoring

## PARTIAL
- explanation engine (начат)

## MISSING
- dedup pipeline integration
- ranking engine
- comparison engine
- search layer

---

# 8. CURRENT STAGE

Stage 2:
Market Intelligence MVP Core

---

# 9. ROADMAP

## Phase 3A
- comparison engine
- ranking engine
- dedup integration

## Phase 3B
- UX layer (Telegram)
- structured responses

## Phase 4
- Mini App Telegram
- map UI
- marketplace interface

---

# 10. BUSINESS MODEL

- subscription
- premium AI concierge
- relocation services

---

# 11. CORE PRINCIPLE

Value = interpretation of market, not listings.

