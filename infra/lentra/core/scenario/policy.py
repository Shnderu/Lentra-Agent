from lentra.core.scenario.scenario_policy_engine import ScenarioPolicyEngine


def build_scenario_policy_engine(registry: dict = None):
    registry = registry or {}

    return ScenarioPolicyEngine(registry)
