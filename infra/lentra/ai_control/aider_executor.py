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

    def _run(self, args: list) -> str:
        cmd = [
            self.aider_path,
            "--yes",
            "--message", args[0],   # <-- КЛЮЧЕВОЕ ИЗМЕНЕНИЕ
        ]

        env = os.environ.copy()

        env.update({
            "PYTHONUNBUFFERED": "1",
            "TERM": "dumb",
            "COLORTERM": "0",
            "PAGER": "cat",
            "GIT_PAGER": "cat",
            "AIDER_NON_INTERACTIVE": "1",
        })

        process = subprocess.run(
            cmd,
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
