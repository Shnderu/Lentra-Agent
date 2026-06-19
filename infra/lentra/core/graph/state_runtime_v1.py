import traceback

from lentra.core.contracts.state_contract_v1 import ExecutionStateV1
from lentra.core.trace.execution_trace_v1 import ExecutionTraceV1
from lentra.core.policy.scenario_policy_v1 import ScenarioPolicyV1
from lentra.core.graph.guards.transition_guard_v1 import TransitionGuardV1
from lentra.core.scoring.scenario_scoring_v1 import ScenarioScoringV1
from lentra.core.conflict.conflict_resolver_v1 import ConflictResolverV1


class StateGraphRuntimeV1:

    def __init__(self):
        self.edges = {}
        self.policy = ScenarioPolicyV1()
        self.guard = TransitionGuardV1()
        self.scorer = ScenarioScoringV1()
        self.conflict = ConflictResolverV1()

    def add_edge(self, src, dst):

        if src not in self.edges:
            self.edges[src] = []

        self.edges[src].append(dst)

    def score_scenarios(self, intent):

        candidates = intent.get("scenarios", ["default_scenario_v1"])

        scored = []

        for sc in candidates:
            scored.append({
                "name": sc,
                "score": self.scorer.score(intent, sc)
            })

        return scored

    def select_execution_plan(self, intent):

        scored = self.score_scenarios(intent)
        return self.conflict.resolve(scored)

    def execute_scenario(self, start_node, state, node_executor, trace):

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

                result = node_executor.execute(node, state)

                state.merge(result)

                trace.record(
                    node=node,
                    input_state=before,
                    output_state=state.data
                )

                next_nodes = result.get("next", [])

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

    def execute(self, intent, node_executor):

        state = ExecutionStateV1(
            intent=intent if isinstance(intent, dict) else intent.__dict__
        )

        trace = ExecutionTraceV1()

        # -------------------------
        # NEW: execution plan
        # -------------------------
        plan = self.select_execution_plan(state.intent)

        primary = plan["primary"]["name"] if plan["primary"] else "default_scenario_v1"

        # execute primary
        final_state = self.execute_scenario(
            primary,
            state,
            node_executor,
            trace
        )

        # execute secondary (light execution)
        for sc in plan["secondary"]:
            if sc["score"] > 0.6:
                self.execute_scenario(
                    sc["name"],
                    state,
                    node_executor,
                    trace
                )

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
