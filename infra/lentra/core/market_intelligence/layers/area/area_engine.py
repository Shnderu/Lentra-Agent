

AREA_PROFILE = {
    "My Khe": {
        "internet": 9.2,
        "noise": 5.1,
        "expats": 8.8,
        "safety": 8.5
    },
    "default": {
        "internet": 6.0,
        "noise": 5.0,
        "expats": 5.0,
        "safety": 6.0
    }
}


def get_area_score(location: str) -> dict:
    return AREA_PROFILE.get(location, AREA_PROFILE["default"])


def compute_area_quality(location: str) -> float:
    score = get_area_score(location)
    return round(
        (score["internet"] * 0.4 +
         (10 - score["noise"]) * 0.2 +
         score["expats"] * 0.2 +
         score["safety"] * 0.2),
        2
    )
