
class EngineOutputNormalizer:
    """
    Ensures engines return FLAT payloads:
    NOT nested like {"risk": {...}}
    BUT clean: {...}
    """

    @staticmethod
    def normalize(result, engine_name: str):
        if result is None:
            return {
                "status": "empty"
            }

        # unwrap double-wrapped engines
        if isinstance(result, dict):
            if engine_name in result:
                return result[engine_name]

            # already clean
            return result

        return {
            "value": result
        }
