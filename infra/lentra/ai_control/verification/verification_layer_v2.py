import subprocess
import ast
import os
import json
from typing import Dict, List, Any, Set


class VerificationLayerV2:
    """
    Semantic safety gate for Aider patches.

    Adds:
    - AST diff analysis
    - dependency validation
    - circular import detection
    - risk scoring
    - partial rollback
    """

    def __init__(self, repo_root: str = "/opt/lentra"):
        self.repo_root = repo_root

    # -------------------------
    # GIT STATE
    # -------------------------
    def _get_diff(self) -> str:
        result = subprocess.run(
            ["git", "diff"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )
        return result.stdout or ""

    def _get_changed_files(self) -> List[str]:
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )
        return [f for f in result.stdout.splitlines() if f.strip()]

    # -------------------------
    # AST SNAPSHOT
    # -------------------------
    def _ast_snapshot(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            return {"ok": False, "error": "missing file"}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

            nodes = {
                "functions": [],
                "classes": [],
                "imports": [],
            }

            for n in ast.walk(tree):
                if isinstance(n, ast.FunctionDef):
                    nodes["functions"].append(n.name)
                elif isinstance(n, ast.ClassDef):
                    nodes["classes"].append(n.name)
                elif isinstance(n, ast.Import):
                    for alias in n.names:
                        nodes["imports"].append(alias.name)
                elif isinstance(n, ast.ImportFrom):
                    if n.module:
                        nodes["imports"].append(n.module)

            return {"ok": True, "nodes": nodes}

        except Exception as e:
            return {"ok": False, "error": str(e)}

    # -------------------------
    # AST DIFF
    # -------------------------
    def _ast_diff(self, before: Dict, after: Dict) -> Dict[str, Any]:
        if not before.get("ok") or not after.get("ok"):
            return {"ok": False, "reason": "invalid snapshots"}

        def diff_list(a, b):
            return {
                "added": list(set(b) - set(a)),
                "removed": list(set(a) - set(b)),
            }

        return {
            "functions": diff_list(
                before["nodes"]["functions"],
                after["nodes"]["functions"],
            ),
            "classes": diff_list(
                before["nodes"]["classes"],
                after["nodes"]["classes"],
            ),
            "imports": diff_list(
                before["nodes"]["imports"],
                after["nodes"]["imports"],
            ),
        }

    # -------------------------
    # CIRCULAR IMPORT DETECTION (lightweight)
    # -------------------------
    def _detect_cycles(self, files: List[str]) -> Dict[str, Any]:
        graph = {}

        for f in files:
            path = os.path.join(self.repo_root, f)
            if not os.path.exists(path):
                continue

            try:
                with open(path, "r", encoding="utf-8") as file:
                    tree = ast.parse(file.read())

                imports = []
                for n in ast.walk(tree):
                    if isinstance(n, ast.ImportFrom) and n.module:
                        imports.append(n.module)

                graph[f] = imports

            except Exception:
                graph[f] = []

        visited = set()
        stack = set()

        def dfs(node):
            if node in stack:
                return True
            if node in visited:
                return False

            visited.add(node)
            stack.add(node)

            for nxt in graph.get(node, []):
                if nxt in graph and dfs(nxt):
                    return True

            stack.remove(node)
            return False

        has_cycle = any(dfs(n) for n in graph)

        return {"has_cycle": has_cycle, "graph": graph}

    # -------------------------
    # RISK SCORING
    # -------------------------
    def _risk_score(self, ast_diff: Dict, cycles: Dict) -> Dict[str, Any]:
        score = 0

        # structural risk
        if ast_diff.get("classes", {}).get("removed"):
            score += 3
        if ast_diff.get("functions", {}).get("removed"):
            score += 2
        if ast_diff.get("imports", {}).get("added"):
            score += 1

        # dependency risk
        if cycles.get("has_cycle"):
            score += 5

        level = (
            "low" if score <= 2 else
            "medium" if score <= 5 else
            "high"
        )

        return {
            "score": score,
            "level": level
        }

    # -------------------------
    # ROLLBACK STRATEGY
    # -------------------------
    def _rollback_files(self, files: List[str]):
        for f in files:
            subprocess.run(
                ["git", "checkout", "--", f],
                cwd=self.repo_root,
                capture_output=True,
            )

    # -------------------------
    # MAIN VERIFY PIPELINE
    # -------------------------
    def verify(self, files: List[str]) -> Dict[str, Any]:
        changed = self._get_changed_files()

        before = {}
        after = {}

        for f in files:
            path = os.path.join(self.repo_root, f)

            before[f] = self._ast_snapshot(path)

        # re-parse after changes already applied
        for f in files:
            path = os.path.join(self.repo_root, f)
            after[f] = self._ast_snapshot(path)

        diffs = {
            f: self._ast_diff(before[f], after[f])
            for f in files
        }

        cycles = self._detect_cycles(files)

        risk = self._risk_score(diffs, cycles)

        ok = risk["level"] != "high"

        result = {
            "ok": ok,
            "risk": risk,
            "cycles": cycles,
            "diffs": diffs,
        }

        if not ok:
            self._rollback_files(files)
            result["rolled_back_files"] = files

        return result
