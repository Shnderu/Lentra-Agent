import subprocess
from typing import List


class AiderDeterministicExecutorV1:
    """
    Deterministic wrapper over aider CLI (fixed version)
    """

    def __init__(self, repo_root: str = "/opt/lentra"):
        self.repo_root = repo_root

    def _ensure_clean_git(self):
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )
        if result.stdout.strip():
            raise Exception("Working tree not clean. Commit or stash before running Aider.")

    def run(self, instruction: str, files: List[str]):
        self._ensure_clean_git()

        cmd = [
            "aider",
            "--yes-always",
            "--no-git",
            "--message", instruction,
        ]

        # IMPORTANT: only real CLI supported args
        for f in files:
            cmd.append(f)

        process = subprocess.run(
            cmd,
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )

        if process.returncode != 0:
            raise Exception(process.stderr)

        return {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "cmd": cmd,
        }
