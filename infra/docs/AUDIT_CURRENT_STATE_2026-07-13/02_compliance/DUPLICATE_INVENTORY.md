# §5. DUPLICATE COMPONENT INVENTORY

> Оставшиеся дубликаты на 2026-07-13. Импортёры проверены grep'ом по живому дереву.

## 1. Pricing-интерпретация

- **Locations:** `core/engines/market_intelligence_engine.py` (канон) vs `core/market_intelligence/engines/pricing_engine.py` + `core/market_intelligence/pricing/engine.py` + `core/market/pricing_engine.py`
- **Канон:** MarketIntelligenceEngine (зарегистрирован в GatewayV3 как `"market_intelligence"`).
- **Retire:** семейство PricingEngine (или легитимизировать через ADR как ingestion-internal).
- **Evidence:** PricingEngine используется только ingestion-адаптерами и `engine_restore.py`; MIE — движок gateway.

## 2. Market truth

- **Locations:** `market/market_service.py` (канонический владелец) vs `pricing/market_truth_engine.py` (новый «Market Truth Authority»).
- **Канон:** MarketService. MarketTruthEngine допустим **только** как его внутренняя деталь.
- **Retire:** два внешних прямых импорта — `adapters/pipeline_pricing_adapter.py`, `area/market_segmentation_engine.py`.
- **Evidence:** grep даёт 3 импортёров MarketTruthEngine, канонический — только MarketService.

## 3. Ingestion enrichment flow (второй поток)

- **Locations:** `SearchPipeline→GatewayV3` (канон) vs `data_layer/pipeline/ingestion_pipeline.py` + `run_pipeline.py` (`PipelineRunner`, `SearchEngine`) + `run_market_seed.py`.
- **Канон:** маршрутизация через GatewayV3.
- **Retire/rewire:** ingestion обязан вызывать движки через gateway ИЛИ получить конституционный carve-out через ADR. Прямое `RiskEngineAdapter(RiskEngine())` в `ingestion_pipeline.py` — нарушение Constitution §4/§11.1.
- **Evidence:** коммиты 2026-07-13 (`843877c0..a42660dd`), нет ADR; пишет в snapshot store, который читает production.
- **ВАЖНО:** `adapters/risk_engine_adapter.py` числится SAFE DELETE в Deletion Manifest §3.3, но был **пересоздан и активно используется** ingestion-контуром. Запись манифеста устарела — слепое исполнение манифеста сломает ingestion.

## 4. Dedup-остатки

- **Locations:** канон `engines/dedup_engine.py` vs на диске: `dedup/dedup_engine.py`, `dedup/unified_dedup_engine.py`, `engines/dedup.py`, `adapters/dedup_engine_adapter.py`, `contracts/dedup_engine_contract.py`, `core/ai/deduplication_engine.py`, `infra/app/core/quality/deduplicator.py`.
- **Retire:** все остатки. **Evidence:** 0 production-импортёров (grep). `dedup/dedup_index.py` НЕ трогать — канонический internal.

## 5. Ranking-остатки

- **Locations:** канон `ranking/unified_ranking_engine.py` vs `ranking_engine_v3.py`, `decision/ranking_engine.py`, `bot/ux/ranking.py`, `domain/scoring/ranking_engine.py`, `rent/ranking/engine/ranking_engine.py`, `services/ranking_service.py` (+ `ranking_ml.py`, `ranking_ensemble.py`, `ranking_adaptive.py`), `application/rent_search/ranking.py`, `ranking/property_ranker.py`, `core/ranker.py`, `core/ranking/ranker.py`.
- **Retire:** все; `services/ranking_service.py` — вместе с telegram/rent_search контурами (его импортёры: `telegram/bot_feed.py`, `telegram/feed_test.py`, `services/feed_service.py`, `application/rent_search/ranking.py`, `bot/features/rent_search/ranking/ranking_service.py`).
- **Evidence:** ни один не достижим из production; правило RANKING_AUTHORITY проходит.

## 6. Gateways

- **Locations:** канон GatewayV3 vs flat `market_intelligence/gateway.py` (`IntelligenceGateway`), `api/gateway.py` (`Gateway`), `api/services/gateway.py` (`GatewayService`), `runtime/bootstrap/engine_restore.py` (параллельная фабрика движков).
- **Retire:** все. **Evidence:** 0 production-импортёров у каждого.

## 7. Worker runtimes

- **Locations:** канон `worker/recovery_worker.py` vs `runtime/bootstrap/worker_main.py` (работающий no-op heartbeat, юнит lentra-worker).
- **Retire:** worker_main + disable юнит. **Evidence:** тело функции — `build_gateway_v3()` + `sleep(5)` в цикле; полезной работы нет; ребро запрещено (arch_lock hit).

## 8. Нормализаторы (малый приоритет)

- **Locations:** `market_intelligence/normalization/listing_normalizer.py` (production, через SearchAdapter) vs `data_layer/normalization/engine.py` (ingestion).
- Решается вместе с ADR по ingestion-контуру (Phase C1) — вероятно оба легитимны на разных слоях, но границу надо зафиксировать.
