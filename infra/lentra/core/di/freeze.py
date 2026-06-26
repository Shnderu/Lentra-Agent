def assert_flow_glue_contract(flow_glue):
    required = [
        "intent_resolver",
        "intent_router",
        "scenario_engine",
        "scenario_policy_engine",
    ]

    for r in required:
        if not hasattr(flow_glue, r):
            raise RuntimeError(f"FlowGlue missing dependency: {r}")
