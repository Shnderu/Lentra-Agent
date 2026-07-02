from typing import Dict, Any


class BaseEngine:
    def evaluate(self, result: Dict[str, Any], ctx: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        V3 CONTRACT:
        - input = accumulated result
        - output = enriched result
        """
        raise NotImplementedError()
