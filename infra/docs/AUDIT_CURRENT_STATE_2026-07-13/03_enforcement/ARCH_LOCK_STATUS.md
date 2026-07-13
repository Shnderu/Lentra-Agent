# §7. ARCH_LOCK STATUS

> Свежий dry-run на 2026-07-13, команда: `venv-bot/bin/python -m lentra.runtime.arch_lock.arch_lock_runner`

## Текущие нарушения: 5 total, 0 на spine (exit 0)

```
rules loaded: 11 (v1=6, v2=3, skipped=0)
modules scanned: 1255
violations: 5 total, 5 on legacy, 0 on spine
  CANONICAL_SPINE_INTEGRITY.also[1]: 5 hit(s)
    lentra.telegram.dispatcher        -> lentra.runtime.bootstrap.gateway_v3
    lentra.api.pipeline_bootstrap      -> lentra.runtime.bootstrap.gateway_v3
    lentra.runtime.bootstrap.main      -> lentra.runtime.bootstrap.gateway_v3
    lentra.runtime.bootstrap.worker_main -> lentra.runtime.bootstrap.gateway_v3
    lentra.runtime.bootstrap.graph_attach -> lentra.runtime.bootstrap.gateway_v3
SPINE CLEAN (no false positives on canonical spine)
```

Все 5 — нелегальные вызывающие `build_gateway_v3` (INV-2: единственный разрешённый — `api/pipeline/search_pipeline.py`).

## Baseline delta

| Метрика | 2026-07-12 (frozen SOAK) | 2026-07-13 (сейчас) |
|---|---|---|
| Total violations | 84 | **5** |
| On spine | 0 | 0 |
| Rules loaded | 11 | 11 |
| Modules scanned | 1286 | 1255 |
| Exit code | 0 | 0 |

Все soak-инварианты держатся: INV-A (exit 0) ✅, INV-B (spine clean) ✅, INV-C (11 rules, skipped 0) ✅, INV-D (монотонное убывание 84→5) ✅, INV-E (нет `<missing required>` на spine) ✅, INV-F (3 юнита active) ✅.

11-строчный Grandfathered Baseline фактически ретайрен — их запрещённые import-строки удалены (файловые остатки — см. LEGACY_INVENTORY).

## Уже решено

- Дефектное `NO_API_TO_CORE_BACKFLOW` удалено (объявляло spine нарушением).
- Direction invariant, spine integrity, legacy isolation, ranking authority, risk-veto wiring — все live и проходят.

## Ложные срабатывания

Нет. SPINE CLEAN на протяжении всего периода.

## Отсутствующие защиты (пробелы)

1. **Нет deny-правила для нового ingestion-контура.** Прямое инстанцирование движков вне gateway невидимо чекеру (он проверяет импорты, а `engines/risk_engine` канонически разрешён).
2. **Нет правила на содержимое routing-карт.** Пересозданные карты называют неканонические классы — и ничего не падает.
3. **`worker_main` в нарушении, но `lentra-worker` его РЕАЛЬНО запускает** в production. Gate non-blocking → живой юнит сидит на запрещённом ребре.
4. **Ещё не в CI/pre-commit** (soak exit-критерий не выполнен). SEAL.json — по-прежнему снимок старого графа. Blocking-режим не включён (`-` префикс на месте).
5. **Процессный дефект:** ADR, регулирующий реализованные Phase 2–3 изменения правил, всё ещё `PROPOSED`. Согласно его §5 — ни одно изменение правил не должно было приземлиться. Нужно ретроактивное одобрение или superseding ADR.

## Порядок фаз arch_lock (по ADR / Migration Plan)

- Phase 1 — documents ✅ (написаны)
- Phase 2 — rules migration ✅ (реализовано, но ADR ещё PROPOSED)
- Phase 3 — SEAL regeneration ❌ (не сделано)
- Phase 4 — blocking enforcement ❌ (`-` префикс на месте)
