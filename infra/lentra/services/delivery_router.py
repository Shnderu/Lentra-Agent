from lentra.services.telegram_notifier import TelegramNotifier
import json

notifier = TelegramNotifier()
notifier.start()


def _chat_id(task):
    try:
        payload = task.get("payload", {})
        if isinstance(payload, str):
            payload = json.loads(payload)
        return payload.get("chat_id")
    except Exception:
        return None


def deliver(task, result):
    chat_id = _chat_id(task)

    if not chat_id:
        return

    text = str(result)

    try:
        notifier.send(chat_id, text)
    except Exception as e:
        print("[DELIVERY ERROR]", str(e))
