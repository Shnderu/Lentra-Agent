from typing import List, Dict, Any


def build_keyboard(buttons: List[Dict[str, Any]]):
    """
    Converts UX buttons → Telegram inline keyboard format
    """

    if not buttons:
        return None

    keyboard = []

    row = []

    for btn in buttons:

        row.append({
            "text": btn["text"],
            "callback_data": btn["callback_data"]
        })

        # 2 buttons per row (simple layout rule)
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return {
        "inline_keyboard": keyboard
    }
