# Arch Lock Migration Plan

> Prepares the migration of `lentra/runtime/arch_lock/` enforcement from the
> old architecture graph to the canonical Lentra AI Market Intelligence OS
> architecture.
>
> Source of truth:
> `ARCHITECTURE_CONSTITUTION.md` → `CANONICAL_COMPONENT_MAP.md` →
> `ARCHITECTURE_CLEANUP_PLAN.md` / `ARCHITECTURE_DELETION_MANIFEST.md` → this plan.
>
> This document is documentation only. It changes no Python, no JSON, no
> systemd units, and does not touch `SEAL.json`.
> Paths are relative to `/opt/lentra/infra` unless stated otherwise.

---

## 1. Current arch_lock State

### 1.1 Existing runners

| Runner | Invocation | Behavior |
|---|---|---|
| `lentra/runtime/arch_lock/arch_lock_runner.py` (v1.6) | `ExecStartPre=-...` in `lentra-bot.service` and `lentra-worker.service` | Instantiates `ArchGovernor` → `hard_gate()`: static file scan of forbidden import edges via `firewall.py`. The leading `-` means failures are **ignored** — the gate never actually blocks startup. |
| `lentra/runtime/arch_lock/arch_lock_v2_runner.py` | `lentra-arch-lock-v2.service` — unit exists but is **disabled** | v2 policy engine path (`v2_policy_engine.py`, `v2_rules.py`, `v2_remediation/`); not running anywhere. |
| Supporting machinery | — | `governor.py`, `policy_engine.py`, `firewall.py`, `freezer.py`, `seal_engine.py`, `boot_seal_check.py`, patch/repair/rollback engines. Only the v1 governor path is live. |

### 1.2 SEAL.json role

`arch_lock/SEAL.json` is a frozen **import-graph snapshot**: a map of
`file → imported modules` for the `lentra` package, captured by
`seal_engine.py` / `sealed_graph.py` at seal time. `boot_seal_check.py`
compares the current graph against it to detect drift.

Problem: the seal snapshots the graph **as it was**, including the legacy
trees (`lentra/rent/*`, load scripts, telegram contour). It therefore
*protects the mess* — deleting legacy files or removing legacy imports reads
as "drift" just as much as adding a rogue pipeline would. The seal encodes
history, not the constitution. (Per task constraints, `SEAL.json` is not
modified yet — re-sealing is a Phase 2+ action.)

### 1.3 Why current rules are outdated

Current live rules (`rules_v1.json`, v1.2) are three import blocks:

1. `NO_RUNTIME_IMPORT_IN_CORE` — core may not import `lentra.runtime.*`
2. `NO_CROSS_MARKET_INTELLIGENCE_TO_RUNTIME` — MI may not import runtime
3. `NO_API_TO_CORE_BACKFLOW` — **denies `lentra.api -> lentra.core`**

Rule 3 is the critical defect: it contradicts the canonical architecture.
The single production pipeline lives at `api/pipeline/search_pipeline.py`
and legitimately imports `lentra.core.market_intelligence.*` and
`lentra.runtime.bootstrap.gateway_v3` — that IS the canonical flow
(Constitution §3). Under rules_v1 the canonical spine is a violation, which
is precisely why the runner is wired with `ExecStartPre=-` (ignore failures).
The enforcement is not merely weak — it guards the **wrong architecture**,
so it cannot be strengthened without first being migrated.

Additional gaps:

- No rule enforces pipeline/gateway/ranking/decision **singularity** — a
  second `SearchPipeline` or gateway builder would pass today's checks.
- No rule blocks imports of the legacy duplicates inventoried in
  `ARCHITECTURE_CLEANUP_PLAN.md` §2–3 (IntelligenceGateway contour, dead
  engines, `rent/domain/services` trees).
- `v2_rules.py` (`RULES_V2`) seals bootstrap/gateway internals of the **old
  IntelligenceGateway contour** — i.e., v2 also protects legacy, not canon.
- Nothing runs in CI; the only hook is best-effort at service start.

---

## 2. Target Enforcement Model

The migrated arch_lock enforces the constitution's invariants, not a
historical graph snapshot.

### Mandatory invariants

**INV-1 — Single production pipeline**

- `lentra/api/pipeline/search_pipeline.py` is the only module defining a
  production `SearchPipeline`.
- Allowed consumers: `api/pipeline/__init__.py` (singleton),
  `core/pipeline/canonical_search_pipeline.py` (zero-logic facade).
- Any other class named/acting as a search pipeline is a violation.

**INV-2 — Single router**

