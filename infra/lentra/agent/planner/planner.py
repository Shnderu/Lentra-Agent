# ============================================================
# AGENT PLANNER V17.0
# ============================================================


class Planner:
    def build_plan(self, intent):
        plan = []

        if intent.goal == "rent_cheapest":
            plan.append("search_low_price")
            plan.append("filter_quality")
            plan.append("rank_budget")

        elif intent.goal == "rent_best":
            plan.append("search_all_sources")
            plan.append("apply_quality_filter")
            plan.append("boost_trusted")

        else:
            plan.append("standard_search")

        return plan
