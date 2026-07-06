from typing import List, Dict


class RemediationEngine:
    """
    ARCH LOCK v1.3 - generates fixes for violations
    """

    def suggest_fixes(self, violations: List[str]) -> List[Dict]:
        fixes = []

        for v in violations:
            if "NO_RUNTIME_IMPORT_IN_CORE" in v:
                fixes.append({
                    "violation": v,
                    "action": "replace_import",
                    "from": "lentra.runtime.",
                    "to": "lentra.services.runtime."
                })

            if "NO_API_TO_CORE_BACKFLOW" in v:
                fixes.append({
                    "violation": v,
                    "action": "invert_dependency",
                    "strategy": "introduce interface layer"
                })

        return fixes
