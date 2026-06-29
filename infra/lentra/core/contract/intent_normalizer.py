def normalize_intent(intent: dict) -> dict:
    return {
        "name": intent.get("name", "unknown"),
        "confidence": intent.get("confidence", 0.3),
        "payload": intent.get("payload", intent),
        "scenarios": intent.get("scenarios", ["default_scenario_v1"])
    }
