import subprocess
import os
from typing import Dict, List, Any

from lentra.ai_control.verification.verification_layer_v2 import VerificationLayerV2


class VerificationLayerV3:
    """
    Agentic repair loop over V2 verification.

    Adds:
    - automatic repair attempts
    - iterative Aider re-run
    - failure-driven prompt refinement
    - bounded recovery loop (max iterations)
    """

    def __init__(self, executor, repo_root: str = "/opt/lentra", max_iters: int = 3):
        self.executor = executor
        self.repo_root = repo_root
        self.max_iters = max_iters
        self.v2 = VerificationLayerV2(repo_root)

    # -------------------------
    # FAILURE ANALYSIS
    # -------------------------
    def _build_repair_prompt(self, base_query: str, report: Dict[str, Any]) -> str:
        issues = []

        risk = report.get("risk", {})
        cycles = report.get("cycles", {})

        if risk.get("level") == "high":
            issues.append(f"High risk score: {risk.get('score')}")

        if cycles.get("has_cycle"):
            issues.append("Circular import detected")

        for f, diff in report.get("diffs", {}).items():
            removed_funcs = diff.get("functions", {}).get("removed", [])
            removed_classes = diff.get("classes", {}).get("removed", [])

            if removed_funcs:
                issues.append(f"{f}: removed functions {removed_funcs}")
            if removed_classes:
                issues.append(f"{f}: removed classes {removed_classes}")

        return f"""
REPAIR TASK:

Original request:
{base_query}

Detected issues:
{chr(10).join('- ' + i for i in issues)}

Rules:
- DO NOT change unrelated modules
- ONLY fix broken logic
- Preserve API compatibility
- Remove circular dependencies if any
- Ensure risk engine / dedup / ranking stability

Return minimal safe patch only.
"""

    # -------------------------
    # RUN SINGLE EXECUTION
    # -------------------------
    def _run_once(self, query: str) -> Any:
        return self.executor.run(query)

    # -------------------------
    # VERIFY WRAPPER
    # -------------------------
    def _verify(self, files: List[str]) -> Dict[str, Any]:
        return self.v2.verify(files)

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run(self, query: str, files: List[str]) -> Dict[str, Any]:

        attempt = 0
        last_report = None
        last_result = None

        while attempt < self.max_iters:

            # 1. run aider
            result = self._run_once(query)

            # 2. verify
            report = self._verify(files)

            last_report = report
            last_result = result

            # 3. success case
            if report.get("ok"):
                return {
                    "status": "success",
                    "attempts": attempt + 1,
                    "result": result,
                    "verification": report,
                }

            # 4. build repair prompt
            query = self._build_repair_prompt(query, report)

            attempt += 1

        # final failure → rollback handled by v2
        return {
            "status": "failed",
            "attempts": self.max_iters,
            "last_result": last_result,
            "last_verification": last_report,
        }
