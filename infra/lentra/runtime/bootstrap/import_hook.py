import builtins
from lentra.core.guards.import_guard import ImportGuard


_original_import = builtins.__import__


def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    importer = (globals or {}).get("__name__", "unknown")

    ImportGuard.validate(importer, name)

    return _original_import(name, globals, locals, fromlist, level)


def install_import_hook():
    builtins.__import__ = guarded_import
