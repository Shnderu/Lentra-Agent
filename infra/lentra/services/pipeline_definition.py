from lentra.domain.search.engine import search_engine
from lentra.domain.ranking.engine import rank_engine
from lentra.domain.aggregation.engine import aggregate_engine
from lentra.core.contracts.pipeline import Pipeline, PipelineStep
from lentra.core.contracts.pipeline_lock import PipelineLock


def build_pipeline():

    pipeline = Pipeline(steps=[
        PipelineStep(
            name="search",
            handler=lambda inp, ctx: search_engine.search(inp["query"])
        ),
        PipelineStep(
            name="ranking",
            handler=lambda inp, ctx: rank_engine.rank(inp)
        ),
        PipelineStep(
            name="aggregation",
            handler=lambda inp, ctx: aggregate_engine.aggregate(inp)
        )
    ])

    PipelineLock.lock()

    return pipeline
