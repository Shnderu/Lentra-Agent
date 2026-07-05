"""
TASK NORMALIZATION ENGINE
=========================

Layer: Normalization Layer (Lentra)

Purpose:
    Convert a raw user task (natural language or partial dict) into a single,
    canonical structured format used downstream by the Market Intelligence and
    AI Decision layers.

Design principles:
    - Pure / stateless: no I/O, no globals, no side effects.
    - No external dependencies (stdlib only).
    - Deterministic and fully unit-testable.
    - Never raises on malformed / empty input (edge-case safe).

Public API:
    normalize_task(raw) -> dict
    NormalizedTask (dataclass, optional typed access)

Output format:
    {
        "location": str | None,
        "price_min": float | None,
        "price_max": float | None,
        "type": str | None,
        "duration": str | None,
        "constraints": [str, ...]
    }
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Union


# ---------------------------------------------------------------------------
# Canonical output container
# ---------------------------------------------------------------------------
@dataclass
class NormalizedTask:
    location: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    type: Optional[str] = None
    duration: Optional[str] = None
    constraints: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Lexicons (kept intentionally small and explicit; extend as needed)
# ---------------------------------------------------------------------------

# property type -> list of trigger keywords (ru + en)
_PROPERTY_TYPES: Dict[str, List[str]] = {
    "studio": ["студия", "студию", "студии", "studio"],
    "apartment": ["квартира", "квартиру", "квартиры", "апартаменты", "apartment", "flat"],
    "villa": ["вилла", "виллу", "виллы", "villa"],
    "house": ["дом", "house"],
    "room": ["комната", "комнату", "room"],
    "bungalow": ["бунгало", "bungalow"],
}

# constraint -> list of trigger keywords (ru + en)
_CONSTRAINTS: Dict[str, List[str]] = {
    "sea_view": ["возле моря", "у моря", "near sea", "sea view", "near the sea", "ocean", "beach"],
    "good_internet": ["хорошим интернетом", "хороший интернет", "интернет", "wifi", "wi-fi", "internet"],
    "pool": ["бассейн", "pool"],
    "pet_friendly": ["с животными", "питомц", "pet", "pets"],
    "parking": ["парковка", "паркинг", "parking"],
    "furnished": ["с мебелью", "меблированная", "furnished"],
    "quiet": ["тихий", "тихое", "quiet"],
    "gym": ["спортзал", "тренажерный", "gym"],
}

# currency symbols / codes used to make single-number budgets more robust
_CURRENCY_TOKENS = ["$", "usd", "долл", "€", "eur", "евро", "₫", "vnd", "донг", "฿", "thb", "бат"]

# duration keywords (ru + en)
_DURATION_PATTERNS = [
    (re.compile(r"(\d+)\s*(?:мес|month)", re.IGNORECASE), lambda m: f"{m.group(1)}m"),
    (re.compile(r"(\d+)\s*(?:нед|week)", re.IGNORECASE), lambda m: f"{m.group(1)}w"),
    (re.compile(r"(\d+)\s*(?:дн|day|дней|день|дня)", re.IGNORECASE), lambda m: f"{m.group(1)}d"),
    (re.compile(r"(\d+)\s*(?:год|year|лет|года)", re.IGNORECASE), lambda m: f"{m.group(1)}y"),
    (re.compile(r"long[\s-]*term|долгосрочн", re.IGNORECASE), lambda m: "long_term"),
    (re.compile(r"short[\s-]*term|краткосрочн", re.IGNORECASE), lambda m: "short_term"),
]

# words that commonly precede a location mention
_LOCATION_HINTS = [
    "in", "at", "near", "around",
    "в", "во", "на", "рядом с", "около", "возле",
]


# ---------------------------------------------------------------------------
# Number / price parsing helpers
# ---------------------------------------------------------------------------
def _to_float(token: Optional[str]) -> Optional[float]:
    """Parse a numeric token that may contain separators like 1,000 or 1.000."""
    if token is None:
        return None
    cleaned = str(token).strip().replace(" ", "")
    if not cleaned:
        return None
    # Normalize thousands separators.
    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", "")
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return None


_NUMBER_RE = re.compile(r"\d[\d\s.,]*\d|\d")


def _extract_numbers(text: str) -> List[float]:
    numbers: List[float] = []
    for match in _NUMBER_RE.finditer(text):
        value = _to_float(match.group(0))
        if value is not None:
            numbers.append(value)
    return numbers


def _extract_price_range(text: str) -> Dict[str, Optional[float]]:
    """
    Heuristic price-range extraction. Understands patterns like:
        "до 700$"                 -> max=700
        "от 300$"                 -> min=300
        "300-700$" / "300..700"   -> min=300, max=700
        "under 700"               -> max=700
        "from 300 to 700"         -> min=300, max=700
    """
    lowered = text.lower()
    price_min: Optional[float] = None
    price_max: Optional[float] = None

    # explicit range "300-700" / "300 – 700" / "300..700" / "300 to 700"
    range_match = re.search(r"(\d[\d\s.,]*)\s*(?:-|–|—|\.\.|to|до)\s*(\d[\d\s.,]*)", lowered)
    if range_match:
        a = _to_float(range_match.group(1))
        b = _to_float(range_match.group(2))
        if a is not None and b is not None:
            price_min, price_max = min(a, b), max(a, b)
            return {"price_min": price_min, "price_max": price_max}

    # "до X" / "under X" / "max X" / "не больше X" -> upper bound
    upper = re.search(r"(?:до|under|below|max|не больше|не дороже)\s*(\d[\d\s.,]*)", lowered)
    if upper:
        price_max = _to_float(upper.group(1))

    # "от X" / "from X" / "min X" / "не меньше X" -> lower bound
    lower = re.search(r"(?:от|from|min|не меньше|не дешевле)\s*(\d[\d\s.,]*)", lowered)
    if lower:
        price_min = _to_float(lower.group(1))

    # If nothing matched but there is a single number next to a currency token,
    # treat it as an upper bound (typical "budget" phrasing).
    if price_min is None and price_max is None:
        numbers = _extract_numbers(lowered)
        has_currency = any(tok in lowered for tok in _CURRENCY_TOKENS)
        if has_currency and len(numbers) == 1:
            price_max = numbers[0]

    return {"price_min": price_min, "price_max": price_max}


# ---------------------------------------------------------------------------
# Field extractors
# ---------------------------------------------------------------------------
def _extract_property_type(text: str) -> Optional[str]:
    lowered = text.lower()
    for canonical, keywords in _PROPERTY_TYPES.items():
        for kw in keywords:
            if kw in lowered:
                return canonical
    return None


def _extract_constraints(text: str) -> List[str]:
    lowered = text.lower()
    found: List[str] = []
    for canonical, keywords in _CONSTRAINTS.items():
        for kw in keywords:
            if kw in lowered:
                found.append(canonical)
                break
    # stable, de-duplicated order
    seen = set()
    ordered: List[str] = []
    for c in found:
        if c not in seen:
            seen.add(c)
            ordered.append(c)
    return ordered


def _extract_duration(text: str) -> Optional[str]:
    for pattern, render in _DURATION_PATTERNS:
        match = pattern.search(text)
        if match:
            return render(match)
    return None


def _extract_location(text: str) -> Optional[str]:
    """
    Best-effort location extraction.

    Strategy:
        1. Look for a hint word ("возле", "near", ...) followed by a
           word token that is NOT a known constraint / type keyword.
        2. Otherwise return None (downstream geocoder can refine).

    This is intentionally conservative to avoid polluting the field with noise.
    """
    if not text:
        return None

    lowered = text.lower()

    # Build a blacklist of phrases we already interpret as constraints/types,
    # so we don't accidentally return them as a "location".
    blacklist_phrases = set()
    for kws in list(_CONSTRAINTS.values()) + list(_PROPERTY_TYPES.values()):
        for kw in kws:
            blacklist_phrases.add(kw)

    for hint in _LOCATION_HINTS:
        idx = lowered.find(hint)
        while idx != -1:
            after = text[idx + len(hint):].strip()
            if after:
                candidate = re.split(r"[,\.;]", after)[0].strip()
                first_words = " ".join(candidate.split()[:2]).strip()
                if first_words and first_words.lower() not in blacklist_phrases:
                    if not any(first_words.lower().startswith(bp) for bp in blacklist_phrases):
                        return first_words
            idx = lowered.find(hint, idx + len(hint))

    return None


# ---------------------------------------------------------------------------
# Dict input normalization (backward-compatible passthrough)
# ---------------------------------------------------------------------------
def _from_dict(raw: Dict[str, Any]) -> NormalizedTask:
    """
    Accept an already-partially-structured task and coerce it into the
    canonical shape without losing existing values. Unknown keys are ignored.
    """
    def _get(*keys):
        for k in keys:
            if k in raw and raw[k] not in (None, ""):
                return raw[k]
        return None

    constraints = _get("constraints") or []
    if isinstance(constraints, str):
        constraints = [constraints]
    elif not isinstance(constraints, (list, tuple)):
        constraints = []

    price_min = _get("price_min", "min_price")
    price_max = _get("price_max", "max_price")

    return NormalizedTask(
        location=_get("location", "city", "area"),
        price_min=_to_float(price_min) if price_min is not None else None,
        price_max=_to_float(price_max) if price_max is not None else None,
        type=_get("type", "property_type"),
        duration=_get("duration", "term"),
        constraints=[str(c) for c in constraints],
    )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def normalize_task(raw: Union[str, Dict[str, Any], None]) -> Dict[str, Any]:
    """
    Normalize a raw task into the canonical Lentra task format.

    Args:
        raw: natural-language string, a partial dict, or None.

    Returns:
        dict with keys:
            location, price_min, price_max, type, duration, constraints

    Edge-case safe: never raises for empty / malformed input.
    """
    # None / empty
    if raw is None:
        return NormalizedTask().to_dict()

    # dict passthrough (backward compatibility)
    if isinstance(raw, dict):
        return _from_dict(raw).to_dict()

    # anything not a string -> coerce defensively
    if not isinstance(raw, str):
        try:
            raw = str(raw)
        except Exception:
            return NormalizedTask().to_dict()

    text = raw.strip()
    if not text:
        return NormalizedTask().to_dict()

    price = _extract_price_range(text)

    task = NormalizedTask(
        location=_extract_location(text),
        price_min=price["price_min"],
        price_max=price["price_max"],
        type=_extract_property_type(text),
        duration=_extract_duration(text),
        constraints=_extract_constraints(text),
    )
    return task.to_dict()
