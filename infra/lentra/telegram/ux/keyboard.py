def build_keyboard(actions):

    if not actions:
        return []

    keyboard = []

    row = []

    for a in actions:

        row.append({
            "text": a.get("text", "action"),
            "callback_data": a.get("callback_data", "noop")
        })

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return keyboard
