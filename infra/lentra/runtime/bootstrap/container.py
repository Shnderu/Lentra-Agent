class Container:
    def __init__(self):
        self.services = {}

    def register(self, name, obj):
        self.services[name] = obj

    def get(self, name):
        return self.services.get(name)


def build_container():
    container = Container()

    # CORE SERVICES REGISTRY
    container.register("execution_mode", "lentra-core")

    return container
