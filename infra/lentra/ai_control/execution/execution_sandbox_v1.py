import subprocess
from dataclasses import dataclass


@dataclass
class ExecutionResult:
    code: int
    stdout: str
    stderr: str


class ExecutionSandboxV1:
    """
    Hard boundary between Lentra and external CLI tools.
    No system_prompt, no injected flags, only sanitized argv execution.
    """

    def __init__(self):
        self.blocked_tokens = {
            "--system_prompt",
            "system_prompt",
        }

    def _sanitize(self, cmd: list[str]) -> list[str]:
        cleaned = []
        for c in cmd:
            if any(b in c for b in self.blocked_tokens):
                continue
            cleaned.append(c)
        return cleaned

    def run(self, cmd: list[str], cwd: str = "/opt/lentra/infra") -> ExecutionResult:
        safe_cmd = self._sanitize(cmd)

        p = subprocess.Popen(
            safe_cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        out, err = p.communicate()

        return ExecutionResult(
            code=p.returncode,
            stdout=out or "",
            stderr=err or "",
        )
