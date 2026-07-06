import json
import difflib


class EvolutionEngine:
    """
    Computes architecture evolution steps.
    """

    def propose_migration(self, old_snapshot: dict, new_snapshot: dict):
        old = json.dumps(old_snapshot, indent=2, sort_keys=True).splitlines()
        new = json.dumps(new_snapshot, indent=2, sort_keys=True).splitlines()

        diff = difflib.unified_diff(
            old,
            new,
            fromfile="previous_arch",
            tofile="next_arch",
            lineterm=""
        )

        return {
            "type": "migration_plan",
            "diff": "\n".join(diff),
            "action": "manual_review_required"
        }
