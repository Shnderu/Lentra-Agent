# ============================================================
# SOURCE REPUTATION SCORING V16.3
# ============================================================

SOURCE_WEIGHTS = {
    "airbnb": 0.95,
    "local_board": 0.80,
    "scraper": 0.65,
}


def get_source_score(source: str) -> float:
    return SOURCE_WEIGHTS.get(source, 0.5) * 100
