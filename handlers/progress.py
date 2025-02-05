from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from data import load_user_data

router = Router()


@router.message(Command("check_progress"))
async def check_progress(message: Message):
    user_id = str(message.from_user.id)
    user_data = load_user_data(user_id)

    if not user_data:
        await message.answer("Ваш профиль пока не заполнен. Используйте /set_profile для настройки.")
        return

    # Прогресс по воде
    water_goal = user_data.get("water_goal", 0)
    logged_water = user_data.get("logged_water", 0)
    remaining_water = max(water_goal - logged_water, 0)

    water_progress = (
        f"💧 *Вода:*\n"
        f"- Выпито: {logged_water} мл из {water_goal} мл.\n"
        f"- Осталось до цели: {remaining_water} мл.\n"
    )

    # Прогресс по калориям
    calorie_goal = user_data.get("calorie_goal", 0)
    logged_calories = user_data.get("logged_calories", 0)
    burned_calories = user_data.get("burned_calories", 0)

    calorie_balance = logged_calories - burned_calories
    remaining_calories = max(calorie_goal - calorie_balance, 0)

    calorie_progress = (
        f"🔥 *Калории:*\n"
        f"- Потреблено: {logged_calories:.1f} ккал из {calorie_goal} ккал.\n"
        f"- Сожжено: {burned_calories:.1f} ккал.\n"
        f"- Баланс: {calorie_balance:.1f} ккал.\n"
        f"- Осталось до цели: {remaining_calories:.1f} ккал."
    )

    await message.answer(f"📊 *Прогресс:*\n\n{water_progress}\n{calorie_progress}", parse_mode="Markdown")
