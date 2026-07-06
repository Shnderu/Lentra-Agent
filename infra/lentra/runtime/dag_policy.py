

RULES = {
    "core": {
        "forbid": ["runtime", "api.worker", "api.bot"]
    },
    "runtime": {
        "forbid": ["api"]
    },
    "api": {
        "forbid": []
    }
}


def check_policy(graph: dict):
    for src, deps in graph.items():
        for dep in deps:
            for layer, rules in RULES.items():
                if layer in src:
                    for forbidden in rules["forbid"]:
                        if forbidden in dep:
                            raise RuntimeError(
                                f"[ARCH POLICY VIOLATION] {src} -> {dep}"
                            )
