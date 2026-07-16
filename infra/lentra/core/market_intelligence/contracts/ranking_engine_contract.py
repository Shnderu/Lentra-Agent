from typing import Protocol, List, Dict, Any, runtime_checkable


@runtime_checkable
class RankingEngineContract(Protocol):
    """
    Ranking Layer Contract.

    Single ranking entry:
        UnifiedRankingEngine

    Input:
        enriched market intelligence cards

    Output:
        ranked cards
    """


    def rank(
        self,
        cards: List[Dict[str, Any]],
        market_truth: Dict[str, Any] | None = None,
    ) -> List[Dict[str, Any]]:
        ...
