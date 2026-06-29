from lentra.scenarios.registry import scenario_registry

def dump_registry():
    # try multiple possible internal shapes safely
    candidates = [
        "_store",
        "store",
        "scenarios",
        "_scenarios",
        "__dict__"
    ]

    result = {}

    for c in candidates:
        if hasattr(scenario_registry, c):
            try:
                result[c] = str(getattr(scenario_registry, c))
            except Exception as e:
                result[c] = f"ERR: {e}"

    return {
        "type": str(type(scenario_registry)),
        "dump": result
    }


if __name__ == "__main__":
    import json
    print(json.dumps(dump_registry(), indent=2))
