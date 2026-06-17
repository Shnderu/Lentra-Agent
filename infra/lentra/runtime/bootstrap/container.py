class Container:
    def __init__(self):
        self.services = {}

    def register(self, name, obj):
        self.services[name] = obj

    def get(self, name):
        return self.services.get(name)


def build_container():
    container = Container()

    container.register("execution_mode", "strict-enforcement-v10-15")

    return container
