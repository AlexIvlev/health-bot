import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from handlers import base, profile, graphs, water, food, workout, progress, recommendations
from middlewares import LoggingMiddleware

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.include_router(base.router)
dp.include_router(profile.router)
dp.include_router(graphs.router)
dp.include_router(water.router)
dp.include_router(food.router)
dp.include_router(workout.router)
dp.include_router(progress.router)
dp.include_router(recommendations.router)

dp.message.middleware(LoggingMiddleware())


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
