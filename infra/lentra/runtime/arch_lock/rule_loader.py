"""
ARCH LOCK Phase 3 rule loader (ADR_ARCH_LOCK_RULE_MIGRATION_V1).

Loads the declarative rule sets (rules_v1.json + v2_rules.RULES_V2),
validates their schema, and runs a DRY-RUN evaluation over the static
import graph of the `lentra` package.

Non-blocking by design: this module only logs. It never raises out of
dry_run(), never changes the governor verdict, and never touches SEAL.json.
"""

import ast
import json
import os

ARCH_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_V1_PATH = os.path.join(ARCH_DIR, "rules_v1.json")

KNOWN_TYPES = ("import_block", "require_imports", "allowed_importers")

# Canonical production spine (CANONICAL_COMPONENT_MAP.md §4/§8).
# A dry-run violation on any of these modules is a rule defect, not a code
# defect, and is reported separately as SPINE FALSE POSITIVE.
SPINE_MODULES = {
    "lentra.api.main",
    "lentra.api.pipeline",
    "lentra.api.pipeline.search_pipeline",
    "lentra.api.routes.search",
    "lentra.api.routes.miniapp",
    "lentra.bot.main",
    "lentra.bot.handlers.handlers",
    "lentra.worker.recovery_worker",
    "lentra.core.pipeline.worker_search_entrypoint",
    "lentra.core.pipeline.canonical_search_pipeline",
    "lentra.runtime.bootstrap.gateway_v3",
    "lentra.core.market_intelligence.engines.market_intelligence_engine",
    "lentra.core.engines.area_engine",
    "lentra.core.engines.base_engine",
    "lentra.core.market_intelligence.market.market_service",
    "lentra.core.market_intelligence.engines.risk_engine",
    "lentra.core.market_intelligence.engines.dedup_engine",
    "lentra.core.market_intelligence.dedup.dedup_index",
    "lentra.core.market_intelligence.ranking.unified_ranking_engine",
    "lentra.core.market_intelligence.ranking.ranking_engine",
    "lentra.core.market_intelligence.decision.decision_layer",
}

MAX_LOGGED_PER_RULE = 1000


# ---------------------------------------------------------------- loading

def load_v1_rules():
    """Load rules_v1.json. Returns (rules, errors)."""
    errors = []
    try:
        with open(RULES_V1_PATH, "r") as f:
            data = json.load(f)
    except Exception as e:
        return [], ["rules_v1.json unreadable: %r" % e]

    rules = data.get("rules")
    if not isinstance(rules, list):
        return [], ["rules_v1.json: 'rules' must be a list"]
    return rules, errors


def load_v2_rules():
    """Convert v2_rules.RULES_V2 entries into import_block rules."""
    errors = []
    try:
        from lentra.runtime.arch_lock.v2_rules import RULES_V2
    except Exception as e:
        return [], ["v2_rules import failed: %r" % e]

    rules = []
    for rule_id, spec in RULES_V2.items():
        prefix = spec.get("deny_prefix")
        if not prefix:
            errors.append("RULES_V2[%s]: missing deny_prefix" % rule_id)
            continue
        rules.append({
            "id": rule_id,
            "type": "import_block",
            "deny_prefixes": [prefix],
            "scope": ["lentra."],
            "match": "prefix",  # historical v2 semantics: plain startswith
            "message": spec.get("message", ""),
        })
    return rules, errors


def validate_rules(rules):
    """Schema validation. Returns (valid_rules, errors, skipped)."""
    valid, errors, skipped = [], [], []
    for i, rule in enumerate(rules):
        rid = rule.get("id") or ("<rule[%d]>" % i)
        rtype = rule.get("type")
        if rtype not in KNOWN_TYPES:
            skipped.append("%s: unknown type %r (skipped, not fatal)" % (rid, rtype))
            continue
        if rtype == "import_block":
            if not rule.get("deny_prefixes") or not rule.get("scope"):
                errors.append("%s: import_block needs deny_prefixes + scope" % rid)
                continue
        if rtype == "allowed_importers":
            if not rule.get("target") or not isinstance(rule.get("allow"), list):
                errors.append("%s: allowed_importers needs target + allow" % rid)
                continue
        if rtype == "require_imports":
            has_direct = rule.get("module") and rule.get("require")
            has_wiring = isinstance(rule.get("pipeline_wiring"), dict)
            if not has_direct and not has_wiring:
                errors.append("%s: require_imports needs module+require or pipeline_wiring" % rid)
                continue
        valid.append(rule)
        # nested allowed_importers under "also" are validated recursively
        for j, sub in enumerate(rule.get("also", []) or []):
            sub = dict(sub)
            sub.setdefault("id", "%s.also[%d]" % (rid, j))
            sub_valid, sub_err, sub_skip = validate_rules([sub])
            valid.extend(sub_valid)
            errors.extend(sub_err)
            skipped.extend(sub_skip)
    return valid, errors, skipped


# ------------------------------------------------------------ import graph

def _module_name(py_path, package_root):
    rel = os.path.relpath(py_path, os.path.dirname(package_root))
    parts = rel[:-3].split(os.sep)  # strip .py
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _resolve_relative(module_name, is_pkg, node):
    base = module_name.split(".") if is_pkg else module_name.split(".")[:-1]
    if node.level > 1:
        base = base[: len(base) - (node.level - 1)]
    if node.module:
        return ".".join(base + node.module.split("."))
    return ".".join(base)


