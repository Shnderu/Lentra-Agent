from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any, Tuple


@dataclass
class GraphIndex:
    node_index: Dict[str, dict]
    type_index: Dict[str, List[str]]
    inverted_index: Dict[str, List[str]]


class GraphSelector:
    """
    Production-grade lightweight selector.

    Strategy:
    - token overlap scoring
    - node frequency boost
    - type weighting
    - deterministic ranking
    """

    def __init__(self, index: GraphIndex):
        self.index = index

    def select(self, query: str, top_k: int = 5) -> List[str]:
        tokens = self._tokenize(query)

        if not tokens:
            return []

        candidate_scores: Dict[str, float] = {}

        # 1. inverted index match
        for t in tokens:
            if t not in self.index.inverted_index:
                continue

            for node_id in self.index.inverted_index[t]:
                candidate_scores[node_id] = candidate_scores.get(node_id, 0.0) + 1.0

        # 2. type boost (light heuristic)
        for node_id in list(candidate_scores.keys()):
            node = self.index.node_index.get(node_id, {})
            node_type = node.get("type")

            if node_type == "property":
                candidate_scores[node_id] += 0.3
            elif node_type == "geo":
                candidate_scores[node_id] += 0.2
            elif node_type == "price":
                candidate_scores[node_id] += 0.1

        # 3. normalize + sort
        ranked = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)

        return [node_id for node_id, _ in ranked[:top_k]]

    def _tokenize(self, query: str) -> List[str]:
        return [t.strip().lower() for t in query.split() if t.strip()]
