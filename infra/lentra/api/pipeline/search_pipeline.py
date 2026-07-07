from typing import Dict, Any, List

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.core.adapters.search_adapter import SearchAdapter

from lentra.core.market_intelligence.engines.risk_engine import RiskEngine
from lentra.core.market_intelligence.engines.dedup_engine import DedupEngine


class SearchPipeline:
    """
    Main Market Intelligence Search Pipeline.

    Core flow:

    Search
      |
      v
    Market Intelligence
      |
      +--> Risk
      |
      +--> Dedup
      |
      +--> Area Intelligence
      |
      v
    Decision Layer
    """

    def __init__(self):

        self.gateway = build_gateway_v3()
        self.adapter = SearchAdapter()

        self.risk_engine = RiskEngine()
        self.dedup_engine = DedupEngine()


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
        dedup: Dict[str, Any],
        area: Dict[str, Any],
    ) -> Dict[str, Any]:

        price_score = market.get(
            "pricing_score",
            0.5
        )

        area_score = area.get(
            "score",
            0.5
        )


        risk_data = risk.get(
            "risk",
            {}
        )

        risk_level = risk_data.get(
            "level",
            "medium"
        )

        fraud_score = risk_data.get(
            "fraud_score",
            0.5
        )


        duplicates = dedup.get(
            "dedup",
            {}
        ).get(
            "duplicates",
            0
        )


        deviation = abs(
            market.get(
                "difference_percent",
                0
            )
        )


        risk_penalty = self._risk_penalty(
            risk_level
        )


        duplicate_penalty = min(
            duplicates * 0.1,
            0.3
        )


        score = (

            price_score * 0.45

            +

            area_score * 0.20

            +

            (1 - fraud_score) * 0.20

            +

            (1 - duplicate_penalty) * 0.15

        )


        score = max(
            0.0,
            min(
                score,
                1.0
            )
        )


        signals = {

            "price": market.get(
                "verdict"
            ),

            "risk": risk_level,

            "fraud_score": fraud_score,

            "duplicates": duplicates,

            "deviation_percent": deviation

        }


        if risk_level == "high":

            action = "AVOID"

            reason = (
                "Высокий риск объявления."
            )


        elif fraud_score >= 0.45:

            action = "REVIEW"

            reason = (
                "Цена привлекательная, "
                "но требуется проверка риска."
            )


        elif deviation > 25:

            action = "REVIEW"

            reason = (
                "Сильное отклонение от рынка."
            )


        elif score >= 0.78:

            action = "BUY"

            reason = (
                "Цена, риск и параметры "
                "соответствуют рынку."
            )


        else:

            action = "REVIEW"

            reason = (
                "Предложение требует анализа."
            )


        return {

            "action": action,

            "score": round(
                score,
                4
            ),

            "confidence": round(
                1 - risk_penalty,
                2
            ),

            "reason": reason,

            "signals": signals

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


        results: List[Dict[str, Any]] = []


        for listing in listings:


            context = {

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
                context
            )


            market = self.gateway.run_engine(
                "market_intelligence",
                context
            )


            risk_result = self.risk_engine.evaluate(
                context.copy()
            )


            dedup_result = self.dedup_engine.evaluate(
                context.copy()
            )


            decision = self._build_decision(
                market,
                risk_result,
                dedup_result,
                area
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
                            listing.get("price"),

                        "market_price":
                            context.get(
                                "market_price"
                            )

                    },


                    "intelligence": {

                        "area": area,

                        "market": market,

                        "risk": risk_result,

                        "dedup": dedup_result

                    },


                    "decision": decision

                }

            )


        return {

            "query": query,

            "count": len(results),

            "results": results

        }
