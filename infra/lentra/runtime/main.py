from lentra.runtime.bootstrap.container import build_container
from lentra.api.main import create_app
from lentra.bot.main import create_bot


def main():
    container = build_container()

    app = create_app()
    bot = create_bot()

    container.register("api", app)
    container.register("bot", bot)

    print("[LENTRA] runtime started")
    print("[LENTRA] api + bot initialized")

    return container


if __name__ == "__main__":
    main()
