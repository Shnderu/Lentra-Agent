from lentra.core.scenario.registry import scenario_registry


def print_registry_state():
    print("[SCENARIO REGISTRY]", scenario_registry.all())


print_registry_state()
