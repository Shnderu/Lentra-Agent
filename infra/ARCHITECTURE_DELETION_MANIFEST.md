# Lentra Architecture Deletion Manifest

> Derived from `ARCHITECTURE_CLEANUP_PLAN.md` (audit of 2026-07-12).
> Subordinate to `ARCHITECTURE_CONSTITUTION.md` and `CANONICAL_COMPONENT_MAP.md`.
>
> This manifest is a **declaration of intent**, not an executed action.
> Nothing listed here has been deleted. Every batch below requires:
> 1. the preceding steps of the migration order (documents → enforcement) to be complete;
> 2. a fresh grep confirming zero production imports at deletion time;
> 3. restart + health check of `lentra-api`, `lentra-bot`, `lentra-recovery` after each batch.
>
> Paths are relative to `/opt/lentra`.

---

## 1. Deletion Principles

1. Delete only what is confirmed dead: zero importers, or importers that are
   themselves dead/broken (chain noted per item).
2. Never edit or delete anything on the production spine — see §6 (DO NOT
   TOUCH) and `ARCHITECTURE_CLEANUP_PLAN.md` §5.
3. Batches are ordered by risk: NONE → LOW → MEDIUM. A batch is executed only
   after the previous batch survived a service restart + `/health` check.
4. Root legacy trees are **archived** (moved to `_deprecated_runtime/` or an
   archive branch), not hard-deleted.
5. Anything not listed in this manifest is NOT approved for deletion.

---

## 2. Batch A — Tooling debris (risk: NONE)

Not code; artifacts of AI tooling and scratch work.

| Path | Reason |
|---|---|
| `infra/--system_prompt=You are working inside Lentra AI Market Intelligence OS.` (directory) | aider artifact — CLI flag written as a directory name |
| `elf.pipeline = pipeline` (root file) | shell/aider artifact |
| `elf.pipeline.run(objects)` (root file) | shell/aider artifact |
| `core/lifecycle ` (directory with trailing space) | duplicate of `core/lifecycle`, filesystem accident |
| `civilizatio/` (empty) | typo-duplicate of `civilization/` |
| `civilization/` | unrelated experiment (agent/evolution/market toys) — **confirm not wanted before removal** |
| `infra/init_v*_dirs.sh`, `infra/init_*_structure.sh`, `infra/create_*_dirs.sh`, `infra/setup_dirs.sh` (~30 scripts) | one-shot scaffolding scripts, already executed |
| `infra/test_write.txt`, `infra/test instruction`, `infra/test_session.session` | scratch/test debris |
| `infra/ngrok-stable-linux-amd64.zip`, `infra/qr.png` | binary debris |

## 3. Batch B — Dead code inside `infra/lentra` (risk: LOW)

All grep-verified: zero production imports. Grouped by component.

### 3.1 Pipelines
| Path | Evidence |
|---|---|
| `infra/lentra/services/search_pipeline.py` | 0 importers |
| `infra/lentra/bot/services/search_pipeline.py` | 0 importers |
| `infra/lentra/bot/features/rent_search/pipeline/search_pipeline.py` | 0 importers |
| `infra/canonical_search_pipeline.py` | top-level scratch copy, 0 importers |

### 3.2 Market / Intelligence engines
| Path | Evidence |
|---|---|
| `infra/lentra/core/market_intelligence/pricing/market_service.py` | 0 importers (canonical MarketService is in `market/`) |
| `infra/lentra/core/market_intelligence/market_intelligence_engine.py` | 0 importers |
| `infra/lentra/core/market_intelligence/engines/market_intelligence_engine.py` | 0 importers (canonical MIE is `core/engines/market_intelligence_engine.py`) |

### 3.3 Risk
| Path | Evidence |
|---|---|
| `infra/lentra/core/market_intelligence/risk/risk_engine.py` | 0 importers (canonical is `engines/risk_engine.py`) |
| `infra/lentra/core/market_intelligence/risk/risk_engine_v2.py` | only importer is dead `risk/risk_adapter.py`; named in routing maps as string only |
| `infra/lentra/core/market_intelligence/risk/risk_adapter.py` | 0 importers |
| `infra/lentra/core/market_intelligence/engines/risk.py` | only "importer" is root `core/runtime/worker_runtime.py` via a broken path |
| `infra/lentra/core/market_intelligence/risk/risk_engine_adapter.py` | importer chain dead |
| `infra/lentra/core/market_intelligence/risk/market_risk_engine.py` | importer (`decision/ai_decision_engine.py`) is dead |
| `infra/lentra/core/market_intelligence/risk/property_risk_engine.py` | 0 importers |
| `infra/lentra/core/market_intelligence/adapters/risk_engine_adapter.py` | 0 importers |
| `infra/lentra/core/market_intelligence/contracts/risk_engine_contract.py` | 0 importers |

