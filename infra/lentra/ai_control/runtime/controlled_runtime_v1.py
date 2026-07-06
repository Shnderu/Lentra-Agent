from dataclasses import dataclass
from typing import Any

from lentra.ai_control.execution.policy.execution_policy_v1 import ExecutionPolicyV1
from lentra.ai_control.execution.ledger.execution_ledger_v1 import ExecutionLedgerV1
from lentra.core.market_intelligence.memory.market_memory_v1 import MarketMemoryV1


@dataclass
class RuntimeResult:
    ok: bool
    data: Any
    error: str | None = None


class ControlledRuntimeV1:
    """
    POLICY + TRACE + MARKET MEMORY EMISSION
    """

    def __init__(self, execution_sandbox, git_guard):
        self.sandbox = execution_sandbox
        self.git_guard = git_guard
        self.policy = ExecutionPolicyV1()
        self.ledger = ExecutionLedgerV1()
        self.memory = MarketMemoryV1()

    def run(self, command: list[str], query: str, plan: dict, cwd: str = "/opt/lentra/infra") -> RuntimeResult:
        self.git_guard.ensure_clean()

        execution_id = self.ledger.create_execution_id(query, plan)

        decision = self.policy.validate(command)

        if not decision.allowed:
            return RuntimeResult(
                ok=False,
                data={"execution_id": execution_id},
                error=decision.reason,
            )

        result = self.sandbox.run(decision.normalized_command or command, cwd=cwd)

        # deterministic signal emission
        self._emit_signals(plan, result)

        return RuntimeResult(
            ok=True,
            data={
                "execution_id": execution_id,
                "output": result.stdout,
            },
        )

    def _emit_signals(self, plan, result):
        nodes = plan.get("nodes", [])

        for n in nodes:
            self.memory.add_signal(n, "execution_count", 1)

            if "risk" in n:
                self.memory.add_signal(n, "risk", 0.5)

            if "area" in n:
                self.memory.add_signal(n, "price", 700)
