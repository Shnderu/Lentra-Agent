import time
import redis
import json
import traceback

from core.lifecycle.task_lifecycle import TaskLifecycleEngine, TaskContext
from core.ledger.task_ledger import TaskLedger
from core.eventstore.event_store import EventStore
from core.workflow_ai.dag_generator import DAGGenerator
from core.workflow_ai.runtime.dag_optimizer import DAGOptimizer

STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"
STREAM_TRACE = "stream:rent:trace"

GROUP = "workers"
CONSUMER = "worker-1"

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

lifecycle = TaskLifecycleEngine()
ledger = TaskLedger()
events = EventStore()
dagger = DAGGenerator()
optimizer = DAGOptimizer()

try:
    r.xgroup_create(STREAM_TASKS, GROUP, id="0", mkstream=True)
except:
    pass


def trace(task_id, stage, error=""):
    r.xadd(STREAM_TRACE, {
        "task_id": task_id,
        "stage": stage,
        "error": str(error)
    })


def execute_dag(task, dag):
    results = {}

    for node in dag["nodes"]:
        node_id = node["id"]
        trace(task.task_id, f"EXEC:{node_id}")
        results[node_id] = "ok"

    return results


def process(task):
    task_id = task.task_id

    ledger.register(task_id, task.payload)
    events.append("TASK_RECEIVED", task_id, task.payload)

    ledger.transition(task_id, "enqueue")

    try:
        trace(task_id, "START")

        ledger.transition(task_id, "start")

        dag = dagger.build(task.type, task.payload)

        # -----------------------------
        # NEW: runtime optimization
        # -----------------------------
        context = {
            "validated": False,
            "fast_mode": task.payload.get("fast", False)
        }

        dag = optimizer.optimize(dag, context)

        events.append("DAG_OPTIMIZED", task_id, dag)

        trace(task_id, "DAG_EXECUTION")

        result = execute_dag(task, dag)

        r.xadd(STREAM_RESULTS, {
            "task_id": task_id,
            "status": "done",
            "data": json.dumps(result)
        })

        ledger.transition(task_id, "success")

        events.append("TASK_DONE", task_id, result)

        trace(task_id, "DONE")

    except Exception as e:
        ledger.transition(task_id, "error")

        events.append("TASK_FAILED", task_id, {"error": str(e)})

        trace(task_id, "ERROR", str(e))
        print(traceback.format_exc())


def run():
    print("WORKER STARTED (DYNAMIC DAG MODE)")

    while True:
        resp = r.xreadgroup(
            GROUP,
            CONSUMER,
            {STREAM_TASKS: ">"},
            count=1,
            block=5000
        )

        if not resp:
            continue

        for _, messages in resp:
            for msg_id, msg in messages:
                try:
                    task = TaskContext(
                        task_id=msg["task_id"],
                        type=msg["type"],
                        payload=json.loads(msg["payload"])
                    )

                    process(task)

                    r.xack(STREAM_TASKS, GROUP, msg_id)

                except Exception as e:
                    trace(msg.get("task_id"), "FATAL", str(e))


if __name__ == "__main__":
    run()
