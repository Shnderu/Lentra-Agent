# §2. CURRENT RUNTIME EXECUTION GRAPH

> Реальный путь выполнения production на 2026-07-13. Все узлы проверены по фактическим импортам и работающим systemd-юнитам.

## Основной production-поток (канонический)

```
[API]      lentra/api/main.py :: create_app()                        active, CANONICAL
   ↓       routes/search.py + routes/miniapp.py (prefix /api/miniapp)
   ↓       api/pipeline/__init__.py :: get_pipeline()  (process singleton)
[PIPELINE] api/pipeline/search_pipeline.py :: SearchPipeline.run     CANONICAL
   ↓       core/adapters/search_adapter.py :: SearchAdapter
           (источник данных: статический JSON seed lentra/data/seeds/da_nang_seed_v1.json)
   ↓       contracts/listing_contract_guard.py :: ListingContractGuard   ⚠ DIRTY UNCOMMITTED
   ↓       market/market_service.py :: MarketService
           (внутри: MarketTruthEngine, PriceHistoryRepository, PriceTrendAnalyzer,
            MarketExplanationEngine, SegmentIntelligence, MarketMovementAnalyzer)
[GATEWAY]  runtime/bootstrap/gateway_v3.py :: GatewayV3               CANONICAL
   ↓       run_engine("area")                → core/engines/area_engine.py :: AreaEngine
   ↓       run_engine("market_intelligence") → core/engines/market_intelligence_engine.py :: MarketIntelligenceEngine
   ↓       (прямые экземпляры — документированная особенность)
           engines/risk_engine.py :: RiskEngine        (search_pipeline.py:302)
           engines/dedup_engine.py :: DedupEngine
[RANKING]  ranking/unified_ranking_engine.py :: UnifiedRankingEngine  CANONICAL
           (делегирует ranking/ranking_engine.py :: MarketRankingEngine — internal)
[DECISION] decision/decision_layer.py :: DecisionLayer (v2.2)         CANONICAL
[OUTPUT]   verdict/market_verdict_engine.py :: MarketVerdictEngine
   ↓       output/object_intelligence_card.py :: ObjectIntelligenceCardBuilder
   ↓
[RESPONSE] API JSON → Bot (httpx-клиент /search) / MiniApp-схемы
```

## Параллельные пути, реально работающие

### lentra-recovery — active, CANONICAL
```
worker/recovery_worker.py
  → Postgres task queue (storage/db.py :: get_conn)
  → core/pipeline/worker_search_entrypoint.py
  → core/pipeline/canonical_search_pipeline.py :: CanonicalSearchPipeline (zero-logic facade)
  → тот же SearchPipeline
```

### lentra-worker — active, НЕ КАНОНИЧЕСКИЙ ⚠
```
runtime/bootstrap/worker_main.py :: main()
  → build_gateway_v3()   ← запрещённое ребро (INV-2: единственный разрешённый вызывающий — search_pipeline)
  → while True: sleep(5)  (heartbeat, никакой работы)
```
- Недокументированный 4-й юнит. Production-reachable, работы не делает.
- Cleanup Plan описывал его указывающим на несуществующий `lentra.worker.main`; с тех пор перенацелен на worker_main.py.
- Рекомендация: disable юнит, затем удалить файл (Phase A2 / B1).

### lentra-telegram — enabled, но DEAD (падает на старте)
```
ExecStart: /usr/bin/python3 lentra/telegram/runtime.py
  → TelegramRuntime.__init__ вызывает build_graph()  ← имя не определено/не импортировано → крах
```
- Legacy-контур (IntelligenceGateway-пакет, который он обслуживал, уже удалён).
- Фактически контур мёртв; юнит нужно disable — это и есть «решение по telegram», блокирующее Batch C.

### Offline seed-контур — НЕ достижим из systemd, но влияет на production ⚠
```
core/data_layer/pipeline/run_market_seed.py (ручной запуск)
  → IngestionPipeline (data_layer/pipeline/ingestion_pipeline.py)
      → NormalizationEngine → PipelineDedupAdapter → PipelinePricingAdapter
        → PipelineAreaAdapter → RiskEngineAdapter(RiskEngine())   ← прямое инстанцирование, мимо GatewayV3
  → пишет storage/market_snapshots/market_snapshots.json
      → который читает production MarketTruthEngine (через MarketSnapshotRepository)
```
- Недокументированный «чёрный ход» в market truth. Требует ADR (Phase C1).

## Сводка узлов

| Узел | Файл | Класс/функция | Prod-reachable | Канон? |
|---|---|---|---|---|
| API | `api/main.py` | `create_app` | ✅ active | CANONICAL |
| Singleton | `api/pipeline/__init__.py` | `get_pipeline` | ✅ | CANONICAL |
| Pipeline | `api/pipeline/search_pipeline.py` | `SearchPipeline` | ✅ | CANONICAL |
| Guard | `contracts/listing_contract_guard.py` | `ListingContractGuard` | ✅ | CANONICAL, но DIRTY |
| Market | `market/market_service.py` | `MarketService` | ✅ | CANONICAL |
| Gateway | `runtime/bootstrap/gateway_v3.py` | `GatewayV3` | ✅ | CANONICAL |
| Area | `core/engines/area_engine.py` | `AreaEngine` | ✅ | CANONICAL |
| MI | `core/engines/market_intelligence_engine.py` | `MarketIntelligenceEngine` | ✅ | CANONICAL |
| Risk | `engines/risk_engine.py` | `RiskEngine` (v3) | ✅ | CANONICAL |
| Dedup | `engines/dedup_engine.py` | `DedupEngine` | ✅ | CANONICAL |
| Ranking | `ranking/unified_ranking_engine.py` | `UnifiedRankingEngine` | ✅ | CANONICAL |
| Decision | `decision/decision_layer.py` | `DecisionLayer` v2.2 | ✅ | CANONICAL |
| Card | `output/object_intelligence_card.py` | `ObjectIntelligenceCardBuilder` | ✅ | CANONICAL |
| Bot | `bot/main.py` | aiogram, httpx → API | ✅ active | CANONICAL |
| Recovery | `worker/recovery_worker.py` | task retry loop | ✅ active | CANONICAL |
| worker_main | `runtime/bootstrap/worker_main.py` | no-op heartbeat | ✅ active | **LEGACY/VIOLATION** |
| telegram runtime | `telegram/runtime.py` | `TelegramRuntime` (broken) | enabled, dead | **LEGACY** |
| Ingestion | `data_layer/pipeline/ingestion_pipeline.py` | `IngestionPipeline` | offline only | **NON-COMPLIANT NEW** |
