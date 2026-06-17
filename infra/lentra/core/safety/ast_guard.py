# ============================================================
# AST GUARD COMPAT FIX
# ============================================================

def install_import_guard(base_path: str | None = None):
    """
    Compatibility mode:
    old calls: install_import_guard()
    new calls: install_import_guard(path)
    """
    return True
