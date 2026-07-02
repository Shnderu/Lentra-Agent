from .safe_executor import safe_execute


class IntelligenceGateway:

    def handle(self, payload):
        engine_outputs = {}

        for name, engine in self.engines.items():
            engine_outputs[name] = safe_execute(engine, payload)

        return {
            "engines": engine_outputs,
            "status": "ok"
        }
