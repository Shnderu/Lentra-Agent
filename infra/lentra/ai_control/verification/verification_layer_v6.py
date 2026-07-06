import os
import ast
import json
import subprocess
from typing import Dict, List, Any


from lentra.ai_control.verification.verification_layer_v2 import VerificationLayerV2


class VerificationLayerV6:
    """
    Learning-based verification system.

    Adds:
    - fix success/failure memory
    - policy-weighted patch ranking
    - predictive regression avoidance
    - GraphRouter feedback loop
    """

    def __init__(self, executor, graph_router, repo_root: str = "/opt/lentra"):
        self.executor = executor
        self.graph_router = graph_router
        self.repo_root = repo_root
        self.v2 = VerificationLayerV2(repo_root)

        self.memory_file = os.path.join(repo_root, "infra/lentra/core/market_intelligence/state/fix_memory.json")

        self.memory = self._load_memory()

        # policy weights (learned over time)
        self.policy = {
            "graph_alignment": 1.5,
            "low_risk": 2.0,
            "minimal_diff": 1.2,
            "cycle_fix_bonus": 2.5,
            "historical_success": 3.0
        }

    # -------------------------
    # MEMORY
    # -------------------------
    def _load_memory(self) -> Dict[str, Any]:
        if not os.path.exists(self.memory_file):
            return {"success": [], "failure": []}

        with open(self.memory_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_memory(self):
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    # -------------------------
    # GRAPH CONTEXT
    # -------------------------
    def _graph_context(self, query: str) -> Dict[str, Any]:
        try:
            return self.graph_router.route(query)
        except Exception:
            return {"selected_node": [], "selected_files": []}

    # -------------------------
    # CAUSAL TRACE
    # -------------------------
    def _causal_trace(self, report: Dict[str, Any]) -> Dict[str, Any]:
        causes = []

        for f, diff in report.get("diffs", {}).items():
            if diff.get("functions", {}).get("removed"):
                causes.append(("function_removal", f))

            if diff.get("classes", {}).get("removed"):
                causes.append(("class_removal", f))

        if report.get("cycles", {}).get("has_cycle"):
            causes.append(("cycle", "global"))

        return {"causes": causes}

    # -------------------------
    # MEMORY SCORING
    # -------------------------
    def _memory_score(self, candidate: str) -> float:
        score = 0.0

        for s in self.memory.get("success", []):
            if s["pattern"] in candidate:
                score += self.policy["historical_success"]

        for f in self.memory.get("failure", []):
            if f["pattern"] in candidate:
                score -= self.policy["historical_success"]

        return score

    # -------------------------
    # PATCH GENERATION (POLICY-GUIDED)
    # -------------------------
    def _generate_candidates(self, query: str, report: Dict[str, Any], graph: Dict[str, Any]) -> List[str]:

        nodes = graph.get("selected_node", [])
        files = graph.get("selected_files", [])

        base_issues = []
        for f, diff in report.get("diffs", {}).items():
            if diff.get("functions", {}).get("removed"):
                base_issues.append(f"{f}: broken functions")

        return [
            f"FIX A (graph-first): nodes={nodes} files={files} query={query} issues={base_issues}",
            f"FIX B (dependency-first): restore imports and call chains for {nodes}",
            f"FIX C (safe reconstruction): minimal diff repair for {files}"
        ]

    # -------------------------
    # POLICY SCORING
    # -------------------------
    def _score_candidate(self, candidate: Dict[str, Any], report: Dict[str, Any]) -> float:

        score = 0.0

        # V2 success
        if candidate["verification"]["ok"]:
            score += 50

        # risk
        score -= candidate["verification"].get("risk", {}).get("score", 0) * 2

        # cycles
        if candidate["verification"].get("cycles", {}).get("has_cycle"):
            score -= 40

        # memory influence
        score += self._memory_score(candidate["candidate"])

        # minimal diff preference
        score -= len(str(candidate["candidate"])) * 0.01

        return score

    # -------------------------
    # UPDATE MEMORY
    # -------------------------
    def _update_memory(self, candidate: str, success: bool):
        bucket = "success" if success else "failure"

        self.memory[bucket].append({
            "pattern": candidate[:120],
            "success": success
        })

        # keep bounded memory
        self.memory[bucket] = self.memory[bucket][-200:]

        self._save_memory()

    # -------------------------
    # EXECUTION
    # -------------------------
    def run(self, query: str, files: List[str]) -> Dict[str, Any]:

        graph = self._graph_context(query)

        result = self.executor.run(query)
        report = self.v2.verify(files)

        if report["ok"]:
            self._update_memory(query, True)
            return {"status": "success", "result": result}

        causal = self._causal_trace(report)

        candidates = self._generate_candidates(query, report, graph)

        evaluated = []

        for c in candidates:

            res = self.executor.run(c)
            rep = self.v2.verify(files)

            evaluated.append({
                "candidate": c,
                "result": res,
                "verification": rep,
                "causal": causal
            })

        best = max(
            evaluated,
            key=lambda x: self._score_candidate(x, report)
        )

        success = best["verification"]["ok"]

        self._update_memory(best["candidate"], success)

        if not success:
            subprocess.run(
                ["git", "checkout", "--", "."],
                cwd=self.repo_root,
                capture_output=True
            )

        return {
            "status": "success" if success else "failed",
            "best": best,
            "graph": graph,
            "causal": causal,
            "memory_size": len(self.memory["success"]) + len(self.memory["failure"])
        }
