from lentra.scenarios.registry import scenario_registry

def assert_scenarios():
    # do NOT assume internal structure
    try:
        test = scenario_registry.get("rent_scenario_v1")
    except Exception as e:
        raise RuntimeError(f"Scenario registry broken: {e}")

    if test is None:
        raise RuntimeError("rent_scenario_v1 is NOT registered")

    return True
