# Arch Lock Phase 3 — Soak Validation Report & Stability Checklist

- **Date of baseline:** 2026-07-12
- **ADR:** `ADR_ARCH_LOCK_RULE_MIGRATION_V1.md` (Phase 3: dry-run, log-only)
- **Mode:** NON-BLOCKING. Gate verdict and exit codes are unchanged; the
  declarative rules are evaluated in dry-run and only logged.
- **Not touched:** SEAL.json, production code, systemd, pipeline.
- This document is a report + checklist only.

---

## 1. Dry-Run Baseline (frozen reference)

Command: `venv-bot/bin/python -m lentra.runtime.arch_lock.arch_lock_runner`

| Metric | Value |
|---|---|
| Rules loaded | **11** (v1 = 6, v2 = 3 + 2 nested `also` checks; skipped = 0) |
| Modules scanned | **1286** |
| Total violations | **84** |
| Violations on canonical spine | **0 — SPINE CLEAN** |
| `require_imports` misses on spine (CANONICAL_SPINE_INTEGRITY / RISK_VETO_INTEGRITY) | **0** — gateway_v3 + risk/dedup/ranking/decision/market_service wiring confirmed statically |
| Gate exit code | **0** (non-blocking preserved) |

### 1.1 Violations by rule (baseline)

| Rule | Hits | Character |
|---|---|---|
| `LEGACY_INTELLIGENCE_ISOLATION` | 69 | Mostly *internal* edges of the legacy `bot/features/rent_search/` tree (~48), plus IntelligenceGateway contour, risk/dedup variants, `rent/domain` subtrees |
| `NO_LEGACY_GATEWAY_CONTOUR` | 8 | All importers of `market_intelligence.gateway.*` — matches Cleanup Plan inventory exactly |
| `NO_LEGACY_GATEWAY_BUILDERS` | 3 | `wiring_safe` importers: `api/pipeline_bootstrap`, `bootstrap/worker_main`, `bootstrap/graph_attach` |
| `NO_LEGACY_BOOTSTRAP_CONTOUR` | 1 | `core.bootstrap` package self-edge |
| `NO_DELIVERY_INTELLIGENCE` | 1 | `telegram.dispatcher -> market_intelligence.build` (telegram contour) |
| `RANKING_AUTHORITY` | 1 | dead `decision/ai_decision_engine` importing UnifiedRankingEngine |
| `CANONICAL_SPINE_INTEGRITY.also[0]` | 1 | `api/services/search_service` imports SearchPipeline outside the allow-list — legacy module (Cleanup Plan: outside production graph), NOT a spine false positive |

### 1.2 Baseline cross-check vs Cleanup Plan

All 84 hits fall inside the legacy inventory of
`ARCHITECTURE_CLEANUP_PLAN.md` §2–3 / `DELETION_MANIFEST` batches B–C.
No hit names a module from the DO-NOT-TOUCH list. **Discrepancies found: 0.**

Reproduce the full per-edge list at any time (read-only):

```bash
cd /opt/lentra/infra && venv-bot/bin/python - <<'PY'
from lentra.runtime.arch_lock.rule_loader import (load_v1_rules, load_v2_rules,
    validate_rules, build_import_graph, evaluate, SPINE_MODULES)
v1,_=load_v1_rules(); v2,_=load_v2_rules()
rules,_,_=validate_rules(v1+v2)
viol=evaluate(rules, build_import_graph("/opt/lentra/infra"))
print(len(viol), "violations,", sum(v['module'] in SPINE_MODULES for v in viol), "on spine")
for v in sorted(viol,key=lambda x:(x['rule'],x['module'])):
    print(f"{v['rule']}: {v['module']} -> {v['import']}")
PY
```

---

## 2. Soak Invariants (what "stable" means)

During the soak period, on every check the following must hold:

- **INV-A:** runner exit code = 0 (non-blocking preserved).
- **INV-B:** `SPINE CLEAN` — spine false positives = 0, always.
- **INV-C:** rules loaded = 11, skipped = 0 (loader parses both sources).
- **INV-D:** total violations ≤ 84. The count may only **decrease**
  (deletion batches) — any increase means a NEW forbidden import appeared
  and must be triaged as a regression.
- **INV-E:** no `<missing required>` entries for `CANONICAL_SPINE_INTEGRITY`
  or `RISK_VETO_INTEGRITY` (spine wiring intact).
- **INV-F:** services `lentra-api`, `lentra-bot`, `lentra-recovery` remain
  active; bot restarts are not delayed by the gate (dry-run adds only an
  AST scan of ~1286 modules to ExecStartPre).

---

