from __future__ import annotations

import os
import subprocess
from typing import List


class AiderExecutor:
    """
    Thin wrapper over aider CLI in non-interactive mode.
    """

    def __init__(self, aider_bin: str = "aider", timeout: int = 600):
        self.aider_bin = aider_bin
        self.timeout = timeout

    def full_cycle(self, instruction: str, files: List[str]) -> str:
        return self.run_aider(instruction, files)

    def run_aider(self, instruction: str, files: List[str]) -> str:
        return self._run(instruction, files)

    def _build_cmd(self, instruction: str, files: List[str]) -> List[str]:
        cmd = [
            self.aider_bin,
            "--message",
            instruction,
            "--yes-always",
            "--no-gui",
            "--no-browser",
            "--cache-prompts",
        ]

        for f in files:
            cmd.extend(["--file", f])

        return cmd

    def _run(self, instruction: str, files: List[str]) -> str:
        env = os.environ.copy()
        env["AIDER_NO_AUTO_UPGRADE"] = "1"
        env["PYTHONUNBUFFERED"] = "1"

        process = subprocess.run(
            self._build_cmd(instruction, files),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            timeout=self.timeout,
        )

        if process.returncode != 0:
            raise Exception(process.stderr)

        return process.stdout
