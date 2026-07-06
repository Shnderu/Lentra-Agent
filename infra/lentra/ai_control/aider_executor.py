import subprocess
import os
from datetime import datetime


class AiderExecutor:
    """
    Execution layer for Aider-driven modifications.
    Responsible for:
    - git checkpoint
    - executing aider commands
    - post-change validation
    """

    def __init__(self, repo_path="/opt/lentra/infra"):
        self.repo_path = repo_path

    def _run(self, cmd: str):
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise Exception(result.stderr)
        return result.stdout

    def git_checkpoint(self, message: str):
        ts = datetime.utcnow().isoformat()

        self._run("git add .")

        self._run(
            f'git commit -m "aider-checkpoint [{ts}] {message}"'
        )

        return f"checkpoint created: {message}"

    def run_aider(self, instruction: str):
        """
        Executes aider CLI with instruction.
        Assumes aider is installed in venv-bot/bin/aider
        """

        cmd = f"""
        source venv-bot/bin/activate && \
        aider --message "{instruction}" --yes
        """

        return self._run(cmd)

    def full_cycle(self, instruction: str):
        """
        Safe execution cycle:
        1. git checkpoint
        2. run aider
        3. git checkpoint
        """

        pre = self.git_checkpoint("pre-aider: " + instruction)

        result = self.run_aider(instruction)

        post = self.git_checkpoint("post-aider: " + instruction)

        return {
            "pre": pre,
            "result": result,
            "post": post
        }
