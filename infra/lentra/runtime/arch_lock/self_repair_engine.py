import os
import ast
import json
import difflib


class SelfRepairEngine:
    """
    Detects architecture violations and produces repair plans.
    Does NOT apply changes automatically.
    """

    def analyze_violation(self, file_path: str, rule: str) -> dict:
        return {
            "file": file_path,
            "violation": rule,
            "severity": "high" if "core" in file_path else "medium"
        }

    def generate_patch_plan(self, file_path: str, description: str) -> dict:
        """
        Produces git-ready patch suggestion (NOT applied).
        """

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original = f.readlines()
        except Exception:
            return {}

        # placeholder "safe rewrite suggestion"
        suggested = original[:]

        plan = difflib.unified_diff(
            original,
            suggested,
            fromfile=file_path,
            tofile=file_path + " (proposed)",
        )

        return {
            "file": file_path,
            "description": description,
            "diff": "\n".join(plan),
            "status": "proposed"
        }

    def scan_and_propose(self, violations: list) -> list:
        plans = []

        for v in violations:
            plans.append(
                self.generate_patch_plan(v["file"], v["violation"])
            )

        return plans
