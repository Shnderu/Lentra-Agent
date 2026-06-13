from lentra.rent.domain_v1 import create_rent_router

router = create_rent_router()


async def process_task(task: dict):
    return await router.route(task)
