class FlowGlue:
    """
    Unified orchestration layer (SINGLE CONTRACT)
    """

    def __init__(self, intent_resolver, scenario_policy_engine):
        self.intent_resolver = intent_resolver
        self.scenario_policy_engine = scenario_policy_engine

    def run(self, flow):
        intent = self.intent_resolver.resolve(flow)

        scenario = self.scenario_policy_engine.select(
            intent=intent,
            user_input=flow
        )

        return self.scenario_policy_engine.run(scenario, flow)
