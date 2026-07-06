from lentra.core.market_intelligence.graph_v2.signal_enricher_contract import EnrichmentResult


class SignalEnricher:
    """
    STRICT CONTRACT ENRICHER

    Rules:
    - ALWAYS accepts dict OR list input safely
    - NEVER assumes structure of graph output
    - NEVER uses .get() on unknown types
    """

    def enrich(self, query: str, graph_result):
        normalized = self._normalize(graph_result)

        nodes = normalized.get("selected_node", [])
        symbols = normalized.get("selected_symbols", [])
        files = normalized.get("selected_files", [])

        intent = self._infer_intent(nodes)

        return EnrichmentResult(
            query=query,
            nodes=nodes,
            symbols=symbols,
            files=files,
            intent=intent,
            metadata={
                "raw_type": type(graph_result).__name__
            }
        ).__dict__

    def _normalize(self, graph_result):
        """
        HARD FIX:
        GraphRouter may return:
        - dict (normal)
        - list (broken legacy path)
        """

        if isinstance(graph_result, dict):
            return graph_result

        if isinstance(graph_result, list):
            # legacy fallback normalization
            return {
                "selected_node": graph_result,
                "selected_symbols": [],
                "selected_files": []
            }

        # absolute safety fallback
        return {
            "selected_node": [],
            "selected_symbols": [],
            "selected_files": []
        }

    def _infer_intent(self, nodes):
        if not nodes:
            return None

        if "risk_engine" in nodes:
            return "risk"

        if "dedup_engine" in nodes:
            return "dedup"

        if "area_engine" in nodes:
            return "area"

        return "unknown"