- `lentra/runtime/bootstrap/gateway_v3.py` (`GatewayV3` /
  `build_gateway_v3()`) is the only engine router.
- `build_gateway_v3()` may be called only from
  `api/pipeline/search_pipeline.py`.
- Any other `build_gateway*` / gateway class reachable from production is a
  violation.

**INV-3 — Single intelligence core**

Exactly one canonical implementation per responsibility
(paths per `CANONICAL_COMPONENT_MAP.md` §4):

| Responsibility | Canonical module |
|---|---|
| MarketService | `core/market_intelligence/market/market_service.py` |
| AreaEngine | `core/engines/area_engine.py` |
| MarketIntelligenceEngine | `core/engines/market_intelligence_engine.py` |
| RiskEngine | `core/market_intelligence/engines/risk_engine.py` |
| DedupEngine | `core/market_intelligence/engines/dedup_engine.py` (+ internal `dedup/dedup_index.py`) |
| UnifiedRankingEngine | `core/market_intelligence/ranking/unified_ranking_engine.py` (+ internal `ranking/ranking_engine.py`) |
| DecisionLayer | `core/market_intelligence/decision/decision_layer.py` |

The rule set must whitelist these modules and treat any competing definition
of the same responsibility as a violation.

**Direction invariant** (replaces the defective `NO_API_TO_CORE_BACKFLOW`):
dependencies flow `API → Pipeline → Runtime(GatewayV3) → Engines → Ranking →
Decision`. Engines/intelligence never import delivery-layer code. The
pipeline's imports of `lentra.core.*` and `gateway_v3` are explicitly
**allowed** — they are the spine, not backflow.

---

## 3. Forbidden Imports

Production code (anything reachable from the three entrypoints:
`api.main`, `bot.main`, `worker.recovery_worker`) must not import:

| Category | Deny targets (per `ARCHITECTURE_CLEANUP_PLAN.md` / `DELETION_MANIFEST` §3–4) |
|---|---|
| Legacy pipelines | `lentra.services.search_pipeline`, `lentra.bot.services.search_pipeline`, `lentra.bot.features.rent_search.pipeline.*`, `lentra.api.pipeline_legacy`, `lentra.api.pipeline_bootstrap` |
| IntelligenceGateway contour | `lentra.core.market_intelligence.gateway.*`, `lentra.core.market_intelligence.gateway` (flat), `lentra.core.market_intelligence.build`, `lentra.services.intelligence_gateway`, `lentra.runtime.intelligence.*` |
| Old gateway builders | `lentra.runtime.bootstrap.wiring`, `lentra.runtime.bootstrap.wiring_safe`, `lentra.runtime.bootstrap.graph_attach`, `lentra.worker.engine`, `lentra.runtime.bootstrap.main`, `lentra.runtime.bootstrap` (module) |
| Old ranking engines | `lentra.core.market_intelligence.ranking.ranking_engine_v3`, `lentra.core.market_intelligence.decision.ranking_engine`, `lentra.bot.ux.ranking`, `lentra.domain.scoring.ranking_engine`, `lentra.rent.ranking.*`, `lentra.services.ranking_service` (until formally scoped) |
| RiskEngineV2 & risk variants | `lentra.core.market_intelligence.risk.risk_engine_v2`, `risk.risk_engine`, `risk.risk_adapter`, `risk.*_risk_engine`, `engines.risk` (EngineV3 variant) |
| Duplicate Decision layers | `lentra.core.market_intelligence.decision_layer` (flat), `decision.ai_decision_engine` |
| Duplicate MI/market/dedup | `market_intelligence.market_intelligence_engine` (flat + engines copy), `pricing.market_service`, `dedup.dedup_engine`, `dedup.unified_dedup_engine`, `engines.dedup` |
| Root legacy runtime trees | any import resolving to root-level `/opt/lentra/{core,bot,api,worker,services,kernel,runtime}` (outside `infra/lentra`) |
| Declared-legacy subtrees | `lentra.rent.*`, `lentra.domain.*`, `lentra.pipeline.*`, `lentra.application.*`, `lentra.ranking.*`, `lentra.property.*` |

Note: deny rules must be droppable in sync with deletion batches — once a
legacy module is deleted (Manifest batches B–D), its deny entry becomes a
tombstone that prevents reintroduction under the same path.

---

## 4. Required arch_lock Checks

