

import traceback


def safe_run(pipeline, payload):

    try:
        return pipeline.run(payload)

    except Exception as e:

        return {
            "error": str(e),
            "trace": traceback.format_exc(),
            "status": "failed_safe"
        }
