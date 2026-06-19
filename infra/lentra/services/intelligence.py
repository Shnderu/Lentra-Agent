from lentra.core.router.intent_router import router
from lentra.services.pipeline_definition import build_pipeline


def handle_request(payload: dict):
    intent = router.route(payload)

    pipeline = build_pipeline(intent)

    return {
        "intent": intent.name,
        "scenario": intent.scenario,
        "result": pipeline.execute(intent.payload)
    }
