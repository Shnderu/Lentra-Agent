from __future__ import annotations

import os
import re
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass


# ----------------------------
# CONFIG (NO LLM REQUIRED)
# ----------------------------

DOMAIN_MAP = {
    "risk": [
        "risk", "scam", "fraud", "antiscam", "confidence"
    ],
    "pricing": [
        "price", "pricing", "market", "forecast", "valuation"
    ],
    "dedup": [
        "dedup", "duplicate", "cluster", "merge"
    ],
    "area": [
        "area", "geo", "location", "expat", "neighborhood"
    ],
    "ranking": [
        "rank", "ranking", "score", "sort"
    ],
    "pipeline": [
        "pipeline", "orchestrator", "flow", "execution"
    ],
    "graph": [
        "graph", "builder", "v2"
    ]
}


WEIGHT_KEYWORDS = {
    "exact_match": 5.0,
    "domain_hit": 2.5,
    "path_match": 3.0,
    "core_layer": 1.5
}


CORE_LAYERS = [
    "market_intelligence_engine.py",
    "decision",
    "risk",
    "ranking",
    "pricing",
    "dedup",
    "graph",
    "pipeline"
]


# ----------------------------
# INDEX (LAZY LOADED)
# ----------------------------

@dataclass
class FileNode:
    path: str
    tokens: set


class GraphIndex:
    """
    Lightweight precomputed index.
    NO full repo scan at runtime:
    only loads cached JSON.
    """

    def __init__(self, index_path: str):
        self.index_path = index_path
        self.nodes: List[FileNode] = []
        self._loaded = False

    def load(self):
        if self._loaded:
            return

        if not os.path.exists(self.index_path):
            raise RuntimeError("Graph index not found. Run build_graph_index first.")

        with open(self.index_path, "r") as f:
            raw = json.load(f)

        for item in raw:
            self.nodes.append(
                FileNode(
                    path=item["path"],
                    tokens=set(item["tokens"])
                )
            )

        self._loaded = True


# ----------------------------
# SIGNAL EXTRACTION
# ----------------------------

class SignalExtractor:

    @staticmethod
    def extract(text: str) -> Dict[str, List[str]]:
        text_l = text.lower()

        signals = {
            "tokens": set(re.findall(r"[a-z_]+", text_l)),
            "domains": []
        }

        for domain, keywords in DOMAIN_MAP.items():
            for kw in keywords:
                if kw in text_l:
                    signals["domains"].append(domain)
                    break

        return signals


# ----------------------------
# SCORER
# ----------------------------

class Scorer:

    def score(self, file: FileNode, signals: Dict) -> float:
        score = 0.0

        # token overlap
        overlap = len(file.tokens & signals["tokens"])
        score += overlap * WEIGHT_KEYWORDS["exact_match"]

        # domain boost
        for d in signals["domains"]:
            if any(d in t for t in file.tokens):
                score += WEIGHT_KEYWORDS["domain_hit"]

        # core layer boost
        if any(core in file.path for core in CORE_LAYERS):
            score += WEIGHT_KEYWORDS["core_layer"]

        # path relevance
        for t in signals["tokens"]:
            if t in file.path:
                score += WEIGHT_KEYWORDS["path_match"]

        return score


# ----------------------------
# GRAPH V2 SELECTOR
# ----------------------------

class GraphV2Selector:

    def __init__(self, index: GraphIndex):
        self.index = index
        self.extractor = SignalExtractor()
        self.scorer = Scorer()

    def select(self, instruction: str, top_k: int = 8) -> List[str]:
        self.index.load()

        signals = self.extractor.extract(instruction)

        scored: List[Tuple[str, float]] = []

        for node in self.index.nodes:
            score = self.scorer.score(node, signals)
            if score > 0:
                scored.append((node.path, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        return [p for p, _ in scored[:top_k]]


# ----------------------------
# OPTIONAL ENTRYPOINT
# ----------------------------

def build_default_selector() -> GraphV2Selector:
    base = "/opt/lentra/infra/lentra/core/market_intelligence/graph_v2/index.json"
    index = GraphIndex(base)
    return GraphV2Selector(index)
