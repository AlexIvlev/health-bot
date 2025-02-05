from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Я бот для отслеживания здоровья 😊\n"
        "Давайте начнем с /set_profile, чтобы заполнить профиль.\n"
        "Для справки введите /help."
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Список команд:\n"
        "/set_profile - Настроить профиль\n"
        "/profile - Показать профиль\n"
        "/edit_profile - Изменить данные профиля\n"
        "/visualize_goals - Визуализировать достижение целей\n"
        "/log_water <количество> - Логирование воды\n"
        "/log_food <название продукта> - Логирование еды\n"
        "/log_workout <тип тренировки> <время (мин)> - Логирование тренировок\n"
        "/check_progress - Прогресс по воде и калориям\n"
        "/get_recommendations - Получение рекомендаций\n"
    )
