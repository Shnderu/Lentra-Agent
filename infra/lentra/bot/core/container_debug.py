import traceback

def safe_call(name, fn):
    try:
        print(f"[INIT] {name}")
        return fn()
    except Exception as e:
        print(f"[INIT ERROR] {name}: {e}")
        traceback.print_exc()
        return None
import traceback

def safe_call(name, fn):
    try:
        print(f"[INIT] {name}")
        return fn()
    except Exception as e:
        print(f"[INIT ERROR] {name}: {e}")
        traceback.print_exc()
        return None
