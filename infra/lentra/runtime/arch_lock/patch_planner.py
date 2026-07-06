from typing import List, Dict


class PatchPlanner:
    """
    ARCH LOCK v1.4 - converts violations into executable diffs
    """

    def build_plan(self, fixes: List[Dict]) -> List[Dict]:
        plan = []

        for f in fixes:
            action = f.get("action")

            if action == "replace_import":
                plan.append({
                    "type": "text_replace",
                    "search": f["from"],
                    "replace": f["to"],
                    "risk": "low"
                })

            elif action == "invert_dependency":
                plan.append({
                    "type": "architecture_refactor",
                    "strategy": "introduce_interface_layer",
                    "risk": "high"
                })

        return plan
