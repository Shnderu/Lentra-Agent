from lentra.scenarios.registry import scenario_registry


def bootstrap_scenarios():
    """
    SAFE BOOTSTRAP:
    - NO scenario imports here
    - NO service imports here
    - ONLY ensures registry is accessible
    """

    # Lazy import scenarios ONLY when module is loaded safely
    import lentra.scenarios.default_scenario_v1  # noqa
    import lentra.scenarios.rent_scenario_v1     # noqa

    # validation
    if not scenario_registry.list():
        raise RuntimeError("CRITICAL: scenario registry is empty")

    return scenario_registry.list()
