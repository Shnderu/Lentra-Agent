from typing import Dict, Any

from lentra.core.market_intelligence.engines.risk_engine import (
    RiskEngine
)


class RiskEngineAdapter:
    """
    Adapter contract boundary.

    Engine output:

        risk_score
        risk_level
        risk_signals

    Pipeline output:

        risk_score
        risk_level
        signals
    """


    def __init__(
        self,
        engine: RiskEngine
    ):
        self.engine = engine



    def evaluate(
        self,
        item: Dict[str, Any],
        market_stats: Dict[str, Any],
        duplicate_count: int
    ) -> Dict[str, Any]:

        payload = {
            **item,

            "market_price":
                market_stats.get(
                    "market_price",
                    0
                ),

            "duplicate_count":
                duplicate_count
        }


        result = self.engine.run(
            payload
        )


        return {

            "risk_score":
                result.get(
                    "risk_score",
                    0.0
                ),


            "risk_level":
                result.get(
                    "risk_level",
                    "unknown"
                ),


            "signals":
                result.get(
                    "risk_signals",
                    []
                )

        }
