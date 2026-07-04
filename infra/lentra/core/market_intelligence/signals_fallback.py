def build_signals(data: dict) -> dict:
    return {
        "pricing": data.get("price", {}),
        "area": {"score": 0.5},
        "dedup": data.get("dedup", {}),
        "coupling": {"score": 0.0},
        "risk": data.get("risk", {})
    }
