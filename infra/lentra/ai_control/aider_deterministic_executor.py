import subprocess
import shlex

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


    def _changed_files(self):
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

        files = []

        for line in result.stdout.splitlines():
            if len(line) > 3:
                files.append(line[3:])

        return files


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
                "--message-file",
                "/tmp/lentra_aider_message.txt"
            ]
        )


        with open(
            "/tmp/lentra_aider_message.txt",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(prompt)


        result = self.sandbox.run(
            cmd,
            cwd="/opt/lentra"
        )


        output = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "before_commit": before,
            "after_commit": self._git_hash(),
            "changed_files": self._changed_files(),
        }


        if result.code != 0:
            raise Exception(result.stderr)


        allowed = set(files)

        output["changed"] = any(
            x in allowed
            for x in output["changed_files"]
        )


        return output