### 3.4 Dedup
| Path | Evidence |
|---|---|
| `infra/lentra/core/market_intelligence/dedup/dedup_engine.py` | 0 importers (canonical is `engines/dedup_engine.py`; keep `dedup/dedup_index.py` — production dependency) |
| `infra/lentra/core/market_intelligence/dedup/unified_dedup_engine.py` | importer chain dead |
| `infra/lentra/core/market_intelligence/engines/dedup.py` | 0 importers |
| `infra/lentra/core/market_intelligence/adapters/dedup_engine_adapter.py` | 0 importers |
| `infra/lentra/core/market_intelligence/contracts/dedup_engine_contract.py` | 0 importers |
| `infra/lentra/core/ai/deduplication_engine.py` | 0 importers |
| `infra/app/core/quality/deduplicator.py` | 0 importers (also inside legacy `infra/app/`) |

### 3.5 Ranking
| Path | Evidence |
|---|---|
| `infra/lentra/core/market_intelligence/ranking/ranking_engine_v3.py` | 0 importers |
| `infra/lentra/core/market_intelligence/decision/ranking_engine.py` | 0 importers |
| `infra/lentra/bot/ux/ranking.py` | 0 importers |
| `infra/lentra/domain/scoring/ranking_engine.py` | 0 importers |
| `infra/lentra/rent/ranking/engine/ranking_engine.py` | importer (`rent/aggregation/engine/aggregation_service.py`) is itself dead |

### 3.6 Decision
| Path | Evidence |
|---|---|
| `infra/lentra/core/market_intelligence/decision_layer.py` | flat duplicate, 0 importers (canonical is `decision/decision_layer.py`) |
| `infra/lentra/core/market_intelligence/decision/ai_decision_engine.py` | dead importer of dead risk/ranking variants |

### 3.7 Gateways / bootstrap
| Path | Evidence |
|---|---|
| `infra/lentra/runtime/bootstrap/wiring.py` | 0 importers |
| `infra/lentra/runtime/bootstrap/graph_attach.py` | 0 importers |
| `infra/lentra/worker/engine.py` | 0 importers |
| `infra/lentra/core/market_intelligence/gateway.py` | flat duplicate, 0 importers |
| `infra/lentra/runtime/intelligence/intelligence_gateway.py` | 0 importers |

### 3.8 Broken modules (would raise ImportError if loaded)
Import nonexistent `lentra.core.pipeline.search_pipeline` — provably outside
the production graph:

| Path |
|---|
| `infra/lentra/api/search/search_api.py` |
| `infra/lentra/api/v1/debug_api.py` |
| `infra/lentra/api/v1/concierge_api_class.py` |

### 3.9 Legacy rent_search tree (whole subtree)

Added per `ARCH_LOCK_PHASE3_SOAK_REPORT.md` §3.4 note 2: ~45 of the 69
`LEGACY_INTELLIGENCE_ISOLATION` baseline hits are legacy-to-legacy edges
*internal* to this tree; they vanish wholesale with its deletion. Deleting
only single files from it (the previous §3.1 entry) would leave the rest of
the internal edges standing and break the expected single large drop in the
violation counter.

| Path | Evidence |
|---|---|
| `infra/lentra/bot/features/rent_search/` (entire tree) | Legacy feature contour outside the canonical flow (Constitution §3, §8); all internal edges are legacy-to-legacy; production bot path (`bot/main.py`, `bot/handlers/handlers.py`) does not depend on it. Subsumes the §3.1 entry `bot/features/rent_search/pipeline/search_pipeline.py`. |

External importers of this tree (`bot/handlers/rent_handler.py`,
`bot/handlers/router_builder.py`) are NOT part of this batch — their import
lines are code edits inside the production bot package and are recorded in
§8 (Grandfathered Baseline) until the next migration step.

