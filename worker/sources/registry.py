from .faswaz import FaswazSource
from .facebook import FacebookSource

SOURCES = [
    FaswazSource(),
    FacebookSource()
]


def run_all_sources(query: dict):
    results = []

    for source in SOURCES:
        try:
            data = source.search(query)
            results.extend(data)
        except Exception as e:
            print(f"[SOURCE ERROR] {source.name}: {e}")

    return results
