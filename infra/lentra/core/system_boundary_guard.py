FORBIDDEN_IMPORTS = [
    "app.core.intent",
    "app.core.scenario",
    "app.core.gateway",
]


def assert_no_legacy_imports(module_name: str):
    for bad in FORBIDDEN_IMPORTS:
        if module_name.startswith(bad):
            raise ImportError(f"Legacy import forbidden: {module_name}")
