from lentra.core.signals.signal_normalizer_v2 import SignalNormalizerV2


class EngineIsolator:
    """
    Центральный контракт:
    - вызывает engines
    - нормализует сигналы
    - НЕ содержит business logic decision/ranking
    """

    def __init__(self, engines: dict):
        self.engines = engines
        self.normalizer = SignalNormalizerV2()

    def run(self, query: str, payload: dict) -> dict:

        raw_context = {
            "query": query,
            **payload
        }

        signals = {}

        # === ENGINE CALLS (isolation layer) ===
        if "market_intelligence" in self.engines:
            try:
                signals["pricing"] = self.engines["market_intelligence"].run(raw_context)
            except Exception as e:
                signals["market_intelligence_error"] = str(e)

        if "area" in self.engines:
            try:
                signals["area"] = self.engines["area"].run(raw_context)
            except Exception as e:
                signals["area_error"] = str(e)

        if "risk" in self.engines:
            try:
                signals["risk"] = self.engines["risk"].run(raw_context)
            except Exception as e:
                signals["risk_error"] = str(e)

        # === NORMALIZATION LAYER v2 ===
        normalized = self.normalizer.normalize({
            "signals": signals,
            "risk": signals.get("risk", {})
        })

        return {
            "query": query,
            "raw_context": raw_context,
            **normalized
        }
