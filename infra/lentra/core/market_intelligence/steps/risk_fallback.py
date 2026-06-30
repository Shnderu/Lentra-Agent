def safe_risk_call(risk_engine, item):
    """
    fallback если где-то ещё старый контракт
    """
    if hasattr(risk_engine, "analyze"):
        return risk_engine.analyze(item)

    if hasattr(risk_engine, "score"):
        return risk_engine.score(item)

    if callable(risk_engine):
        return risk_engine(item)

    return item
