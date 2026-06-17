from lentra.runtime.bootstrap.container import build_container
from lentra.runtime.bootstrap.import_hook import install_import_hook
from lentra.api.main import create_app
from lentra.bot.main import create_bot
from lentra.core.contracts.pipeline_lock import PipelineLock
from lentra.core.graph.compiler.compiler import ArchitectureCompiler


def main():

    install_import_hook()

    # 🔍 FULL ARCHITECTURE COMPILATION STEP
    graph = ArchitectureCompiler.compile()

    container = build_container()

    app = create_app()
    bot = create_bot()

    container.register("api", app)
    container.register("bot", bot)

    PipelineLock.lock()

    print("[LENTRA] SYSTEM STARTED")
    print("[LENTRA] architecture compiled + validated")

    return container


if __name__ == "__main__":
    main()
