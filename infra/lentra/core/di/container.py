from lentra.core.gateway.flow_glue import FlowGlue
from lentra.core.intent.intent_resolver import IntentResolver
from lentra.core.scenario.scenario_policy_engine import ScenarioPolicyEngine
from lentra.core.queue.task_queue_repository import TaskQueueRepository

def build_container():
    db = build_db()

    intent_resolver = IntentResolver()
    scenario_engine = ScenarioPolicyEngine()

    flow_glue = FlowGlue(
        intent_resolver=intent_resolver,
        scenario_policy_engine=scenario_engine
    )

    return {
        "task_queue": TaskQueueRepository(db),
        "flow_glue": flow_glue
    }
