import time


def freshness_score(prop):
    """
    Newer listings rank higher
    """
    ts = prop.get("created_at")

    if not ts:
        return 0.0

    age_hours = (time.time() - ts) / 3600

    if age_hours < 24:
        return 0.5
    if age_hours < 72:
        return 0.3
    if age_hours < 168:
        return 0.1

    return 0.0
