from dataclasses import dataclass
from typing import Any

from lentra.ai_control.execution.policy.execution_policy_v1 import ExecutionPolicyV1
from lentra.ai_control.execution.ledger.execution_ledger_v1 import ExecutionLedgerV1
from lentra.ai_control.aider_deterministic_executor import AiderDeterministicExecutor

from lentra.core.market_intelligence.memory.market_memory_v1 import MarketMemoryV1
from lentra.core.market_intelligence.risk.risk_calibration_v1 import RiskCalibrationV1


@dataclass
class RuntimeResult:
    ok: bool
    data: Any
    error: str | None = None


class ControlledRuntimeV1:
    """
    CONTROLLED EXECUTION RUNTIME

    Flow:

    Policy
        ->
    Aider executor / Sandbox
        ->
    Trace
        ->
    Memory
        ->
    Risk calibration
    """

    def __init__(
        self,
        execution_sandbox,
        git_guard
    ):
        self.sandbox = execution_sandbox
        self.git_guard = git_guard

        self.policy = ExecutionPolicyV1()
        self.ledger = ExecutionLedgerV1()

        self.aider = AiderDeterministicExecutor()

        self.memory = MarketMemoryV1()
        self.risk = RiskCalibrationV1()


    def run(
        self,
        command: list[str],
        query: str,
        plan: dict,
        cwd: str = "/opt/lentra/infra"
    ) -> RuntimeResult:

        self.git_guard.ensure_clean()

        execution_id = self.ledger.create_execution_id(
            query,
            plan
        )


        decision = self.policy.validate(command)


        if not decision.allowed:
            return RuntimeResult(
                ok=False,
                data={
                    "execution_id": execution_id
                },
                error=decision.reason
            )


        normalized = (
            decision.normalized_command
            or command
        )


        try:

            if normalized and normalized[0] == "aider":

                files = [
                    x
                    for x in normalized[1:]
                    if not x.startswith("--")
                    and x != "aider"
                ]

                execution = self.aider.run(
                    prompt=query,
                    files=files
                )

            else:

                result = self.sandbox.run(
                    normalized,
                    cwd=cwd
                )

                execution = {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "code": result.code,
                }


        except Exception as e:

            return RuntimeResult(
                ok=False,
                data={
                    "execution_id": execution_id
                },
                error=str(e)
            )


        self._emit_signals(
            plan,
            execution
        )

        self._simulate_risk_feedback(
            plan
        )


        return RuntimeResult(
            ok=True,
            data={
                "execution_id": execution_id,
                "execution": execution,
            },
        )


    def _emit_signals(
        self,
        plan,
        result
    ):
        for n in plan.get("nodes", []):
            self.memory.add_signal(
                n,
                "execution_count",
                1
            )


    def _simulate_risk_feedback(
        self,
        plan
    ):
        for n in plan.get("nodes", []):

            base_risk = 0.5

            actual = (
                0.6
                if "risk" in n
                else 0.2
            )

            self.risk.log_event(
                n,
                base_risk,
                actual
            )
