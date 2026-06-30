import os
import importlib

_engine = None


def get_engine():
    global _engine

    if _engine is not None:
        return _engine

    module_path = os.getenv("LENTRA_INTELLIGENCE_MODULE")
    class_name = os.getenv("LENTRA_INTELLIGENCE_CLASS", "Engine")

    module = importlib.import_module(module_path)
    _engine = getattr(module, class_name)()

    return _engine


def run_intelligence(payload: dict) -> dict:
    engine = get_engine()
    return engine.interpret(payload)