Expected violation counter after Batch B (incl. §3.9): **84 → 28**
(45 tree-internal edges + 11 Batch-B importer edges removed; see
`ARCH_LOCK_PHASE3_SOAK_REPORT.md` §1). After Batch A the counter must
stay at **84** — Batch A is non-code debris and produces no import edges.

## 4. Batch C — Conditional deletions (risk: MEDIUM, decision required first)

Blocked on the fate of `lentra-telegram.service` (the parallel
`IntelligenceGateway` contour) — a product/ops decision, not a grep result.

| Path | Condition |
|---|---|
| `infra/lentra/core/market_intelligence/gateway/` (IntelligenceGateway package) | only after `lentra-telegram` is disabled/retired |
| `infra/lentra/core/market_intelligence/build.py` | same condition (feeds telegram dispatcher) |
| `infra/lentra/runtime/bootstrap/main.py`, `runtime/bootstrap.py` | same contour |
| `infra/lentra/runtime/bootstrap/wiring_safe.py` | reached only via `api/pipeline_bootstrap.py` → `api/pipeline_legacy.py`; delete together |
| `infra/lentra/api/pipeline_bootstrap.py`, `api/pipeline_legacy.py` | legacy pipeline path, delete as a set with wiring_safe |
| `infra/lentra/services/intelligence_gateway.py` | after its three side-module importers (`api/search_handler_patch.py`, `ingestion_router_v8.py`, `stream_processor.py`) are retired |
| `infra/lentra/telegram/` | only if telegram contour is retired |
| `infra/lentra/services/ranking_service.py` | only after feed ranking is folded under UnifiedRankingEngine or formally scoped as non-market |
| `infra/lentra/worker/loop.py`, `infra/lentra/worker/runtime.py` | dead worker variants tied to the old contour |

## 5. Batch D — Root legacy trees (ARCHIVE, do not hard-delete)

Move to `_deprecated_runtime/` or an archive branch; not part of the live
system (all enabled units run from `/opt/lentra/infra`).

| Path | Note |
|---|---|
| `/opt/lentra/core/` | old competing stack: flight_engine, predictive v9, fusion v7; `core/runtime/worker_runtime.py` has broken imports |
| `/opt/lentra/bot/` | root aiogram bot; its `lentra.service` unit is disabled |
| `/opt/lentra/api/`, `/opt/lentra/worker/`, `/opt/lentra/services/`, `/opt/lentra/kernel/`, `/opt/lentra/runtime/` | root legacy trees off the production graph |
| root `docker-compose.yml`, `main.py`, `worker_main.py`, `dispatcher.py`, root Dockerfiles | flyrum-era compose stack; no running containers |
| `_deprecated_runtime/`, `lentra_DISABLED/`, `infra/archive/`, `infra/app/`, `infra/infra/` | already-parked trees; consolidate into one archive location |

## 6. DO NOT TOUCH (deletion forbidden)

The production spine — full list in `ARCHITECTURE_CLEANUP_PLAN.md` §5. Summary:

- `infra/lentra/api/pipeline/search_pipeline.py`, `api/pipeline/__init__.py`
- `infra/lentra/api/main.py`, `api/app_patch.py`, `api/routes/search.py`, `api/routes/miniapp.py`
- `infra/lentra/bot/main.py`, `bot/handlers/handlers.py`, `bot/cards/intelligence_renderer.py`
- `infra/lentra/worker/recovery_worker.py`, `core/pipeline/worker_search_entrypoint.py`, `core/pipeline/canonical_search_pipeline.py`
- `infra/lentra/runtime/bootstrap/gateway_v3.py`
- `infra/lentra/core/engines/` (market_intelligence_engine, area_engine, base_engine)
- `infra/lentra/core/market_intelligence/engines/risk_engine.py`, `engines/dedup_engine.py`, **`dedup/dedup_index.py`**
- `infra/lentra/core/market_intelligence/market/market_service.py`
- `infra/lentra/core/market_intelligence/ranking/unified_ranking_engine.py`, `ranking/ranking_engine.py`
- `infra/lentra/core/market_intelligence/decision/decision_layer.py`
- `infra/lentra/core/market_intelligence/engine_wrapper.py` + observability wrapper
- `infra/lentra/runtime/arch_lock/`
- systemd units `lentra-api`, `lentra-bot`, `lentra-recovery`; `infra/venv-bot/`
- `infra/alembic/`, `infra/migrations/`, `infra/sql/` (data layer — out of scope)

