# ============================================================
# AGENT DECIDER V17.0
# ============================================================


class Decider:
    def choose_action(self, plan_step, context):
        if plan_step == "search_low_price":
            return {"action": "search", "mode": "price_asc"}

        if plan_step == "apply_quality_filter":
            return {"action": "filter", "threshold": 60}

        if plan_step == "boost_trusted":
            return {"action": "rank", "boost": "trust"}

        return {"action": "search"}
