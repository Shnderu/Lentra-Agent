# Lentra Architecture Cleanup Plan

> Generated from a read-only architecture audit (2026-07-12).
> Source of truth hierarchy: `ARCHITECTURE_CONSTITUTION.md` → `CANONICAL_COMPONENT_MAP.md` → this plan → code.
> All paths are relative to `/opt/lentra` unless stated otherwise.
> Production = the three enabled+running systemd units: `lentra-api`, `lentra-bot`, `lentra-recovery`
> (all run from `/opt/lentra/infra`, package root `infra/lentra/`).

---

## 1. CURRENT CANONICAL COMPONENTS

Verified by tracing actual imports from the running entrypoints
(`lentra.api.main`, `lentra.bot.main`, `lentra.worker.recovery_worker`).
All three entrypoints converge on a single pipeline.

| Component | File | Class | Responsibility |
|---|---|---|---|
| SearchPipeline | `infra/lentra/api/pipeline/search_pipeline.py` | `SearchPipeline` (line 32) | Single production entrypoint of the intelligence flow. Orchestrates: SearchAdapter → ListingContractGuard → MarketService → GatewayV3 → engines → UnifiedRankingEngine → DecisionLayer → ObjectIntelligenceCardBuilder. Singleton via `api/pipeline/__init__.py`. |
| CanonicalSearchPipeline (facade) | `infra/lentra/core/pipeline/canonical_search_pipeline.py` | `CanonicalSearchPipeline` | Zero-logic facade over SearchPipeline; used by worker path (`core/pipeline/worker_search_entrypoint.py` → `recovery_worker`). |
| MarketService | `infra/lentra/core/market_intelligence/market/market_service.py` | `MarketService` | Owns market truth: price baselines, market context. Only importer: `api/pipeline/search_pipeline.py:28`. |
| GatewayV3 | `infra/lentra/runtime/bootstrap/gateway_v3.py` | `GatewayV3` / `build_gateway_v3()` (line 62) | Single engine router. Registers `area`, `market_intelligence`, `risk`, `dedup` (each in `EngineWrapper` + `ObservabilityEngineV1`). Only caller: `api/pipeline/search_pipeline.py:36`. |
| MarketIntelligenceEngine | `infra/lentra/core/engines/market_intelligence_engine.py` | `MarketIntelligenceEngine(BaseEngine)` | Price-vs-market interpretation ("pricing_v3_product"). Registered in gateway_v3 (line 71) as `"market_intelligence"`. |
| AreaEngine | `infra/lentra/core/engines/area_engine.py` | `AreaEngine` | Area/district intelligence; registered in gateway_v3 (line 66). |
| RiskEngine | `infra/lentra/core/market_intelligence/engines/risk_engine.py` | `RiskEngine` (v3) | Risk scoring + veto authority. Used directly by pipeline (line 7/40) AND registered in gateway_v3 (line 76). |
| DedupEngine | `infra/lentra/core/market_intelligence/engines/dedup_engine.py` | `DedupEngine` | Duplicate collapsing (uses `dedup/dedup_index.py` internally). Used directly by pipeline (line 8/42) AND registered in gateway_v3 (line 81). |
| UnifiedRankingEngine | `infra/lentra/core/market_intelligence/ranking/unified_ranking_engine.py` | `UnifiedRankingEngine` | Single ranking authority; delegates to `ranking/ranking_engine.py` (`MarketRankingEngine`). Called at pipeline line 459. |
| DecisionLayer | `infra/lentra/core/market_intelligence/decision/decision_layer.py` | `DecisionLayer` ("v2.1") | Final decision authority; must respect risk veto. Called at pipeline line 164. |

Supporting canonical modules (imported by SearchPipeline): `SearchAdapter`,
`ListingContractGuard`, `MarketVerdictEngine`, `ObjectIntelligenceCardBuilder`,
`MarketSnapshotRepository`.

Known wiring quirk (not a bug, document before changing): the pipeline calls
`gateway.run_engine("area")` and `run_engine("market_intelligence")`
(`search_pipeline.py:359,365`) but invokes risk/dedup on its own direct
instances (`:371,:376`). Same classes — the gateway's risk/dedup registrations
are redundant but consistent.

---

## 2. LEGACY COMPONENTS

