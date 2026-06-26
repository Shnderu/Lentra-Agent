import asyncio
from lentra.core.di.container import build_container


async def main():
    container = build_container()

    flow = container["flow_glue"]
    engine = container["execution_engine"]

    print("[WORKER] STARTED OK")

    result = engine.run(flow)

    print("[WORKER] RESULT:", result)

    return result


if __name__ == "__main__":
    asyncio.run(main())
