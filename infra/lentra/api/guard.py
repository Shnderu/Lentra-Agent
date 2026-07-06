from lentra.runtime.bootstrap_guard import enforce_bootstrap


def api_guard():
    enforce_bootstrap()
