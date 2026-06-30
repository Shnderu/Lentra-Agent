class Orchestrator:
    """
    Minimal execution orchestrator (TRACE v2 fix)
    """

    def __init__(self, steps=None):
        self.steps = steps or []

    def execute(self, payload: dict):
        result = payload

        for step in self.steps:
            if hasattr(step, "run"):
                result = step.run(result)

        return result
