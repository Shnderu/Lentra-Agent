from lentra.core.typesystem.layers.layer_types import LayerType


ALLOWED_CONNECTIONS = {
    LayerType.API: {
        LayerType.SERVICE,
    },

    LayerType.BOT: {
        LayerType.SERVICE,
    },

    LayerType.SERVICE: {
        LayerType.DOMAIN,
        LayerType.DATA,
    },

    LayerType.DOMAIN: set(),

    LayerType.DATA: {
        LayerType.INFRASTRUCTURE,
    },

    LayerType.INFRASTRUCTURE: set(),
}
