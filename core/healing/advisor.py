def generate_advice(diagnosis, metrics):
    root = diagnosis.get("root_cause")

    if root == "PIPELINE_EXECUTION_STUCK":
        return [
            "check worker consumption loop",
            "verify xack / xadd flow",
            "inspect redis stream consumer group lag"
        ]

    if root == "REDIS_CONNECTION_FAILURE":
        return [
            "verify docker network connectivity",
            "check redis host resolution",
            "ensure correct network (infra_default)"
        ]

    if root == "DEPENDENCY_MISSING":
        return [
            "rebuild docker image with updated requirements.txt",
            "ensure pip install includes missing packages"
        ]

    return ["no safe automated fix available"]
