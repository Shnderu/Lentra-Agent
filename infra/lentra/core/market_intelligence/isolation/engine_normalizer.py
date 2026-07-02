from typing import Any, Dict


class EngineResultNormalizer:
    """
    Guarantees all engines return a dict
    """

    @staticmethod
    def normalize(result: Any, engine_name: str) -> Dict[str, Any]:
        if result is None:
            return {
                "engine": engine_name,
                "status": "empty",
                "data": {}
            }

        if isinstance(result, dict):
            return result

        return {
            "engine": engine_name,
            "status": "wrapped",
            "data": result
        }
