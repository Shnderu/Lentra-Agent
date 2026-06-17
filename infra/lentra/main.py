from lentra.api.main import create_app
from lentra.bot.main import create_bot


def bootstrap():
    app = create_app()
    bot = create_bot()

    return {
        "api": app,
        "bot": bot
    }


if __name__ == "__main__":
    system = bootstrap()
    print("[LENTRA] system booted")
