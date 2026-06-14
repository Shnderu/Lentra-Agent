from lentra.telegram.ux.router.callback_router import CallbackRouter
from lentra.telegram.ux.router.handlers import open_property_list, noop


router = CallbackRouter()

router.register("list", open_property_list)
router.register("noop", noop)
