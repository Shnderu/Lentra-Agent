from lentra.core.bootstrap.bootstrap_intelligence_system import bootstrap_intelligence_system

_pipeline_instance = None


def get_pipeline():
    global _pipeline_instance

    if _pipeline_instance is None:
        _pipeline_instance = bootstrap_intelligence_system()

    return _pipeline_instance
