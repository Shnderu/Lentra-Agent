from datetime import datetime
from typing import Dict, Any, List


class MarketPriceHistory:
    """
    Market Intelligence Price Timeline Store.

    Responsibility:
    - preserve price observations
    - track source changes
    - provide historical context

    Not responsible:
    - pricing decisions
    - market calculation
    """


    def add_observation(
        self,
        snapshot: Dict[str, Any],
        item: Dict[str, Any],
    ) -> Dict[str, Any]:

        history: List[Dict[str, Any]] = snapshot.get(
            "price_history",
            []
        )


        history.append(
            {
                "price": item.get(
                    "price"
                ),

                "source": item.get(
                    "source"
                ),

                "timestamp": (
                    item.get(
                        "timestamp"
                    )
                    or datetime.utcnow().isoformat()
                )
            }
        )


        snapshot["price_history"] = history


        return snapshot
