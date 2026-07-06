from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class GraphIndex:
    node_index: Dict[str, dict]
    type_index: Dict[str, List[str]]
    inverted_index: Dict[str, List[str]]


def build_graph_index() -> GraphIndex:
    """
    PURE INDEX BUILDER (NO RUNTIME DEPENDENCIES)

    IMPORTANT:
    - must NOT import engines
    - must NOT import risk layer
    - must NOT import DI runtime

    Only static graph extraction.
    """

    # TODO: replace with real graph loader later
    # for now we enforce safe bootstrap mode

    node_index: Dict[str, dict] = {}
    type_index: Dict[str, List[str]] = {}
    inverted_index: Dict[str, List[str]] = {}

    # SAFE BOOTSTRAP SAMPLE (temporary)
    # ensures selector is testable immediately

    seed_nodes = [
        {"id": "studio_beach", "type": "property", "text": "studio near beach"},
        {"id": "budget_700", "type": "price", "text": "under 700"},
        {"id": "location_beach", "type": "geo", "text": "near beach"},
    ]

    for n in seed_nodes:
        node_index[n["id"]] = n

        t = n["type"]
        type_index.setdefault(t, []).append(n["id"])

        for token in n["text"].lower().split():
            inverted_index.setdefault(token, []).append(n["id"])

    return GraphIndex(
        node_index=node_index,
        type_index=type_index,
        inverted_index=inverted_index,
    )
