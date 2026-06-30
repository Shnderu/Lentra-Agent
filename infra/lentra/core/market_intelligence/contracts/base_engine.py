from typing import Any


class BaseEngine:
    """
    SAFE WRAPPER FOR ALL ENGINES
    """

    def safe_execute(self, fn, *args, **kwargs) -> Any:
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            return {
                "error": str(e),
                "engine": self.__class__.__name__
            }
