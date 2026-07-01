class OutputAssembler:

    def build(self, context: dict) -> dict:

        ui = context.get("ui", {})
        api = context.get("api", {})
        meta = context.get("meta", {})

        # STRICT: no recomputation, no overrides
        return {
            "ui": {
                "price": ui.get("price"),
                "market_price": ui.get("market_price"),
                "deviation_pct": ui.get("deviation_pct"),
                "risk_level": ui.get("risk_level"),
                "duplicates": ui.get("duplicates"),
                "verdict": ui.get("verdict"),  # PASS-THROUGH ONLY
            },
            "api": api,
            "meta": meta
        }
