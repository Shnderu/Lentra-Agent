from typing import Protocol, List, Dict, Any, runtime_checkable


@runtime_checkable
class MarketIntelligenceContract(Protocol):
    """
    MASTER AI OS CONTRACT

    Pipeline:
    dedup → risk → geo → expat → ranking
    """

    def analyze(
        self,
        listings: List[Dict[str, Any]],
        query_text: str = None
    ) -> List[Dict[str, Any]]:
        ...
