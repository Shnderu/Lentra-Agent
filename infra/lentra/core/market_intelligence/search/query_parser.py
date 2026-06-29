from dataclasses import dataclass
from typing import Dict, Any

from lentra.core.market_intelligence.search.parsers.query_parser import QueryParser as _QueryParser


class QueryParser:
    """
    Compatibility wrapper.

    Keeps pipeline stable while parsers layer evolves.
    """

    def __init__(self):
        self._parser = _QueryParser()

    def parse(self, query: str) -> Dict[str, Any]:
        """
        Normalize query into structured intent.
        """
        return self._parser.parse(query)

    def __call__(self, query: str) -> Dict[str, Any]:
        return self.parse(query)
