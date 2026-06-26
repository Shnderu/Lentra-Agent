from typing import Dict, Any
from lentra.core.executor.dec_executor import DECExecutor


class ScenarioEngineV1:

    def __init__(self):
        self.executor = DECExecutor()

    def execute(self, scenario: str, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        ScenarioEngine теперь = thin adapter над DECExecutor
        """

        return self.executor.execute(scenario, user_input)
