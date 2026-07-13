# §10. FINAL ANSWERS

## 1. Где мы сейчас?

Канонический spine полностью восстановлен, работает и статически верифицирован: три канонических entrypoint'а сходятся на одном `SearchPipeline` → GatewayV3 → четыре канонических движка → UnifiedRankingEngine → DecisionLayer. arch_lock: **SPINE CLEAN**, нарушения упали с 84 → 5. Удаление legacy выполнено на ~70–75% (с опережением манифеста, хотя и вне документированного порядка). Текущее состояние определяют три хвоста:

1. **Грязная незакоммиченная правка защищённого spine-файла** (`listing_contract_guard.py` — убирает backfill `price_vnd`).
2. **Новый недокументированный ingestion-контур**, обходящий GatewayV3 и пишущий в snapshot store, который читает production.
3. **Два systemd-юнита**: `lentra-worker` (no-op на запрещённом ребре) и `lentra-telegram` (enabled, но мёртв).

## 2. Какой процент целевой архитектуры восстановлен?

**~80–85%.**
- Spine: ~100%.
- Enforcement: ~70% (правила live в dry-run; нет SEAL re-seal, CI, blocking-режима; ADR формально не одобрен).
- Удаление legacy: ~70–75%.
- Продуктовый контур: все 6 слоёв существуют, но вход данных — статический seed-файл, поэтому продуктовая полнота ниже архитектурной.

## 3. Крупнейшие оставшиеся блокеры?

1. Незакоммиченная spine-правка `ListingContractGuard` (поведенческий риск, без ADR, загрузится при следующем рестарте).
2. Конституционный статус ingestion-контура (дублирует enrichment, инстанцирует движки напрямую, чёрный ход в market truth) — нужен ADR.
3. Решения по юнитам telegram/worker — блокируют последние батчи удаления.
4. Неодобренный ADR — блокирует легитимный переход к Phase 4 enforcement.

## 4. Что НЕ трогать?

Весь DO-NOT-TOUCH список (Cleanup Plan §5 / Manifest §6): pipeline + singleton, `gateway_v3.py`, все канонические движки, `dedup_index.py`, MarketService, ranking-пара, DecisionLayer, engine/observability wrappers, entrypoint'ы и facades, `arch_lock/` (только расширять), три production-юнита, `venv-bot/`, data-слой (`alembic/`, `migrations/`, `sql/`) и **теперь также `storage/market_snapshots/`** — production его читает. Корневые legacy-деревья — только архив, никогда hard-delete.

## 5. Минимальный путь к production-ready канонической архитектуре?

Семь ходов:

1. Разрешить грязный spine-файл (revert или ADR).
2. Disable `lentra-telegram` + `lentra-worker` (две команды — ретайрит последние живые legacy-рёбра).
3. Удалить 5 запрещённых вызывающих gateway → arch_lock = 0.
4. Один ADR по ingestion-контуру (gateway-маршрутизация; MarketTruthEngine internal-only; починить routing-карты).
5. Удалить верифицированные orphan-остатки малыми батчами.
6. Re-seal SEAL.json + CI-хук.
7. Перевести gate в blocking-режим.

Всё остальное (архивация корневых деревьев, review rent/domain, MiniApp) — неблокирующие последующие шаги.

---

**Цель — не переписать Lentra, а восстановить и стабилизировать существующую каноническую архитектуру минимальными изменениями. Реализация — только после явного одобрения.**
