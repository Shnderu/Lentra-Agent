class EngineV3:
    """
    Unified V3 engine contract
    """

    name: str = "base"

    def evaluate(self, context: dict, result: dict):
        """
        V3 STANDARD:
        - context: shared runtime context
        - result: mutable result accumulator
        """
        return result
