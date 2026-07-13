# §3. CURRENT PRODUCTION DEPENDENCY GRAPH

> Статическая AST-трассировка импортов от реальных entrypoint'ов (пакет `lentra`, корень `/opt/lentra/infra`).

## Активные production-модули (56 всего)

| Entrypoint | Модулей в замыкании | Примечание |
|---|---|---|
| `lentra.api.main` | 7 | app_patch, routes/{search,miniapp}, schemas, api/pipeline (singleton лениво тянет pipeline) |
| `lentra.bot.main` | 5 | ноль intelligence-импортов — чистый HTTP-клиент ✅ |
| `lentra.worker.recovery_worker` | 43 | суперсет: содержит весь spine (pipeline, gateway, все движки, market, ranking, decision, output, storage/db) |
| `lentra.runtime.bootstrap.worker_main` | 14 | gateway + движки; юнит-нарушитель, работы не делает |

Все импорты в production-замыкании разрешаются; битых импортов на production-графе нет.

## Orphan-модули (0 импортёров — кандидаты на удаление)

- `runtime/bootstrap/engine_restore.py` (параллельная фабрика движков)
- `api/gateway.py` (класс `Gateway`, не используется)
- `core/market_intelligence/gateway.py` (flat `IntelligenceGateway`; только строковые ссылки в `arch_lock/v2_rules.py`)
- `services/intelligence_gateway.py` (его 3 импортёра-сайдмодуля удалены 2026-07-13)
- Dedup-остатки: `dedup/dedup_engine.py`, `dedup/unified_dedup_engine.py`, `engines/dedup.py`, `adapters/dedup_engine_adapter.py`, `contracts/dedup_engine_contract.py`, `core/ai/deduplication_engine.py`, `infra/app/core/quality/deduplicator.py`
- Ranking-остатки: `ranking/ranking_engine_v3.py`, `decision/ranking_engine.py`, `bot/ux/ranking.py`, `domain/scoring/ranking_engine.py`, `rent/ranking/engine/ranking_engine.py`
- `risk/market_risk_engine.py`
- Битые (импортируют несуществующий `lentra.core.pipeline.search_pipeline`): `api/search/search_api.py`, `api/v1/debug_api.py`, `api/v1/concierge_api_class.py`

## Недостижимые контуры (внутренне связны, но без production-ребра)

| Контур | Размер | Вход |
|---|---|---|
| `telegram/` | 59 py | только мёртвый юнит lentra-telegram |
| `services/` | 32 py | импортёры — telegram + rent_search контуры |
| `rent/` | 50 py | нет |
| `domain/` | 53 py | нет |
| `application/` | 31 py | нет |
| `bot/features/rent_search/` | 11 py | не зарегистрирован в bot/main |
| `pipeline/`, `ranking/`, `property/` | по 1 py | нет |
| graph_v2-деревья, `ai_control/` | — | нет |
| Цепочка `api/services/gateway.py → core/product_router.py → api/services/search_service.py` | 3 файла | тупик: `GatewayService` никто не импортирует |

## Корневые деревья (вне `/opt/lentra/infra`) — вне графа

`/opt/lentra/core` (366 py), `/opt/lentra/worker` (67), `/opt/lentra/bot` (21), `/opt/lentra/api` (11), `/opt/lentra/kernel` (4), `/opt/lentra/services` (2), `/opt/lentra/runtime` (0). Достижимы только через отключённые юниты/compose. Политика: ARCHIVE (Batch D), не hard-delete.

## Дублирующие пути

1. Pipeline вызывает risk/dedup и через gateway-регистрацию, и через прямые экземпляры — документированная особенность (те же классы, безвредно; унификация = отдельный ADR, отложено).
2. Новый ingestion-контур дублирует enrichment-путь мимо GatewayV3 — см. `02_compliance/DUPLICATE_INVENTORY.md` п.3.
3. Два нормализатора: `data_layer/normalization/engine.py` (ingestion-контур) и `market_intelligence/normalization/listing_normalizer.py` (production, через SearchAdapter).
