from lentra.runtime.bootstrap.main import gateway

print("GATEWAY TYPE:", type(gateway))
print("HAS REGISTRY:", hasattr(gateway, "registry"))
print("HAS HANDLE:", hasattr(gateway, "handle"))
