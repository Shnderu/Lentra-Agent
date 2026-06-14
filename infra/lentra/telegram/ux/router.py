from lentra.telegram.ux.keyboard import build_keyboard


def build_telegram_message(result):

    ux = result.get("ux", {})

    screen = ux.get("screen")

    if screen == "property_list":

        cards = ux.get("cards", [])

        if not cards:
            return {
                "text": "No properties found",
                "keyboard": []
            }

        text = "🏠 <b>Available properties</b>\n\n"

        keyboard = []

        for c in cards[:10]:

            text += (
                f"• <b>{c['title']}</b>\n"
                f"  {c['subtitle']}\n\n"
            )

            keyboard.append([
                {
                    "text": f"Open {c['id']}",
                    "callback_data": f"open:{c['id']}"
                },
                {
                    "text": "Save",
                    "callback_data": f"save:{c['id']}"
                }
            ])

        return {
            "text": text,
            "keyboard": keyboard
        }

    return {
        "text": "Unknown screen",
        "keyboard": []
    }