| Path | Why legacy | Deletion risk |
|---|---|---|
| `infra/lentra/core/market_intelligence/gateway/` (`IntelligenceGateway`) + `runtime/bootstrap/wiring.py`, `runtime/bootstrap/main.py`, `runtime/bootstrap.py`, `core/market_intelligence/build.py` | Second, parallel orchestration flow (the one `CANONICAL.md` describes). Live only via `lentra-telegram.service` (enabled unit) and dead `worker/loop.py`. Violates "exactly ONE canonical runtime flow". | **MEDIUM** — `lentra-telegram` unit is enabled; decide its fate first (see §4 step 2). |
| `infra/lentra/services/intelligence_gateway.py` | Third gateway variant; importers are patch/side modules (`api/search_handler_patch.py`, `ingestion_router_v8.py`, `stream_processor.py`) outside the production graph. | LOW |
| `infra/lentra/runtime/bootstrap/wiring_safe.py` (`build_gateway`) | Older gateway builder; reached only via `api/pipeline_bootstrap.py` → `api/pipeline_legacy.py`. | LOW |
| `infra/lentra/contracts/routing_map.py` + `routing_map_lock.py` | Declare `RiskEngineV2` as canonical — contradicts actual wiring (v3). String-only, nothing dereferences them, but as "lock" documents they are false. | LOW (fix content, don't delete blindly) |
| `infra/lentra/services/ranking_service.py` (`RankingService`) | Parallel feed-ranking outside UnifiedRankingEngine; used by `telegram/bot_feed.py` (telegram contour). | MEDIUM — tied to telegram contour decision. |
| `infra/lentra/rent/*`, `infra/lentra/domain/*`, `infra/lentra/pipeline/*`, `infra/lentra/application/*`, `infra/lentra/ranking/*`, `infra/lentra/property/*` | Declared legacy by `CANONICAL.md` §4; not on the production import graph. | LOW–MEDIUM (large trees; verify per-module before removal) |
| Root trees: `/opt/lentra/core`, `/opt/lentra/bot`, `/opt/lentra/api`, `/opt/lentra/worker`, `/opt/lentra/services`, `/opt/lentra/kernel`, `/opt/lentra/runtime` | Entire older competing stack (flight_engine, predictive v9, fusion v7 — foreign domains). `core/runtime/worker_runtime.py` imports nonexistent `core.market_intelligence.*` → broken. Only reachable via root `docker-compose.yml` (no running containers) and the **disabled** `lentra.service`. | LOW for live system; archive rather than delete (history value). |
| `_deprecated_runtime/`, `lentra_DISABLED/`, `infra/archive/`, `infra/app/`, `infra/infra/` | Already-parked or duplicate trees. | LOW |
| Aider artifacts: `infra/--system_prompt=You are working inside Lentra AI Market Intelligence OS.` (directory), `elf.pipeline = pipeline`, `elf.pipeline.run(objects)`, `civilizatio/`, `civilization/`, `core/lifecycle ` (trailing space), `infra/init_v*_dirs.sh` (~30 scripts), `infra/test_write.txt`, `infra/test instruction` | Tooling debris, not architecture. | NONE (but confirm `civilization/` content is not wanted before removing). |
| Broken systemd unit: `lentra-worker.service` → `python -m lentra.worker.main` | `infra/lentra/worker/main.py` does not exist; unit is enabled but cannot start. | NONE to fix (repoint to `lentra.worker.run` or disable). |

---

## 3. SAFE TO DELETE

Confirmed **zero production imports** (grep-verified across the repo, excluding
venv/node_modules/.git). Dead code — no importers at all unless noted:

**Pipelines**
- `infra/lentra/services/search_pipeline.py`
- `infra/lentra/bot/services/search_pipeline.py`
- `infra/lentra/bot/features/rent_search/pipeline/search_pipeline.py`
- `infra/canonical_search_pipeline.py` (top-level scratch copy)

**Market / MI engines**
- `infra/lentra/core/market_intelligence/pricing/market_service.py`
- `infra/lentra/core/market_intelligence/market_intelligence_engine.py`
- `infra/lentra/core/market_intelligence/engines/market_intelligence_engine.py`

**Risk**
- `infra/lentra/core/market_intelligence/risk/risk_engine.py`
- `infra/lentra/core/market_intelligence/risk/risk_engine_v2.py` (+ `risk/risk_adapter.py`, its only dead importer)
- `infra/lentra/core/market_intelligence/engines/risk.py` (only "importer" is root `core/runtime/worker_runtime.py` via a broken path)
- `infra/lentra/core/market_intelligence/risk/risk_engine_adapter.py`, `risk/market_risk_engine.py`, `risk/property_risk_engine.py`, `adapters/risk_engine_adapter.py`, `contracts/risk_engine_contract.py`

**Dedup**
- `infra/lentra/core/market_intelligence/dedup/dedup_engine.py`
- `infra/lentra/core/market_intelligence/dedup/unified_dedup_engine.py` (importer chain is dead)
- `infra/lentra/core/market_intelligence/engines/dedup.py`
- `infra/lentra/core/market_intelligence/adapters/dedup_engine_adapter.py`, `contracts/dedup_engine_contract.py`
- `infra/lentra/core/ai/deduplication_engine.py`, `infra/app/core/quality/deduplicator.py`

**Ranking**
- `infra/lentra/core/market_intelligence/ranking/ranking_engine_v3.py`
- `infra/lentra/core/market_intelligence/decision/ranking_engine.py`
- `infra/lentra/bot/ux/ranking.py`
- `infra/lentra/domain/scoring/ranking_engine.py`
- `infra/lentra/rent/ranking/engine/ranking_engine.py` (importer `rent/aggregation/engine/aggregation_service.py` is itself dead)

**Decision**
- `infra/lentra/core/market_intelligence/decision_layer.py` (flat duplicate)
- `infra/lentra/core/market_intelligence/decision/ai_decision_engine.py` (dead importer of ranking/risk variants)

**Gateways / bootstrap**
- `infra/lentra/runtime/bootstrap/wiring.py`
- `infra/lentra/runtime/bootstrap/graph_attach.py`
- `infra/lentra/worker/engine.py`
- `infra/lentra/core/market_intelligence/gateway.py` (flat duplicate)
- `infra/lentra/runtime/intelligence/intelligence_gateway.py`

**Broken modules inside the production package** (import nonexistent
`lentra.core.pipeline.search_pipeline` — would raise ImportError if ever loaded,
proving they are outside the production graph):
- `infra/lentra/api/search/search_api.py`
- `infra/lentra/api/v1/debug_api.py`
- `infra/lentra/api/v1/concierge_api_class.py`

Deletion protocol: remove in small batches; after each batch restart and
health-check `lentra-api`, `lentra-bot`, `lentra-recovery`.

---

## 4. MIGRATION ORDER

### Step 1 — Documents first (zero risk)
1. Complete the truncated `infra/ARCHITECTURE_CONSTITUTION.md` (currently cut
   off at "## 2. Canonical Architecture", 35 lines) and
   `infra/CANONICAL_COMPONENT_MAP.md` (28 lines) using the flow from
   `AIDER_ARCH_CONSTITUTION_TASK.txt` and the verified paths in §1 above.
2. Commit them (they exist only in the index, not in HEAD).
3. Mark `infra/CANONICAL.md` and root `ARCHITECTURE.md` as **superseded** —
   today three documents canonize three different architectures.
4. Fix false declarations: `contracts/routing_map.py` /
   `routing_map_lock.py` (RiskEngineV2 → v3), stale KEEP entries in
   `ARCHITECTURE_CLASSIFICATION_V1.md`.

### Step 2 — Enforcement & infra hygiene (low risk)
1. Decide the fate of `lentra-telegram.service` (the parallel
   IntelligenceGateway contour). Disabling it retires the entire second flow in
   one action.
2. Fix or disable `lentra-worker.service` (points to nonexistent
   `lentra.worker.main`).
3. Extend `lentra/runtime/arch_lock/` rules to enforce the constitution:
   single pipeline, single router, no imports of legacy modules.
4. Remove the `-` prefix from `ExecStartPre` in `lentra-bot.service` so an
   arch-lock violation actually blocks startup; add the same check to
   pre-commit/CI.

### Step 3 — Delete duplicates (only after Steps 1–2)
1. Delete everything in §3 (SAFE TO DELETE), batch by batch, with service
   restarts + `/health` checks between batches.
2. Archive (do not hard-delete) the root legacy trees (`/opt/lentra/core`,
   `/opt/lentra/bot`, `/opt/lentra/api`, `/opt/lentra/worker`, root
   `docker-compose.yml`) into `_deprecated_runtime/` or an archive branch.
3. Remove aider debris (see §2 last rows).
4. Only then, consolidation inside the canon (requires ADR):
   unify risk/dedup invocation (direct vs gateway) into one path;
   fold or formally scope `RankingService` relative to UnifiedRankingEngine.

---

## 5. DO NOT TOUCH

Live production spine — any change here requires an ADR and explicit approval:

- `infra/lentra/api/pipeline/search_pipeline.py` and `api/pipeline/__init__.py` (the singleton)
- `infra/lentra/api/main.py`, `api/app_patch.py`, `api/routes/search.py`, `api/routes/miniapp.py`
- `infra/lentra/bot/main.py`, `bot/handlers/handlers.py`, `bot/cards/intelligence_renderer.py`
- `infra/lentra/worker/recovery_worker.py`, `core/pipeline/worker_search_entrypoint.py`, `core/pipeline/canonical_search_pipeline.py`
- `infra/lentra/runtime/bootstrap/gateway_v3.py`
- `infra/lentra/core/engines/` (`market_intelligence_engine.py`, `area_engine.py`, `base_engine.py`)
- `infra/lentra/core/market_intelligence/engines/risk_engine.py`, `engines/dedup_engine.py`, `dedup/dedup_index.py`
- `infra/lentra/core/market_intelligence/market/market_service.py`
- `infra/lentra/core/market_intelligence/ranking/unified_ranking_engine.py`, `ranking/ranking_engine.py`
- `infra/lentra/core/market_intelligence/decision/decision_layer.py`
- `infra/lentra/core/market_intelligence/engine_wrapper.py` and the observability wrapper
- `infra/lentra/runtime/arch_lock/` (extend rules only; do not weaken)
- systemd units `lentra-api.service`, `lentra-bot.service`, `lentra-recovery.service` (except the documented `ExecStartPre` hardening in §4 step 2)
- `infra/venv-bot/` (production virtualenv)
- Databases, migrations (`infra/alembic/`, `infra/migrations/`, `infra/sql/`) — out of scope for this cleanup

Rule of thumb: nothing on the import path
`api.main → api/pipeline/search_pipeline.py → gateway_v3 → engines → ranking → decision`
may be modified as part of cleanup. Cleanup deletes what is *outside* this path;
it never edits what is *on* it.
