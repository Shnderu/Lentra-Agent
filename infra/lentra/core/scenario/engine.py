from lentra.core.scenario.scenario_engine import ScenarioEngine


class ScenarioEngineV1:
    """
    Thin wrapper for compatibility.
    """

    def __init__(self):
        self.engine = ScenarioEngine()

    def resolve(self, intent: str, context=None):
        return self.engine.resolve(intent=intent, context=context)