| ID | Name | Validates | Fails when |
|---|---|---|---|
| CHECK-001 | Single pipeline enforcement | INV-1 | A second module defines a production pipeline class, or any module other than the two allowed consumers imports `SearchPipeline` directly |
| CHECK-002 | Single gateway enforcement | INV-2 | Any `build_gateway*` besides `build_gateway_v3` is imported from production code, or `build_gateway_v3` gains a caller other than `api/pipeline/search_pipeline.py` |
| CHECK-003 | Canonical engine ownership | INV-3 | A responsibility (market truth, area, MI, risk, dedup, ranking, decision) resolves to a non-canonical module anywhere on the production import graph |
| CHECK-004 | Legacy import blocking | §3 deny list | Any production module imports a denied path (directly or transitively) |
| CHECK-005 | Ranking authority protection | UnifiedRankingEngine as sole external ranking authority | Any production module other than `search_pipeline.py` imports a ranking engine; or any ranking implementation outside `ranking/` is reachable from production |
| CHECK-006 | Risk veto protection | Binding veto (Constitution §6.3, §11.5) | RiskEngine is removed from the pipeline/gateway wiring; DecisionLayer stops consuming risk verdicts; or a presentation/delivery module reorders or filters around vetoed objects |

Check output contract: each check reports `PASS`/`FAIL` with the offending
import edge or module path. In blocking mode any `FAIL` is fatal.

---

## 5. Migration Phases

### Phase 1 — Document only (current phase)

- This plan + the four source-of-truth documents committed together.
- No behavior change: runner still `ExecStartPre=-` (non-blocking),
  `rules_v1.json`, `v2_rules.py`, `SEAL.json` untouched.
- Exit criterion: documents reviewed and committed.

### Phase 2 — Update rules

- Rewrite `rules_v1.json` (or introduce the successor consumed by the
  governor): remove the defective `NO_API_TO_CORE_BACKFLOW`, add the §3 deny
  list and §2 direction invariant; encode CHECK-001…006.
- Retire `v2_rules.py` entries that seal the legacy IntelligenceGateway
  contour.
- Re-seal `SEAL.json` against the canonical graph **after** the rules pass on
  the current production spine (first change allowed to touch SEAL.json).
- Runner remains non-blocking (`-` prefix stays); violations are logged only.
- Exit criterion: all six checks PASS on the live tree; legacy violations
  produce warnings matching the cleanup plan inventory exactly (no false
  positives on the spine).

### Phase 3 — CI enforcement

- Run the same checks in CI / pre-commit (repo already has `.githooks/`).
- New violations block merges; pre-existing inventoried legacy is
  grandfathered via an explicit baseline file that shrinks with each
  deletion batch and may never grow.
- Exit criterion: one full deletion batch (Manifest batch A or B) lands with
  CI green and baseline reduced.

### Phase 4 — Blocking production startup

- Remove the `-` prefix from `ExecStartPre` in `lentra-bot.service` (and the
  worker unit once fixed): an arch_lock FAIL now blocks service start.
- Enable the v2 runner path or fold it into v1 — one runner, one rule set.
- Precondition: Phases 2–3 stable for an agreed soak period and Manifest
  batches A–B completed (so no known-legacy noise can block a restart).
- Exit criterion: services restart cleanly with blocking gate active.

Phase order is strict; each phase requires the previous one's exit criterion.
Phases 2–4 each require an ADR (Constitution §10).

---

## 6. Rollback Strategy

Per-phase, smallest-step-back first:

| Phase | Rollback action | Blast radius |
|---|---|---|
| 2 (rules) | `git revert` the rules/SEAL commit; runner is still non-blocking, so a bad rule set only produces log noise — zero runtime impact | none |
| 3 (CI) | Disable the CI job / hook; merges proceed as before. Baseline file is kept so re-enabling resumes where it stopped | dev workflow only |
| 4 (startup gate) | Restore the `-` prefix on `ExecStartPre` (one-line unit edit + `daemon-reload`); services start regardless of gate verdict. If the unit edit itself is suspect, previous unit file is restored from the git-tagged checkpoint | minutes of degraded enforcement, no downtime — gate is ExecStartPre, not the service itself |

Standing safeguards:

- A git tag is created before each phase transition (same discipline as the
  deletion manifest batches).
- `SEAL.json` re-seal keeps the prior seal as a versioned backup
  (`backup_manager.py` already exists in arch_lock for this purpose); the
  boot seal check can be pointed back at the previous seal in one commit.
- The gate must never be "fixed forward" during an incident: rollback first,
  diagnose offline. arch_lock is enforcement, not availability-critical
  logic, and must never keep the API/bot down for architecture reasons other
  than a genuine forbidden-flow regression.
- Rollback of enforcement never rolls back documents: constitution and maps
  stay authoritative even while a phase is reverted.
