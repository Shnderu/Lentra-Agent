from dataclasses import dataclass
from typing import Dict, Any


# ---------------------------
# SAFE NORMALIZATION LAYER
# ---------------------------

def safe_get(d: Dict[str, Any], path: str, default=None):
    """
    Safe getter for nested dicts: "a.b.c"
    """
    try:
        for part in path.split("."):
            d = d.get(part, {})
        return d or default
    except Exception:
        return default


def normalize_engine_output(name: str, result: Any) -> Dict[str, Any]:
    """
    Normalizes ALL engines into stable contract.
    """
    if result is None:
        return {"status": "failed", "data": {}, "meta": {}}

    if not isinstance(result, dict):
        return {"status": "ok", "data": {"value": result}, "meta": {}}

    # unwrap nested duplication (engine inside engine bug)
    if name in result and isinstance(result[name], dict):
        result = result[name]

    return {
        "status": result.get("status", "ok"),
        "data": {k: v for k, v in result.items() if k != "status"},
        "meta": {}
    }


# ---------------------------
# FEATURE EXTRACTION
# ---------------------------

def build_features(engines: Dict[str, Any]) -> Dict[str, float]:
    """
    Converts engine outputs into normalized feature vector (0..1)
    """

    pricing = engines.get("pricing", {})
    risk = engines.get("risk", {})
    signals = engines.get("signals", {})
    area = engines.get("area", {})
    dedup = engines.get("dedup", {})

    # ---------------------------
    # PRICING SCORE (0..1)
    # ---------------------------
    delta = safe_get(pricing, "delta", 0) or 0
    price_score = 1.0 / (1.0 + abs(delta) / 100.0)

    # ---------------------------
    # RISK SCORE (0..1 inverted)
    # ---------------------------
    risk_level = safe_get(risk, "level", "unknown")

    risk_map = {
        "low": 0.9,
        "medium": 0.5,
        "high": 0.1,
        "unknown": 0.5
    }
    risk_score = risk_map.get(risk_level, 0.5)

    # ---------------------------
    # SIGNAL SCORE
    # ---------------------------
    signal_len = safe_get(signals, "length", 0) or 0
    signal_score = min(signal_len / 30.0, 1.0)

    # ---------------------------
    # AREA SCORE
    # ---------------------------
    area_conf = 0.3 if safe_get(area, "detected", "unknown") == "unknown" else 0.8

    # ---------------------------
    # DEDUP PENALTY
    # ---------------------------
    duplicates = safe_get(dedup, "duplicates", 0) or 0
    dedup_score = 1.0 if duplicates == 0 else max(0.0, 1.0 - duplicates * 0.2)

    return {
        "price": price_score,
        "risk": risk_score,
        "signals": signal_score,
        "area": area_conf,
        "dedup": dedup_score,
    }


# ---------------------------
# WEIGHTS (tunable v2)
# ---------------------------

WEIGHTS = {
    "price": 0.30,
    "risk": 0.25,
    "signals": 0.20,
    "area": 0.15,
    "dedup": 0.10,
}


# ---------------------------
# CALIBRATION LAYER
# ---------------------------

def calibrate(raw_score: float) -> float:
    """
    Stabilizes score into real-world probability-like range
    """

    # sigmoid-like compression
    calibrated = 1 / (1 + (2.718 ** (-3 * (raw_score - 0.5))))

    return round(calibrated, 4)


# ---------------------------
# DECISION ENGINE
# ---------------------------

def decision(score: float) -> str:
    if score >= 0.72:
        return "MATCH"
    elif score >= 0.45:
        return "REVIEW"
    return "REJECT"


# ---------------------------
# FUSION ENGINE V2
# ---------------------------

class FusionEngineV2:

    def evaluate(self, engine_results: Dict[str, Any]) -> Dict[str, Any]:

        features = build_features(engine_results)

        # weighted sum
        raw_score = sum(
            features[k] * WEIGHTS[k]
            for k in WEIGHTS
        )

        calibrated_score = calibrate(raw_score)

        explanation_parts = []

        explanation_parts.append(f"Price score={features['price']:.2f}")
        explanation_parts.append(f"Risk score={features['risk']:.2f}")
        explanation_parts.append(f"Signals score={features['signals']:.2f}")
        explanation_parts.append(f"Area score={features['area']:.2f}")
        explanation_parts.append(f"Dedup score={features['dedup']:.2f}")

        return {
            "score": calibrated_score,
            "raw_score": round(raw_score, 4),
            "decision": decision(calibrated_score),
            "explanation": " | ".join(explanation_parts),
            "features": features,
            "weights": WEIGHTS,
        }


def build_fusion_engine_v2():
    return FusionEngineV2()
