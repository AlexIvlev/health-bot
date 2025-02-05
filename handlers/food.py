from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from data import load_user_data, save_user_data
from services.get_food_info import get_food_info

router = Router()


@router.message(Command("log_food"))
async def log_food(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Введите название продукта. Пример: /log_food банан")
        return

    product_name = args[1]
    food_info = get_food_info(product_name)

    if food_info and food_info["calories"] > 0:
        await state.update_data(food_name=food_info["name"], food_calories=food_info["calories"], user_id=user_id)
        await message.answer(
            f"🍽 {food_info['name']} — {food_info['calories']} ккал на 100 г.\nСколько грамм вы съели?")
        await state.set_state("waiting_for_food_weight")
    else:
        await state.update_data(user_id=user_id)
        await message.answer("❌ Не удалось найти продукт в базе. Введите калорийность вручную (ккал на 100 г):")
        await state.set_state("waiting_for_manual_calories")


@router.message(StateFilter("waiting_for_food_weight"))
async def process_food_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text)
        food_data = await state.get_data()
        user_id = food_data.get("user_id")

        if not user_id:
            await message.answer("Ошибка: не найден ID пользователя. Попробуйте снова.")
            await state.clear()
            return

        user_data = load_user_data(user_id)

        if not user_data:
            await message.answer("Ваш профиль пока не заполнен. Используйте /set_profile для настройки.")
            return

        calories_per_100g = food_data.get("food_calories", 0)
        total_calories = (calories_per_100g * weight) / 100

        total_logged = user_data.get("logged_calories", 0) + total_calories
        calorie_goal = user_data.get("calorie_goal", 0)

        save_user_data(user_id, "logged_calories", total_logged)

        remaining = max(calorie_goal - total_logged, 0)

        response = f"✅ Записано: {total_calories:.1f} ккал.\n"
        response += f"Всего за день: {total_logged:.1f} ккал.\n"

        if remaining > 0:
            response += f"До выполнения нормы осталось {remaining:.1f} ккал."
        else:
            response += f"Вы выполнили свою норму в {calorie_goal} ккал на сегодня! 🎉"

        await message.answer(response)
        await state.clear()
    except ValueError:
        await message.answer("Введите корректное количество граммов (например, 150).")


@router.message(StateFilter("waiting_for_manual_calories"))
async def process_manual_calories(message: Message, state: FSMContext):
    try:
        calories_per_100g = float(message.text)
        await state.update_data(food_calories=calories_per_100g)
        await message.answer("Теперь введите вес продукта (в граммах):")
        await state.set_state("waiting_for_food_weight")
    except ValueError:
        await message.answer("Введите корректное число (например, 100).")
