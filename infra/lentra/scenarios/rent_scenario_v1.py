from lentra.scenarios.registry import scenario_registry

print("[SCENARIO LOAD] rent_scenario_v1 importing")

def rent_scenario_v1(state):
    return type("Result", (), {
        "data": {"rent": True},
        "next": []
    })

print("[SCENARIO LOAD] registering rent_scenario_v1")

scenario_registry.register("rent_scenario_v1", rent_scenario_v1)

print("[SCENARIO LOAD] registered rent_scenario_v1 OK")
