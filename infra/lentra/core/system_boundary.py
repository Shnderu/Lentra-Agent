ALLOWED_RUNTIME_IMPORTS = {
    "lentra.core.gateway",
    "lentra.core.intent",
    "lentra.core.scenario",
    "lentra.core.registry",
    "lentra.core.graph",
    "lentra.core.guards",
}


def is_allowed(module: str) -> bool:
    return any(module.startswith(p) for p in ALLOWED_RUNTIME_IMPORTS)


def assert_no_legacy_import(module: str):
    if module.startswith("app.core"):
        raise ImportError(
            "[SEAL] LEGACY LAYER IS DEPRECATED"
        )