## 3. Stability Checklist

### 3.1 Daily (or per deploy/restart) — ~1 minute

```bash
cd /opt/lentra/infra

# C1. Gate healthy, non-blocking
venv-bot/bin/python -m lentra.runtime.arch_lock.arch_lock_runner > /tmp/al.log 2>&1; echo "exit=$?"   # expect exit=0

# C2. Invariants B, C, D in one look
grep -E 'rules loaded|violations:|SPINE' /tmp/al.log
# expect: rules loaded: 11 (... skipped=0)
#         violations: <=84 total, ... 0 on spine
#         SPINE CLEAN

# C3. Services alive after any restart
systemctl is-active lentra-api lentra-bot lentra-recovery                       # expect: active x3

# C4. Gate did not slow bot startup materially
systemctl show lentra-bot -p ExecMainStartTimestamp
journalctl -u lentra-bot -n 20 --no-pager | grep -m1 'ARCH LOCK'
```

### 3.2 Per merge / weekly

```bash
# C5. Violation count trend (must be monotonically non-increasing)
venv-bot/bin/python -m lentra.runtime.arch_lock.arch_lock_runner 2>&1 \
  | grep 'violations:'    # log the number; compare with previous record

# C6. New-edge triage: if count > last recorded, diff the edge lists
#     (rerun the §1.2 script, diff vs saved baseline). Every new edge is
#     either (a) a regression to revert, or (b) a rule defect -> fix rules
#     via a superseding ADR, never by weakening the checker ad hoc.

# C7. Rules files untouched outside ADR flow
cd /opt/lentra && git status --short infra/lentra/runtime/arch_lock/
```

### 3.3 Exit criteria for the soak (gate to Phase 4)

All must be true, per ADR §3:

- [ ] Soak period elapsed (agreed duration; suggested ≥ 2 weeks of restarts/merges)
- [ ] INV-A…F held on every recorded check (no unexplained flips)
- [ ] Zero spine false positives for the entire period
- [ ] Violation count strictly decreased at least once via a completed
      Deletion Manifest batch (A and B done) — Phase 4 precondition, since
      blocking mode with 84 standing legacy hits would block every restart
- [ ] Baseline file of remaining grandfathered hits written and agreed
      (it may only shrink)
- [ ] CI/pre-commit runs the same dry-run and blocks NEW edges only
- [ ] Rollback rehearsed once: restore `-` semantics confirmed
      (currently trivial — dry-run is already non-blocking)

### 3.4 Known baseline notes (do not re-triage each time)

1. `api/services/search_service -> api.pipeline.search_pipeline` — legacy
   module outside the production graph importing the canonical pipeline;
   scheduled with the legacy pipeline path set (Cleanup Plan). Not a false
   positive; will disappear with its deletion batch.
2. ~48 of the 69 `LEGACY_INTELLIGENCE_ISOLATION` hits are legacy-to-legacy
   internal edges inside `bot/features/rent_search/` — they vanish wholesale
   when that tree is deleted (Manifest batch B), so expect a single large
   drop, not gradual decline.
3. `risk.risk_engine -> risk.risk_calibration_v1` is a legacy-internal edge;
   the canonical RiskEngine (`engines/risk_engine.py`) is unaffected.
4. The historical governor tuples and stub firewall remain in place and
   always return OK; the dry-run block is additive. This is expected until
   Phase 4 consolidates enforcement into one path.

---

## 4. Incident Playbook

| Symptom | Action |
|---|---|
| Runner exit ≠ 0 | This cannot come from dry-run (it never raises). Suspect the legacy gate path; check `journalctl -u lentra-bot`, restore arch_lock files from git if modified |
| SPINE FALSE POSITIVE appears | Rule defect by definition. Do not touch production code. Fix the rule under a superseding ADR; until then the finding is recorded but nothing blocks |
| Violations > 84 | New forbidden import merged. Identify the edge (§1.2 script diff), revert the offending change or file an ADR if it is intentionally architectural |
| Loader errors (`schema:` lines) | Rules file edited incorrectly; restore from git / `/tmp/arch_lock_backup_phase2/` and re-apply via ADR flow |
| Bot startup noticeably slower | Measure the dry-run duration alone (`venv-bot/bin/python -m lentra.runtime.arch_lock.rule_loader`); if material, move dry-run out of ExecStartPre into CI-only — allowed, it is log-only |

Rollback of the whole Phase 3: `git checkout -- infra/lentra/runtime/arch_lock/governor.py && rm infra/lentra/runtime/arch_lock/rule_loader.py` (dry-run detaches; rules files remain as inert declarations). Documents are never rolled back.
