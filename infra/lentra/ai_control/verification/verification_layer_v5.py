import subprocess
import os
import ast
from typing import Dict, List, Any, Set

from lentra.ai_control.verification.verification_layer_v2 import VerificationLayerV2


class VerificationLayerV5:
    """
    Graph-aware patch execution layer.

    Adds:
    - AST structural patch simulation (function/class level)
    - dependency graph impact analysis
    - causal failure tracing
    - localized rollback (function/class level)
    """

    def __init__(self, executor, graph_router, repo_root: str = "/opt/lentra"):
        self.executor = executor
        self.graph_router = graph_router
        self.repo_root = repo_root
        self.v2 = VerificationLayerV2(repo_root)

    # -------------------------
    # GRAPH IMPACT ANALYSIS
    # -------------------------
    def _graph_impact(self, query: str) -> Dict[str, Any]:
        try:
            route = self.graph_router.route(query)
            return route
        except Exception:
            return {"selected_node": [], "selected_files": []}

    # -------------------------
    # CAUSAL FAILURE TRACE
    # -------------------------
    def _trace_failure(self, report: Dict[str, Any]) -> Dict[str, Any]:
        causes = []

        for file, diff in report.get("diffs", {}).items():
            if diff.get("functions", {}).get("removed"):
                causes.append({
                    "type": "function_removal",
                    "file": file,
                    "impact": "high"
                })

            if diff.get("classes", {}).get("removed"):
                causes.append({
                    "type": "class_removal",
                    "file": file,
                    "impact": "high"
                })

            if report.get("cycles", {}).get("has_cycle"):
                causes.append({
                    "type": "circular_dependency",
                    "impact": "critical"
                })

        return {"causes": causes}

    # -------------------------
    # AST FUNCTION PATCH SIMULATION
    # -------------------------
    def _extract_symbols(self, file_path: str) -> Dict[str, Set[str]]:
        full_path = os.path.join(self.repo_root, file_path)

        if not os.path.exists(full_path):
            return {}

        with open(full_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        symbols = {
            "functions": set(),
            "classes": set()
        }

        for n in ast.walk(tree):
            if isinstance(n, ast.FunctionDef):
                symbols["functions"].add(n.name)
            elif isinstance(n, ast.ClassDef):
                symbols["classes"].add(n.name)

        return symbols

    # -------------------------
    # PATCH GENERATION (GRAPH-AWARE)
    # -------------------------
    def _generate_candidates(self, query: str, report: Dict[str, Any], graph_ctx: Dict[str, Any]) -> List[str]:

        nodes = graph_ctx.get("selected_node", [])
        files = graph_ctx.get("selected_files", [])

        base_issues = []

        for f, diff in report.get("diffs", {}).items():
            if diff.get("functions", {}).get("removed"):
                base_issues.append(f"{f}: lost functions {diff['functions']['removed']}")

        return [
            f"""
PATCH A (graph-local fix):
Target nodes: {nodes}
Target files: {files}

Fix: minimal local repair only
Query: {query}
Issues: {base_issues}
""",
            f"""
PATCH B (dependency repair):
Fix graph inconsistencies:
Nodes: {nodes}

Focus: restore broken call chains and imports
Query: {query}
""",
            f"""
PATCH C (safe reconstruction):
Rebuild affected modules only:
Files: {files}

Keep API stable and preserve external contracts
Query: {query}
"""
        ]

    # -------------------------
    # LOCAL PATCH APPLY SIMULATION
    # -------------------------
    def _simulate_apply(self, file_path: str) -> Dict[str, Any]:
        full_path = os.path.join(self.repo_root, file_path)

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                ast.parse(f.read())
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # -------------------------
    # LOCAL ROLLBACK
    # -------------------------
    def _rollback(self, files: List[str]):
        for f in files:
            subprocess.run(
                ["git", "checkout", "--", f],
                cwd=self.repo_root,
                capture_output=True
            )

    # -------------------------
    # MAIN PIPELINE
    # -------------------------
    def run(self, query: str, files: List[str]) -> Dict[str, Any]:

        # 1. graph context
        graph_ctx = self._graph_impact(query)

        # 2. initial execution
        result = self.executor.run(query)

        # 3. base verification
        report = self.v2.verify(files)

        if report["ok"]:
            return {
                "status": "success",
                "result": result,
                "graph_context": graph_ctx,
                "verification": report,
            }

        # 4. causal analysis
        causal = self._trace_failure(report)

        # 5. generate candidates
        candidates = self._generate_candidates(query, report, graph_ctx)

        evaluated = []

        # 6. evaluate each candidate
        for c in candidates:

            res = self.executor.run(c)
            rep = self.v2.verify(files)

            evaluated.append({
                "candidate": c,
                "result": res,
                "verification": rep,
                "causal": causal
            })

        # 7. rank (simple heuristic V5 core)
        best = max(
            evaluated,
            key=lambda x: (
                100 if x["verification"]["ok"] else 0,
                -len(x["causal"]["causes"]),
                -x["verification"].get("risk", {}).get("score", 0),
                not x["verification"].get("cycles", {}).get("has_cycle", False)
            )
        )

        # 8. apply or rollback
        if best["verification"]["ok"]:
            return {
                "status": "success",
                "best": best,
                "graph_context": graph_ctx
            }

        # fallback rollback
        self._rollback(files)

        return {
            "status": "failed",
            "best_attempt": best,
            "graph_context": graph_ctx,
            "causal": causal
        }
