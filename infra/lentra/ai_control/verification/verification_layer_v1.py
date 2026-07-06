import subprocess
import ast
import os
from typing import Dict, List, Any


class VerificationLayerV1:
    """
    Post-execution safety gate for Aider output.
    """

    def __init__(self, repo_root: str = "/opt/lentra"):
        self.repo_root = repo_root

    def _get_diff(self) -> str:
        result = subprocess.run(
            ["git", "diff"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )
        return result.stdout or ""

    def _validate_python_syntax(self, files: List[str]) -> Dict[str, Any]:
        errors = []

        for f in files:
            if not f.endswith(".py"):
                continue

            path = os.path.join(self.repo_root, f)

            if not os.path.exists(path):
                errors.append({"file": f, "error": "missing file"})
                continue

            try:
                with open(path, "r", encoding="utf-8") as file:
                    ast.parse(file.read())
            except SyntaxError as e:
                errors.append({"file": f, "error": str(e)})

        return {"ok": len(errors) == 0, "errors": errors}

    def _smoke_import(self, files: List[str]) -> Dict[str, Any]:
        errors = []

        for f in files:
            if not f.endswith(".py"):
                continue

            module = f.replace("/", ".").replace(".py", "")

            try:
                __import__(module)
            except Exception as e:
                errors.append({"module": module, "error": str(e)})

        return {"ok": len(errors) == 0, "errors": errors}

    def _rollback(self):
        subprocess.run(
            ["git", "reset", "--hard"],
            cwd=self.repo_root,
            capture_output=True,
        )

    def verify(self, files: List[str]) -> Dict[str, Any]:
        diff = self._get_diff()
        syntax = self._validate_python_syntax(files)
        smoke = self._smoke_import(files)

        ok = syntax["ok"] and smoke["ok"]

        result = {
            "ok": ok,
            "diff_size": len(diff),
            "syntax": syntax,
            "smoke": smoke,
        }

        if not ok:
            self._rollback()
            result["rolled_back"] = True

        return result
