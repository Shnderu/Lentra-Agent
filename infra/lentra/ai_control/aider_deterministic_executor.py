import subprocess
from lentra.ai_control.execution.execution_sandbox_v1 import ExecutionSandboxV1


class AiderDeterministicExecutor:

    def __init__(self):
        self.sandbox = ExecutionSandboxV1()

    def run(self, prompt: str, files: list[str]):
        cmd = [
            "aider",
            "--yes-always",
            "--no-suggest-shell-commands",
            "--auto-commits",
        ]

        for f in files:
            cmd.append(f)

        cmd += [
            "--message",
            prompt
        ]

        result = self.sandbox.run(cmd)

        if result.code != 0:
            raise Exception(result.stderr)

        return result.stdout
