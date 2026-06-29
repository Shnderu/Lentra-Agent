from lentra.services.pipeline_definition import pipeline
from lentra.core.contract.intent_normalizer import normalize_intent


def handle_request(payload: dict):

    intent = payload.get("intent")

    if not intent:
        intent = {
            "name": "unknown",
            "confidence": 0.3,
            "payload": payload,
            "scenarios": ["default_scenario_v1"]
        }

    intent = normalize_intent(intent)

    result = pipeline.execute(intent)

    return {
        "intent": intent["name"],
        "scenario": "ok",
        "result": result
    }
