def enforce_bootstrap():
    """
    Ensures runtime is clean entrypoint.
    """
    try:
        from lentra.runtime.guard import validate_import_chain
        validate_import_chain()
    except Exception as e:
        print("[BOOTSTRAP LOCK FAILED]", str(e))
        raise
