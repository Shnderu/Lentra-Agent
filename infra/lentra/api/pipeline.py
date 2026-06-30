# IMPORTANT: API must NOT construct graph

from lentra.core.bootstrap import bootstrap_intelligence_system

pipeline = bootstrap_intelligence_system()


def get_pipeline():
    return pipeline
