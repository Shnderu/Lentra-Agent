import subprocess
import shutil
import os


class AiderExecutor:
    def __init__(self):
        self.aider_path = self._resolve_aider()

    def _resolve_aider(self) -> str:
        """
        Resolve aider binary across different runtime environments:
        - systemd
        - interactive shell
        - minimal PATH subprocess
        """
        path = shutil.which("aider")

        if path:
            return path

        # hard fallback for typical installs
        fallback_paths = [
            "/usr/local/bin/aider",
            "/usr/bin/aider",
        ]

        for p in fallback_paths:
            if os.path.exists(p):
                return p

        raise Exception("aider binary not found in PATH or known locations")

    def _run(self, cmd: list) -> str:
        """
        Execute aider via absolute path to avoid PATH issues in systemd/subprocess.
        """
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
