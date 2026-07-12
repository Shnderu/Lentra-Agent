# Lentra Canonical Component Map

> Companion to `ARCHITECTURE_CONSTITUTION.md`.
> Evidence base: `ARCHITECTURE_CLEANUP_PLAN.md` (audit 2026-07-12), `ARCHITECTURE_DELETION_MANIFEST.md`.
>
> Rule of precedence:
> 1. `ARCHITECTURE_CONSTITUTION.md`
> 2. `CANONICAL_COMPONENT_MAP.md` (this file)
> 3. Code
>
> If code contradicts these documents, the code is legacy.
> Paths are relative to `/opt/lentra/infra` unless stated otherwise.

---

## 1. Purpose

- This is the map of the **single canonical implementation** of every
  architectural responsibility in Lentra.
- It is used together with the Architecture Constitution: the constitution
  defines the rules; this map binds them to concrete modules and classes.
- It defines **ownership**: which module owns which responsibility, and what
  it may depend on.
- It fixes **forbidden duplicates**: any component that duplicates a
  responsibility listed here is legacy by definition (Constitution §9) and is
  inventoried in §6 below.

Lentra = AI Market Intelligence OS for the SEA rental market. Not a
marketplace. The product is market interpretation: AI Price Check, Duplicate
Detection, Risk Score, Area Intelligence, Ranking, Decision Layer.

---

## 2. Production Runtime Entry Points

All enabled production units run from `/opt/lentra/infra` (package `lentra`).

| Entry point | Path | Purpose | Next layer |
|---|---|---|---|
| API | `lentra/api/main.py` | FastAPI app; routes `/search`, `/miniapp`, `/health` | `api/routes/search.py`, `api/routes/miniapp.py` → `api/pipeline/__init__.py` (process singleton) → `SearchPipeline` |
| Bot | `lentra/bot/main.py` | aiogram bot; thin HTTP client of the API (`/search`). Imports no pipeline and no intelligence code | HTTP → API `/search`; rendering via `bot/cards/intelligence_renderer.py` |
| Recovery | `lentra/worker/recovery_worker.py` | Retry/recovery of failed search tasks | `core/pipeline/worker_search_entrypoint.py` → `CanonicalSearchPipeline` (facade) → `SearchPipeline` |

All three converge on `lentra/api/pipeline/search_pipeline.py`.

---

## 3. Canonical Production Flow

```
api.main
  ↓
api/pipeline/search_pipeline.py   (SearchPipeline)
  ↓  SearchAdapter → ListingContractGuard → MarketService
GatewayV3                          (runtime/bootstrap/gateway_v3.py)
  ↓
Engines:
  - MarketIntelligenceEngine   ("market_intelligence")
  - AreaEngine                 ("area")
  - RiskEngine                 (also held directly by the pipeline)
  - DedupEngine                (also held directly by the pipeline)
  ↓
UnifiedRankingEngine
  ↓
DecisionLayer
  ↓
ObjectIntelligenceCardBuilder
```

- **This is the ONLY production flow.** No alternative pipeline, gateway, or
  orchestrator may reach the intelligence layer (Constitution §3, §11).
- Every other pipeline/gateway in the repository is **legacy** (§6).
- Known wiring detail (documented, do not change without ADR): the pipeline
  calls `area` and `market_intelligence` through GatewayV3, but invokes
  risk/dedup on its own direct instances of the same canonical classes.

---

## 4. Canonical Component Ownership

### Pipeline

| Component | Canonical Path | Class | Responsibility | Dependencies | Status |
|---|---|---|---|---|---|
| SearchPipeline | `lentra/api/pipeline/search_pipeline.py` | `SearchPipeline` | Single production entrypoint; flow orchestration only, no market logic | SearchAdapter, ListingContractGuard, MarketService, GatewayV3, RiskEngine, DedupEngine, UnifiedRankingEngine, DecisionLayer, MarketVerdictEngine, ObjectIntelligenceCardBuilder, MarketSnapshotRepository | CANONICAL |
| CanonicalSearchPipeline | `lentra/core/pipeline/canonical_search_pipeline.py` | `CanonicalSearchPipeline` | Zero-logic facade over SearchPipeline for the worker path; must never accumulate logic | SearchPipeline | CANONICAL (facade) |

