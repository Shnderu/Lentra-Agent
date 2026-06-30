import os
import importlib


def load_intelligence():
    """
    Подключение готового AI ядра Lentra.
    Это НЕ фреймворк — это точка привязки.
    """

    module_path = os.getenv("LENTRA_INTELLIGENCE_MODULE")
    class_name = os.getenv("LENTRA_INTELLIGENCE_CLASS", "Engine")

    if not module_path:
        raise RuntimeError("LENTRA_INTELLIGENCE_MODULE is not set")

    module = importlib.import_module(module_path)
    engine = getattr(module, class_name)()

    return engine
