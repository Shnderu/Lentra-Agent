from lentra.core.normalization.signal_normalization_v2 import SignalNormalizationV2


class EngineIsolator:

    def __init__(self, engines: dict):
        self.engines = engines
        self.normalizer = SignalNormalizationV2()

    def run_all(self, request: dict):

        raw = {
            "query": request.get("query"),
            "price": request.get("price"),
            "market_price": request.get("market_price"),
        }

        # STEP 1: collect engine outputs
        engine_outputs = {}

        for name, engine in self.engines.items():
            try:
                if hasattr(engine, "run"):
                    engine_outputs[name] = engine.run(raw)
                elif hasattr(engine, "process"):
                    engine_outputs[name] = engine.process(raw)
                else:
                    engine_outputs[name] = engine(raw)
            except Exception as e:
                engine_outputs[name] = {"error": str(e)}

        # STEP 2: attach raw signals
        raw.update(engine_outputs)

        # STEP 3: normalize signals (NEW LAYER)
        normalized = self.normalizer.normalize(raw)

        # STEP 4: return unified context
        return {
            "dedup": normalized["dedup"],
            "ranking": engine_outputs.get("ranking", {}),
            "risk": engine_outputs.get("risk", {}),
            "signals": {
                "pricing": normalized["pricing"],
                "area": normalized["area"],
                "coupling": normalized["coupling"]
            },
            "features": {
                "raw_context": raw
            }
        }
