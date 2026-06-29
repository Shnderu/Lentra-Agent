from lentra.core.scenario.registry import ScenarioRegistry


def bootstrap_scenarios():
    registry = ScenarioRegistry.instance()

    # ЯВНЫЕ ИМПОРТЫ (фикс side-effects)
    import lentra.scenarios.default_scenario_v1
    import lentra.scenarios.rent_scenario_v1
    import lentra.scenarios.pricing_scenario_v1

    return registry
