import time

def trace_gateway_call(gateway):
    def wrapped(payload):
        t0 = time.time()

        try:
            result = gateway.handle(payload)

            return {
                "result": result,
                "_trace": {
                    "ms": time.time() - t0,
                    "status": "ok"
                }
            }

        except Exception as e:
            return {
                "error": str(e),
                "_trace": {
                    "ms": time.time() - t0,
                    "status": "failed"
                }
            }

    gateway._debug_handle = gateway.handle
    gateway.handle = wrapped

    return gateway
