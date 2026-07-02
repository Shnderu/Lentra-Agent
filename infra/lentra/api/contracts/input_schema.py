from typing import Dict, Any


ALLOWED_FIELDS = {
    "query",
    "price",
    "market_price"
}


def validate_input(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    IMMUTABLE INPUT CONTRACT

    RULE:
    - ONLY CORE FIELDS ARE ALLOWED
    - EVERYTHING ELSE IS STRIPPED
    """

    return {
        k: v for k, v in payload.items()
        if k in ALLOWED_FIELDS
    }