def build_import_graph(project_root):
    """module name -> set of imported module names (lentra.* only)."""
    package_root = os.path.join(project_root, "lentra")
    graph = {}
    for dirpath, dirnames, filenames in os.walk(package_root):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(dirpath, fn)
            mod = _module_name(path, package_root)
            try:
                with open(path, "r", errors="replace") as f:
                    tree = ast.parse(f.read())
            except Exception:
                continue  # unparsable files are out of dry-run scope
            imports = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for a in node.names:
                        imports.add(a.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.level:
                        imports.add(_resolve_relative(mod, fn == "__init__.py", node))
                    elif node.module:
                        imports.add(node.module)
            graph[mod] = {i for i in imports if i.startswith("lentra")}
    return graph


# -------------------------------------------------------------- evaluation

def _matches(name, pattern, mode="exact_or_dot"):
    if pattern.endswith("."):
        return name.startswith(pattern)
    if mode == "prefix":
        return name.startswith(pattern)
    return name == pattern or name.startswith(pattern + ".")


def evaluate(rules, graph):
    """Dry-run evaluation. Returns list of violation dicts."""
    violations = []
    for rule in rules:
        rid, rtype = rule["id"], rule["type"]
        mode = rule.get("match", "exact_or_dot")

        if rtype == "import_block":
            for mod, imports in graph.items():
                if not any(_matches(mod, s, "prefix") for s in rule["scope"]):
                    continue
                for imp in imports:
                    for deny in rule["deny_prefixes"]:
                        if _matches(imp, deny, mode):
                            violations.append(
                                {"rule": rid, "module": mod, "import": imp})

        elif rtype == "allowed_importers":
            target = rule["target"]
            allow = rule["allow"]
            for mod, imports in graph.items():
                if any(_matches(mod, a) for a in allow):
                    continue
                for imp in imports:
                    if _matches(imp, target, "prefix" if target.endswith(".") else mode):
                        violations.append(
                            {"rule": rid, "module": mod, "import": imp})

        elif rtype == "require_imports":
            checks = []
            if rule.get("module") and rule.get("require"):
                checks.append((rule["module"], rule["require"]))
            wiring = rule.get("pipeline_wiring")
            if isinstance(wiring, dict) and wiring.get("module"):
                checks.append((wiring["module"], wiring.get("must_wire", [])))
            for module, required in checks:
                imports = graph.get(module)
                if imports is None:
                    violations.append(
                        {"rule": rid, "module": module, "import": "<module missing>"})
                    continue
                for req in required:
                    if not any(_matches(imp, req) for imp in imports):
                        violations.append(
                            {"rule": rid, "module": module,
                             "import": "<missing required: %s>" % req})
            # require_inputs (e.g. risk_verdict) is a runtime contract,
            # not statically checkable here — noted, not evaluated.

    return violations


# ---------------------------------------------------------------- dry run

def dry_run(project_root="/opt/lentra/infra"):
    """
    Load + validate + evaluate, logging only.
    Never raises, never changes the gate verdict (Phase 2/3 non-blocking,
    ADR_ARCH_LOCK_RULE_MIGRATION_V1 §4).
    """
    try:
        v1, err1 = load_v1_rules()
        v2, err2 = load_v2_rules()
        rules, schema_errors, skipped = validate_rules(v1 + v2)
        for e in err1 + err2 + schema_errors:
            print("[ARCH LOCK dry-run] schema:", e)
        for s in skipped:
            print("[ARCH LOCK dry-run] schema:", s)

        graph = build_import_graph(project_root)
        violations = evaluate(rules, graph)

        spine_hits = [v for v in violations if v["module"] in SPINE_MODULES]
        legacy_hits = [v for v in violations if v["module"] not in SPINE_MODULES]

        print("[ARCH LOCK dry-run] rules loaded: %d (v1=%d, v2=%d, skipped=%d)"
              % (len(rules), len(v1), len(v2), len(skipped)))
        print("[ARCH LOCK dry-run] modules scanned: %d" % len(graph))
        print("[ARCH LOCK dry-run] violations: %d total, %d on legacy, %d on spine"
              % (len(violations), len(legacy_hits), len(spine_hits)))

        per_rule = {}
        for v in legacy_hits:
            per_rule.setdefault(v["rule"], []).append(v)
        for rid in sorted(per_rule):
            items = per_rule[rid]
            print("[ARCH LOCK dry-run]   %s: %d hit(s)" % (rid, len(items)))
            for v in items[:MAX_LOGGED_PER_RULE]:
                print("[ARCH LOCK dry-run]     %s -> %s" % (v["module"], v["import"]))
            if len(items) > MAX_LOGGED_PER_RULE:
                print("[ARCH LOCK dry-run]     ... and %d more"
                      % (len(items) - MAX_LOGGED_PER_RULE))

        if spine_hits:
            print("[ARCH LOCK dry-run] !! SPINE FALSE POSITIVE(S) — rule defect, fix rules:")
            for v in spine_hits:
                print("[ARCH LOCK dry-run]   %s: %s -> %s"
                      % (v["rule"], v["module"], v["import"]))
        else:
            print("[ARCH LOCK dry-run] SPINE CLEAN (no false positives on canonical spine)")

        return {"rules": len(rules), "violations": violations, "spine_hits": spine_hits}

    except Exception as e:  # dry-run must never break the gate
        print("[ARCH LOCK dry-run] internal error (non-blocking):", repr(e))
        return {"rules": 0, "violations": [], "spine_hits": [], "error": repr(e)}


if __name__ == "__main__":
    dry_run()
