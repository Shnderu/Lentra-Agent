from typing import Dict, Any
from datetime import datetime, timezone

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.core.adapters.search_adapter import SearchAdapter

from lentra.core.market_intelligence.engines.risk_engine import RiskEngine
from lentra.core.market_intelligence.engines.dedup_engine import DedupEngine

from lentra.core.market_intelligence.decision.decision_layer import DecisionLayer
from lentra.core.market_intelligence.ranking.unified_ranking_engine import UnifiedRankingEngine
from lentra.core.market_intelligence.contracts.listing_contract_guard import ListingContractGuard

from lentra.core.market_intelligence.history.price_observation import (
    PriceObservation
)


from lentra.core.market_intelligence.verdict.market_verdict_engine import (
    MarketVerdictEngine
)


from lentra.core.market_intelligence.output.object_intelligence_card import (
    ObjectIntelligenceCardBuilder
)

from lentra.core.market_intelligence.market.market_service import MarketService
from lentra.core.market_intelligence.repository.market_snapshot_repository import MarketSnapshotRepository


class SearchPipeline:

    def __init__(self):

        self.gateway = build_gateway_v3()

        self.adapter = SearchAdapter()

        self.risk_engine = RiskEngine()

        self.dedup_engine = DedupEngine()

        self.decision_layer = DecisionLayer()

        self.ranking_engine = UnifiedRankingEngine()

        self.market_service = MarketService()

        self.verdict_engine = MarketVerdictEngine()

        self.object_card_builder = ObjectIntelligenceCardBuilder()

        self.market_snapshot_repository = MarketSnapshotRepository()


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


    def _build_ai_verdict(
        self,
        market: Dict[str, Any],
        risk: Dict[str, Any],
        dedup: Dict[str, Any]
    ) -> str:

        price_status = market.get(
            "verdict",
            "unknown"
        )

        difference_percent = market.get(
            "difference_percent",
            0
        )

        risk_level = risk.get(
            "risk",
            {}
        ).get(
            "level",
            "medium"
        )

        duplicates = dedup.get(
            "dedup",
            {}
        ).get(
            "duplicates",
            0
        )


        if risk_level == "high":
            return (
                "Цена выглядит выгодной, "
                "но высокий риск объявления требует проверки."
            )


        if price_status == "good_deal":
            return (
                f"Хорошее предложение: цена ниже рынка "
                f"примерно на {abs(difference_percent)}%."
            )


        if price_status == "overpriced":
            return (
                f"Цена выше рынка примерно на "
                f"{difference_percent}%."
            )


        if duplicates > 0:
            return (
                "Объект найден в нескольких источниках. "
                "Проверьте оригинальное объявление."
            )


        return (
            "Цена соответствует рынку. "
            "Объект выглядит сбалансированным."
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


        decision = self.decision_layer.build(
            {
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

            "reason":
                "Решение сформировано Market Intelligence Decision Layer.",

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


        for listing in listings:

            listing = ListingContractGuard.normalize(
                listing
            )


            self.market_service.history_repository.save(
                PriceObservation(
                    listing_id=str(
                        listing.get("id")
                    ),

                    price=float(
                        listing.get(
                            "price",
                            0
                        )
                    ),

                    currency=listing.get(
                        "currency",
                        "USD"
                    ),

                    city=listing.get(
                        "city",
                        "da_nang"
                    ),

                    source=listing.get(
                        "source"
                    ),

                    area=listing.get(
                        "location"
                    )
                )
            )



        market_analysis = self.market_service.analyze(
            listings
        )

        market_truth = market_analysis.get(
            "market_truth",
            {}
        )

        price_intelligence = market_analysis.get(
            "price_intelligence",
            {}
        )


        segment_intelligence = market_analysis.get(
            "segment_intelligence",
            {}
        )


        market_movement = market_analysis.get(
            "market_movement",
            {}
        )


        market_explanation = market_analysis.get(
            "market_explanation",
            {}
        )


        market_verdict = market_analysis.get(
            "market_verdict",
            {}
        )


        raw_cards = []

        prepared = []


        for listing in listings:

            context = {

                "id": listing.get("id"),

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

                "market_price": (
                    market_truth.get(
                        "median_price"
                    )
                    or 650
                ),

                "market_truth": market_truth,

                "city": listing.get(
                    "city",
                    "da_nang"
                )

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



            market_verdict = self.verdict_engine.verdict(
                market,
                price_intelligence,
                market_explanation,
                risk_result,
                dedup_result,
                area
            )


            raw_cards.append(
                {
                    "id": listing.get("id"),

                    "price": listing.get(
                        "price",
                        0
                    ),

                    "risk": risk_result.get(
                        "risk",
                        {}
                    ).get(
                        "fraud_score",
                        0.5
                    ),

                    "confidence": market.get(
                        "confidence",
                        0.5
                    ),

                    "pricing_score": market.get(
                        "pricing_score",
                        0.5
                    ),

                    "area_score": area.get(
                        "score",
                        0.5
                    ),

                    "duplicates": dedup_result.get(
                        "dedup",
                        {}
                    ).get(
                        "duplicates",
                        0
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
                    "dedup": dedup_result,

                    "market_verdict": market_verdict
                }
            )


        market_truth_record = self.market_snapshot_repository.save(
            market_truth
        )


        ranked = self.ranking_engine.rank(
            raw_cards,
            market_truth
        )


        rank_map = {
            item.get("id"): item
            for item in ranked
        }


        results = []


        for item in prepared:

            listing = item["listing"]


            results.append(
                {

                    "id": listing.get("id"),

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

                    "ranking": rank_map.get(
                        listing.get("id"),
                        {}
                    ),

                    "card":
                        self.object_card_builder.build(
                            listing,
                            {
                                "market":
                                    item["market"],

                                "area":
                                    item["area"],

                                "risk":
                                    item["risk"],

                                "dedup":
                                    item["dedup"],

                                "price_intelligence":
                                    price_intelligence,

                                "segment_intelligence":
                                    segment_intelligence,

                                "market_movement":
                                    market_movement,

                                "market_explanation":
                                    market_explanation,

                                "market_verdict":
                                    item["market_verdict"]
                            },
                            rank_map.get(
                                listing.get("id"),
                                {}
                            )
                        ),

                    "intelligence": {

                        "market_truth":
                            market_truth,

                        "market":
                            item["market"],

                        "area":
                            item["area"],

                        "risk":
                            item["risk"],

                        "dedup":
                            item["dedup"],

                        "price_intelligence":
                            price_intelligence,

                        "segment_intelligence":
                            segment_intelligence,

                        "market_movement":
                            market_movement,

                        "market_explanation":
                            market_explanation,

                        "market_verdict":
                            item["market_verdict"],

                        "object_card":
                            self.object_card_builder.build(
                                listing,
                                {
                                    "market":
                                        item["market"],

                                    "area":
                                        item["area"],

                                    "risk":
                                        item["risk"],

                                    "dedup":
                                        item["dedup"],

                                    "price_intelligence":
                                        price_intelligence,

                                    "market_explanation":
                                        market_explanation,

                                    "market_verdict":
                                        item["market_verdict"]
                                },
                                rank_map.get(
                                    listing.get("id"),
                                    {}
                                )
                            )

                    },

                    "decision":
                        self._build_decision(
                            item["market"],
                            item["risk"],
                            item["area"],
                            rank_map.get(
                                listing.get("id"),
                                {}
                            ).get(
                                "ranking_score",
                                0.5
                            )
                        ),

                    "mini_app": {

                        "schema_version": "3.0.3",

                        "object": {

                            "id":
                                listing.get("id"),

                            "title":
                                listing.get("title"),

                            "price":
                                listing.get("price"),

                            "currency":
                                listing.get(
                                    "currency",
                                    "USD"
                                ),

                            "city":
                                listing.get(
                                    "city",
                                    "da_nang"
                                )

                        },

                        "intelligence": {

                            "price_signal":
                                item["market"].get(
                                    "price_signal",
                                    "unknown"
                                ),

                            "market_difference":
                                item["market"].get(
                                    "difference_percent",
                                    0
                                ),

                            "risk_level":
                                item["risk"].get(
                                    "risk",
                                    {}
                                ).get(
                                    "level",
                                    "unknown"
                                ),

                            "duplicates":
                                item["dedup"].get(
                                    "dedup",
                                    {}
                                ).get(
                                    "duplicates",
                                    0
                                ),

                            "trend":
                                price_intelligence.get(
                                    "trend",
                                    "unknown"
                                )

                        },

                        "verdict": {

                            "label":
                                item["market_verdict"].get(
                                    "verdict",
                                    "REVIEW"
                                ),

                            "confidence":
                                item["market_verdict"].get(
                                    "confidence",
                                    0.5
                                )

                        },

                        "explanation": {

                            "summary":
                                market_explanation.get(
                                    "summary",
                                    ""
                                ),

                            "movement":
                                market_explanation.get(
                                    "movement_explanation",
                                    ""
                                )

                        }

                    }

                }
            )


        return {

            "api_version": "1.0",

            "schema_version": "3.0.2",

            "platform": "Lentra",

            "generated_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "query": query,

            "count": len(results),

            "market_snapshot": market_truth_record,

            "price_intelligence": price_intelligence,

            "segment_intelligence": segment_intelligence,

            "market_movement": market_movement,

            "market_explanation": market_explanation,

            "market_verdict": market_verdict,

            "results": results

        }
