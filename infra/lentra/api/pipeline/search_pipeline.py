from typing import Dict, Any

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.core.adapters.search_adapter import SearchAdapter

from lentra.core.market_intelligence.engines.risk_engine import RiskEngine
from lentra.core.market_intelligence.engines.dedup_engine import DedupEngine

from lentra.core.market_intelligence.decision.decision_layer import DecisionLayer
from lentra.core.market_intelligence.ranking.unified_ranking_engine import UnifiedRankingEngine


class SearchPipeline:
    """
    Main Market Intelligence Search Pipeline.

    Flow:

    Search
      |
      v
    Market Intelligence
      |
      +--> Market
      +--> Risk
      +--> Dedup
      +--> Area
      |
      v
    Ranking
      |
      v
    Decision Layer
      |
      v
    Final Verdict
    """

    def __init__(self):

        self.gateway = build_gateway_v3()

        self.adapter = SearchAdapter()

        self.risk_engine = RiskEngine()

        self.dedup_engine = DedupEngine()

        self.decision_layer = DecisionLayer()

        self.ranking_engine = UnifiedRankingEngine()


    def _risk_penalty(
        self,
        level: str
    ) -> float:

        return {
            "low": 0.0,
            "medium": 0.15,
            "high": 0.35,
        }.get(
            level,
            0.15
        )


    def _build_decision(
        self,
        market: Dict[str, Any],
        risk: Dict[str, Any],
        area: Dict[str, Any],
        ranking_score: float = 0.5,
    ) -> Dict[str, Any]:

        risk_data = risk.get(
            "risk",
            {}
        )

        fraud_score = risk_data.get(
            "fraud_score",
            0.5
        )

        risk_level = risk_data.get(
            "level",
            "medium"
        )


        decision_input = {

            "signals": {

                "pricing": market,

                "area": area

            },

            "ranking": {

                "score": ranking_score

            },

            "risk": {

                "risk_level": fraud_score

            }

        }


        decision = self.decision_layer.build(
            decision_input
        )


        return {

            "action": decision.get(
                "decision",
                "REVIEW"
            ),

            "score": decision.get(
                "decision_score",
                0.5
            ),

            "confidence": round(
                1 - self._risk_penalty(
                    risk_level
                ),
                2
            ),

            "reason": (
                "Решение сформировано "
                "Market Intelligence Decision Layer."
            ),

            "signals": {

                "price": market.get(
                    "verdict"
                ),

                "risk": risk_level,

                "fraud_score": fraud_score

            },

            "decision_layer": decision

        }


    def run(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        query = payload.get(
            "query",
            ""
        )


        listings = self.adapter.build_objects(
            query
        )


        raw_cards = []

        prepared = []


        for listing in listings:

            context = {

                "id": listing.get(
                    "id"
                ),

                "title": listing.get(
                    "title",
                    ""
                ),

                "description": listing.get(
                    "description",
                    ""
                ),

                "source": listing.get(
                    "source",
                    "unknown"
                ),

                "type": listing.get(
                    "type",
                    "apartment"
                ),

                "query": query,

                "price": listing.get(
                    "price",
                    0
                ),

                "market_price": listing.get(
                    "market_price",
                    650
                ),

                "city": listing.get(
                    "city",
                    "da_nang"
                ),

            }


            area = self.gateway.run_engine(
                "area",
                context.copy()
            )


            market = self.gateway.run_engine(
                "market_intelligence",
                context.copy()
            )


            risk_result = self.risk_engine.evaluate(
                context.copy()
            )


            dedup_result = self.dedup_engine.evaluate(
                context.copy()
            )


            risk_data = risk_result.get(
                "risk",
                {}
            )


            raw_cards.append(

                {

                    "id": listing.get(
                        "id"
                    ),

                    "price": listing.get(
                        "price",
                        0
                    ),

                    "risk": risk_data.get(
                        "fraud_score",
                        0.5
                    ),

                    "confidence": market.get(
                        "confidence",
                        0.5
                    )

                }

            )


            prepared.append(

                {

                    "listing": listing,

                    "context": context,

                    "area": area,

                    "market": market,

                    "risk": risk_result,

                    "dedup": dedup_result

                }

            )


        ranked = self.ranking_engine.rank(
            raw_cards
        )


        rank_map = {

            item.get(
                "id"
            ): item.get(
                "rank"
            )

            for item in ranked

        }


        results = []


        for item in prepared:

            listing = item["listing"]


            decision = self._build_decision(

                item["market"],

                item["risk"],

                item["area"],

                ranking_score=(
                    1 /
                    max(
                        rank_map.get(
                            listing.get(
                                "id"
                            ),
                            1
                        ),
                        1
                    )
                )

            )


            results.append(

                {

                    "id": listing.get(
                        "id"
                    ),

                    "title": listing.get(
                        "title"
                    ),

                    "price": listing.get(
                        "price"
                    ),

                    "city": listing.get(
                        "city",
                        "da_nang"
                    ),

                    "source": listing.get(
                        "source",
                        "seed"
                    ),

                    "market_analysis": {

                        "listing_price":
                            listing.get(
                                "price"
                            ),

                        "market_price":
                            item["context"].get(
                                "market_price"
                            )

                    },

                    "intelligence": {

                        "area":
                            item["area"],

                        "market":
                            item["market"],

                        "risk":
                            item["risk"],

                        "dedup":
                            item["dedup"]

                    },

                    "decision":
                        decision

                }

            )


        return {

            "query": query,

            "count": len(results),

            "results": results

        }
