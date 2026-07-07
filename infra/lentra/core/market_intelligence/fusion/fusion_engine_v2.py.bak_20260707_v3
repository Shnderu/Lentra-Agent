from typing import Dict, Any


def safe_get(d: Dict[str, Any], path: str, default=None):
    try:
        for part in path.split("."):
            if isinstance(d, dict):
                d = d.get(part, {})
            else:
                return default

        return d if d != {} else default

    except Exception:
        return default


def extract_engine_block(name: str, value: Dict[str, Any]) -> Dict[str, Any]:

    if not isinstance(value, dict):
        return {}

    nested = value.get(name)

    if isinstance(nested, dict):
        return nested

    return value


def build_features(engines: Dict[str, Any]) -> Dict[str, float]:

    pricing = extract_engine_block(
        "pricing",
        engines.get("pricing", {})
    )

    risk = extract_engine_block(
        "risk",
        engines.get("risk", {})
    )

    signals = extract_engine_block(
        "signals",
        engines.get("signals", {})
    )

    area = extract_engine_block(
        "area",
        engines.get("area", {})
    )

    dedup = extract_engine_block(
        "dedup",
        engines.get("dedup", {})
    )


    # ---------------------------
    # AI PRICE CHECK
    # ---------------------------

    price = safe_get(
        pricing,
        "price",
        None
    )

    market_price = safe_get(
        pricing,
        "market_price",
        None
    )

    if price is not None and market_price:
        deviation = abs(
            price - market_price
        ) / market_price

        price_score = max(
            0.0,
            min(
                1.0,
                1 - deviation
            )
        )

    else:
        delta = safe_get(
            pricing,
            "delta",
            0
        ) or 0

        price_score = 1.0 / (
            1.0 + abs(delta) / 100.0
        )


    # ---------------------------
    # RISK SCORE
    # ---------------------------

    risk_level = safe_get(
        risk,
        "level",
        "unknown"
    )

    risk_map = {
        "low": 0.9,
        "medium": 0.5,
        "high": 0.1,
        "unknown": 0.5
    }

    risk_score = risk_map.get(
        risk_level,
        0.5
    )


    # ---------------------------
    # SIGNAL SCORE
    # ---------------------------

    signal_len = safe_get(
        signals,
        "length",
        0
    ) or 0

    signal_score = min(
        signal_len / 30.0,
        1.0
    )


    # ---------------------------
    # AREA SCORE
    # ---------------------------

    area_conf = (
        0.3
        if safe_get(
            area,
            "detected",
            "unknown"
        ) == "unknown"
        else 0.8
    )


    # ---------------------------
    # DEDUP SCORE
    # ---------------------------

    duplicates = safe_get(
        dedup,
        "duplicates",
        0
    ) or 0

    dedup_score = (
        1.0
        if duplicates == 0
        else max(
            0.0,
            1.0 - duplicates * 0.2
        )
    )


    return {
        "price": price_score,
        "risk": risk_score,
        "signals": signal_score,
        "area": area_conf,
        "dedup": dedup_score,
    }


WEIGHTS = {
    "price": 0.30,
    "risk": 0.25,
    "signals": 0.20,
    "area": 0.15,
    "dedup": 0.10,
}


def calibrate(raw_score: float) -> float:

    calibrated = 1 / (
        1 + (2.718 ** (-3 * (raw_score - 0.5)))
    )

    return round(
        calibrated,
        4
    )


def decision(score: float) -> str:

    if score >= 0.72:
        return "MATCH"

    if score >= 0.45:
        return "REVIEW"

    return "REJECT"


class FusionEngineV2:

    def evaluate(
        self,
        engine_results: Dict[str, Any]
    ) -> Dict[str, Any]:

        features = build_features(
            engine_results
        )

        raw_score = sum(
            features[k] * WEIGHTS[k]
            for k in WEIGHTS
        )

        calibrated_score = calibrate(
            raw_score
        )

        return {
            "score": calibrated_score,
            "raw_score": round(
                raw_score,
                4
            ),
            "decision": decision(
                calibrated_score
            ),
            "explanation": (
                f"Price score={features['price']:.2f} | "
                f"Risk score={features['risk']:.2f} | "
                f"Signals score={features['signals']:.2f} | "
                f"Area score={features['area']:.2f} | "
                f"Dedup score={features['dedup']:.2f}"
            ),
            "features": features,
            "weights": WEIGHTS,
        }


def build_fusion_engine_v2():
    return FusionEngineV2()
