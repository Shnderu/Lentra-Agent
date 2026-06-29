class ScenarioAdapter:
    """
    Приводит function-based сценарии к interface:
    handler.execute(state)
    """

    def __init__(self, fn):
        self.fn = fn

    def execute(self, state: dict):
        return self.fn(state)
