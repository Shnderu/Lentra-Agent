import importlib
import os
from typing import Any


_ENGINE = None


def get_engine() -> Any:
    """
    Lazy load intelligence engine.

    LENTRA_INTELLIGENCE_BACKEND:
        - local (default)
        - remote
        - external
        - custom.module.path
    """
    global _ENGINE

    if _ENGINE is not None:
        return _ENGINE

    backend = os.getenv("LENTRA_INTELLIGENCE_BACKEND", "local")

    if backend == "local":
        from lentra.core.intelligence.local_engine import LocalEngine
        _ENGINE = LocalEngine()
        return _ENGINE

    # external / custom engine injection
    module_path = os.getenv("LENTRA_INTELLIGENCE_MODULE")
    class_name = os.getenv("LENTRA_INTELLIGENCE_CLASS", "Engine")

    if module_path:
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        _ENGINE = cls()
        return _ENGINE

    raise RuntimeError(f"Unknown intelligence backend: {backend}")
