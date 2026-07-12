# Lentra Architecture Constitution

This document is the single source of architectural truth for Lentra.
All code, reviews, migrations, and design decisions are subordinate to it.

Rule of precedence:

1. `ARCHITECTURE_CONSTITUTION.md` (this document)
2. `CANONICAL_COMPONENT_MAP.md` (concrete module map)
3. `ARCHITECTURE_CLEANUP_PLAN.md` (verified current state + migration plan)
4. Code

If code contradicts these documents, the code is legacy.
Older documents (`CANONICAL.md`, root `ARCHITECTURE.md`) are **superseded**
by this constitution and must not be used as design authority.

---

## 1. Product Identity

**Lentra = AI Market Intelligence OS for the SEA rental market.**

Lentra is NOT:

- a marketplace
- a listing aggregator
- an ordinary housing search tool
- a generic backend framework or a platform for building platforms

Lentra's core value is the interpretation layer it builds on top of the market:

- **Price Intelligence** — understanding whether a price is fair, high, or an opportunity.
- **Risk Analysis** — detecting scams, anomalies, and unsafe deals before the user is exposed.
- **Duplicate Detection** — collapsing the noisy multi-source market into unique real objects.
- **Area Intelligence** — contextual knowledge of districts, infrastructure, and micro-markets.
- **AI Decision Support** — turning raw signals into explainable recommendations.

A marketplace shows listings. Lentra creates a **layer of market interpretation**:
it explains what a listing means, what it is worth, what risks it carries, and
whether the user should act on it. The catalog is raw input; intelligence is the product.

> Value is in market interpretation, not infrastructure complexity.

---

## 2. Canonical Architecture

There is exactly ONE canonical runtime flow. No alternative flows may exist.

The canonical implementation lives in the `lentra` package under
`/opt/lentra/infra`. Everything outside it — root-level `core/`, `bot/`,
`api/`, `worker/`, `services/` trees — is legacy (see §8).

The architecture has four layers, in strict order:

1. **Delivery layer** — API (FastAPI), Telegram bot, worker. Thin interfaces.
   No business logic, no intelligence, no market reasoning.
2. **Pipeline layer** — `SearchPipeline`. Orchestration only: sequencing,
   contract guarding, delegation. No market logic of its own.
3. **Routing layer** — `GatewayV3`. The single engine router. Registers and
   dispatches engines; adds observability wrapping. No decisions.
4. **Intelligence layer** — Market Intelligence Core (§5). All market
   reasoning lives here and only here.

Delivery interfaces never reach into the intelligence layer directly.
The bot is an HTTP client of the API. The worker enters through the
canonical pipeline facade. There is no second door.

---

## 3. Single Runtime Flow

The one and only allowed runtime flow:

```
SearchPipeline
 -> SearchAdapter
 -> ListingContractGuard
 -> MarketService
 -> GatewayV3
     -> AreaEngine
     -> MarketIntelligenceEngine
     -> RiskEngine
     -> DedupEngine
 -> UnifiedRankingEngine
 -> DecisionLayer
 -> ObjectIntelligenceCardBuilder
```

Entry points that are allowed to reach this flow:

- **API**: `lentra.api.main` → `api/routes/search.py`, `api/routes/miniapp.py`
  → `api/pipeline/__init__.py` (process singleton) → `SearchPipeline`
- **Bot**: `lentra.bot.main` → HTTP call to the API `/search`. The bot
  imports no pipeline and no intelligence code.
- **Worker**: `lentra.worker.recovery_worker` →
  `core/pipeline/worker_search_entrypoint.py` → `CanonicalSearchPipeline`
  (zero-logic facade over the same `SearchPipeline`).

All entry points converge on `lentra/api/pipeline/search_pipeline.py`.
Creating any additional path into the intelligence layer is a
constitutional violation.

---

## 4. Runtime Components Ownership

Canonical component map (verified against production imports; see
`ARCHITECTURE_CLEANUP_PLAN.md` §1 for exact file paths and line references):

| Component | Canonical module | Owns |
|---|---|---|
| SearchPipeline | `lentra/api/pipeline/search_pipeline.py` | Flow orchestration, sequencing, singleton lifecycle |
| CanonicalSearchPipeline | `lentra/core/pipeline/canonical_search_pipeline.py` | Facade for worker entry; NO logic |
| MarketService | `lentra/core/market_intelligence/market/market_service.py` | Market truth, price baselines, market context |
| GatewayV3 | `lentra/runtime/bootstrap/gateway_v3.py` | Engine registration and routing; the ONLY router |
| MarketIntelligenceEngine | `lentra/core/engines/market_intelligence_engine.py` | Price-vs-market interpretation |
| AreaEngine | `lentra/core/engines/area_engine.py` | Area / district intelligence |
| RiskEngine | `lentra/core/market_intelligence/engines/risk_engine.py` | Risk scoring, risk veto |
| DedupEngine | `lentra/core/market_intelligence/engines/dedup_engine.py` | Duplicate collapsing |
| UnifiedRankingEngine | `lentra/core/market_intelligence/ranking/unified_ranking_engine.py` | Ranking; the ONLY ranking authority |
| DecisionLayer | `lentra/core/market_intelligence/decision/decision_layer.py` | Final decision |
| ObjectIntelligenceCardBuilder | (per component map) | Result presentation contract |

