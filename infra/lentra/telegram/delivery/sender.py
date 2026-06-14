import requests

BOT_TOKEN = "8963242841:AAFHQn4thrOcHGGdggiWOeiYA5OSv9jWeQE"


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    r = requests.post(url, json=payload)

    try:
        data = r.json()
    except Exception:
        return {"ok": False, "error": "bad_response"}

    if not data.get("ok"):
        print("[SEND ERROR]", data)

    return data
