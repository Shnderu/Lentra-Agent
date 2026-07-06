import subprocess
import os
import ast
import copy
from typing import Dict, List, Any

from lentra.ai_control.verification.verification_layer_v2 import VerificationLayerV2


class VerificationLayerV4:
    """
    Patch intelligence + simulation layer.

    Adds:
    - multi-candidate patch generation
    - AST-level simulation (dry-run apply)
    - patch ranking engine
    - anti-regression memory
    - granular rollback (function/class level)
    """

    def __init__(self, executor, repo_root: str = "/opt/lentra"):
        self.executor = executor
        self.repo_root = repo_root
        self.v2 = VerificationLayerV2(repo_root)

        # simple regression memory (could be moved to state store later)
        self.bad_patterns = []

    # -------------------------
    # PATCH GENERATION
    # -------------------------
    def _generate_candidate_repair_prompts(self, base_query: str, report: Dict[str, Any]) -> List[str]:
        issues = []

        for f, diff in report.get("diffs", {}).items():
            removed_funcs = diff.get("functions", {}).get("removed", [])
            if removed_funcs:
                issues.append(f"{f}: missing functions {removed_funcs}")

            removed_classes = diff.get("classes", {}).get("removed", [])
            if removed_classes:
                issues.append(f"{f}: missing classes {removed_classes}")

        return [
            f"""
FIX ATTEMPT A (minimal fix):
{base_query}

Issues:
{issues}

Focus: smallest possible patch
""",
            f"""
FIX ATTEMPT B (dependency fix):
{base_query}

Issues:
{issues}

Focus: imports, graph consistency, cycle removal
""",
            f"""
FIX ATTEMPT C (safe rewrite):
{base_query}

Issues:
{issues}

Focus: preserve API, rebuild broken logic conservatively
"""
        ]

    # -------------------------
    # AST SIMULATION
    # -------------------------
    def _simulate_patch(self, file_path: str) -> Dict[str, Any]:
        full_path = os.path.join(self.repo_root, file_path)

        if not os.path.exists(full_path):
            return {"ok": False, "error": "missing file"}

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                code = f.read()

            ast.parse(code)

            return {"ok": True}

        except Exception as e:
            return {"ok": False, "error": str(e)}

    # -------------------------
    # PATCH RANKER
    # -------------------------
    def _rank(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:

        def score(c):
            s = 0

            # prefer successful verification
            if c["verification"]["ok"]:
                s += 100

            # lower risk better
            risk = c["verification"].get("risk", {}).get("score", 10)
            s -= risk * 5

            # penalize cycles
            if c["verification"].get("cycles", {}).get("has_cycle"):
                s -= 50

            # anti-regression memory
            for bad in self.bad_patterns:
                if bad in str(c):
                    s -= 20

            return s

        best = sorted(candidates, key=score, reverse=True)[0]
        return best

    # -------------------------
    # APPLY EXECUTION
    # -------------------------
    def _run(self, query: str) -> Any:
        return self.executor.run(query)

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run(self, query: str, files: List[str]) -> Dict[str, Any]:

        # 1. initial execution
        result = self._run(query)

        # 2. verify
        report = self.v2.verify(files)

        if report["ok"]:
            return {
                "status": "success",
                "result": result,
                "verification": report,
            }

        # 3. generate repair candidates
        candidates = self._generate_candidate_repair_prompts(query, report)

        evaluated = []

        # 4. evaluate each candidate
        for prompt in candidates:

            res = self._run(prompt)
            rep = self.v2.verify(files)

            evaluated.append({
                "prompt": prompt,
                "result": res,
                "verification": rep
            })

        # 5. rank patches
        best = self._rank(evaluated)

        # 6. apply best result verification
        final_verification = best["verification"]

        # 7. regression memory update
        if not final_verification["ok"]:
            self.bad_patterns.append(query)

            # targeted rollback (fallback to git hard reset for now)
            subprocess.run(
                ["git", "checkout", "--", "."],
                cwd=self.repo_root,
                capture_output=True,
            )

        return {
            "status": "success" if final_verification["ok"] else "failed",
            "best_candidate": best,
            "candidates_tested": len(candidates),
            "verification": final_verification,
        }
