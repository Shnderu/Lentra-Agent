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

        for p in ["/usr/local/bin/aider", "/usr/bin/aider"]:
            if os.path.exists(p):
                return p

        raise Exception("aider binary not found")

    def _run(self, cmd: list) -> str:
        full_cmd = [
            self.aider_path,
            "--yes",              # автосогласие (critical)
            "--no-git",           # отключает git-interaction (если поддерживается)
            *cmd
        ]

        env = os.environ.copy()

        # FORCE non-interactive behavior
        env["PYTHONUNBUFFERED"] = "1"
        env["AIDER_NON_INTERACTIVE"] = "1"
        env["TERM"] = "dumb"
        env["COLORTERM"] = "0"
        env["GIT_PAGER"] = "cat"
        env["PAGER"] = "cat"

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
        return self.run_aider(instruction)
