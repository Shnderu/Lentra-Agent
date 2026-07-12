RULES_V2 = {
    "NO_LEGACY_GATEWAY_CONTOUR": {
        "deny_prefix": "lentra.core.market_intelligence.gateway",
        "message": "IntelligenceGateway contour is legacy; the only router is runtime.bootstrap.gateway_v3 (ADR_ARCH_LOCK_RULE_MIGRATION_V1)"
    },
    "NO_LEGACY_BOOTSTRAP_CONTOUR": {
        "deny_prefix": "lentra.core.bootstrap",
        "message": "legacy bootstrap contour is forbidden; canonical wiring is build_gateway_v3 (ADR_ARCH_LOCK_RULE_MIGRATION_V1)"
    },
    "NO_LEGACY_GATEWAY_BUILDERS": {
        "deny_prefix": "lentra.runtime.bootstrap.wiring",
        "message": "legacy gateway builders (wiring, wiring_safe) are forbidden; only build_gateway_v3 is canonical (ADR_ARCH_LOCK_RULE_MIGRATION_V1)"
    }
}

# Removed by ADR_ARCH_LOCK_RULE_MIGRATION_V1 (Phase 2):
# - NO_RUNTIME_TO_CORE: inverted relative to reality — gateway_v3 (runtime)
#   MUST import canonical engines from core (CANONICAL_COMPONENT_MAP.md §4).
# - NO_CORE_TO_GATEWAY_INTERNAL: sealed internals of the legacy
#   IntelligenceGateway contour; the contour itself is forbidden, superseded
#   by NO_LEGACY_GATEWAY_CONTOUR.
# - NO_BYPASS_INTELLIGENCE: sealed lentra.core.bootstrap as protected legacy;
#   superseded by NO_LEGACY_BOOTSTRAP_CONTOUR (same prefix, meaning flipped
#   from "sealed, protected" to "legacy, forbidden").
