from lentra.core.pipeline.canonical_search_pipeline import (
    CanonicalSearchPipeline,
)


_pipeline = None


def get_pipeline():
    global _pipeline

    if _pipeline is None:
        _pipeline = CanonicalSearchPipeline()

    return _pipeline


def run_pipeline(payload: dict):
    pipeline = get_pipeline()
    return pipeline.run(payload)