Ownership rules:

- **MarketService** owns market truth, price baselines, and market context.
  No other component may compute or cache a competing "market truth".
- **UnifiedRankingEngine** owns ranking. No parallel ranking engines.
  It may delegate internally (to `MarketRankingEngine`) but remains the
  single external authority.
- **DecisionLayer** owns the final decision. Nothing downstream of it may
  override or re-decide.
- **RiskEngine** owns risk veto authority. DecisionLayer MUST respect the
  veto. A vetoed object cannot be recommended, regardless of ranking score.
- **GatewayV3** owns engine routing. No component may instantiate or call
  engines through any other router.

---

## 5. Market Intelligence Core

`lentra/core/market_intelligence/` is the intelligence heart of the system.

Principles:

- ALL market reasoning happens inside the Market Intelligence Core and the
  two canonical engines under `lentra/core/engines/`.
- The core is organized by responsibility (market, risk, dedup, ranking,
  decision), not by version. Versioned duplicates (`*_v2.py`, `*_v3.py`
  living side by side) are constitutional violations, not options.
- Intelligence modules are stateless with respect to requests. Market state
  belongs to MarketService and the snapshot repositories.
- The core never imports from the delivery layer (api routes, bot handlers,
  telegram). Dependencies flow strictly downward (§7).
- Only the modules named in §4 are canonical. Everything else currently
  inside `core/market_intelligence/` that duplicates their responsibility
  is legacy pending removal (see `ARCHITECTURE_CLEANUP_PLAN.md` §3).

---

## 6. Engine Responsibilities

### 6.1 Market Intelligence (`MarketIntelligenceEngine`)

- Interprets a listing's price against market context supplied by MarketService.
- Produces fair-price / overpriced / opportunity signals with explanations.
- MUST NOT rank, veto, deduplicate, or make final decisions.
- Is registered in GatewayV3 under the key `"market_intelligence"` and is the
  fallback interpreter for unknown request types.

### 6.2 Area Intelligence (`AreaEngine`)

- Owns district, infrastructure, and micro-market context.
- Enriches objects with area signals; never alters price or risk verdicts.
- Registered in GatewayV3 under the key `"area"`.

### 6.3 Risk Engine (`RiskEngine`)

- Detects scams, anomalies, and unsafe deals.
- Produces a risk score AND a binding veto flag.
- The veto is absolute: no downstream component may recommend a vetoed object.
- MUST NOT be bypassed, sampled, or made advisory.

### 6.4 Dedup Engine (`DedupEngine`)

- Collapses multi-source listings into unique real objects
  (internally backed by `dedup/dedup_index.py`).
- Runs before ranking: ranking operates on unique objects only.
- MUST NOT drop objects for any reason other than duplication.

### 6.5 Ranking Engine (`UnifiedRankingEngine`)

- The single ranking authority. Orders unique, risk-annotated objects.
- Delegates computation to `MarketRankingEngine` internally; this delegation
  is an implementation detail, not a second public engine.
- MUST NOT re-implement risk, pricing, or dedup logic.
- Any other ranking implementation anywhere in the repository is legacy.

### 6.6 Decision Layer (`DecisionLayer`)

- Produces the final, explainable recommendation.
- Consumes ranking output + risk verdicts + market context.
- MUST respect the RiskEngine veto unconditionally.
- Is the last reasoning step: after DecisionLayer only presentation
  (`ObjectIntelligenceCardBuilder`) may run.

---

## 7. Data Flow Rules

1. Data flows in ONE direction:
   `sources → ingestion → normalization → market objects → intelligence → decision → presentation`.
2. Dependencies point strictly downward: delivery → pipeline → gateway →
   engines → models. No layer imports from a layer above it.
3. The pipeline enters the intelligence layer through GatewayV3 or through
   the direct engine instances it constructs at startup — never through
   ad-hoc imports inside handlers.
4. Engines receive data as explicit inputs and return explicit outputs.
   No engine reads global state, another engine's internals, or the database
   directly; market data access goes through MarketService and repositories.
5. Contracts are guarded at the boundary (`ListingContractGuard`).
   Data that fails the contract does not enter the intelligence layer.
6. Presentation (cards, bot rendering, miniapp schemas) may format results
   but may not recompute, filter, or re-rank them.

---

## 8. Legacy Architecture Rules

Legacy is any module that duplicates a canonical responsibility or lies
outside the canonical flow. The authoritative inventory is
`ARCHITECTURE_CLEANUP_PLAN.md` §2–§3. This includes, at minimum:

