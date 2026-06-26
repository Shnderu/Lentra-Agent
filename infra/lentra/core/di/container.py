from lentra.core.gateway.flow_glue import FlowGlue

from lentra.core.scenario.policy import build_scenario_policy_engine
from lentra.core.intent.router import build_intent_resolver


def build_container():
    """
    CLEAN DI CONTAINER (FLOW-GLUE ONLY)
    """

    intent_resolver = build_intent_resolver()

    scenario_policy_engine = build_scenario_policy_engine({})

    flow_glue = FlowGlue(
        intent_resolver=intent_resolver,
        scenario_policy_engine=scenario_policy_engine
    )

    return {
        "flow_glue": flow_glue,
        "intent_resolver": intent_resolver,
        "scenario_policy_engine": scenario_policy_engine,
    }
