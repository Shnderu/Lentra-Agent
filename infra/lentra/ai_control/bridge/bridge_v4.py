from lentra.ai_control.bridge.bridge_v3 import BridgeV3  # kept for graph only
from lentra.ai_control.execution.execution_sandbox_v1 import ExecutionSandboxV1
from lentra.ai_control.runtime.controlled_runtime_v1 import ControlledRuntimeV1
from lentra.ai_control.runtime.git_guard_v1 import GitGuardV1


class BridgeV4:
    """
    BridgeV4 = Pure orchestration layer

    Responsibilities:
    - interpret query → graph routing
    - send execution ONLY via ControlledRuntime
    - NO subprocess, NO CLI logic
    """

    def __init__(self, graph_router):
        self.bridge_v3 = BridgeV3(graph_router)

        self.runtime = ControlledRuntimeV1(
            execution_sandbox=ExecutionSandboxV1(),
            git_guard=GitGuardV1(),
        )

    def run(self, query: str):
        plan = self.bridge_v3.build_plan(query)

        # normalize execution request
        command = self._build_command(plan)

        result = self.runtime.run(command)

        return {
            "plan": plan,
            "execution": {
                "ok": result.ok,
                "data": result.data,
                "error": result.error,
            },
        }

    def _build_command(self, plan: dict) -> list[str]:
        """
        Convert graph plan → safe deterministic CLI command
        """
        nodes = plan.get("nodes", [])

        # minimal deterministic mapping (NO AI HERE)
        if "risk_engine" in nodes:
            return ["python", "-c", "print('risk engine safe execution')"]

        if "dedup_engine" in nodes:
            return ["python", "-c", "print('dedup safe execution')"]

        return ["python", "-c", "print('noop')"]
