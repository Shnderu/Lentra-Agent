from lentra.scenarios.registry import scenario_registry


def rent_scenario_v1(state):

    return {
        "rent_analyzed": True,
        "processed_intent": state.intent.get("name"),
        "payload": state.intent.get("payload"),
        "next": ["pricing_scenario_v1"]
    }


scenario_registry.register(
    "rent_scenario_v1",
    rent_scenario_v1
)
