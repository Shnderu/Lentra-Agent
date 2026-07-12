# ADR: Arch Lock Rule Migration v1 — Align enforcement with canonical architecture

- **Status:** PROPOSED (awaiting approval — see §5)
- **Date:** 2026-07-12
- **Deciders:** Lentra architecture owner
- **Governed by:** `ARCHITECTURE_CONSTITUTION.md` §10 (ADR required for enforcement changes)
- **Inputs:** `ARCH_LOCK_MIGRATION_PLAN.md`, `CANONICAL_COMPONENT_MAP.md`, `ARCHITECTURE_CLEANUP_PLAN.md`, `ARCHITECTURE_DELETION_MANIFEST.md`
- **Scope of this ADR:** decision record only. No changes to `rules_v1.json`, `v2_rules.py`, `SEAL.json`, Python code, or systemd units are made by this document.

---

## 1. Context

1. The live Arch Lock (`lentra/runtime/arch_lock/`, runner v1.6 via
   `ExecStartPre=-`) enforces the **old architecture graph**, not the
   canonical architecture. Its rules predate the consolidation fixed in the
   Constitution and the Component Map.

2. Rule `NO_API_TO_CORE_BACKFLOW` (`rules_v1.json`) denies
   `lentra.api -> lentra.core`. This **directly conflicts with the canonical
   pipeline**: the single production entrypoint
   `api/pipeline/search_pipeline.py` legitimately imports
   `lentra.core.market_intelligence.*` and
   `lentra.runtime.bootstrap.gateway_v3` — that import path IS the canonical
   flow (Constitution §3). Under the current rules the production spine is a
   violation, which is why the runner can only run in ignore-failures mode.
   Enforcement cannot be strengthened before it is migrated.

3. `v2_rules.py` seals internals of the **legacy IntelligenceGateway
   contour** (`gateway.internal`, `core.bootstrap`) — it protects components
   the Constitution forbids (§11.1) and the Deletion Manifest schedules for
   removal. Both rule sets guard the wrong architecture.

4. `SEAL.json` is a **snapshot of the old import graph**, captured before
   consolidation. It encodes history, not the constitution: legacy trees are
   inside the seal, so deleting legacy reads as drift while the seal
   simultaneously legitimizes it. The seal must be regenerated — but only
   after the rules are migrated (Phase 3, not now).

---

## 2. Decision

Migrate the Arch Lock rule set from graph-history protection to
constitutional-invariant protection.

### REMOVE

| Rule | Location | Reason |
|---|---|---|
| `NO_API_TO_CORE_BACKFLOW` | `rules_v1.json` | Declares the canonical spine a violation (§1.2). Blocks any move to blocking enforcement. |
| `NO_CORE_TO_GATEWAY_INTERNAL` | `v2_rules.py` | Seals internals of the legacy IntelligenceGateway contour; the contour itself is forbidden (Constitution §11.1) and scheduled for removal. |
| `NO_BYPASS_INTELLIGENCE` | `v2_rules.py` | Seals `lentra.core.bootstrap` — a module of the old contour, outside the canonical flow. Protects legacy, not canon. |

### RESCOPE

Replace protection of **legacy internals** with prohibition of the **legacy
contour as a whole**:

- `NO_RUNTIME_IMPORT_IN_CORE` / `NO_CROSS_MARKET_INTELLIGENCE_TO_RUNTIME` →
  one upward-import rule: intelligence (`lentra.core.*`) never imports
  delivery or runtime layers (Constitution §7.2, §11.7).
- `NO_RUNTIME_TO_CORE` (v2) is inverted relative to reality —
  `gateway_v3.py` must import canonical engines from core (Map §4). Rescope
  to: GatewayV3 imports canonical modules only.

### ADD

