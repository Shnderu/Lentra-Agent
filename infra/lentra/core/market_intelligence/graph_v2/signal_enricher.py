from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class EnrichedSignal:
    query: str
    intent: str
    nodes: List[str]
    symbols: List[str]
    files: List[str]


class SignalEnricherV1:
    """
    Deterministic enrichment layer between GraphRouter and Bridge.
    Adds fallback semantic signal expansion for sparse GraphV2 outputs.
    """

    def __init__(self):
        self.intent_map = {
            "risk": {
                "keywords": ["risk", "scam", "fraud", "fake", "danger"],
                "nodes": ["risk_engine"],
                "symbols": ["RiskModule", "RiskModule.run", "RiskModule.__init__"],
                "files": [
                    "infra/lentra/core/market_intelligence/risk/risk_engine.py",
                    "infra/lentra/core/market_intelligence/risk/risk_engine_adapter.py",
                ],
            },
            "pricing": {
                "keywords": ["price", "cost", "cheap", "expensive", "budget"],
                "nodes": ["pricing_engine"],
                "symbols": ["PricingEngine", "PricingEngine.run"],
                "files": [
                    "infra/lentra/core/market_intelligence/layers/pricing/pricing.py",
                    "infra/lentra/core/market_intelligence/engines/pricing_engine.py",
                ],
            },
            "area": {
                "keywords": ["area", "location", "beach", "district", "neighborhood"],
                "nodes": ["area_engine"],
                "symbols": ["AreaEngine", "AreaScoreEngine"],
                "files": [
                    "infra/lentra/core/market_intelligence/area/area_engine.py",
                    "infra/lentra/core/market_intelligence/area/area_score_engine.py",
                ],
            },
            "dedup": {
                "keywords": ["duplicate", "same", "repeat", "copy"],
                "nodes": ["dedup_engine"],
                "symbols": ["DedupEngine", "ClusterMergeEngine"],
                "files": [
                    "infra/lentra/core/market_intelligence/dedup/dedup_engine.py",
                    "infra/lentra/core/market_intelligence/dedup/cluster_merge_engine.py",
                ],
            },
        }

    def _detect_intent(self, query: str) -> str:
        q = query.lower()

        for intent, cfg in self.intent_map.items():
            if any(k in q for k in cfg["keywords"]):
                return intent

        return "generic"

    def enrich(self, query: str, graph_result: Dict[str, Any]) -> EnrichedSignal:
        intent = self._detect_intent(query)

        nodes = list(graph_result.get("selected_node", []))
        symbols = list(graph_result.get("selected_symbols", []))
        files = list(graph_result.get("files", []))

        # Fallback enrichment if GraphV2 is empty
        if intent != "generic" and not nodes:
            nodes = self.intent_map[intent]["nodes"]

        if intent != "generic" and not symbols:
            symbols = self.intent_map[intent]["symbols"]

        if intent != "generic" and not files:
            files = self.intent_map[intent]["files"]

        return EnrichedSignal(
            query=query,
            intent=intent,
            nodes=nodes,
            symbols=symbols,
            files=files,
        )
