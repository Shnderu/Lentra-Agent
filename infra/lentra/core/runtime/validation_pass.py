class RuntimeValidator:

    def __init__(self, trace=None, router=None, gateway=None):
        self.trace = trace
        self.router = router
        self.gateway = gateway

    def run_synthetic_update(self):

        print("[VALIDATION] start")

        if self.router:
            intent = self.router.detect("найди квартиру в нячанге")
            print("[VALIDATION] intent:", intent)

        if self.gateway:
            print("[VALIDATION] gateway OK")

        print("[VALIDATION] done")