### Runtime

| Component | Canonical Path | Class | Responsibility | Dependencies | Status |
|---|---|---|---|---|---|
| GatewayV3 | `lentra/runtime/bootstrap/gateway_v3.py` | `GatewayV3` / `build_gateway_v3()` | The ONLY engine router; registers engines wrapped in `EngineWrapper` + `ObservabilityEngineV1` | AreaEngine, MarketIntelligenceEngine, RiskEngine, DedupEngine, engine_wrapper | CANONICAL |

### Market Intelligence

| Component | Canonical Path | Class | Responsibility | Dependencies | Status |
|---|---|---|---|---|---|
| MarketService | `lentra/core/market_intelligence/market/market_service.py` | `MarketService` | Owns market truth: price baselines, market context. No competing "market truth" allowed | market data / snapshot repositories | CANONICAL |
| MarketIntelligenceEngine | `lentra/core/engines/market_intelligence_engine.py` | `MarketIntelligenceEngine(BaseEngine)` | Price-vs-market interpretation ("pricing_v3_product"); fallback interpreter for unknown request types | `core/engines/base_engine.py`, market context from MarketService | CANONICAL |

### Area Intelligence

| Component | Canonical Path | Class | Responsibility | Dependencies | Status |
|---|---|---|---|---|---|
| AreaEngine | `lentra/core/engines/area_engine.py` | `AreaEngine` | District / infrastructure / micro-market context; enrichment only | `core/engines/base_engine.py` | CANONICAL |

### Risk

| Component | Canonical Path | Class | Responsibility | Dependencies | Status |
|---|---|---|---|---|---|
| RiskEngine (v3) | `lentra/core/market_intelligence/engines/risk_engine.py` | `RiskEngine` | Anti-scam scoring; binding veto authority | — (explicit inputs only) | CANONICAL |

### Dedup

| Component | Canonical Path | Class | Responsibility | Dependencies | Status |
|---|---|---|---|---|---|
| DedupEngine | `lentra/core/market_intelligence/engines/dedup_engine.py` | `DedupEngine` | Collapsing multi-source listings into unique real objects | DedupIndex | CANONICAL |
| DedupIndex | `lentra/core/market_intelligence/dedup/dedup_index.py` | `DedupIndex` | Internal index backing DedupEngine; production dependency — protected | — | CANONICAL (internal) |

### Ranking

| Component | Canonical Path | Class | Responsibility | Dependencies | Status |
|---|---|---|---|---|---|
| UnifiedRankingEngine | `lentra/core/market_intelligence/ranking/unified_ranking_engine.py` | `UnifiedRankingEngine` | The ONLY external ranking authority | MarketRankingEngine | CANONICAL |
| MarketRankingEngine | `lentra/core/market_intelligence/ranking/ranking_engine.py` | `MarketRankingEngine` | Internal ranking computation; implementation detail of UnifiedRankingEngine, not a second public engine | — | CANONICAL (internal) |

### Decision

| Component | Canonical Path | Class | Responsibility | Dependencies | Status |
|---|---|---|---|---|---|
| DecisionLayer | `lentra/core/market_intelligence/decision/decision_layer.py` | `DecisionLayer` (v2.1) | Final, explainable recommendation; MUST respect RiskEngine veto | ranking output, risk verdicts, market context | CANONICAL |

---

## 5. Engine Responsibility Map

| Engine | Responsibility | MUST NOT |
|---|---|---|
| MarketIntelligenceEngine | Price vs market interpretation: fair / overpriced / opportunity, with explanations | rank, veto, deduplicate, make final decisions |
| AreaEngine | District analytics: infrastructure, micro-markets; enriches objects with area signals | alter price or risk verdicts |
| RiskEngine | Anti-scam scoring + binding **veto authority**; a vetoed object cannot be recommended by anything downstream | be bypassed, sampled, or made advisory |
| DedupEngine | Entity resolution and duplicate grouping; runs before ranking so ranking sees unique objects only | drop objects for any reason other than duplication |
| UnifiedRankingEngine | Final ordering authority over unique, risk-annotated objects | re-implement risk, pricing, or dedup logic |
| DecisionLayer | Final recommendation authority; last reasoning step before presentation | be overridden downstream; ignore the risk veto |

