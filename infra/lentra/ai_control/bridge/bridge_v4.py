from __future__ import annotations

import subprocess
from typing import Dict, Any

# FIX: explicit local import path consistency
from lentra.ai_control.bridge.bridge_v3 import BridgeV3
from lentra.ai_control.bridge.bridge_v4_safety import BridgeV4Safety
from lentra.ai_control.aider_deterministic_executor import AiderDeterministicExecutor


class BridgeV4:

    def __init__(self, graph_router, git_root="/opt/lentra"):
        self.graph_router = graph_router
        self.git_root = git_root

        self.safety = BridgeV4Safety()
        self.aider = AiderDeterministicExecutor(repo_root=git_root)

        # BridgeV3 MUST exist in same package layer
        self.bridge_v3 = BridgeV3(
            graph_router=graph_router,
            git_root=git_root
        )

    def run(self, query: str) -> Dict[str, Any]:

        plan = self.bridge_v3.build_plan(query)

        check = self.safety.full_check(plan.expanded_files)

        if not check.ok:
            return {
                "status": "blocked",
                "reason": check.reason,
                "plan": plan.__dict__
            }

        self._git_commit(f"bridge_v4 pre: {query}")

        try:
            result = self.aider.execute(
                instruction=plan.query,
                files=plan.expanded_files,
                system_prompt="Lentra controlled execution mode"
            )

            post_check = self.safety.full_check(plan.expanded_files)

            if not post_check.ok:
                self._rollback()
                return {
                    "status": "rolled_back",
                    "reason": post_check.reason
                }

            self._git_commit(f"bridge_v4 post: {query}")

        except Exception as e:
            self._rollback()
            return {
                "status": "error",
                "reason": str(e)
            }

        return {
            "status": "ok",
            "plan": plan.__dict__,
            "result": result
        }

    def _git_commit(self, message: str):
        subprocess.run(["git", "-C", self.git_root, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.git_root, "commit", "-m", message], check=False)

    def _rollback(self):
        subprocess.run(["git", "-C", self.git_root, "reset", "--hard", "HEAD~1"], check=False)
