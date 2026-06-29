import traceback

from lentra.core.contracts.state_contract_v1 import ExecutionStateV1
from lentra.core.trace.execution_trace_v1 import ExecutionTraceV1
from lentra.core.policy.scenario_policy_v1 import ScenarioPolicyV1
from lentra.core.graph.guards.transition_guard_v1 import TransitionGuardV1
from lentra.core.scoring.scenario_scoring_v1 import ScenarioScoringV1
from lentra.core.conflict.conflict_resolver_v1 import ConflictResolverV1

from lentra.scenarios.registry import scenario_registry


class StateGraphRuntimeV1:

    def __init__(self):
        self.policy = ScenarioPolicyV1()
        self.guard = TransitionGuardV1()
        self.scorer = ScenarioScoringV1()
        self.conflict = ConflictResolverV1()
        self.edges = {}

    def add_edge(self, src, dst):
        if src not in self.edges:
            self.edges[src] = []
        self.edges[src].append(dst)

    def build_execution_plan(self, intent):

        candidates = intent.get(
            "scenarios",
            ["default_scenario_v1"]
        )

        scored = []

        for sc in candidates:
            scored.append(
                {
                    "name": sc,
                    "score": self.scorer.score(intent, sc)
                }
            )

        resolved = self.conflict.resolve(scored)

        return {
            "primary": resolved.get(
                "primary",
                {"name": "default_scenario_v1"}
            ),
            "secondary": resolved.get(
                "secondary",
                []
            )
        }

    def execute_scenario(self, start_node, state, trace):

        visited = set()

        def run(node):

            try:
                if node in visited:
                    return

                visited.add(node)

                if not self.policy.should_run_node(node, state):
                    return

                before = {
                    "intent": state.intent,
                    "data": dict(state.data)
                }

                handler = scenario_registry.get(node)

                if handler is None:
                    raise Exception(f"Scenario not found in registry: {node}")

                result = handler.execute(state)

                data = getattr(result, "data", {}) or {}
                next_nodes = getattr(result, "next", []) or []

                if isinstance(data, dict):
                    state.data.update(data)

                trace.record(
                    node=node,
                    input_state=before,
                    output_state=dict(state.data)
                )

                for nxt in next_nodes:
                    if self.guard.can_transition(node, nxt, state):
                        run(nxt)

            except Exception:
                trace.record(
                    node=node,
                    input_state={"error": "execution_failed"},
                    output_state={"traceback": traceback.format_exc()}
                )
                raise

        run(start_node)

        return state

    def execute(self, intent, node_executor=None):

        state = ExecutionStateV1(
            intent=intent if isinstance(intent, dict) else intent.__dict__
        )

        trace = ExecutionTraceV1()

        plan = self.build_execution_plan(state.intent)

        primary = plan["primary"]["name"]

        final_state = self.execute_scenario(primary, state, trace)

        executed_nodes = {
            item["node"]
            for item in trace.export()
        }

        for sc in plan["secondary"]:
            scenario_name = sc["name"]

            if sc.get("score", 0) <= 0.6:
                continue

            if scenario_name in executed_nodes:
                continue

            self.execute_scenario(scenario_name, state, trace)

        return {
            "entry": primary,
            "plan": plan,
            "trace": trace.export(),
            "state": {
                "intent": final_state.intent,
                "data": final_state.data
            }
        }


state_graph_runtime = StateGraphRuntimeV1()
