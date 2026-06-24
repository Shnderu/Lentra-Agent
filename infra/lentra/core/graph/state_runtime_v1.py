import traceback

from lentra.core.contracts.state_contract_v1 import ExecutionStateV1
from lentra.core.trace.execution_trace_v1 import ExecutionTraceV1
from lentra.core.policy.scenario_policy_v1 import ScenarioPolicyV1
from lentra.core.graph.guards.transition_guard_v1 import TransitionGuardV1
from lentra.core.scenario.scenario_engine_v1 import scenario_engine
from lentra.core.scoring.scenario_scoring_v1 import ScenarioScoringV1
from lentra.core.conflict.conflict_resolver_v1 import ConflictResolverV1


class StateGraphRuntimeV1:

    def __init__(self):
        self.policy = ScenarioPolicyV1()
        self.guard = TransitionGuardV1()
        self.scorer = ScenarioScoringV1()
        self.conflict = ConflictResolverV1()
        self.edges = {}  # RESTORED

    # -------------------------
    # BACKWARD COMPATIBILITY FIX
    # -------------------------
    def add_edge(self, src, dst):
        if src not in self.edges:
            self.edges[src] = []
        self.edges[src].append(dst)

    def build_execution_plan(self, intent):

        candidates = intent.get("scenarios", ["default_scenario_v1"])

        scored = []
        for sc in candidates:
            scored.append({
                "name": sc,
                "score": self.scorer.score(intent, sc)
            })

        resolved = self.conflict.resolve(scored)

        return {
            "primary": resolved.get("primary", {"name": "default_scenario_v1"}),
            "secondary": resolved.get("secondary", [])
        }

    def execute_scenario(self, start_node, state, trace):

        visited = set()

        def run(node, state):

            try:
                if node in visited:
                    return state

                visited.add(node)

                if not self.policy.should_run_node(node, state):
                    return state

                before = {
                    "intent": state.intent,
                    "data": dict(state.data)
                }

                result = scenario_engine.execute(node, state)

                data = getattr(result, "data", {}) or {}
                next_nodes = getattr(result, "next", []) or []

                if isinstance(data, dict):
                    state.data.update(data)

                trace.record(
                    node=node,
                    input_state=before,
                    output_state=state.data
                )

                for nxt in next_nodes:
                    if self.guard.can_transition(node, nxt, state):
                        run(nxt, state)

                return state

            except Exception as e:

                trace.record(
                    node=node,
                    input_state={"error": str(e)},
                    output_state={"traceback": traceback.format_exc()}
                )

                raise e

        return run(start_node, state)

    def execute(self, intent, node_executor=None):

        state = ExecutionStateV1(
            intent=intent if isinstance(intent, dict) else intent.__dict__
        )

        trace = ExecutionTraceV1()

        plan = self.build_execution_plan(state.intent)

        primary = plan["primary"]["name"]

        final_state = self.execute_scenario(primary, state, trace)

        for sc in plan["secondary"]:
            if sc.get("score", 0) > 0.6:
                self.execute_scenario(sc["name"], state, trace)

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
