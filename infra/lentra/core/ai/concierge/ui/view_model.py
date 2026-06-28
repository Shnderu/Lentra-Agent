
def build_card(self, obj):

    return {
        "id": getattr(obj, "id", "unknown"),
        "price": getattr(obj, "market_price", None),
        "risk": getattr(obj, "risk", 0.5),
        "area_score": getattr(obj, "area_score", 5.0),
        "ui_state": getattr(obj, "ui_state", "green"),

        # 🔥 SAFE fallback (CRITICAL FIX)
        "final_score": getattr(obj, "final_score", 0.0),

        "confidence": getattr(obj, "confidence", 0.0),
        "explanation": getattr(obj, "explanation", []),
    }

