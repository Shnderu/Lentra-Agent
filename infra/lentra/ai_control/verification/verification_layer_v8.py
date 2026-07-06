import copy
import math
import time
import subprocess
from typing import Dict, List, Any

from lentra.ai_control.verification.verification_layer_v7 import VerificationLayerV7


class VerificationLayerV8:
    """
    Policy-learning verification layer.

    Extends V7 with:
    - trajectory learning
    - reward assignment
    - policy scoring model
    - adaptive patch ranking
    """

    def __init__(self, executor, graph_router, repo_root: str = "/opt/lentra"):
        self.executor = executor
        self.graph_router = graph_router
        self.repo_root = repo_root

        self.v7 = VerificationLayerV7(executor, graph_router, repo_root)

        # learning memory
        self.trajectory_log: List[Dict[str, Any]] = []
        self.policy_weights = {
            "risk": 1.0,
            "stability": 1.0,
            "causal_penalty": 1.0
        }

    # -------------------------
    # GRAPH CONTEXT
    # -------------------------
    def _graph(self, query: str) -> Dict[str, Any]:
        return self.graph_router.route(query)

    # -------------------------
    # TRAJECTORY BUILDER (NEW CORE)
    # -------------------------
    def _build_trajectory(self, candidate: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "candidate": candidate["candidate"],
            "future_score": candidate.get("future_score", 0.0),
            "verification_ok": candidate.get("verification", {}).get("ok", False),
            "risk": candidate.get("counterfactual", {}).get("scenarios", [{}])[0].get("risk", 0.0),
            "timestamp": time.time()
        }

    # -------------------------
    # REWARD FUNCTION (NEW CORE)
    # -------------------------
    def _reward(self, traj: Dict[str, Any]) -> float:

        reward = 0.0

        # correctness
        reward += 2.0 if traj["verification_ok"] else -2.0

        # stability preference
        reward += traj["future_score"] * self.policy_weights["stability"]

        # risk penalty
        reward -= traj["risk"] * self.policy_weights["risk"]

        return reward

    # -------------------------
    # POLICY SCORER (NEW CORE)
    # -------------------------
    def _policy_score(self, candidate: Dict[str, Any]) -> float:

        traj = self._build_trajectory(candidate)
        reward = self._reward(traj)

        return reward

    # -------------------------
    # UPDATE POLICY (NEW CORE)
    # -------------------------
    def _update_policy(self, trajectory: Dict[str, Any]):

        self.trajectory_log.append(trajectory)

        # simple adaptive weighting (heuristic learning)
        if trajectory["verification_ok"]:
            self.policy_weights["stability"] *= 1.01
        else:
            self.policy_weights["risk"] *= 1.02

    # -------------------------
    # PATCH RANKING v2
    # -------------------------
    def _rank(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:

        scored = []

        for c in candidates:
            score = self._policy_score(c)
            scored.append((score, c))

        scored.sort(key=lambda x: x[0], reverse=True)

        return scored[0][1]

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run(self, query: str, files: List[str]) -> Dict[str, Any]:

        v7_result = self.v7.run(query, files)

        if v7_result["status"] == "success":
            self._update_policy(self._build_trajectory(v7_result["best"]))
            return v7_result

        candidates = v7_result["best"]["candidate"]

        # normalize
        if isinstance(candidates, str):
            candidates = [candidates]

        evaluated = []

        for c in candidates:

            simulated = {
                "candidate": c,
                "future_score": v7_result["best"].get("future_score", 0.0),
                "verification": v7_result["best"].get("verification", {}),
                "counterfactual": v7_result["best"].get("counterfactual", {})
            }

            evaluated.append(simulated)

        best = self._rank(evaluated)

        traj = self._build_trajectory(best)
        self._update_policy(traj)

        if best.get("verification", {}).get("ok", False):
            return {
                "status": "success",
                "best": best,
                "policy": self.policy_weights,
                "trajectory_log": self.trajectory_log[-10:]
            }

        subprocess.run(
            ["git", "checkout", "--", "."],
            cwd=self.repo_root,
            capture_output=True
        )

        return {
            "status": "failed",
            "best": best,
            "policy": self.policy_weights,
            "trajectory_log": self.trajectory_log[-10:]
        }
