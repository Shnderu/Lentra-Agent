from lentra.core.scenario.bootstrap import bootstrap_scenarios
from lentra.core.graph.state_runtime_v1 import state_graph_runtime


class Pipeline:

    def __init__(self):
        self.registry = None

    def _ensure_scenarios_loaded(self):
        # единая точка загрузки сценариев
        self.registry = bootstrap_scenarios()

    def execute(self, intent):
        self._ensure_scenarios_loaded()
        return state_graph_runtime.execute(intent)


pipeline = Pipeline()
