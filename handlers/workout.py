from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from data import load_user_data, save_user_data
from recommendations_data import workout_calories, workout_water

router = Router()


@router.message(Command("log_workout"))
async def log_workout(message: Message):
    user_id = str(message.from_user.id)
    user_data = load_user_data(user_id)

    if not user_data:
        await message.answer("Ваш профиль пока не заполнен. Используйте /set_profile для настройки.")
        return

    args = message.text.split(maxsplit=2)
    if len(args) < 3 or not args[2].isdigit():
        await message.answer("Введите тип тренировки и время в минутах, например: /log_workout бег 30")
        return

    workout_type = args[1].lower()
    workout_time = int(args[2])

    # Проверка типа тренировки
    if workout_type not in workout_calories:
        await message.answer(f"Неизвестный тип тренировки: {workout_type}.\n"
                             f"Доступные типы: бег, плавание, велотренажер, силовая, йога, пилатес.")
        return

    # Расчет сожжённых калорий и воды
    calories_burned = (workout_time / 30) * workout_calories[workout_type]
    water_needed = (workout_time / 30) * workout_water[workout_type]

    total_burned_calories = user_data.get("burned_calories", 0) + calories_burned
    total_logged_water = user_data.get("logged_water", 0) + water_needed

    save_user_data(user_id, "burned_calories", total_burned_calories)
    save_user_data(user_id, "logged_water", total_logged_water)

    response = f"💪 {workout_type.capitalize()} {workout_time} минут - {int(calories_burned)} ккал."
    response += f"\nДополнительно: выпейте {int(water_needed)} мл воды."

    await message.answer(response)
