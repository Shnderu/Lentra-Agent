from lentra.core.contracts.v1 import ScenarioV1, IntentV1, FlowV1


class ScenarioPolicyEngine:
    """
    DOMAIN LAYER v2

    Отвечает только за:
    - выбор сценария
    - запуск сценария

    ❌ НЕ делает классификацию
    ❌ НЕ знает про parsing текста
    """

    def select(self, intent: IntentV1, flow: FlowV1) -> ScenarioV1:
        intent_type = intent.type

        if intent_type == "search":
            return ScenarioV1(
                name="search_scenario",
                handler="lentra.scenarios.search.handler",
                params={}
            )

        if intent_type == "question":
            return ScenarioV1(
                name="qa_scenario",
                handler="lentra.scenarios.qa.handler",
                params={}
            )

        if intent_type == "command":
            return ScenarioV1(
                name="command_scenario",
                handler="lentra.scenarios.command.handler",
                params={}
            )

        return ScenarioV1(
            name="fallback_scenario",
            handler="lentra.scenarios.fallback.handler",
            params={}
        )

    def run(self, scenario: ScenarioV1, flow: FlowV1):
        # В v2 пока заглушка исполнения сценариев
        handler_path = scenario.handler

        return {
            "status": "ok",
            "scenario": scenario.name,
            "handler": handler_path,
            "input": flow.text
        }
