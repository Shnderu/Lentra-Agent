import hashlib
import re


def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9а-я\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def make_canonical_key(title: str, price: float, city: str) -> str:
    """
    Lightweight deterministic dedup key (MVP)
    """

    base = f"{normalize_text(title)}|{city.lower()}"

    # price bucket (stable grouping)
    price_bucket = int(price // 50) * 50 if price else 0

    raw = f"{base}|{price_bucket}"

    return hashlib.sha256(raw.encode()).hexdigest()


def is_probable_duplicate(a: dict, b: dict) -> bool:
    """
    Heuristic dedup check (MVP stage)
    """

    if not a or not b:
        return False

    if a.get("city") != b.get("city"):
        return False

    price_a = float(a.get("price") or 0)
    price_b = float(b.get("price") or 0)

    if abs(price_a - price_b) > 100:
        return False

    title_a = normalize_text(a.get("title", ""))
    title_b = normalize_text(b.get("title", ""))

    # simple overlap heuristic
    overlap = len(set(title_a.split()) & set(title_b.split()))

    return overlap >= 3
