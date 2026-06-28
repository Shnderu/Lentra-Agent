
def safe_float(x, default=0.0):

    if isinstance(x, list):
        return float(x[0]) if x else default

    if x is None:
        return default

    return float(x)
