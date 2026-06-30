import os
import sys
import asyncio
import logging
import signal
from typing import Optional


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("lentra.bootstrap")


# ----------------------------
# MODE RESOLUTION
# ----------------------------

def get_mode() -> str:
    """
    LENTRA_MODE:
      - api
      - worker
      - ingestion
    """
    return os.getenv("LENTRA_MODE", "api").lower()


# ----------------------------
# ENTRYPOINTS (lazy imports)
# ----------------------------

def run_api():
    """
    API bootstrap (FastAPI/Uvicorn entrypoint assumed external)
    """
    try:
        import uvicorn
        from lentra.runtime.main import app  # expected ASGI app
    except Exception as e:
        logger.error(f"[API] failed to import runtime app: {e}")
        sys.exit(1)

    host = os.getenv("LENTRA_API_HOST", "0.0.0.0")
    port = int(os.getenv("LENTRA_API_PORT", "8000"))

    logger.info(f"[API] starting on {host}:{port}")

    uvicorn.run(
        "lentra.runtime.main:app",
        host=host,
        port=port,
        reload=False,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )


async def run_worker():
    """
    Generic worker loop entrypoint
    """
    logger.info("[WORKER] starting event loop")

    stop_event = asyncio.Event()

    def _stop(*_):
        logger.info("[WORKER] shutdown signal received")
        stop_event.set()

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    # lazy import to avoid heavy init before fork
    try:
        from lentra.worker.loop import run_loop
    except Exception as e:
        logger.error(f"[WORKER] failed to import loop: {e}")
        sys.exit(1)

    task = asyncio.create_task(run_loop())

    await stop_event.wait()

    task.cancel()
    try:
        await task
    except Exception:
        pass

    logger.info("[WORKER] stopped cleanly")


def run_ingestion():
    """
    Batch ingestion / collectors bootstrap
    """
    logger.info("[INGESTION] starting")

    try:
        from lentra.data.ingest import run_ingest_pipeline
    except Exception as e:
        logger.error(f"[INGESTION] import failed: {e}")
        sys.exit(1)

    try:
        run_ingest_pipeline()
    except Exception as e:
        logger.error(f"[INGESTION] execution failed: {e}")
        sys.exit(1)

    logger.info("[INGESTION] finished")


# ----------------------------
# MAIN
# ----------------------------

def main():
    mode = get_mode()

    logger.info(f"[BOOTSTRAP] mode={mode}")

    if mode == "api":
        run_api()

    elif mode == "worker":
        asyncio.run(run_worker())

    elif mode == "ingestion":
        run_ingestion()

    else:
        logger.error(f"[BOOTSTRAP] unknown mode: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
