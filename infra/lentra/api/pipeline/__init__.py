from .search_pipeline import SearchPipeline


_pipeline = None


def get_pipeline():
    global _pipeline

    if _pipeline is None:
        _pipeline = SearchPipeline()

    return _pipeline


def run_pipeline(payload: dict):
    pipeline = get_pipeline()
    return pipeline.run(payload)
