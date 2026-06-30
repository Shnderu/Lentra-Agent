from lentra.core.intelligence.loader import get_engine


def interpret(query: str, context: dict | None = None):
    engine = get_engine()
    return engine.interpret(query, context)
