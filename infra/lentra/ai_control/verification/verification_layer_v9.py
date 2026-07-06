import time
import subprocess
from typing import Dict, List, Any

from lentra.ai_control.verification.verification_layer_v8 import VerificationLayerV8


class VerificationLayerV9:
    """
    Multi-agent verification system.

    Adds:
    - agentic scoring debate
    - graph router weight evolution
    - consensus-based patch selection
    """

    def __init__(self, executor, graph_router, repo_root: str = "/opt/lentra"):
        self.executor = executor
        self.graph_router = graph_router
        self.repo_root = repo_root

        self.v8 = VerificationLayerV8(executor, graph_router, repo_root)

        # agent registry (static initial policy)
        self.agents = {
            "risk": 1.0,
            "stability": 1.0,
            "dedup": 1.0,
            "area": 1.0,
            "causal": 1.0
        }

        # router evolution weights (NEW CORE)
        self.router_weights = {
            "risk_engine": 1.0,
            "area_engine": 1.0,
            "dedup_engine": 1.0,
            "ranking_engine": 1.0
        }

    # -------------------------
    # GRAPH ENRICHMENT
    # -------------------------
    def _graph(self, query: str) -> Dict[str, Any]:
        return self.graph_router.route(query)

    # -------------------------
    # MULTI AGENT SCORING
    # -------------------------
    def _agent_score(self, agent: str, candidate: Dict[str, Any]) -> float:

        base = candidate.get("future_score", 0.0)
        risk = candidate.get("counterfactual", {}).get("risk", 0.0)

        if agent == "risk":
            return base - risk * 2.0
        if agent == "stability":
            return base
        if agent == "dedup":
            return base - candidate.get("dedup_penalty", 0.0)
        if agent == "area":
            return base + candidate.get("area_bonus", 0.0)
        if agent == "causal":
            return base + candidate.get("causal_consistency", 0.0)

        return base

    # -------------------------
    # CONSENSUS SOLVER (game-like aggregation)
    # -------------------------
    def _consensus(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:

        scored = []

        for c in candidates:
            total = 0.0

            for agent, weight in self.agents.items():
                total += self._agent_score(agent, c) * weight

            scored.append((total, c))

        scored.sort(key=lambda x: x[0], reverse=True)

        return scored[0][1]

    # -------------------------
    # ROUTER EVOLUTION (NEW CORE)
    # -------------------------
    def _evolve_router(self, winner: Dict[str, Any]):

        nodes = winner.get("selected_node", [])

        for n in nodes:
            if n in self.router_weights:
                self.router_weights[n] *= 1.01

        # normalize drift
        total = sum(self.router_weights.values())
        for k in self.router_weights:
            self.router_weights[k] /= total

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run(self, query: str, files: List[str]) -> Dict[str, Any]:

        v8_result = self.v8.run(query, files)

        # success path
        if v8_result.get("status") == "success":
            best = v8_result["best"]
            self._evolve_router(best)

            return {
                "status": "success",
                "best": best,
                "agents": self.agents,
                "router_weights": self.router_weights,
                "trace": v8_result.get("trajectory_log", [])[-10:]
            }

        candidates = v8_result["best"]["candidate"]

        if isinstance(candidates, str):
            candidates = [candidates]

        evaluated = []

        for c in candidates:
            enriched = {
                "candidate": c,
                "future_score": v8_result["best"].get("future_score", 0.0),
                "counterfactual": v8_result["best"].get("counterfactual", {}),
                "dedup_penalty": 0.1,
                "area_bonus": 0.2,
                "causal_consistency": 0.3,
                "selected_node": v8_result["best"].get("selected_node", [])
            }
            evaluated.append(enriched)

        best = self._consensus(evaluated)

        self._evolve_router(best)

        # SAFE APPLY
        if best.get("verification", {}).get("ok", False):
            return {
                "status": "success",
                "best": best,
                "agents": self.agents,
                "router_weights": self.router_weights
            }

        subprocess.run(
            ["git", "checkout", "--", "."],
            cwd=self.repo_root,
            capture_output=True
        )

        return {
            "status": "failed",
            "best": best,
            "agents": self.agents,
            "router_weights": self.router_weights
        }
