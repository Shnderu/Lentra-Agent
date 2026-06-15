def safe_get_payload(event: dict):
    if not event:
        return {}

    payload = event.get("payload")

    if isinstance(payload, dict):
        return payload

    return {}
