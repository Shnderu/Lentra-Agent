FORBIDDEN_PATTERNS = [
    "EngineRegistryV2",
    "EngineRegistryV3",
    "EngineRegistryV4",
    "GraphEngine",
    "DAGEngine",
    "WorkflowEngine",
    "OrchestratorV2",
]

FORBIDDEN_PATHS = [
    "graph_v2/",
    "graph_v3/",
    "engine_registry_v2",
]


def check_diff(diff: str) -> list[str]:
    violations = []

    for p in FORBIDDEN_PATTERNS:
        if p in diff:
            violations.append(f"FORBIDDEN_PATTERN: {p}")

    for path in FORBIDDEN_PATHS:
        if path in diff:
            violations.append(f"FORBIDDEN_PATH: {path}")

    return violations