---

## 6. Legacy Duplicate Mapping

Full evidence and deletion batches: `ARCHITECTURE_CLEANUP_PLAN.md` §2–3,
`ARCHITECTURE_DELETION_MANIFEST.md`. Statuses: **SAFE DELETE** (zero
production imports, confirmed), **REVIEW** (decision required first),
**ARCHIVE** (move, don't hard-delete), **KEEP** (canonical).

### Pipelines

| Legacy Component | Legacy Path | Canonical Replacement | Action |
|---|---|---|---|
| SearchPipeline (services copy) | `lentra/services/search_pipeline.py` | `api/pipeline/search_pipeline.py` | SAFE DELETE |
| SearchPipeline (bot services copy) | `lentra/bot/services/search_pipeline.py` | same | SAFE DELETE |
| SearchPipeline (rent_search copy) | `lentra/bot/features/rent_search/pipeline/search_pipeline.py` | same | SAFE DELETE |
| Scratch pipeline copy | `infra/canonical_search_pipeline.py` (top-level) | `core/pipeline/canonical_search_pipeline.py` | SAFE DELETE |
| Legacy pipeline path | `lentra/api/pipeline_bootstrap.py`, `api/pipeline_legacy.py` | `api/pipeline/search_pipeline.py` | REVIEW (delete as a set with wiring_safe) |

### Gateways / routers

| Legacy Component | Legacy Path | Canonical Replacement | Action |
|---|---|---|---|
| IntelligenceGateway contour | `lentra/core/market_intelligence/gateway/`, `core/market_intelligence/build.py`, `runtime/bootstrap/main.py`, `runtime/bootstrap.py` | GatewayV3 | REVIEW (blocked on `lentra-telegram.service` decision) |
| build_gateway (safe wiring) | `lentra/runtime/bootstrap/wiring_safe.py` | GatewayV3 | REVIEW |
| build_gateway (old wiring) | `lentra/runtime/bootstrap/wiring.py` | GatewayV3 | SAFE DELETE |
| build_gateway_with_graph | `lentra/runtime/bootstrap/graph_attach.py` | GatewayV3 | SAFE DELETE |
| Worker gateway builder | `lentra/worker/engine.py` | GatewayV3 | SAFE DELETE |
| IntelligenceGateway (flat) | `lentra/core/market_intelligence/gateway.py` | GatewayV3 | SAFE DELETE |
| IntelligenceGateway (runtime) | `lentra/runtime/intelligence/intelligence_gateway.py` | GatewayV3 | SAFE DELETE |
| IntelligenceGateway (services) | `lentra/services/intelligence_gateway.py` | GatewayV3 | REVIEW (three side-module importers) |

### Market / Intelligence engines

| Legacy Component | Legacy Path | Canonical Replacement | Action |
|---|---|---|---|
| MarketService (pricing copy) | `lentra/core/market_intelligence/pricing/market_service.py` | `market/market_service.py` | SAFE DELETE |
| MarketIntelligenceEngine (flat) | `lentra/core/market_intelligence/market_intelligence_engine.py` | `core/engines/market_intelligence_engine.py` | SAFE DELETE |
| MarketIntelligenceEngine (engines copy) | `lentra/core/market_intelligence/engines/market_intelligence_engine.py` | same | SAFE DELETE |

### Risk engines

| Legacy Component | Legacy Path | Canonical Replacement | Action |
|---|---|---|---|
| RiskEngine (risk pkg) | `lentra/core/market_intelligence/risk/risk_engine.py` | `engines/risk_engine.py` (v3) | SAFE DELETE |
| RiskEngineV2 | `lentra/core/market_intelligence/risk/risk_engine_v2.py` (+ `risk/risk_adapter.py`) | same | SAFE DELETE |
| RiskEngine (EngineV3 variant) | `lentra/core/market_intelligence/engines/risk.py` | same | SAFE DELETE |
| Risk adapters/contracts | `risk/risk_engine_adapter.py`, `risk/market_risk_engine.py`, `risk/property_risk_engine.py`, `adapters/risk_engine_adapter.py`, `contracts/risk_engine_contract.py` | same | SAFE DELETE |
| RiskEngine v9 (root) | `/opt/lentra/core/predictive/risk_engine_v9.py` | same | ARCHIVE (root tree) |

### Dedup engines

| Legacy Component | Legacy Path | Canonical Replacement | Action |
|---|---|---|---|
| DedupEngine (dedup pkg) | `lentra/core/market_intelligence/dedup/dedup_engine.py` | `engines/dedup_engine.py` | SAFE DELETE |
| UnifiedDedupEngine | `lentra/core/market_intelligence/dedup/unified_dedup_engine.py` | same | SAFE DELETE |
| DedupEngine (EngineV3 variant) | `lentra/core/market_intelligence/engines/dedup.py` | same | SAFE DELETE |
| Dedup adapters/contracts | `adapters/dedup_engine_adapter.py`, `contracts/dedup_engine_contract.py` | same | SAFE DELETE |
| Misc deduplicators | `lentra/core/ai/deduplication_engine.py`, `infra/app/core/quality/deduplicator.py` | same | SAFE DELETE |

### Ranking engines

| Legacy Component | Legacy Path | Canonical Replacement | Action |
|---|---|---|---|
| RankingEngineV3 | `lentra/core/market_intelligence/ranking/ranking_engine_v3.py` | UnifiedRankingEngine | SAFE DELETE |
| RankingEngine (decision pkg) | `lentra/core/market_intelligence/decision/ranking_engine.py` | same | SAFE DELETE |
| RankingEngine (bot ux) | `lentra/bot/ux/ranking.py` | same | SAFE DELETE |
| Ranking functions (domain) | `lentra/domain/scoring/ranking_engine.py` | same | SAFE DELETE |
| RankingEngine (rent) | `lentra/rent/ranking/engine/ranking_engine.py` | same | SAFE DELETE |
| RankingService (feed) | `lentra/services/ranking_service.py` | UnifiedRankingEngine (or formal non-market scope) | REVIEW |
| Flight ranking stack (root) | `/opt/lentra/core/flight_engine/ranking/*` | same | ARCHIVE (root tree) |

### Decision

| Legacy Component | Legacy Path | Canonical Replacement | Action |
|---|---|---|---|
| DecisionLayer (flat) | `lentra/core/market_intelligence/decision_layer.py` | `decision/decision_layer.py` | SAFE DELETE |
| AIDecisionEngine | `lentra/core/market_intelligence/decision/ai_decision_engine.py` | DecisionLayer | SAFE DELETE |

### Broken modules (import nonexistent `lentra.core.pipeline.search_pipeline`)

| Legacy Component | Legacy Path | Canonical Replacement | Action |
|---|---|---|---|
| Search API (alt) | `lentra/api/search/search_api.py` | `api/routes/search.py` | SAFE DELETE |
| Debug API | `lentra/api/v1/debug_api.py` | — | SAFE DELETE |
| Concierge API class | `lentra/api/v1/concierge_api_class.py` | — | SAFE DELETE |

### Root legacy trees (outside `/opt/lentra/infra`)

| Legacy Component | Legacy Path | Canonical Replacement | Action |
|---|---|---|---|
| Old competing stack (flight_engine, predictive v9, fusion v7) | `/opt/lentra/core/` | infra `lentra` package | ARCHIVE |
| Root bot / api / worker / services / kernel / runtime | `/opt/lentra/{bot,api,worker,services,kernel,runtime}/` | infra `lentra` package | ARCHIVE |
| flyrum compose stack | root `docker-compose.yml`, `main.py`, `worker_main.py`, root Dockerfiles | systemd units under `/opt/lentra/infra` | ARCHIVE |
| Already-parked trees | `_deprecated_runtime/`, `lentra_DISABLED/`, `infra/archive/`, `infra/app/`, `infra/infra/` | — | ARCHIVE (consolidate) |
| Declared-legacy subtrees | `lentra/rent/*`, `lentra/domain/*`, `lentra/pipeline/*`, `lentra/application/*`, `lentra/ranking/*`, `lentra/property/*` | canonical flow | REVIEW (per-module before removal) |
| Telegram contour | `lentra/telegram/`, `worker/loop.py`, `worker/runtime.py` | Bot → API HTTP path | REVIEW (blocked on `lentra-telegram.service` decision) |
| False routing declarations | `lentra/contracts/routing_map.py`, `routing_map_lock.py` (name RiskEngineV2 as canonical) | fix content to v3 | REVIEW (fix, don't delete blindly) |

---

## 7. Dependency Rules

Allowed flow (dependencies point strictly downward):

```
API
 ↓
Pipeline
 ↓
Runtime (GatewayV3)
 ↓
Engines
 ↓
Ranking
 ↓
Decision
```

Forbidden (Constitution §7, §11):

- An engine importing API / delivery-layer code (upward import).
- Legacy importing canonical, or canonical importing legacy — no new import
  edges into or out of legacy.
- A second pipeline.
- A second gateway / router.
- A second ranking authority.
- Risk bypass — veto is binding; no component may recommend a vetoed object.
- Dedup bypass — ranking and decision operate on deduplicated objects only.

---

## 8. Production Spine Protection

Files that may not be modified or deleted without an ADR
(full list: `ARCHITECTURE_CLEANUP_PLAN.md` §5):

- `lentra/api/pipeline/search_pipeline.py` (+ `api/pipeline/__init__.py`)
- `lentra/runtime/bootstrap/gateway_v3.py`
- `lentra/core/engines/*` (`market_intelligence_engine.py`, `area_engine.py`, `base_engine.py`)
- `lentra/core/market_intelligence/market/market_service.py`
- `lentra/core/market_intelligence/engines/risk_engine.py`
- `lentra/core/market_intelligence/engines/dedup_engine.py`
- `lentra/core/market_intelligence/dedup/dedup_index.py`
- `lentra/core/market_intelligence/ranking/unified_ranking_engine.py` (+ `ranking/ranking_engine.py`)
- `lentra/core/market_intelligence/decision/decision_layer.py`
- `lentra/runtime/arch_lock/*` (may be extended, never weakened)
- Entry points and facades: `api/main.py`, `bot/main.py`,
  `worker/recovery_worker.py`, `core/pipeline/worker_search_entrypoint.py`,
  `core/pipeline/canonical_search_pipeline.py`
- `lentra/core/market_intelligence/engine_wrapper.py` + observability wrapper

---

## 9. Current Migration State

| State | Contents |
|---|---|
| **KEEP** | All canonical components in §4; production spine in §8; systemd units `lentra-api`, `lentra-bot`, `lentra-recovery`; `infra/venv-bot/`; data layer (`alembic/`, `migrations/`, `sql/`) |
| **REVIEW** | Telegram / IntelligenceGateway contour (blocked on `lentra-telegram.service` decision); `wiring_safe.py` + `pipeline_bootstrap.py` + `pipeline_legacy.py` set; `services/intelligence_gateway.py` + its side-module importers; `services/ranking_service.py`; `rent/domain/pipeline/application/ranking/property` subtrees; routing maps (fix RiskEngineV2 → v3); broken `lentra-worker.service` (repoint or disable) |
| **ARCHIVE** | Root legacy trees (`/opt/lentra/core`, `bot`, `api`, `worker`, `services`, `kernel`, `runtime`), root compose stack, already-parked trees (`_deprecated_runtime/`, `lentra_DISABLED/`, `infra/archive/`, `infra/app/`, `infra/infra/`) |
| **SAFE DELETE** | All items marked SAFE DELETE in §6 — confirmed zero production imports; executed only per `ARCHITECTURE_DELETION_MANIFEST.md` batches (documents → enforcement → deletion, with service restarts between batches) |

Migration order (`ARCHITECTURE_CLEANUP_PLAN.md` §4): documents first →
enforcement (arch_lock, unit fixes, telegram decision) → deletion in batches.
