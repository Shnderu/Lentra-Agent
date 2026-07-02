from typing import Any, Dict


def safe_evaluate(engine, payload: Any):
    """
    Universal compatibility layer for mixed V2/V3 engines
    WITHOUT introducing new architecture layers.
    """

    try:
        # normalize ctx-like objects
        ctx = _normalize_ctx(payload)

        return engine.evaluate(ctx)

    except TypeError:
        try:
            result = {}
            return engine.evaluate(ctx, result)
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    except Exception as e:
        return {"status": "failed", "error": str(e)}


def _normalize_ctx(payload: Any) -> Dict[str, Any]:
    """
    Converts all known ctx formats into flat dict.
    """

    if payload is None:
        return {}

    # already dict
    if isinstance(payload, dict):
        return payload

    # EngineContextV3 or similar
    if hasattr(payload, "__dict__"):
        return payload.__dict__

    # ctx.payload style
    if hasattr(payload, "payload"):
        inner = getattr(payload, "payload")
        if isinstance(inner, dict):
            return inner
        if hasattr(inner, "__dict__"):
            return inner.__dict__

    return {}
