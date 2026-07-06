from dataclasses import dataclass
from typing import Any

from lentra.ai_control.execution.policy.execution_policy_v1 import ExecutionPolicyV1
from lentra.ai_control.execution.ledger.execution_ledger_v1 import ExecutionLedgerV1
from lentra.core.market_intelligence.memory.market_memory_v1 import MarketMemoryV1
from lentra.core.market_intelligence.risk.risk_calibration_v1 import RiskCalibrationV1


@dataclass
class RuntimeResult:
    ok: bool
    data: Any
    error: str | None = None


class ControlledRuntimeV1:
    """
    POLICY + TRACE + MEMORY + RISK CALIBRATION LOOP
    """

    def __init__(self, execution_sandbox, git_guard):
        self.sandbox = execution_sandbox
        self.git_guard = git_guard
        self.policy = ExecutionPolicyV1()
        self.ledger = ExecutionLedgerV1()
        self.memory = MarketMemoryV1()
        self.risk = RiskCalibrationV1()

    def run(self, command: list[str], query: str, plan: dict, cwd: str = "/opt/lentra/infra") -> RuntimeResult:
        self.git_guard.ensure_clean()

        execution_id = self.ledger.create_execution_id(query, plan)

        decision = self.policy.validate(command)

        if not decision.allowed:
            return RuntimeResult(ok=False, data={"execution_id": execution_id}, error=decision.reason)

        result = self.sandbox.run(decision.normalized_command or command, cwd=cwd)

        self._emit_signals(plan, result)
        self._simulate_risk_feedback(plan)

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

    def _simulate_risk_feedback(self, plan):
        nodes = plan.get("nodes", [])

        for n in nodes:
            base_risk = 0.5

            # deterministic pseudo-feedback loop
            actual = 0.6 if "risk" in n else 0.2

            self.risk.log_event(n, base_risk, actual)
