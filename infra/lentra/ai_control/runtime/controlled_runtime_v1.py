from dataclasses import dataclass
from typing import Any

from lentra.ai_control.execution.policy.execution_policy_v1 import ExecutionPolicyV1
from lentra.ai_control.execution.ledger.execution_ledger_v1 import ExecutionLedgerV1


@dataclass
class RuntimeResult:
    ok: bool
    data: Any
    error: str | None = None


class ControlledRuntimeV1:
    """
    POLICY + TRACE ENABLED RUNTIME
    """

    def __init__(self, execution_sandbox, git_guard):
        self.sandbox = execution_sandbox
        self.git_guard = git_guard
        self.policy = ExecutionPolicyV1()
        self.ledger = ExecutionLedgerV1()

    def run(self, command: list[str], query: str, plan: dict, cwd: str = "/opt/lentra/infra") -> RuntimeResult:
        self.git_guard.ensure_clean()

        execution_id = self.ledger.create_execution_id(query, plan)

        trace_policy = self.ledger.create_trace(execution_id, "policy_input", {
            "command": command
        })

        decision = self.policy.validate(command)

        trace_policy["data"]["decision"] = decision.__dict__

        if not decision.allowed:
            return RuntimeResult(
                ok=False,
                data={
                    "execution_id": execution_id,
                    "trace": trace_policy
                },
                error=decision.reason,
            )

        trace_runtime_start = self.ledger.create_trace(execution_id, "runtime_start", {
            "command": command
        })

        result = self.sandbox.run(decision.normalized_command or command, cwd=cwd)

        trace_runtime_end = self.ledger.create_trace(execution_id, "runtime_end", {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.code
        })

        if result.code != 0:
            return RuntimeResult(
                ok=False,
                data={
                    "execution_id": execution_id,
                    "trace": [trace_policy, trace_runtime_start, trace_runtime_end]
                },
                error=result.stderr,
            )

        return RuntimeResult(
            ok=True,
            data={
                "execution_id": execution_id,
                "output": result.stdout,
                "trace": [trace_policy, trace_runtime_start, trace_runtime_end]
            },
        )
