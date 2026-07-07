import subprocess

from lentra.ai_control.execution.execution_sandbox_v1 import ExecutionSandboxV1


class AiderDeterministicExecutor:

    def __init__(self):
        self.sandbox = ExecutionSandboxV1()


    def _git_hash(self):

        result = subprocess.run(
            [
                "git",
                "rev-parse",
                "HEAD"
            ],
            cwd="/opt/lentra",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return result.stdout.strip()


    def _has_changes(self):

        result = subprocess.run(
            [
                "git",
                "status",
                "--porcelain"
            ],
            cwd="/opt/lentra",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return bool(result.stdout.strip())


    def run(
        self,
        prompt: str,
        files: list[str]
    ):

        before = self._git_hash()


        cmd = [
            "aider",
            "--yes-always",
            "--no-suggest-shell-commands",
            "--auto-commits",
        ]


        for file in files:
            cmd.extend(
                [
                    "--file",
                    file
                ]
            )


        cmd.extend(
            [
                "--message",
                prompt
            ]
        )


        result = self.sandbox.run(
            cmd,
            cwd="/opt/lentra"
        )


        if result.code != 0:
            raise Exception(
                result.stderr
            )


        after = self._git_hash()


        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "before_commit": before,
            "after_commit": after,
            "changed": self._has_changes(),
        }