## 7. Execution Preconditions

Per `ARCHITECTURE_CLEANUP_PLAN.md` §4, deletion is step 3 of 3:

1. **Documents complete and committed** — `ARCHITECTURE_CONSTITUTION.md`,
   `CANONICAL_COMPONENT_MAP.md`, cleanup plan, this manifest.
2. **Enforcement active** — arch_lock rules extended (single pipeline/router,
   no legacy imports), `lentra-worker.service` fixed or disabled,
   `lentra-telegram` decision recorded, routing maps corrected (RiskEngineV2 → v3).
3. Only then: execute batches A → B → C → D, one batch per commit, with
   service restart + health check between batches, and a rollback point
   (git tag) before each batch.

---

## 8. Grandfathered Baseline (temporarily permitted)

The following **11** dry-run violations from the frozen Phase 3 baseline
(`ARCH_LOCK_PHASE3_SOAK_REPORT.md` §1) belong to **no batch** (not A, not B,
not C). They are **temporarily permitted** until the next migration step
(post-Batch-C / Phase 4 enforcement scoping). This section declares no new
rules, changes no rules, and authorizes no deletions — it is a standing
allow-list of *known old* edges so that the counter expectation after
Batch B (28 = 17 Batch-C edges + these 11) is explicit and any edge NOT
listed here or in a batch is treated as a regression.

| # | Module (importer) | Forbidden edge (target) | Rule |
|---|---|---|---|
| 1 | `lentra/api/services/search_service.py` | `api.pipeline.search_pipeline` | `CANONICAL_SPINE_INTEGRITY.also[0]` |
| 2 | `lentra/core/bootstrap/__init__.py` | `core.bootstrap.bootstrap_intelligence_system` | `NO_LEGACY_BOOTSTRAP_CONTOUR` |
| 3 | `lentra/core/bootstrap/bootstrap_intelligence_system.py` | `market_intelligence.gateway.intelligence_gateway` | `LEGACY_INTELLIGENCE_ISOLATION` |
| 4 | `lentra/core/bootstrap/bootstrap_intelligence_system.py` | `market_intelligence.gateway.intelligence_gateway` | `NO_LEGACY_GATEWAY_CONTOUR` |
| 5 | `lentra/core/market_intelligence/graph/graph_adapter.py` | `market_intelligence.gateway.graph_adapter` | `LEGACY_INTELLIGENCE_ISOLATION` |
| 6 | `lentra/core/market_intelligence/graph/graph_adapter.py` | `market_intelligence.gateway.graph_adapter` | `NO_LEGACY_GATEWAY_CONTOUR` |
| 7 | `lentra/runtime/intelligence/intelligence_runtime.py` | `runtime.intelligence.intelligence_enforcer` | `LEGACY_INTELLIGENCE_ISOLATION` |
| 8 | `lentra/runtime/bootstrap/worker_main.py` | `runtime.bootstrap.wiring_safe` | `NO_LEGACY_GATEWAY_BUILDERS` |
| 9 | `lentra/bot/services/search_service.py` | `domain.property.search` | `LEGACY_INTELLIGENCE_ISOLATION` |
| 10 | `lentra/bot/handlers/rent_handler.py` | `bot.features.rent_search.handler` | `LEGACY_INTELLIGENCE_ISOLATION` |
| 11 | `lentra/bot/handlers/router_builder.py` | `bot.features.rent_search.service` | `LEGACY_INTELLIGENCE_ISOLATION` |

Notes:

- Rows 10–11 will start failing at import time once Batch B §3.9 removes
  the `rent_search` tree; retiring those two import lines is a code edit
  inside the production bot package and is therefore deferred to the next
  migration step, not smuggled into a deletion batch.
- Row 1 is the known legacy `search_service` hit
  (`ARCH_LOCK_PHASE3_SOAK_REPORT.md` §3.4 note 1) — not a spine false
  positive.
- This list may only **shrink** (per SOAK exit criteria: "baseline file of
  remaining grandfathered hits ... may only shrink"). Adding to it requires
  a superseding ADR.
