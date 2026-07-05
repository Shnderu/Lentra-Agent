class EngineIsolator:
    """
    PHASED ARCHITECTURE CONTRACT:

    - engines MUST NOT be called directly
    - all access goes through this adapter
    """

    def __init__(self, engines: dict):
        self.engines = engines

    # -------------------------
    # PHASE 1: normalization
    # -------------------------
    def normalize_signals(self, payload: dict) -> dict:
        normalizer = self.engines.get("signal_normalizer")
        if normalizer:
            return normalizer.normalize(payload)

        # fallback passthrough
        return payload

    # -------------------------
    # ENGINE EXECUTION LAYER
    # -------------------------
    def run_all(self, payload: dict) -> dict:
        result = {}

        for name, engine in self.engines.items():

            # skip non-engine utilities
            if name in ["signal_normalizer", "decision_policy"]:
                continue

            # FIX: unified contract
            if hasattr(engine, "run"):
                result[name] = engine.run(payload)
                continue

            if callable(engine):
                result[name] = engine(payload)
                continue

            result[name] = {
                "error": f"{engine.__class__.__name__} is not callable",
                "fallback": True,
            }

        return result

    # -------------------------
    # TEMP DECISION (will be extracted in PHASE 2)
    # -------------------------
    def apply_decision(self, engine_outputs: dict) -> dict:
        decision_engine = self.engines.get("decision_policy")

        if decision_engine and hasattr(decision_engine, "evaluate"):
            return decision_engine.evaluate(engine_outputs)

        # fallback rule
        return {
            "decision": "AVOID",
            "final_score": 0.3,
            "confidence": 0.5,
            "explanation": {
                "ranking_contribution": 0.0,
                "coupling_contribution": 0.0,
                "risk_penalty": 0.0,
                "final_score": 0.3,
            },
        }
