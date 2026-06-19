from typing import Any, Dict


class FlowGlue:
    """
    Minimal binding layer between:
    - Intent Router v1
    - Scenario Engine v1

    Purpose:
    Deterministic routing without expanding architecture.
    """

    def __init__(self, intent_router, scenario_engine):
        self.intent_router = intent_router
        self.scenario_engine = scenario_engine

    def resolve(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Single entrypoint:
        1. Resolve intent
        2. Select scenario
        3. Execute scenario flow

        Returns unified response contract.
        """

        intent = self.intent_router.classify(user_input)
        scenario = self.scenario_engine.select(intent, user_input)

        result = self.scenario_engine.execute(scenario, user_input)

        return {
            "intent": intent,
            "scenario": scenario,
            "result": result
        }
