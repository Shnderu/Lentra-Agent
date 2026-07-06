"""
CORE STEP = PURE DECISION FUNCTION

NO runtime dependencies
NO gateway calls
"""

def risk_fallback(risk_score: float) -> str:
    if risk_score > 0.7:
        return "HIGH_RISK"
    if risk_score > 0.3:
        return "MEDIUM_RISK"
    return "LOW_RISK"
