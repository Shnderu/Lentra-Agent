import subprocess
from datetime import datetime


class AiderExecutor:

    def __init__(self, repo_path="/opt/lentra/infra"):
        self.repo_path = repo_path
        self.python_bin = "/opt/lentra/infra/venv-bot/bin/python"
        self.aider_bin = "/opt/lentra/infra/venv-bot/bin/aider"

    def _run(self, cmd: str):
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=self.repo_path,
            executable="/bin/bash",
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        return result.stdout

    def git_checkpoint(self, message: str):
        ts = datetime.utcnow().isoformat()

        self._run("git add .")
        self._run(f'git commit -m "aider-checkpoint [{ts}] {message}"')

        return f"checkpoint: {message}"

    def run_aider(self, instruction: str):

        cmd = f'''
        {self.aider_bin} --message "{instruction}" --yes
        '''

        return self._run(cmd)

    def full_cycle(self, instruction: str):

        pre = self.git_checkpoint("pre-aider: " + instruction)

        result = self.run_aider(instruction)

        post = self.git_checkpoint("post-aider: " + instruction)

        return {
            "pre": pre,
            "result": result,
            "post": post
        }
