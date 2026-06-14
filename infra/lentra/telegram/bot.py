# LENTRA TELEGRAM BOT - STRICT UX MODE

from lentra.ux.scenarios import run_scenario


def handle_update(intent, payload, state):

    ux = run_scenario(intent, payload, state)

    # ❗ ВАЖНО: больше НЕ делаем BEST OPTION fallback

    return {
        "telegram_text": ux.get("text", ""),
        "ux": ux
    }
