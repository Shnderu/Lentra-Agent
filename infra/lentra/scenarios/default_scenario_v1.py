from lentra.scenarios.registry import scenario_registry


def default_scenario_v1(state: dict):
    """
    Fallback сценарий для неизвестных intent.
    Должен всегда возвращать валидный state.
    """

    return {
        "intent": state.get("intent", {"name": "unknown"}),
        "result": {
            "type": "fallback",
            "message": "No matching scenario found",
            "data": state.get("data", {})
        },
        "next": None
    }


# регистрация сценария
scenario_registry.register("default_scenario_v1", default_scenario_v1)
