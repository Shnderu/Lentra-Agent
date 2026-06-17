from lentra.runtime.bootstrap.container import build_container
from lentra.runtime.bootstrap.import_hook import install_import_hook
from lentra.api.main import create_app
from lentra.bot.main import create_bot
from lentra.core.contracts.pipeline_lock import PipelineLock


def main():
    install_import_hook()

    container = build_container()

    app = create_app()
    bot = create_bot()

    container.register("api", app)
    container.register("bot", bot)

    # 🔒 FINAL SEAL
    PipelineLock.lock()

    print("[LENTRA] runtime started (SEALED MODE)")
    print("[LENTRA] system is now immutable")

    return container


if __name__ == "__main__":
    main()
