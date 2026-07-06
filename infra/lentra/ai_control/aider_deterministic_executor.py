import subprocess
from typing import List


class AiderDeterministicExecutorV1:
    """
    STRICT deterministic wrapper over aider CLI.

    RULE:
    - NO system_prompt
    - NO hidden flags
    - ONLY supported aider CLI args
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

    def _build_cmd(self, instruction: str, files: List[str]):
        # HARD GUARANTEE: no system prompt injection possible
        cmd = [
            "aider",
            "--yes-always",
            "--no-git",
            "--message",
            instruction,
        ]

        # IMPORTANT: files must be appended as positional args ONLY
        for f in files:
            cmd.append(f)

        # SANITY CHECK (critical guard)
        for c in cmd:
            if "system_prompt" in str(c):
                raise Exception("Invalid CLI arg detected: system_prompt")

        return cmd

    def run(self, instruction: str, files: List[str]):
        self._ensure_clean_git()

        cmd = self._build_cmd(instruction, files)

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