- the parallel `IntelligenceGateway` contour
  (`core/market_intelligence/gateway/`, `runtime/bootstrap/wiring*.py`,
  the telegram dispatcher path);
- all duplicate pipelines, gateways, and engines listed in the cleanup plan;
- the entire root-level trees (`/opt/lentra/core`, `/opt/lentra/bot`,
  `/opt/lentra/api`, `/opt/lentra/worker`, flight/predictive/fusion stacks);
- `lentra/rent/*`, `lentra/domain/*`, `lentra/pipeline/*`,
  `lentra/application/*`, `lentra/ranking/*`, `lentra/property/*`.

Rules:

1. **No new imports into legacy.** Production code must not import legacy
   modules, directly or transitively.
2. **Legacy cannot receive new features.** Only removal or archival.
3. **Canonical architecture wins over existing code.** If working code
   contradicts this constitution, the code is scheduled for migration,
   not the constitution for revision.
4. Legacy is removed following the order in `ARCHITECTURE_CLEANUP_PLAN.md`
   §4: documents → enforcement → deletion in verified batches.
5. Root-level legacy trees are archived, not silently deleted.

---

## 9. Duplicate Component Policy

Any duplicate of the following is legacy by definition, regardless of quality:

- pipeline
- router / gateway
- ranking engine
- intelligence engine
- risk engine
- dedup engine
- decision engine / decision layer

Policy:

1. Exactly ONE canonical implementation exists per responsibility (§4).
2. A second implementation may exist ONLY as a short-lived migration step,
   introduced through an ADR with a written removal date.
3. Versioned copies (`_v2`, `_v3`, `_new`, `_old`) sitting side by side in
   the tree are forbidden. Versions live in git history, not in the package.
4. Facades with zero logic (e.g. `CanonicalSearchPipeline`) are not
   duplicates; a facade that accumulates logic becomes a duplicate and
   violates this policy.
5. Declarative maps and locks (routing maps, registries) must name the
   actual canonical classes. A map that names a non-canonical class is a
   defect and must be fixed immediately.

---

## 10. Change Management Rules

1. Any architectural change requires an ADR. ADR is required for:
   - a new pipeline
   - a new engine
   - a new router
   - ownership changes (§4)
   - decision authority changes
   - any second implementation of a canonical responsibility (§9.2)
2. Changes to the production spine (the import path
   `api.main → search_pipeline → gateway_v3 → engines → ranking → decision`;
   full DO-NOT-TOUCH list in `ARCHITECTURE_CLEANUP_PLAN.md` §5) require an
   ADR and explicit approval — including "cleanup" edits.
3. Allowed without ADR: bug fixes, minimal safety improvements, small
   refactors inside existing class boundaries, documentation.
4. AI-assisted development (aider, agents, LLM tools) is bound by this
   constitution. If an instruction conflicts with this document, this
   document wins. AI tools must not invent parallel systems or perform
   speculative refactors.
5. An automated architecture checker (`lentra/runtime/arch_lock/`) must
   validate on every service start and in CI:
   - single pipeline
   - single router
   - single ranking authority
   - single decision authority
   - market truth ownership (MarketService)
   - risk veto integrity
   - no legacy imports
   - canonical flow direction (§7)
   Checker failures block startup and merges; the checker may be extended
   but never weakened.

---

## 11. Forbidden Architecture Patterns

The following are STRICTLY FORBIDDEN:

1. **Second runtime flow** — any alternative pipeline, orchestrator, or
   gateway that reaches the intelligence layer (including reviving the
   `IntelligenceGateway` contour).
2. **Engine/registry duplication** — `GatewayV2`, `EngineRegistryV2/V3`,
   alternative routers, parallel engine factories.
3. **Intelligence fragmentation** — splitting canonical engines into
   competing sub-engines, or stacking new "AI layers" above DecisionLayer.
4. **Ranking pluralism** — any ranking implementation outside
   UnifiedRankingEngine, including "just for the feed" or "just for the bot".
5. **Risk veto bypass** — making the veto advisory, sampling it, or letting
   any component recommend a vetoed object.
6. **Delivery-layer intelligence** — market reasoning in API routes, bot
   handlers, telegram code, or presentation builders.
7. **Upward imports** — intelligence or pipeline code importing from the
   delivery layer.
8. **Graph/DAG execution frameworks as core architecture** — Lentra is a
   market intelligence system, not a workflow platform.
9. **Side-by-side versioned duplicates** in the source tree (§9.3).
10. **Silent architecture changes** — any of the above introduced without an
    ADR, or code that contradicts this constitution merged as "temporary".

---

*This constitution supersedes `CANONICAL.md` and the root `ARCHITECTURE.md`.
Verified current-state evidence and the migration sequence live in
`ARCHITECTURE_CLEANUP_PLAN.md`.*
