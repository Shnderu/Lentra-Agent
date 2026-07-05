from lentra.core.market_intelligence.signals.signals_engine_v1 import SignalsEngineV1
from lentra.core.market_intelligence.context.pipeline_context import (
    SignalContext,
    RiskContext,
    RankingContext,
    EnrichmentView,
    PipelineContext
)


class IntelligenceGateway:

    def __init__(self):
        self.signals_engine = SignalsEngineV1()
        self._enrichment = None

    def _get_enrichment(self):
        if self._enrichment is None:
            from lentra.core.market_intelligence.enrichment.enrichment_layer import EnrichmentLayer
            self._enrichment = EnrichmentLayer()
        return self._enrichment

    def compute(self, payload: dict):

        raw = self.signals_engine.compute(payload)

        signals = SignalContext(
            pricing=raw["pricing"],
            area=raw["area"],
            dedup=raw["dedup"],
        )

        risk_raw = raw["risk"]
        risk = RiskContext(
            risk_level=risk_raw["risk_level"],
            score=risk_raw["score"],
            level=risk_raw["level"],
            components=risk_raw["components"],
        )

        ranking_raw = raw["ranking"]
        ranking = RankingContext(
            score=ranking_raw["score"],
            components=ranking_raw["components"],
            version=ranking_raw.get("version", "ranking_v2"),
        )

        enrichment = self._get_enrichment().compute(raw)

        enrichment_view = EnrichmentView(
            market_context=enrichment.get("market_context", ""),
            recommendation_hint=enrichment.get("recommendation_hint", ""),
            meta=enrichment.get("meta", {}),
        )

        ctx = PipelineContext(
            raw=raw,
            signals=signals,
            risk=risk,
            ranking=ranking,
            enrichment=enrichment_view,
        )

        # BACKWARD COMPATIBILITY OUTPUT (NO API BREAK)
        return {
            "pricing": signals.pricing,
            "area": signals.area,
            "dedup": signals.dedup,
            "coupling": raw["coupling"],
            "risk": {
                "risk_level": risk.risk_level,
                "score": risk.score,
                "level": risk.level,
                "components": risk.components,
            },
            "ranking": {
                "score": ranking.score,
                "components": ranking.components,
                "version": ranking.version,
            },
            "enrichment": {
                "market_context": enrichment_view.market_context,
                "recommendation_hint": enrichment_view.recommendation_hint,
                "meta": enrichment_view.meta,
            }
        }
