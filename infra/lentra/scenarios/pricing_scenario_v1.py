from lentra.scenarios.registry import scenario_registry


def pricing_scenario_v1(state):

    return {
        "pricing_checked": True
    }


scenario_registry.register(
    "pricing_scenario_v1",
    pricing_scenario_v1
)
