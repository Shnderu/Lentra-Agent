from lentra.core.market_intelligence.geo.vietnam_geo_engine import VietnamGeoEngine
from lentra.core.market_intelligence.risk.risk_engine import RiskEngine
from lentra.core.market_intelligence.area.area_engine import AreaEngine
from lentra.core.market_intelligence.area.market_segmentation_engine import MarketSegmentationEngine
from lentra.core.market_intelligence.area.micro_market_engine import MicroMarketEngine
from lentra.core.market_intelligence.area.temporal_market_engine import TemporalMarketEngine
from lentra.core.market_intelligence.decision.market_decision_core import MarketDecisionCore
from lentra.core.market_intelligence.confidence.confidence_decomposition_engine import ConfidenceDecompositionEngine
from lentra.core.market_intelligence.explanation.decision_narrative_engine import DecisionNarrativeEngine
from lentra.core.market_intelligence.ui.market_card_builder import MarketCardBuilder
from lentra.core.market_intelligence.comparison.market_comparison_engine import MarketComparisonEngine
from lentra.core.market_intelligence.search.search_engine import MarketSearchEngine
from lentra.core.market_intelligence.ranking.ranking_engine import MarketRankingEngine
from lentra.core.market_intelligence.search.nlp.query_parser import QueryParser


class MarketIntelligenceEngine:

    def __init__(self):
        self.geo = VietnamGeoEngine()

        self.area_engine = AreaEngine()
        self.segmenter = MarketSegmentationEngine()
        self.micro = MicroMarketEngine()
        self.temporal = TemporalMarketEngine()
        self.risk_engine = RiskEngine()
        self.decision = MarketDecisionCore()
        self.confidence = ConfidenceDecompositionEngine()
        self.explainer = DecisionNarrativeEngine()
        self.card_builder = MarketCardBuilder()
        self.comparison = MarketComparisonEngine()

        self.search_engine = MarketSearchEngine()
        self.ranking_engine = MarketRankingEngine()
        self.query_parser = QueryParser()

    def analyze(self, listings, query_text=None):

        if isinstance(listings, dict):
            listings = [listings]

        results = []

        for listing in listings:

            # -------------------------
            # GEO LAYER (NEW CORE)
            # -------------------------
            listing = self.geo.normalize(listing)

            listing.update(self.area_engine.evaluate(listing))

            listing["segment"] = self.segmenter.update(listing)
            listing["micro_market"] = self.micro.update(listing)

            listing.update(self.risk_engine.evaluate(listing))

            listing["market_volatility"] = self.temporal.volatility(listing["micro_market"])
            listing["market_deviation"] = self.micro.deviation(listing)

            listing = self.decision.decide(listing)

            listing = self.confidence.compute(listing)

            listing = self.explainer.explain(listing)

            card = self.card_builder.build(listing)

            results.append(card)

        if query_text:
            query = self.query_parser.parse(query_text)
            results = self.search_engine.search(results, query)

        results = self.ranking_engine.rank(results)

        return results
