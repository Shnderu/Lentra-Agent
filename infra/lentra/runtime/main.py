from lentra.runtime.bootstrap.container import build_container
from lentra.runtime.bootstrap.import_hook import install_import_hook
from lentra.api.main import create_app
from lentra.bot.main import create_bot
from lentra.core.contracts.pipeline_lock import PipelineLock
from lentra.core.graph.compiler.compiler import ArchitectureCompiler

# 🔥 SINGLE SOURCE OF TRUTH
from app.core.gateway.execution_entry_v1 import init as gateway_init
from lentra.bot.core.intent_router import IntentRouter
from lentra.core.scenario.scenario_engine_v1 import ScenarioEngineV1


def main():

    install_import_hook()

    graph = ArchitectureCompiler.compile()

    container = build_container()

    app = create_app()
    bot = create_bot()

    container.register("api", app)
    container.register("bot", bot)

    # ======================================================
    # CLEAN GATEWAY INITIALIZATION (CRITICAL FIX)
    # ======================================================
    gateway_init(
        IntentRouter(),
        ScenarioEngineV1()
    )

    # freeze system
    PipelineLock.lock()

    print("[LENTRA] SYSTEM STARTED")
    print("[LENTRA] CLEAN ARCHITECTURE MODE ACTIVE")

    return container


if __name__ == "__main__":
    main()
