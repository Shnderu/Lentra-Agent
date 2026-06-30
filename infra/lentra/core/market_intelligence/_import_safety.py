import sys


class ImportGuard:

    def __init__(self, layer: str):
        self.layer = layer

    def __enter__(self):
        sys._lentra_import_layer = self.layer

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys._lentra_import_layer = None
