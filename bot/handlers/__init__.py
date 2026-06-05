from aiogram import Router

from .start import router as start_router
from .flights import router as flights_router

router = Router()

router.include_router(start_router)
router.include_router(flights_router)
