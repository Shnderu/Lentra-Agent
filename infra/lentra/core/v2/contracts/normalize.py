from typing import Any, Dict


def ensure_dict(item: Any) -> Dict:
    """
    HARD CONTRACT NORMALIZER (v2 safe mode)

    Forces everything into dict.
    """

    if item is None:
        return {}

    if isinstance(item, dict):
        return item

    # Listing object (primary fix)
    if hasattr(item, "__dict__"):
        data = dict(item.__dict__)

        # safety cleanup: remove None internal refs
        return {k: v for k, v in data.items() if not k.startswith("_")}

    # fallback (string / primitive / weird object)
    return {
        "value": str(item)
    }
