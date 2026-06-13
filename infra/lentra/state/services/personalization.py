# ============================================================
# PATCH V16.6 - EVENT BOOST INTEGRATION
# ============================================================


class PersonalizationEngine:
    def apply(self, listings: list, session, event_signals=None):
        prefs = session.preferences or {}
        event_signals = event_signals or {}

        budget = prefs.get("budget_max")
        rooms = prefs.get("rooms")

        for l in listings:
            boost = 0

            if budget and l.get("price") <= budget:
                boost += 10

            if rooms and l.get("rooms") == rooms:
                boost += 15

            # EVENT FEEDBACK LOOP
            boost += event_signals.get(l.get("id"), 0)

            l["personalization_boost"] = boost

        return listings
