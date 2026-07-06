import subprocess
import shutil
import os


class AiderExecutor:
    def __init__(self):
        self.aider_path = self._resolve_aider()

    def _resolve_aider(self) -> str:
        path = shutil.which("aider")

        if path:
            return path

        fallback_paths = [
            "/usr/local/bin/aider",
            "/usr/bin/aider",
        ]

        for p in fallback_paths:
            if os.path.exists(p):
                return p

        raise Exception("aider binary not found")

    def _run(self, cmd: list) -> str:
        full_cmd = [self.aider_path] + cmd

        env = os.environ.copy()
        env["PATH"] = "/usr/local/bin:/usr/bin:/bin"

        process = subprocess.run(
            full_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True
        )

        if process.returncode != 0:
            raise Exception(process.stderr)

        return process.stdout

    def run_aider(self, instruction: str) -> str:
        return self._run([instruction])

    def full_cycle(self, instruction: str) -> str:
        """
        Main execution contract used by CLI layer.
        Keeps pipeline stable for future stages:
        - preprocessing (future)
        - execution (aider)
        - postprocessing (future)
        """
        return self.run_aider(instruction)
