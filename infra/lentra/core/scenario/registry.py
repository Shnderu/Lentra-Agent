from .default_scenario_v1 import run as default_scenario_v1

SCENARIOS = {
    "default_scenario_v1": default_scenario_v1
}


def get_scenario(name: str):
    return SCENARIOS.get(name)
