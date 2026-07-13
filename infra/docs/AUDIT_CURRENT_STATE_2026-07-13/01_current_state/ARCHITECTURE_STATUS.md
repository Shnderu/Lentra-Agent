# §1. CURRENT ARCHITECTURE STATUS

> Все пути относительно `/opt/lentra/infra`, пакет `lentra`, если не указано иное.

## Canonical Spine (Pipeline → Gateway → Engines → Ranking → Decision)

**Status: COMPLETE**

Evidence:
- Все 11 компонентов из `CANONICAL_COMPONENT_MAP.md` §4 существуют по документированным путям.
- `api/pipeline/search_pipeline.py:32` (`SearchPipeline`) импортирует `build_gateway_v3` (строка 4), RiskEngine/DedupEngine (7–8), DecisionLayer/UnifiedRankingEngine (10–11), MarketService (28).
- GatewayV3 регистрирует ровно 4 движка: `market_intelligence`, `area`, `risk`, `dedup` (`runtime/bootstrap/gateway_v3.py:107-128`).
- arch_lock правила `CANONICAL_SPINE_INTEGRITY` и `RISK_VETO_INTEGRITY` проходят без пропусков.
- Документированная особенность сохранена: risk/dedup вызываются напрямую (`search_pipeline.py:302` и далее), area/market_intelligence — через gateway. Те же классы, не баг.

## Entry Points (API / Bot / Recovery)

**Status: COMPLETE**

Evidence:
- systemd: `lentra-api`, `lentra-bot`, `lentra-recovery` — active.
- API `/health` → `{"status":"ok"}`.
- Замыкание импортов бота = 5 модулей, ноль intelligence-импортов (Constitution §3 соблюдена: бот — HTTP-клиент API).
- Recovery: `worker/recovery_worker.py` → `core/pipeline/worker_search_entrypoint.py` → `CanonicalSearchPipeline` (facade без логики, не деградировал) → тот же `SearchPipeline`.

## Arch Lock Enforcement

**Status: PARTIAL** (Phase 3 из 4 — dry-run live, non-blocking)

Evidence:
- `rules_v1.json` v2.0 (11 правил), `rule_loader.py`, runner v1.6 через `ExecStartPre=-`.
- Дефектное правило `NO_API_TO_CORE_BACKFLOW` удалено согласно ADR.
- Отсутствует: пере-генерация SEAL.json, CI-хук, blocking mode (`-` префикс на месте).
- Процессный дефект: `ADR_ARCH_LOCK_RULE_MIGRATION_V1.md` до сих пор **Status: PROPOSED**, хотя Phases 2–3, которые он регулирует, уже реализованы.

## Legacy Deletion

**Status: PARTIAL (~70–75% выполнено)**

Evidence:
- Batch B в основном выполнен: удалены все дубликаты pipeline'ов, risk-семейство, flat decision/MIE, wiring*, пакет IntelligenceGateway, `build.py`, worker/loop/runtime, runtime/intelligence/*.
- Остатки — см. `02_compliance/LEGACY_INVENTORY.md`.
- Внимание: удаления выполнены ДО документированных предусловий (documents → enforcement → deletion). Уже сделано, но это отклонение от порядка.

## Data Layer / Ingestion (целевая цель по Consolidation Map и Master Plan)

**Status: PARTIAL — существует, но НЕ СООТВЕТСТВУЕТ конституции** (новое после аудита, без ADR)

Evidence:
- `core/data_layer/` (23 py-файла, коммиты `843877c0..a42660dd`, все 2026-07-13).
- `data_layer/pipeline/ingestion_pipeline.py` (`IngestionPipeline`) инстанцирует `RiskEngine()` напрямую и вызывает MI через новые адаптеры, минуя GatewayV3 → нарушение Constitution §4 («никто не вызывает движки через другой маршрутизатор») и §11.1 (второй поток).
- Контур недостижим из production-юнитов (offline seed-путь), но пишет в `storage/market_snapshots/market_snapshots.json`, который читает production `MarketTruthEngine` → фактический «чёрный ход» в market truth.

## Documents

**Status: PARTIAL**

- Правила (Constitution, Component Map) актуальны.
- Инвентари (Cleanup Plan §2–3, Deletion Manifest батчи) устарели на 1 день: многое уже удалено, часть SAFE DELETE записей теперь ложна (см. `risk_engine_adapter.py` — пересоздан и используется ingestion-контуром).
- DecisionLayer в коде self-describes «v2.2», карта говорит «v2.1» — дрейф документации.

## Working Tree

**Status: DIRTY — на защищённом spine**

```
 M infra/lentra/core/market_intelligence/contracts/listing_contract_guard.py   ← SPINE (DO-NOT-TOUCH)
 M infra/lentra/core/market_intelligence/adapters/pipeline_pricing_adapter.py
 M infra/lentra/storage/market_snapshots/market_snapshots.json
```

- Грязный `listing_contract_guard.py` **убирает backfill `price_vnd`** (`listing["price_vnd"] = listing["price"]` удалён) — поведенческий риск, без ADR, загрузится при следующем рестарте `lentra-api`/`lentra-recovery`.
- Грязный `pipeline_pricing_adapter.py` превращает `build_market()` в заглушку, возвращающую нули.
- **Это блокер №1 — решить до любых других работ.**
