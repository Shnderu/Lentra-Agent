import re
from difflib import SequenceMatcher


def normalize(text: str) -> str:
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def similarity(a: str, b: str) -> float:
    """
    Lightweight fuzzy similarity (no external deps)
    """
    a = normalize(a)
    b = normalize(b)

    if not a or not b:
        return 0.0

    return SequenceMatcher(None, a, b).ratio()


def text_score(query: str, title: str) -> float:
    """
    Converts similarity into scoring boost
    """
    base = similarity(query, title)

    # nonlinear boost (emphasize high relevance)
    if base > 0.8:
        return 0.6
    if base > 0.6:
        return 0.4
    if base > 0.4:
        return 0.2

    return 0.0
