from lentra.core.contracts.v1 import FlowV1


class FlowGlue:

    def __init__(self, intent_resolver, scenario_engine):
        self.intent_resolver = intent_resolver
        self.scenario_engine = scenario_engine

    def run(self, flow: FlowV1):
        intent = self.intent_resolver.resolve(flow)

        scenario = self.scenario_engine.select(
            intent=intent,
            flow=flow
        )

        return self.scenario_engine.run(scenario, flow)
