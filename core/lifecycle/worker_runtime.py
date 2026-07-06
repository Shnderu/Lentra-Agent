import asyncio
import time
import logging

from core.lifecycle.execution_envelope import ExecutionEnvelope

log = logging.getLogger("lentra.worker")


class WorkerRuntime:
    """
    SHIM worker runtime (safe mode)

    - no architecture changes
    - no dependency on queues yet
    - keeps process alive
    - prepares hook for future event bus
    """

    def __init__(self):
        self.envelope = ExecutionEnvelope()
        self.running = True

    async def process_fake_task(self):
        """
        Temporary loop placeholder.
        Will be replaced by DB queue consumer in Step B.
        """
        task = {
            "task_id": "heartbeat",
            "type": "system.ping",
            "payload": {"ts": time.time()},
            "retry": 0,
        }

        wrapped = self.envelope.build(task)
        log.info(f"[worker] heartbeat: {wrapped['idempotency_key']}")

    async def run(self):
        log.info("[worker] runtime started")

        while self.running:
            try:
                await self.process_fake_task()
                await asyncio.sleep(5)
            except Exception as e:
                log.exception(f"[worker] error: {e}")
                await asyncio.sleep(2)


def main():
    runtime = WorkerRuntime()
    asyncio.run(runtime.run())


if __name__ == "__main__":
    main()
