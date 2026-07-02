from fastapi import FastAPI


class IntelligenceGateway:
    def __init__(self, engines=None, graph=None):
        self.engines = engines or {}
        self.graph = graph

    def build_app(self) -> FastAPI:
        app = FastAPI()

        @app.get("/health")
        async def health():
            return {"status": "ok"}

        @app.post("/search")
        async def search(payload: dict):
            return self.handle(payload)

        return app

    # --------------------------
    # SAFE ADAPTER CORE
    # --------------------------
    def _safe_call(self, engine, payload: dict):
        """
        Normalize engine contract:
        - supports dict-based engines
        - supports legacy positional engines
        """

        if engine is None:
            return None

        try:
            # NEW STYLE (future engines)
            return engine.evaluate(payload)

        except TypeError:
            # LEGACY STYLE fallback
            return engine.evaluate(
                payload.get("price"),
                payload.get("market_price")
            )

    def handle(self, payload: dict):
        engine_outputs = {}

        for name, engine in (self.engines or {}).items():
            try:
                engine_outputs[name] = self._safe_call(engine, payload)
            except Exception as e:
                engine_outputs[name] = {"error": str(e)}

        # graph = optional enrichment layer (SAFE MODE)
        if self.graph:
            try:
                engine_outputs["graph"] = self.graph.build(engine_outputs)
            except Exception as e:
                engine_outputs["graph_error"] = str(e)

        engine_outputs["decision"] = {
            "score": 0.5,
            "verdict": "neutral",
            "mode": "safe_adapter_v1"
        }

        return engine_outputs
