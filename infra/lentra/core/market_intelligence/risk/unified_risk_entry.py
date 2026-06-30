class UnifiedRiskEntry:

    def __init__(self, engines: dict):
        self.engines = engines

    def score(self, listing):

        base = self.engines["market"].score(listing)
        scam = self.engines["scam"].score(listing)

        calibrated = self.engines["calibration"].adjust(base, scam)

        return calibrated
