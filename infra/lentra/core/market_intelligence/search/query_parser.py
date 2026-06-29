from lentra.core.market_intelligence.search.parsers.query_parser import QueryParser as _QueryParser


def parse_query(query: str):
    parser = _QueryParser()
    return parser.parse(query)


class QueryParser:
    """
    Backward-compatible facade used by pipeline_definition.
    """

    def __init__(self):
        self._parser = _QueryParser()

    def parse(self, query: str):
        return self._parser.parse(query)
