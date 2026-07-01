from lentra.runtime.intelligence_gateway import interpret


def risk_fallback(item: dict):
    return interpret({
        "task": "risk_fallback",
        "item": item
    })
