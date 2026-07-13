# LENTRA — CURRENT STATE AUDIT (2026-07-13)

> Read-only аудит. HEAD `a42660dd`. Проверено против живых systemd-юнитов и свежего arch_lock dry-run.
> Источник истины: `infra/ARCHITECTURE_CONSTITUTION.md` → `infra/CANONICAL_COMPONENT_MAP.md` → arch_lock документы → cleanup-документы.
> ВАЖНО: инвентари cleanup-документов устарели на 1 день (аудит 2026-07-12, затем 59 коммитов 2026-07-13). Правила действительны, инвентари — нет.

## Headline

- Канонический spine **полностью восстановлен и работает**: 3 канонических entrypoint сходятся на одном `SearchPipeline` → GatewayV3 → 4 канонических движка → UnifiedRankingEngine → DecisionLayer.
- arch_lock: **84 нарушения (baseline 2026-07-12) → 5 сейчас, 0 на spine**.
- Восстановлено ~80–85% целевой архитектуры.
- Три открытых риска: (1) **незакоммиченная правка spine-файла** `listing_contract_guard.py`; (2) **новый недокументированный ingestion-контур** в обход GatewayV3; (3) юниты `lentra-worker` (no-op на запрещённом ребре) и `lentra-telegram` (enabled, но мёртв).

## Структура отчёта

| Папка / файл | Содержание |
|---|---|
| `01_current_state/ARCHITECTURE_STATUS.md` | §1 Статус компонентов (COMPLETE/PARTIAL/MISSING/LEGACY) |
| `01_current_state/RUNTIME_EXECUTION_GRAPH.md` | §2 Реальный граф выполнения production |
| `01_current_state/DEPENDENCY_GRAPH.md` | §3 Граф зависимостей: активные / orphan / недостижимые модули |
| `02_compliance/CANONICAL_COMPLIANCE.md` | §4 Соответствие каноническим компонентам (Expected/Actual/Gap) |
| `02_compliance/DUPLICATE_INVENTORY.md` | §5 Оставшиеся дубликаты |
| `02_compliance/LEGACY_INVENTORY.md` | §6 Legacy: SAFE TO REMOVE / NEEDS REWIRING / KEEP FOR NOW |
| `03_enforcement/ARCH_LOCK_STATUS.md` | §7 Состояние arch_lock: нарушения, пробелы, процессные дефекты |
| `04_product/PRODUCT_CONTOUR.md` | §8 Валидация продуктового контура (SEA Rent Intelligence) |
| `05_roadmap/REMAINING_WORK.md` | §9 Роадмап только из текущей реальности (Phase A–D) |
| `05_roadmap/FINAL_ANSWERS.md` | §10 Итоговые ответы: где мы, %, блокеры, минимальный путь |

## Правила для агента-исполнителя

1. Ничего не менять на spine (DO-NOT-TOUCH: `ARCHITECTURE_CLEANUP_PLAN.md` §5, `ARCHITECTURE_DELETION_MANIFEST.md` §6) без ADR.
2. Перед любым удалением — свежий grep импортёров на момент удаления.
3. Каждый батч = отдельный коммит + git tag + рестарт `lentra-api`/`lentra-bot`/`lentra-recovery` + `/health`.
4. Счётчик arch_lock может только уменьшаться (INV-D из SOAK-отчёта).
5. Начинать с Phase A0 (грязное рабочее дерево) — это блокер всего остального.
