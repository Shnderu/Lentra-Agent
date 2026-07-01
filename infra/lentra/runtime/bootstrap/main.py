import asyncio

from lentra.runtime.bootstrap.container import build_container
from lentra.runtime.bootstrap.import_hook import install_import_hook

from lentra.api.main import create_app
from lentra.bot.main import create_bot

from lentra.core.contracts.pipeline_lock import PipelineLock
from lentra.core.graph.compiler.compiler import ArchitectureCompiler

from lentra.core.gateway.execution_entry_v1 import init as gateway_init
from lentra.bot.core.intent_router import IntentRouter
from lentra.core.scenario.scenario_engine_v1 import ScenarioEngineV1

from lentra.runtime.intelligence_gateway import get_engine


def bootstrap_runtime():
    """
    Canonical runtime bootstrap:
    - DI container
    - Graph compilation
    - API + Bot init
    - Intelligence binding
    - Gateway activation
    - System freeze
    """

    install_import_hook()

    # ---------------------------
    # 1. ARCHITECTURE GRAPH
    # ---------------------------
    graph = ArchitectureCompiler.compile()

    # ---------------------------
    # 2. DEPENDENCY CONTAINER
    # ---------------------------
    container = build_container()

    # ---------------------------
    # 3. API + BOT
    # ---------------------------
    app = create_app()
    bot = create_bot()

    container.register("api", app)
    container.register("bot", bot)

    # ---------------------------
    # 4. INTELLIGENCE ENGINE WARMUP
    # ---------------------------
    engine = get_engine()
    container.register("intelligence_engine", engine)

    # ---------------------------
    # 5. GATEWAY INIT (CORE ROUTING LAYER)
    # ---------------------------
    gateway_init(
        IntentRouter(),
        ScenarioEngineV1()
    )

    # ---------------------------
    # 6. SYSTEM FREEZE (NO MORE STRUCTURAL CHANGES)
    # ---------------------------
    PipelineLock.lock()

    print("[LENTRA] BOOTSTRAP COMPLETE")
    print("[LENTRA] GRAPH COMPILED:", bool(graph))
    print("[LENTRA] INTELLIGENCE READY:", engine is not None)

    return container


async def async_bootstrap():
    """
    Async wrapper (for future worker integration)
    """
    return bootstrap_runtime()


if __name__ == "__main__":
    bootstrap_runtime()
