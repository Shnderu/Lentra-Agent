import os
import time
import json
import redis

from core.queue.streams import STREAM_TASKS
from core.lifecycle.task_lifecycle import TaskLifecycle
from core.lifecycle.execution_envelope import ExecutionEnvelope
from core.lifecycle.retry_policy import RetryPolicy
from core.lifecycle.idempotency_store import IdempotencyStore

from core.workflow.ai_workflow_engine import AIWorkflowEngine
from core.workflow.workflow_executor import WorkflowExecutor
from core.workflow.handlers import HANDLERS

from worker.handlers.rent_search import handle_rent_search


r = redis.Redis(
    host=os.getenv("REDIS_HOST", "lentra-redis"),
    port=6379,
    decode_responses=True
)

lifecycle = TaskLifecycle(r)
envelope = ExecutionEnvelope()
retry_policy = RetryPolicy()
idem = IdempotencyStore(r)

workflow_engine = AIWorkflowEngine()
executor = WorkflowExecutor()

GROUP = "workers"
CONSUMER = f"worker-{os.getenv('HOSTNAME', 'local')}"


def ensure_group():
    try:
        r.xgroup_create(STREAM_TASKS, GROUP, id="0", mkstream=True)
    except Exception:
        pass


def main():
    ensure_group()
    print("AI WORKFLOW ENGINE ACTIVE (DAG MODE)")

    while True:
        messages = r.xreadgroup(
            GROUP,
            CONSUMER,
            {STREAM_TASKS: ">"},
            count=10,
            block=5000
        )

        if not messages:
            continue

        for _, entries in messages:
            for msg_id, data in entries:

                task = envelope.build(data)

                try:
                    if idem.seen(task["idempotency_key"]):
                        lifecycle.mark_completed(task, {"skipped": "duplicate"})
                        r.xack(STREAM_TASKS, GROUP, msg_id)
                        continue

                    idem.mark(task["idempotency_key"])

                    lifecycle.mark_processing(task)

                    workflow = workflow_engine.build(task)

                    result = executor.execute(workflow, HANDLERS)

                    lifecycle.mark_completed(task, result)

                    r.xack(STREAM_TASKS, GROUP, msg_id)

                except Exception as e:
                    lifecycle.mark_failed(task, str(e))
                    r.xack(STREAM_TASKS, GROUP, msg_id)


if __name__ == "__main__":
    main()
