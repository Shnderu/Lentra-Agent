# Lentra Architecture Map v1

## 1. PRINCIPLE (КАНОН СИСТЕМЫ)

Lentra = AI Market Intelligence OS для рынка аренды недвижимости SEA.

Главная ценность системы:
- интерпретация рынка аренды
- оценка цены относительно рынка
- риск-анализ (анти-скам)
- дедупликация объявлений
- ранжирование объектов

Execution layer является инфраструктурой, а не продуктовым ядром.

---

## 2. SYSTEM LAYERS

### 2.1 CORE (PRODUCT INTELLIGENCE LAYER)

Это ядро продукта. Здесь создаётся ценность.

#### Market Intelligence
- core/market/pricing.py

#### Risk Engine
- core/risk/risk_scorer.py

#### Deduplication Engine
- core/dedup/deduplicator.py

#### Ranking Engine
- core/ranking/ranker.py

#### Feature Store
- core/feature_store.py

#### Data Interpretation Layer
- core/data_layer/
  - builders/task_builder.py
  - sources/facebook.py
  - sources/base.py
  - fetcher.py
  - response/builder.py

---

### 2.2 INFRASTRUCTURE LAYER (SUPPORT SYSTEM)

Это слой исполнения и доставки задач.

#### Pipeline Execution
- core/pipeline/pipeline.py
- core/executor.py

#### Queue System
- core/queue/
  - task_model.py
  - task_repository.py
  - task_queue_repository.py
  - schema.sql

#### Router Layer
- core/intent_router.py
- core/intent/intent_router.py
- core/intent/intent_classifier.py
- core/intent/intent_resolver.py

#### Scenario System (execution logic only)
- core/scenario/
  - engine.py
  - scenario_engine.py
  - policy_engine.py

#### Worker Layer
- worker/
- telegram workers:
  - telegram/queue_worker.py
  - telegram/event_worker.py

---

### 2.3 SYSTEM CONTROL / SAFETY LAYER

Control plane системы (ограничения и защита исполнения).

- core/guards/
- core/system_guard.py
- core/system_boundary.py
- core/system_boundary_guard.py
- core/safety/
- core/contracts/
- core/trace/

---

### 2.4 EXPERIMENTAL LAYER (НЕ ЯДРО)

Это НЕ часть продуктового ядра.

#### Graph Execution System (эксперимент)
- core/graph/
- core/compiler/

#### Advanced Abstractions
- core/contracts/pipeline.py (частично)
- core/contracts/state_contract_v1.py
- core/typesystem/

---

## 3. ARCHITECTURAL RULES

### RULE 1 — CORE is dominant
Любая новая логика должна усиливать:
- pricing accuracy
- risk scoring
- dedup quality
- ranking quality

---

### RULE 2 — INFRA is passive
Pipeline / queue / worker:
- НЕ принимают бизнес решений
- НЕ содержат market logic

---

### RULE 3 — EXPERIMENTAL is isolated
graph/compiler:
- не участвует в production flow
- не влияет на core decision making

---

## 4. CURRENT SYSTEM STATE (REALITY CHECK)

Система сейчас находится в состоянии:

- CORE: partially implemented
- INFRA: over-engineered but stable
- EXPERIMENTAL: present but not integrated

---

## 5. REQUIRED NEXT STEP

Стабилизация:

1. Убрать graph/compiler из production dependency chain
2. Зафиксировать pipeline → market intelligence flow
3. Упростить scenario layer до execution role
4. Усилить core/risk + core/market + core/dedup

---

END OF CANONICAL MAP v1
