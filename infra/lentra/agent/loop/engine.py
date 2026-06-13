# ============================================================
# AUTONOMOUS LOOP ENGINE V17.1
# ============================================================

import asyncio


class AutonomousLoop:
    def __init__(self, handler, market_state, price_tracker, alert_engine):
        self.handler = handler
        self.market_state = market_state
        self.price_tracker = price_tracker
        self.alert_engine = alert_engine

    async def run_cycle(self, query):
        result = await self.handler.handle({
            "id": "loop",
            "type": "search_rent",
            "payload": query,
        })

        listings = result.get("results", [])

        alerts = []

        for l in listings:
            old = self.market_state.get_previous(l["id"])
            change = self.price_tracker.detect_change(old, l)

            if change:
                alerts.append(self.alert_engine.generate(change))

            self.market_state.update(l)

        return {
            "listings": listings,
            "alerts": alerts,
            "mode": "v17_autonomous"
        }
