from lentra.runtime.execution.trace import ExecutionTrace
from lentra.runtime.execution.execution_dag import ExecutionDAG
from lentra.runtime.execution.lineage import LineageTracker


class RuntimeInstrument:
    def __init__(self):
        self.trace = ExecutionTrace()
        self.dag = ExecutionDAG()
        self.lineage = LineageTracker()

    def start_task(self, task_id: str):
        self.trace.emit("task_start", {"task_id": task_id})

    def end_task(self, task_id: str):
        self.trace.emit("task_end", {"task_id": task_id})

    def link(self, a: str, b: str):
        self.dag.link(a, b)
        self.lineage.link(b, a)

    def snapshot(self):
        return {
            "trace": self.trace.get(),
            "dag": self.dag.get(),
            "lineage_root": self.lineage.get_root()
        }