| New rule | Enforces | Constitutional basis |
|---|---|---|
| Single canonical pipeline | Only `api/pipeline/search_pipeline.py` defines the production pipeline; only the singleton `__init__` and the `CanonicalSearchPipeline` facade may import it | §3, §11.1 (CHECK-001) |
| Legacy import prohibition | Deny list from `ARCH_LOCK_MIGRATION_PLAN.md` §3: legacy pipelines, IntelligenceGateway contour, old gateway builders, legacy subtrees, root trees. Entries persist as tombstones after deletion | §8.1 (CHECK-004) |
| Duplicate intelligence core prohibition | Exactly one canonical module per responsibility (MarketService, AreaEngine, MIE, RiskEngine, DedupEngine, UnifiedRankingEngine, DecisionLayer — paths per Map §4); competing implementations in the production graph fail | §9.1 (CHECK-003) |
| Ranking duplication prohibition | `UnifiedRankingEngine` is the sole external ranking authority; `MarketRankingEngine` reachable only through it | §11.4 (CHECK-005) |
| Decision bypass prohibition | `DecisionLayer` is the last reasoning step; risk veto binding; no delivery/presentation module re-ranks, re-filters, or re-decides after it | §6.3, §6.6, §11.5 (CHECK-006) |

Companion single-gateway rule (CHECK-002) is included in the same rule-set
change, per the Migration Plan: `build_gateway_v3` keeps exactly one caller.

Ordering constraint: `NO_API_TO_CORE_BACKFLOW` is removed **in the same
change** that adds the single-pipeline/single-gateway rules — no window
without spine protection. The two v2 seals are removed only together with
the legacy import prohibition, which is strictly stronger.

---

## 3. Migration Order

| Phase | Content | Gate |
|---|---|---|
| **Phase 1 — documents** | Constitution, Component Map, Cleanup Plan, Deletion Manifest, Migration Plan, this ADR. No behavior change. | Documents reviewed; this ADR approved |
| **Phase 2 — rules migration** | Apply REMOVE / RESCOPE / ADD above to the rule set consumed by the governor. Runner stays non-blocking; violations logged only. Expected legacy hits must match Cleanup Plan §2–3 one-to-one; a mismatch is a rule defect, not a code defect | All checks pass on the live tree with zero false positives on the spine |
| **Phase 3 — SEAL regeneration** | Re-seal `SEAL.json` against the canonical graph; previous seal kept as versioned backup (existing `backup_manager.py`) | Boot seal check green against the new seal |
| **Phase 4 — blocking enforcement** | Remove `-` from `ExecStartPre`; arch_lock FAIL blocks service start. CI/pre-commit runs the same checks | Phases 2–3 stable over soak period; Deletion Manifest batches A–B completed |

Each phase transition is a separate change with its own git tag.

---

## 4. Safety Constraints

1. **Runner remains non-blocking** through Phases 1–3 (`ExecStartPre=-`
   preserved). Blocking mode is exclusively Phase 4 and has its own
   preconditions.
2. **Production spine protected:** nothing on the import path
   `api.main → search_pipeline → gateway_v3 → engines → ranking → decision`
   is edited by this migration (DO-NOT-TOUCH list:
   `ARCHITECTURE_CLEANUP_PLAN.md` §5, Map §8). Rule changes must produce
   zero violations against the spine before they ship.
3. **Rollback via git tag:** a tag is created before each phase; rollback is
   `git revert` / tag restore. In Phase 4 the additional one-line rollback
   is restoring the `-` prefix (+ `daemon-reload`). Rollback of enforcement
   never rolls back the documents. The gate is never "fixed forward" during
   an incident: revert first, diagnose offline.
4. Arch Lock is enforcement, not availability-critical logic: it must never
   keep the API/bot down for any reason other than a genuine forbidden-flow
   regression.
5. `SEAL.json` is untouched until Phase 3, and its regeneration always keeps
   the prior seal restorable in one commit.

---

## 5. Approval

- Per Constitution §10, **this ADR must be approved before any rule change
  is made.** No modification of `rules_v1.json`, `v2_rules.py`, or
  `SEAL.json` may land while this ADR is in PROPOSED status.
- Approval scope: Phases 2–4 as specified here. Any deviation (new rules,
  changed deny lists, reordered phases) requires a superseding ADR
  (`ADR_ARCH_LOCK_RULE_MIGRATION_V2`).
- On approval: set Status to ACCEPTED with date and approver; the Phase 2
  implementation change must reference this ADR in its commit message.
- On rejection: set Status to REJECTED; the current (non-blocking, legacy)
  rule set remains in force and no enforcement work proceeds.
