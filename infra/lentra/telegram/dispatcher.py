"""
Lentra Bot Dispatcher (TRACE INSTRUMENTED v1)
"""

import logging

logging.basicConfig(level=logging.INFO)


def main():
    print("[BOT] dispatcher start")

    try:
        from lentra.core.bootstrap import get_gateway
        from lentra.core.runtime_trace_v1 import RuntimeTraceV1

        trace = RuntimeTraceV1()

        trace.enter("dispatcher")

        gateway = get_gateway()
        print("[BOT] gateway loaded:", gateway)

        trace.emit("dispatcher", "gateway_loaded", {"ok": True})

        print("[BOT] running event loop...")

        trace.exit("dispatcher")

        # snapshot dump (read-only)
        print("[TRACE SNAPSHOT]", trace.dump())

    except Exception as e:
        print("[BOT][FATAL]", str(e))
        try:
            trace.error("dispatcher", str(e))
        except:
            pass
        raise


if __name__ == "__main__":
    main()
