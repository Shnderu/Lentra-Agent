from typing import Protocol, List, Dict, Any, runtime_checkable


@runtime_checkable
class RankingEngineContract(Protocol):
    """
    Ranking Layer Contract:
    input: enriched listings
    output: ranked listings
    """

    def analyze(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ...
