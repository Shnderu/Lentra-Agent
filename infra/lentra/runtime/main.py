from lentra.runtime.bootstrap.container import build_container
from lentra.runtime.bootstrap.import_hook import install_import_hook

from lentra.core.contracts.pipeline_lock import PipelineLock
from lentra.core.graph.compiler.compiler import ArchitectureCompiler

from lentra.api.main import create_app
from lentra.bot.main import create_bot

from lentra.core.gateway.execution_entry_v1 import init as gateway_init
from lentra.bot.core.intent_router import IntentRouter
from lentra.core.scenario.scenario_engine_v1 import ScenarioEngineV1


def main():
    # 1. import system hooks (DI / overrides / lazy import control)
    install_import_hook()

    # 2. compile architecture graph (validation layer, not execution engine)
    ArchitectureCompiler.compile()

    # 3. build DI container (single system container)
    container = build_container()

    # 4. initialize API + BOT
    app = create_app()
    bot = create_bot()

    container.register("api", app)
    container.register("bot", bot)

    # 5. CANONICAL GATEWAY (single decision entrypoint)
    gateway_init(
        IntentRouter(),
        ScenarioEngineV1()
    )

    # 6. freeze pipeline to prevent runtime mutation
    PipelineLock.lock()

    print("[LENTRA] CANONICAL RUNTIME STARTED")
    print("[LENTRA] INTELLIGENCE GATEWAY ACTIVE")
    print("[LENTRA] MARKET INTELLIGENCE OS CONNECTED")

    return container


if __name__ == "__main__":
    main()
