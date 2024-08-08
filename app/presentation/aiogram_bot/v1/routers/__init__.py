from aiogram import Dispatcher

# routers
from app.presentation.aiogram_bot.v1.routers.start import router as start_router
from app.presentation.aiogram_bot.v1.routers.posts import router as posts_router

all_routers = [
    start_router,
    posts_router,
]


def include_all_routers(dp: Dispatcher) -> None:
    for router in all_routers:
        dp.include_router(router)
