from dataclasses import dataclass
from typing import Any


@dataclass
class RuntimeResult:
    ok: bool
    data: Any
    error: str | None = None


class ControlledRuntimeV1:
    """
    SINGLE ENTRYPOINT FOR ALL EXECUTION
    NO subprocess outside sandbox adapter
    """

    def __init__(self, execution_sandbox, git_guard):
        self.sandbox = execution_sandbox
        self.git_guard = git_guard

    def run(self, command: list[str], cwd: str = "/opt/lentra/infra") -> RuntimeResult:
        self.git_guard.ensure_clean()

        result = self.sandbox.run(command, cwd=cwd)

        if result.code != 0:
            return RuntimeResult(
                ok=False,
                data=None,
                error=result.stderr,
            )

        return RuntimeResult(
            ok=True,
            data=result.stdout,
        )
