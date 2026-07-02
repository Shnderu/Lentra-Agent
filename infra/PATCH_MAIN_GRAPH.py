# ADD ONLY THIS AFTER gateway.evaluate()

from lentra.api.patch_graph_integration import apply_graph_layer


def safe_finalize_response(gateway, engines, payload):
    response = gateway.evaluate(engines, payload)

    # SAFE GRAPH OVERLAY
    response = apply_graph_layer(gateway, engines, payload, response)

    return response
