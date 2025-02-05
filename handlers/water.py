from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from data import load_user_data, save_user_data

router = Router()


@router.message(Command("log_water"))
async def log_water(message: Message):
    user_id = str(message.from_user.id)
    user_data = load_user_data(user_id)

    if not user_data:
        await message.answer("Ваш профиль пока не заполнен. Используйте /set_profile для настройки.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Введите количество воды в миллилитрах, например: /log_water 250")
        return

    water_logged = int(args[1])
    total_logged = user_data.get("logged_water", 0) + water_logged
    water_goal = user_data.get("water_goal", 0)

    save_user_data(user_id, "logged_water", total_logged)

    remaining = max(water_goal - total_logged, 0)

    response = f"Вы выпили {water_logged} мл воды. Всего за день: {total_logged} мл.\n"
    if remaining > 0:
        response += f"До выполнения нормы осталось {remaining} мл."
    else:
        response += f"Вы выполнили свою норму в {water_goal} на сегодня! 🎉"

    await message.answer(response)
