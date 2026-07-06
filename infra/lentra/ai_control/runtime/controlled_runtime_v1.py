from dataclasses import dataclass
from typing import Any

from lentra.ai_control.execution.policy.execution_policy_v1 import ExecutionPolicyV1


@dataclass
class RuntimeResult:
    ok: bool
    data: Any
    error: str | None = None


class ControlledRuntimeV1:
    """
    FULL CONTROLLED RUNTIME WITH POLICY GATE
    """

    def __init__(self, execution_sandbox, git_guard):
        self.sandbox = execution_sandbox
        self.git_guard = git_guard
        self.policy = ExecutionPolicyV1()

    def run(self, command: list[str], cwd: str = "/opt/lentra/infra") -> RuntimeResult:
        self.git_guard.ensure_clean()

        decision = self.policy.validate(command)

        if not decision.allowed:
            return RuntimeResult(
                ok=False,
                data=None,
                error=f"Policy rejected execution: {decision.reason}",
            )

        result = self.sandbox.run(decision.normalized_command or command, cwd=cwd)

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
