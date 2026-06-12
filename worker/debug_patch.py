import json

def debug(msg):
    print("[DEBUG]", json.dumps(msg, ensure_ascii=False, default=str))
