import time
from core.kernel.system_kernel import SystemKernel

class EvolutionEngine:
    """
    Self-improvement loop:
    - observes system performance
    - modifies kernel model
    - adjusts execution capabilities
    """

    def __init__(self):
        self.kernel = SystemKernel()

    # -----------------------------
    # OBSERVATION
    # -----------------------------
    def observe(self, state, trace):
        return {
            "failure_rate": self._calc_failures(trace),
            "load": state.get("tasks", 0),
            "idle": state.get("results", 0) == 0
        }

    def _calc_failures(self, trace):
        count = 0
        for t in trace[:50]:
            if "ERROR" in str(t):
                count += 1
        return count

    # -----------------------------
    # DECISION (EVOLUTION POLICY)
    # -----------------------------
    def decide_evolution(self, metrics):
        if metrics["failure_rate"] > 5:
            return "add_recovery_mode"

        if metrics["load"] > 10:
            return "enable_parallel_execution"

        if metrics["idle"]:
            return "enable_energy_saving_mode"

        return None

    # -----------------------------
    # APPLY EVOLUTION
    # -----------------------------
    def apply(self, action):
        if not action:
            return

        if action == "add_recovery_mode":
            self.kernel.evolve("auto_recovery_v2")

        if action == "enable_parallel_execution":
            self.kernel.evolve("parallel_executor")

        if action == "enable_energy_saving_mode":
            self.kernel.evolve("sleep_scheduler")

    # -----------------------------
    # LOOP
    # -----------------------------
    def run(self, state_provider, trace_provider):
        print("EVOLUTION ENGINE STARTED")

        while True:
            state = state_provider()
            trace = trace_provider()

            metrics = self.observe(state, trace)
            action = self.decide_evolution(metrics)

            print("[EVOLUTION]", metrics, "→", action)

            self.apply(action)

            time.sleep(15)


if __name__ == "__main__":
    EvolutionEngine().run()
