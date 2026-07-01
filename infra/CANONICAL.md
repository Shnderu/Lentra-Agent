# LENTRA CANONICAL ARCHITECTURE

## 1. PRINCIPLE OF TRUTH

В системе существует только один производственный контур:

- Runtime = единственная точка входа выполнения
- Intelligence OS = единственный источник решений
- Market Intelligence = единственный домен интерпретации рынка
- Data Layer = единственный слой получения данных
- Bot/API = только интерфейсы доставки результата

Запрещено:
- создавать альтернативные pipeline / runtime / intelligence слои
- дублировать логику анализа рынка в разных доменах
- обходить Market Intelligence через domain/services/rent/* напрямую

---

## 2. CANONICAL EXECUTION FLOW

Telegram / API / Worker
        ↓
runtime/main.py
        ↓
runtime/bootstrap/container.py
        ↓
core/data_layer (ingestion + normalization)
        ↓
core/market_intelligence (ALL market reasoning)
        ↓
core/intelligence (AI OS - final decision layer)
        ↓
core/market_intelligence/verdict
        ↓
API / Bot response layer

---

## 3. SINGLE SOURCES OF TRUTH

### Runtime
/opt/lentra/infra/lentra/runtime

### Intelligence OS (EXTERNAL AI ENGINE HOOK)
/opt/lentra/infra/lentra/runtime/intelligence_gateway.py
/opt/lentra/infra/lentra/core/intelligence

### Market Intelligence Core
/opt/lentra/infra/lentra/core/market_intelligence

### Data Layer
/opt/lentra/infra/lentra/core/data_layer

### Bootstrap
/opt/lentra/infra/lentra/runtime/bootstrap

---

## 4. LEGACY (DO NOT EXTEND)

Следующие модули считаются legacy и не должны использоваться для новых решений:

- lentra/rent/*
- lentra/domain/*
- lentra/services/*
- lentra/pipeline/*
- lentra/application/*
- lentra/ranking/*
- lentra/property/*

Они могут существовать только как:
- адаптеры
- источники данных
- временные мосты

---

## 5. AI INTELLIGENCE OS

Единственная точка интеграции:

lentra/runtime/intelligence_gateway.py

Контракт:

    interpret(payload: dict) -> dict

Запрещено:
- добавлять промежуточные AI layers
- добавлять feature-specific intelligence wrappers
- создавать task-specific engines (price/risk/dedup отдельно)

---

## 6. MARKET PRINCIPLE

Система НЕ является агрегатором.

Система является:

> Market Interpretation OS

Функции:
- цена относительно рынка
- риск объявления
- дубли
- районная аналитика
- объяснение качества объекта

---

## 7. GOVERNANCE RULE

Любая новая функциональность должна:
1. идти через Market Intelligence
2. затем через Intelligence OS
3. не обходить runtime gateway

---

## 8. FREEZE RULE

После фиксации canonical architecture:
- новые слои архитектуры запрещены
- допускается только расширение существующих модулей
- любые новые engines должны быть plugin-based внутри core/market_intelligence/plugins
