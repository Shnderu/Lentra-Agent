import os
import subprocess


class AiderExecutor:

    def __init__(self):
        self.working_dir = "/opt/lentra"

    def _run(self, cmd: str):
        process = subprocess.Popen(
            cmd,
            cwd=self.working_dir,
            shell=True,
            executable="/bin/bash",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self._env()
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise Exception(stderr.decode("utf-8", errors="ignore"))

        return stdout.decode("utf-8", errors="ignore")

    def _env(self):
        env = os.environ.copy()

        # FIX: normalize Anthropic proxy auth for aider compatibility
        if "ANTHROPIC_AUTH_TOKEN" in env and "ANTHROPIC_API_KEY" not in env:
            env["ANTHROPIC_API_KEY"] = env["ANTHROPIC_AUTH_TOKEN"]

        # required for proxy routing
        if "ANTHROPIC_BASE_URL" in env:
            env["ANTHROPIC_BASE_URL"] = env["ANTHROPIC_BASE_URL"]

        # model routing
        env["ANTHROPIC_MODEL"] = env.get("ANTHROPIC_MODEL", "claude-opus-4-8")

        return env

    def run_aider(self, instruction: str):
        cmd = f"aider --yes --message \"{instruction}\""
        return self._run(cmd)

    def full_cycle(self, instruction: str):
        return self.run_aider(instruction)
