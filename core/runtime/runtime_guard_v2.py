import time
import traceback

"""
Runtime Guard v2
- ловит silent runtime failure
- превращает их в structured logs
"""


def safe_run(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(">>> RUNTIME ERROR (GUARD V2)")
            print(str(e))
            traceback.print_exc()

            return {
                "error": str(e),
                "status": "SAFE_FAIL"
            }
    return wrapper


if __name__ == "__main__":
    print("Runtime guard loaded")
