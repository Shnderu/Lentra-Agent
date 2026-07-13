# §8. CORE PRODUCT CONTOUR VALIDATION

> Продукт: SEA Rent Intelligence / AI Property OS (Master Plan §5, Consolidation Map §1).

## Ожидаемый контур

```
Data Layer → Normalization → Deduplication → Market Intelligence → AI Decision → API/Telegram/MiniApp
```

## Валидация по слоям

| Слой | Существует | Работает | Отсутствует |
|---|---|---|---|
| **Data Layer** | ✅ новый `core/data_layer/` (sources, adapters для Facebook/Telegram/local sites, seeds) | ⚠️ только как offline seed-runner; production `SearchAdapter` читает **статический JSON seed** (`lentra/data/seeds/da_nang_seed_v1.json`) | реальные коннекторы источников, подключённые к production; планировщик ingestion; контур не gateway-compliant |
| **Normalization** | ✅ `data_layer/normalization/engine.py` + `market_intelligence/normalization/listing_normalizer.py` | ✅ listing_normalizer на production-графе (через SearchAdapter) | унификация двух нормализаторов (разнесены по контурам) |
| **Dedup Engine** | ✅ канонический DedupEngine + DedupIndex | ✅ в pipeline, до ranking | — |
| **Market Intelligence** | ✅ MarketService + MarketTruthEngine + MIE + AreaEngine, snapshot/history репозитории | ✅ live; снапшоты в JSON-store | Postgres-backed market history (сейчас JSON-файл); segmentation engine не gateway-routed |
| **AI Decision** | ✅ RiskEngine (veto) + UnifiedRankingEngine + DecisionLayer v2.2 + verdict/explanation движки | ✅ live | veto держится на dict-defaults, нет контрактного теста |
| **API / Telegram / MiniApp** | ✅ FastAPI (`/search`, `/api/miniapp/*`, `/health`) + aiogram-бот (HTTP-клиент) + miniapp-схемы + `frontend/` + `miniapp/` | ✅ API+бот active | MiniApp-доставка сверх схем — Phase-4 роадмапа (Master Plan §9); старый telegram-контур мёртв (корректно) |

## Что существует

Все шесть слоёв присутствуют end-to-end и запускаются. Каноническая интеллект-часть (dedup → market → risk → ranking → decision → card) работает в production через один pipeline.

## Что работает

- Полный production-путь `/search` → карточка интеллекта.
- Bot как тонкий HTTP-клиент.
- Recovery-worker через Postgres-очередь.
- Snapshot-персистенция market truth.

## Что отсутствует / слабо

- **Верх воронки — статический seed-файл.** Новый Data Layer имеет правильную целевую форму (совпадает с Master Plan §5), но не подключён к production и конституционно не соответствует (обходит GatewayV3).
- Market history на JSON-файле вместо Postgres.
- Risk veto — по соглашению, без контрактного теста.
- MiniApp-доставка сверх схем не реализована (ожидаемо — Phase 4 роадмапа).

## Вердикт

Продуктовый контур существует end-to-end и работает, но архитектурная полнота (~80–85%) выше продуктовой: интеллект готов, а вход данных — заглушка-seed. Ближайшая продуктовая ценность — легитимизировать (ADR) и подключить Data Layer к production-входу.
