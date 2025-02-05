from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from data import load_user_data
from recommendations_data import low_calorie_foods, base_workouts

router = Router()


@router.message(Command("get_recommendations"))
async def get_recommendations(message: Message):
    user_id = str(message.from_user.id)
    user_data = load_user_data(user_id)

    if not user_data:
        await message.answer("Ваш профиль пока не заполнен. Используйте /set_profile для настройки.")
        return

    activity = user_data.get("activity", None)
    calorie_goal = user_data.get("calorie_goal", None)
    water_goal = user_data.get("water_goal", None)

    response = "Вот несколько рекомендаций для вас:\n"

    response += "\n"

    # Рекомендации по питанию
    response += "Продукты с низким содержанием калорий:\n" + "\n".join(low_calorie_foods) + "\n"

    response += "\n"

    # Рекомендации по тренировкам
    response += "Рекомендуемые тренировки:\n" + "\n".join(base_workouts) + "\n"

    response += "\n"

    # Водный баланс
    if water_goal and water_goal > 0:
        response += f"Ваша цель по воде: {water_goal} мл в день.\n"
    else:
        response += "Не указана цель по воде. Рекомендуем пить минимум 1,5 литра воды в день."

    response += "\n"

    # Общие рекомендации по активности
    if activity:
        if activity < 30:
            response += "Рекомендуем увеличить физическую активность минимум до 30 минут в день для улучшения здоровья."
        elif activity >= 30:
            response += "Вы уже достаточно активны, прекрасно! Продолжайте в том же духе."

    response += "\n\n"

    # Цель по калориям
    if calorie_goal:
        if calorie_goal < 2000:
            response += "Ваша цель по калориям ниже 2000 ккал. Это подходящая цель для похудения."
        elif calorie_goal > 2500:
            response += "Ваша цель по калориям выше 2500 ккал. Это нормальная цель для набора массы."
        else:
            response += "Ваша цель по калориям в пределах нормы для поддержания веса."

    await message.answer(response)
