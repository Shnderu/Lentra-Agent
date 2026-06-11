from core.ingestion.sources.facebook import FacebookSource
from core.ingestion.sources.faswaz import FaswazSource


def load_sources():
    return {
        "facebook": FacebookSource(),
        "faswaz": FaswazSource()
    }


def select_sources(payload: dict):
    return ["facebook", "faswaz"]
