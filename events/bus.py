from core.redis import r
import json

CHANNEL = "flyrum_events"

def publish(event: dict):
    r.publish(CHANNEL, json.dumps(event))

def subscribe():
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL)
    return pubsub
