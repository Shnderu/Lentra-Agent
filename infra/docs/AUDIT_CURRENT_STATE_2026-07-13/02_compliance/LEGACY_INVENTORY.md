# §6. LEGACY COMPONENT INVENTORY

> Три категории. Удаление не рекомендуется без доказательства (grep импортёров на момент удаления).

## SAFE TO REMOVE (0 production-импортёров, проверено grep + arch_lock)

**Dedup-остатки:**
- `dedup/dedup_engine.py`, `dedup/unified_dedup_engine.py`, `engines/dedup.py`
- `adapters/dedup_engine_adapter.py`, `contracts/dedup_engine_contract.py`
- `core/ai/deduplication_engine.py`, `infra/app/core/quality/deduplicator.py`

**Ranking-остатки:**
- `ranking/ranking_engine_v3.py`, `decision/ranking_engine.py`, `bot/ux/ranking.py`
- `domain/scoring/ranking_engine.py`, `rent/ranking/engine/ranking_engine.py`

**Прочие движки/шлюзы:**
- `risk/market_risk_engine.py`
- `core/market_intelligence/gateway.py` (flat), `services/intelligence_gateway.py`, `api/gateway.py`
- `runtime/bootstrap/engine_restore.py`

**Битые модули (импортируют несуществующий `lentra.core.pipeline.search_pipeline`):**
- `api/search/search_api.py`, `api/v1/debug_api.py`, `api/v1/concierge_api_class.py`

**Мусор (Batch A):**
- `elf.pipeline = pipeline`, `elf.pipeline.run(objects)` (корневые файлы)
- `civilizatio/` (пустой typo-дубль), `init_v*_dirs.sh` / `init_*_structure.sh` / `create_*_dirs.sh` (~30 скриптов)
- test-мусор (`infra/test_write.txt`, `infra/test instruction`, бинарники)
- `civilization/` — **подтвердить содержимое перед удалением** (Manifest Batch A)

## NEEDS REWIRING (есть живые/полуживые рёбра — не удалять вслепую)

- `runtime/bootstrap/worker_main.py` + **юнит `lentra-worker.service`** (active). Сначала disable юнит, потом удалить файл.
- `runtime/bootstrap/main.py`, `runtime/bootstrap/graph_attach.py`, `runtime/bootstrap.py`, `api/pipeline_bootstrap.py`, `telegram/dispatcher.py` — это 5 текущих arch_lock-нарушений; удалять после решений по юнитам.
- **Ingestion-контур:** `data_layer/pipeline/*`, `adapters/{pipeline_pricing,pipeline_dedup,pipeline_area,risk_engine}_adapter.py`, `engines/pricing_engine.py`, внешние импорты `market_truth_engine` — нужен ADR + маршрутизация через gateway, НЕ удаление (это реализация целевого Data Layer).
- `contracts/routing_map.py` / `routing_map_lock.py` — чинить содержимое, не удалять (декларативные lock'и).
- Цепочка `api/services/gateway.py → core/product_router.py → api/services/search_service.py` — orphan-голова; убрать комплектом.
- `bot/handlers/{rent_handler,router_builder}.py` — файлы внутри production-пакета бота; в `bot/main` не зарегистрированы; их rent_search-импорты, похоже, уже ретайрены (arch_lock показывает 0 rent_search-хитов) — проверить и убрать вместе с деревом rent_search.

## KEEP FOR NOW

- `telegram/` (59 py) + `services/` (32 py) — Batch C требует зафиксированного продуктового решения по telegram-контуру (юнит `lentra-telegram` enabled, но мёртв). Одно решение ретайрит оба.
- `rent/`, `domain/`, `application/`, `pipeline/`, `ranking/`, `property/` — объявленные legacy-деревья, помодульный review перед удалением (Manifest §6).
- Корневые деревья `/opt/lentra/{core,bot,api,worker,services,kernel,runtime}` + compose-стек — **ARCHIVE, никогда не hard-delete** (Batch D).
- Всё из DO-NOT-TOUCH (Cleanup Plan §5 / Manifest §6).

## DO-NOT-TOUCH (напоминание — удаление запрещено)

- `api/pipeline/search_pipeline.py` + `api/pipeline/__init__.py`
- `api/main.py`, `api/app_patch.py`, `api/routes/{search,miniapp}.py`
- `bot/main.py`, `bot/handlers/handlers.py`, `bot/cards/intelligence_renderer.py`
- `worker/recovery_worker.py`, `core/pipeline/worker_search_entrypoint.py`, `core/pipeline/canonical_search_pipeline.py`
- `runtime/bootstrap/gateway_v3.py`
- `core/engines/*` (market_intelligence_engine, area_engine, base_engine)
- `engines/risk_engine.py`, `engines/dedup_engine.py`, **`dedup/dedup_index.py`**
- `market/market_service.py`
- `ranking/unified_ranking_engine.py`, `ranking/ranking_engine.py`
- `decision/decision_layer.py`
- `engine_wrapper.py` + observability wrapper
- `runtime/arch_lock/` (только расширять)
- юниты `lentra-api`, `lentra-bot`, `lentra-recovery`; `venv-bot/`
- `alembic/`, `migrations/`, `sql/`; **`storage/market_snapshots/`** (production читает)
