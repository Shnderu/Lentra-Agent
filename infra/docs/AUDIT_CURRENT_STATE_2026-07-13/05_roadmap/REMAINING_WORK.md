# §9. REMAINING WORK — роадмап только из текущей реальности

> НЕ из старых планов. Каждый шаг: файлы / риск / валидация.
> Дисциплина: один батч = один коммит + git tag + рестарт `lentra-api`/`lentra-bot`/`lentra-recovery` + `/health` + arch_lock счётчик не растёт.

## Phase A — Safe cleanup (риск: LOW)

| # | Шаг | Файлы | Риск | Валидация |
|---|---|---|---|---|
| A0 | **Разрешить грязное рабочее дерево ПЕРВЫМ.** Решение: revert ИЛИ ADR+commit для `listing_contract_guard.py` (spine!) + `pipeline_pricing_adapter.py` + `market_snapshots.json`. Рекомендация: revert guard (убирает backfill `price_vnd` без ADR = поведенческий риск) | 3 грязных файла | **MEDIUM, если оставить молча** | `git status` чист; рестарт api+recovery; `/health`; smoke-тест одного поиска |
| A1 | Disable `lentra-telegram.service` (мёртв на старте: `build_graph` не определён). Это фиксирует «решение по telegram» и разблокирует Batch C | 1 юнит | NONE | `systemctl is-enabled lentra-telegram` → disabled |
| A2 | Disable `lentra-worker.service` (no-op heartbeat на запрещённом ребре) | 1 юнит | NONE (работы не делает) | очередь дренится через lentra-recovery; журналы чисты |
| A3 | Удалить SAFE-TO-REMOVE список (см. LEGACY_INVENTORY), 2–3 батчами: dedup-остатки → ranking-остатки + битые api/v1 → шлюзы-сироты | ~20 файлов | LOW | свежий grep на каждый файл в момент удаления; рестарты + `/health` между батчами; arch_lock не растёт |
| A4 | Мусор Batch A: `elf.pipeline*`, `init_v*_dirs.sh` (~30), `civilizatio/`, test-мусор; `civilization/` — подтвердить содержимое | ~35 не-код файлов | NONE | сервисы не затронуты |

## Phase B — Small rewiring (риск: LOW-MEDIUM)

| # | Шаг | Файлы | Риск | Валидация |
|---|---|---|---|---|
| B1 | Удалить 5 запрещённых вызывающих `build_gateway_v3` (после A1/A2): `telegram/dispatcher.py`, `api/pipeline_bootstrap.py`, `runtime/bootstrap/main.py`, `runtime/bootstrap/worker_main.py`, `runtime/bootstrap/graph_attach.py`, + `runtime/bootstrap.py` | 6 файлов | LOW | arch_lock → **0 violations** |
| B2 | Починить содержимое routing-карт: `contracts/routing_map.py`, `routing_map_lock.py` должны называть канонические классы (MarketIntelligenceEngine, DedupEngine) | 2 файла | NONE (string-only) | arch_lock + ревью |
| B3 | Убрать orphan-цепочку `api/services/{gateway,search_service}.py` + `core/product_router.py`; проверить-и-убрать `bot/handlers/{rent_handler,router_builder}.py` + дерево `bot/features/rent_search/` | ~15 файлов | LOW-MED (внутри пакета бота) | рестарт бота + ручной Telegram smoke-тест |
| B4 | Регуляризовать ADR: одобрить `ADR_ARCH_LOCK_RULE_MIGRATION_V1` ретроактивно (или superseding ADR) + написать Audit Delta, обновляющий устаревшие инвентари (в т.ч. `adapters/risk_engine_adapter.py`: SAFE DELETE → KEEP/Batch-C) | только документы | NONE | ревью |

## Phase C — Core architecture restoration (риск: MEDIUM, каждый шаг = свой ADR)

| # | Шаг | Файлы | Риск | Валидация |
|---|---|---|---|---|
| C1 | **ADR по ingestion-контуру**: маршрутизировать вызовы движков `IngestionPipeline` через GatewayV3; `MarketTruthEngine` — internal-only для MarketService; свернуть/ретайрить `PricingEngine` в MIE | `data_layer/pipeline/*`, 4 адаптера, `engines/pricing_engine.py`, `area/market_segmentation_engine.py` | MED | seed-прогон воспроизводит текущие снапшоты; регрессия pipeline на `/search` |
| C2 | Подключить Data Layer к production-входу (заменить/дополнить статический seed `SearchAdapter`) — фактический продуктовый разрыв | граница `core/adapters/search_adapter.py` (ADR: примыкает к spine) | MED | end-to-end поиск на ingested-данных |
| C3 | Ретайрить деревья `telegram/` + `services/` (решение зафиксировано в A1); помодульный review `rent/`, `domain/`, `application/`, `pipeline/`, `ranking/`, `property/` | 90+ файлов | MED | ступенчатые батчи, рестарты, arch_lock |
| C4 | Архивировать корневые деревья `/opt/lentra/{core,bot,api,worker,services,kernel,runtime}` + compose-стек в одно архивное место (НЕ hard-delete) | корневые директории | LOW | ни один юнит на них не ссылается (проверено) |

## Phase D — Final validation & lock (риск: LOW)

| # | Шаг | Файлы | Риск | Валидация |
|---|---|---|---|---|
| D1 | Добавить недостающие arch_lock-правила: запрет прямого инстанцирования движков вне gateway/pipeline; проверка содержимого routing-карт; scope ingestion-контура; tombstone'ы на удалённое | `rules_v1.json`, `rule_loader.py` | LOW (сначала dry-run) | 0 violations, spine clean |
| D2 | Пере-запечатать SEAL.json против канонического графа (старый seal — versioned backup через `backup_manager.py`) | SEAL.json | LOW | boot_seal_check зелёный |
| D3 | CI/pre-commit хук (`.githooks/` уже есть) — блокирует только НОВЫЕ рёбра | hooks | LOW | тестовый PR с новым ребром блокируется |
| D4 | Убрать `-` из `ExecStartPre` (blocking mode) после soak; добавить контрактный тест risk veto | 2 юнита, 1 тест | LOW (rollback = вернуть `-` + daemon-reload) | сервисы чисто рестартуют с активным gate |

## Порядок строгий

A0 блокирует всё. A1/A2 разблокируют B1. B1 даёт arch_lock=0, что является предусловием D2/D4. C1 (ADR) — предусловие C2. D4 — последний шаг.
