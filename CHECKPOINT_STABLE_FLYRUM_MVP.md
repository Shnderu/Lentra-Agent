# 🚀 FlyRum Stable Checkpoint (MVP)

Дата: 2026-06-09

---

## 💡 СТАТУС СИСТЕМЫ

Полностью рабочий event-driven pipeline:
---

## ✅ РАБОЧИЕ КОМПОНЕНТЫ

### 1. Bot (aiogram)
- Command /start
- unified_entry pipeline
- routing в FSM + intent layer

### 2. FSM Layer (Redis)
- route_from
- route_to
- route_date
- set/get/clear state

### 3. Intent System
- classify(text) → route_search

### 4. Queue System (PostgreSQL)
- table: tasks
- enqueue(task_type, payload)
- claim(worker)
- ack / fail

### 5. Worker
- worker_main.py loop
- process_once()
- route_search handler
- Telegram send_message

---

## 📦 DATABASE SCHEMA

Table: tasks

- id SERIAL
- type TEXT
- payload JSONB
- status TEXT
- attempts INT
- run_after TIMESTAMP
- locked_by TEXT
- timestamps

---

## ⚙️ INFRASTRUCTURE

- docker compose (bot + worker + db + redis)
- PostgreSQL 15
- Redis 7
- Python 3.11

---

## 💬 FLOW EXAMPLE---

## 🧠 КРИТИЧЕСКИЕ ЗАМЕТКИ

- FSM не возвращает UI напрямую
- Queue отделена от bot
- Worker полностью async consumer
- Pipeline event-driven

---

## 🚀 СТАБИЛЬНОЕ СОСТОЯНИЕ

✔ Bot работает  
✔ FSM работает  
✔ Queue работает  
✔ Worker работает  
✔ End-to-end flow работает  

