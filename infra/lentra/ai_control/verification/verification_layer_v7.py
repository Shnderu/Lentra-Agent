import os
import ast
import json
import copy
import subprocess
from typing import Dict, List, Any

from lentra.ai_control.verification.verification_layer_v2 import VerificationLayerV2


class VerificationLayerV7:
    """
    Counterfactual execution + replay-based verification system.

    Adds:
    - execution graph replay
    - counterfactual patch simulation
    - future state scoring
    - regression prediction BEFORE apply
    """

    def __init__(self, executor, graph_router, repo_root: str = "/opt/lentra"):
        self.executor = executor
        self.graph_router = graph_router
        self.repo_root = repo_root
        self.v2 = VerificationLayerV2(repo_root)

        self.history = []  # execution replay memory

    # -------------------------
    # GRAPH CONTEXT
    # -------------------------
    def _graph(self, query: str) -> Dict[str, Any]:
        try:
            return self.graph_router.route(query)
        except Exception:
            return {"selected_node": [], "selected_files": []}

    # -------------------------
    # EXECUTION REPLAY CAPTURE
    # -------------------------
    def _capture_state(self, label: str, data: Any):
        self.history.append({
            "label": label,
            "state": copy.deepcopy(data)
        })

    # -------------------------
    # CAUSAL TRACE
    # -------------------------
    def _causal(self, report: Dict[str, Any]) -> Dict[str, Any]:
        causes = []

        for f, diff in report.get("diffs", {}).items():
            if diff.get("functions", {}).get("removed"):
                causes.append(("function_removal", f))

        if report.get("cycles", {}).get("has_cycle"):
            causes.append(("cycle", "global"))

        return {"causes": causes}

    # -------------------------
    # REPLAY ENGINE (NEW CORE)
    # -------------------------
    def _replay(self, baseline_state: Dict[str, Any], patch: str) -> Dict[str, Any]:

        simulated = copy.deepcopy(baseline_state)

        # simulate patch effect (abstract)
        simulated["applied_patch"] = patch

        # simulate degradation risk
        risk = len(patch) * 0.01

        simulated["simulated_risk"] = risk

        return simulated

    # -------------------------
    # COUNTERFACTUAL SIMULATION
    # -------------------------
    def _counterfactual(self, state: Dict[str, Any]) -> Dict[str, Any]:

        scenarios = [
            {"name": "optimistic", "mult": 0.7},
            {"name": "neutral", "mult": 1.0},
            {"name": "worst_case", "mult": 1.6}
        ]

        results = []

        for s in scenarios:
            results.append({
                "scenario": s["name"],
                "risk": state.get("simulated_risk", 1.0) * s["mult"],
                "stability": 1.0 / (1.0 + state.get("simulated_risk", 1.0) * s["mult"])
            })

        return {"scenarios": results}

    # -------------------------
    # FUTURE STATE SCORING
    # -------------------------
    def _future_score(self, counterfactual: Dict[str, Any]) -> float:

        score = 0.0

        for s in counterfactual["scenarios"]:
            score += s["stability"]

        return score / len(counterfactual["scenarios"])

    # -------------------------
    # PATCH GENERATION
    # -------------------------
    def _generate(self, query: str, graph: Dict[str, Any]) -> List[str]:

        nodes = graph.get("selected_node", [])
        files = graph.get("selected_files", [])

        return [
            f"PATCH A: graph-local fix nodes={nodes} files={files} query={query}",
            f"PATCH B: dependency repair for nodes={nodes}",
            f"PATCH C: conservative rebuild for files={files}"
        ]

    # -------------------------
    # MAIN PIPELINE
    # -------------------------
    def run(self, query: str, files: List[str]) -> Dict[str, Any]:

        graph = self._graph(query)

        baseline = {
            "query": query,
            "files": files,
            "graph": graph
        }

        self._capture_state("baseline", baseline)

        result = self.executor.run(query)
        report = self.v2.verify(files)

        if report["ok"]:
            return {
                "status": "success",
                "result": result,
                "replay": self.history
            }

        causal = self._causal(report)

        candidates = self._generate(query, graph)

        evaluated = []

        for c in candidates:

            replay_state = self._replay(baseline, c)
            cf = self._counterfactual(replay_state)
            score = self._future_score(cf)

            exec_result = self.executor.run(c)
            rep = self.v2.verify(files)

            evaluated.append({
                "candidate": c,
                "future_score": score,
                "counterfactual": cf,
                "verification": rep,
                "result": exec_result,
                "causal": causal
            })

        best = max(evaluated, key=lambda x: x["future_score"])

        # commit decision logic
        if best["verification"]["ok"]:
            self._capture_state("accepted_patch", best)
            return {
                "status": "success",
                "best": best,
                "replay": self.history
            }

        self._capture_state("rejected_patch", best)

        subprocess.run(
            ["git", "checkout", "--", "."],
            cwd=self.repo_root,
            capture_output=True
        )

        return {
            "status": "failed",
            "best": best,
            "causal": causal,
            "replay": self.history
        }
