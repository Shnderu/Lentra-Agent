from lentra.core.market_intelligence._import_safety import ImportGuard


def build_intelligence_stack(engine_factory):

    with ImportGuard("INTELLIGENCE_STACK"):

        engine = engine_factory()

        from lentra.core.pipeline.canonical_search_pipeline import CanonicalSearchPipeline

        pipeline = CanonicalSearchPipeline(engine)

        from lentra.core.intelligence.orchestrator import IntelligenceOrchestrator

        return IntelligenceOrchestrator(pipeline_factory=lambda: pipeline)
