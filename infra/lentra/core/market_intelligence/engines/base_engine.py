from typing import Any


class BaseEngine:
    def evaluate(self, ctx: Any, result: dict) -> dict:
        """
        V3 CONTRACT:
        - ctx = EngineContextV3
        - result = shared mutable accumulator
        """

        raise NotImplementedError()
