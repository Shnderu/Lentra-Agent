from __future__ import annotations

from typing import List, Dict, Any, Set, Optional


class FileScopeResolver:
    """
    Deterministic graph-based file scope resolver.

    This is the FIRST layer of AI-controlled selection:
    - no LLM
    - no repo scan explosion
    - only structural + architectural graph rules
    """

    def __init__(self):
        # lightweight architectural map (can later be replaced by graph_v2 runtime)
        self.layer_map = {
            "risk": "risk",
            "ranking": "ranking",
            "dedup": "dedup",
            "pricing": "pricing",
            "area": "area",
            "search": "search",
            "signals": "signals",
        }

    def resolve(self, target_file: str, instruction: str, context: Optional[Dict[str, Any]] = None) -> List[str]:
        scope: Set[str] = set()

        scope.add(target_file)

        layer = self._detect_layer(target_file)
        if layer:
            scope.update(self._expand_layer(layer))

        if context:
            scope.update(context.get("related_files", []))

        # instruction-driven expansion (light heuristic, not LLM)
        scope.update(self._instruction_bias(instruction))

        return list(scope)

    def _detect_layer(self, path: str) -> Optional[str]:
        for key in self.layer_map:
            if f"/{key}/" in path:
                return key
        return None

    def _expand_layer(self, layer: str) -> Set[str]:
        """
        Expand to minimal required architectural neighbors.
        """
        base = "infra/lentra/core/market_intelligence"

        expansions = {
            "risk": {
                f"{base}/risk/",
                f"{base}/contracts/",
                f"{base}/engines/",
                f"{base}/signals/",
            },
            "ranking": {
                f"{base}/ranking/",
                f"{base}/contracts/",
                f"{base}/features/",
            },
            "dedup": {
                f"{base}/dedup/",
                f"{base}/contracts/",
                f"{base}/models/",
            },
            "pricing": {
                f"{base}/pricing/",
                f"{base}/contracts/",
                f"{base}/features/",
            },
            "area": {
                f"{base}/area/",
                f"{base}/contracts/",
            },
            "search": {
                f"{base}/search/",
                f"{base}/contracts/",
            },
            "signals": {
                f"{base}/signals/",
                f"{base}/contracts/",
                f"{base}/features/",
            },
        }

        return expansions.get(layer, set())

    def _instruction_bias(self, instruction: str) -> Set[str]:
        """
        Minimal semantic hinting WITHOUT LLM.
        """
        instruction = instruction.lower()
        bias: Set[str] = set()

        if "risk" in instruction or "scam" in instruction:
            bias.add("infra/lentra/core/market_intelligence/risk/")
        if "price" in instruction or "pricing" in instruction:
            bias.add("infra/lentra/core/market_intelligence/pricing/")
        if "duplicate" in instruction:
            bias.add("infra/lentra/core/market_intelligence/dedup/")
        if "rank" in instruction:
            bias.add("infra/lentra/core/market_intelligence/ranking/")

        return bias
