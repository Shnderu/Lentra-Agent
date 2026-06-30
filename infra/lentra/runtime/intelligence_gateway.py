from lentra.core.intelligence.binding import load_intelligence

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = load_intelligence()
    return _engine


def interpret(payload: dict):
    """
    Единственный вход в интеллект.
    Никаких query типов (price_check, risk_score и т.д.)

    payload = нормализованный объект рынка
    """
    engine = get_engine()
    return engine.interpret(payload)
