RULES_V2 = {
    "NO_RUNTIME_TO_CORE": {
        "deny_prefix": "lentra.runtime",
        "message": "runtime cannot depend on core intelligence layer"
    },
    "NO_CORE_TO_GATEWAY_INTERNAL": {
        "deny_prefix": "lentra.core.market_intelligence.gateway.internal",
        "message": "internal gateway is sealed"
    },
    "NO_BYPASS_INTELLIGENCE": {
        "deny_prefix": "lentra.core.bootstrap",
        "message": "bootstrap is sealed after initialization"
    }
}
