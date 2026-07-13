# §4. CANONICAL COMPONENT COMPLIANCE

> По каждому каноническому компоненту из `CANONICAL_COMPONENT_MAP.md` §4: Expected / Actual / Gap / Required action.

| Component | Expected (Map §4) | Actual | Gap | Required action |
|---|---|---|---|---|
| **SearchPipeline** | `api/pipeline/search_pipeline.py`, только оркестрация | ✅ присутствует, wired как задокументировано | нет | нет |
| **CanonicalSearchPipeline** | facade без логики | ✅ facade не деградировал, worker-путь использует его | нет | нет |
| **GatewayV3** | единственный маршрутизатор; 4 регистрации | ✅ регистрирует ровно area/MI/risk/dedup | 4–5 нелегальных **вызывающих** `build_gateway_v3` | удалить вызывающих (Phase B1) |
| **MarketService** | владеет market truth | ✅ присутствует; делегирует `MarketTruthEngine` внутри | `MarketTruthEngine` также импортируется напрямую `pipeline_pricing_adapter`, `area/market_segmentation_engine` — конкурентный доступ к market truth | сделать internal-only или ADR на границу |
| **MarketIntelligenceEngine** | единственный интерпретатор цены | ✅ зарегистрирован как `"market_intelligence"` | новый `engines/pricing_engine.py` дублирует ответственность (§9) | ADR: свернуть/ретайрить PricingEngine |
| **AreaEngine** | `core/engines/area_engine.py` | ✅ зарегистрирован как `"area"` | нет | нет |
| **RiskEngine (v3)** | `engines/risk_engine.py`, binding veto | ✅ в pipeline + gateway; DecisionLayer применяет «risk authority gate» | veto реализован через dict-defaults (`fraud_score`, 0.5) — binding по соглашению, не по контракту | контрактный тест (Phase D) |
| **DedupEngine + DedupIndex** | `engines/dedup_engine.py` | ✅ | нет | нет |
| **UnifiedRankingEngine (+MarketRankingEngine)** | единственный ranking-авторитет | ✅ единственный импортёр — pipeline; правило RANKING_AUTHORITY проходит | на production чисто; legacy ranking-классы остались на диске | удалить остатки (Phase A) |
| **DecisionLayer** | v2.1 по карте | ✅ присутствует, self-describes **v2.2** | дрейф документации | правка документа |
| **ObjectIntelligenceCardBuilder** | контракт презентации | ✅ `output/object_intelligence_card.py` | нет | нет |
| **Routing maps (§9.5)** | должны называть канонические классы | ❌ пересозданные `contracts/routing_map.py`/`routing_map_lock.py` называют `PricingEngine` как pricing-авторитет и `UnifiedDedupEngine` (SAFE-DELETE файл!) / `DedupIndex` как dedup-авторитет | **дефект — тот же класс дефекта, что документы предписали чинить (RiskEngineV2 → v3)** | починить содержимое: указать MIE + DedupEngine |

## Ключевые выводы

- **Spine-компоненты: 100% соответствие.** Все на местах, wired корректно.
- **3 дефекта соответствия, не ломающие runtime:**
  1. Routing-карты называют неканонические классы (§9.5 defect) — правка содержимого.
  2. `MarketTruthEngine` доступен извне MarketService — нарушает §4 (владение market truth).
  3. `PricingEngine` дублирует MarketIntelligenceEngine — §9 duplicate policy.
- **1 дрейф документации:** DecisionLayer v2.1 (карта) vs v2.2 (код).
- **1 слабое место контракта:** risk veto держится на соглашении (dict defaults), а не на явном контракте — нужен тест до включения blocking-режима.
