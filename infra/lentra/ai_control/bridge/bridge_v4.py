from lentra.ai_control.bridge.bridge_v3 import BridgeV3
from lentra.ai_control.execution.execution_sandbox_v1 import ExecutionSandboxV1
from lentra.ai_control.runtime.controlled_runtime_v1 import ControlledRuntimeV1
from lentra.ai_control.runtime.git_guard_v1 import GitGuardV1


class BridgeV4:
    """
    FULL TRACEABLE DETEMINISTIC PIPELINE
    """

    def __init__(self, graph_router):
        self.bridge_v3 = BridgeV3(graph_router)

        self.runtime = ControlledRuntimeV1(
            execution_sandbox=ExecutionSandboxV1(),
            git_guard=GitGuardV1(),
        )

    def run(self, query: str):
        plan = self.bridge_v3.build_plan(query)

        command = self._build_deterministic_command(plan)

        result = self.runtime.run(
            command=command,
            query=query,
            plan=plan
        )

        return {
            "plan": plan,
            "execution": result.data,
            "error": result.error,
        }

    def _build_deterministic_command(self, plan: dict) -> list[str]:
        nodes = plan.get("nodes", [])

        if "risk_engine" in nodes:
            return ["python", "-c", "print('risk_ok')"]

        if "dedup_engine" in nodes:
            return ["python", "-c", "print('dedup_ok')"]

        if "area_engine" in nodes:
            return ["python", "-c", "print('area_ok')"]

        return ["echo", "noop"]
