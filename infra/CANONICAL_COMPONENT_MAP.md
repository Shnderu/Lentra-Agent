# Canonical Component Map

> Companion document to `ARCHITECTURE_CONSTITUTION.md`.
> Purpose: eliminate confusion between **canonical** and **legacy** architecture.
>
> Rule of precedence:
> 1. `ARCHITECTURE_CONSTITUTION.md` (product + architectural truth)
> 2. `CANONICAL_COMPONENT_MAP.md` (this file — concrete module map)
> 3. Code
>
> If code contradicts these documents, the code is legacy.

---

## 0. TL;DR

- **Single production entrypoint:** `lentra.api.pipeline.search_pipeline.SearchPipeline`
- **Single engine router:** `lentra.runtime.bootstrap.gateway_v3.build_gateway_v3`
- **Single ranking source of truth:** `UnifiedRankingEngine` → `MarketRankingEngine`
- **Single decision authority:** `DecisionLayer`
- Everything else that duplicates these responsibilities is **legacy** and must not be imported by production code.

---

## 1. Canonical Production Flow

The one and only allowed runtime flow:

