import asyncio
from core.worker.pool import run_pool


if __name__ == "__main__":
    asyncio.run(run_pool())
