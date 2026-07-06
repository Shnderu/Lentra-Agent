import os
import subprocess
from typing import List, Dict


class AiderDeterministicExecutorV1:
    """
    Deterministic wrapper over aider execution.
    Enforces:
    - strict file scope
    - no repo expansion
    - controlled git diff boundary
    """

    def __init__(self, repo_root: str = "/opt/lentra"):
        self.repo_root = repo_root
        self.allowed_prefixes = [
            "infra/lentra/core",
            "infra/lentra/api",
            "infra/lentra/ai_control",
        ]

    # -------------------------
    # VALIDATION LAYER
    # -------------------------

    def _validate_files(self, files: List[str]) -> List[str]:
        if not files:
            raise Exception("No files provided to AiderDeterministicExecutorV1")

        safe_files = []
        for f in files:
            if not any(f.startswith(p) for p in self.allowed_prefixes):
                raise Exception(f"File outside allowed scope: {f}")
            safe_files.append(f)

        return safe_files

    # -------------------------
    # PRE-FLIGHT STATE CHECK
    # -------------------------

    def _ensure_clean_git(self):
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )
        if result.stdout.strip():
            raise Exception(
                "Working tree not clean. Commit or stash before running Aider."
            )

    # -------------------------
    # CORE EXECUTION
    # -------------------------

    def run(self, instruction: str, files: List[str]) -> Dict:
        self._ensure_clean_git()

        safe_files = self._validate_files(files)

        cmd = [
            "aider",
            "--yes",
            "--no-auto-commits",
            "--model", "claude-opus-4-8",
            "--subtree-only",
            self.repo_root,
        ]

        # inject file scope explicitly
        for f in safe_files:
            cmd.append(f)

        env = os.environ.copy()
        env["AIDER_MODEL"] = "claude-opus-4-8"

        process = subprocess.run(
            cmd,
            cwd=self.repo_root,
            env=env,
            input=instruction,
            text=True,
            capture_output=True,
        )

        if process.returncode != 0:
            raise Exception(process.stderr)

        return {
            "status": "ok",
            "files": safe_files,
            "output": process.stdout,
        }
