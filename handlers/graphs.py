import io
import matplotlib.pyplot as plt
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from data import load_user_data

router = Router()


@router.message(Command("visualize_goals"))
async def visualize_goals(message: Message):
    user_id = message.from_user.id
    user_data = load_user_data(user_id)

    if not user_data:
        await message.answer("Ваш профиль пока не заполнен. Используйте /set_profile для настройки.")
        return

    water_goal = user_data.get('water_goal', 0)
    calorie_goal = user_data.get('calorie_goal', 0)
    logged_water = user_data.get('logged_water', 0)
    logged_calories = user_data.get('logged_calories', 0)
    burned_calories = user_data.get('burned_calories', 0)

    # Рассчитываем баланс калорий
    balance_calories = logged_calories - burned_calories

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(['Цель по воде', 'Выпито'], [water_goal, logged_water], color=['blue', 'cyan'])
    ax.set_title("Достижение цели по воде")
    ax.set_ylabel("Мл")
    ax.set_ylim(0, max(water_goal, logged_water) + 500)

    water_img = io.BytesIO()
    plt.tight_layout()
    fig.savefig(water_img, format='png')
    water_img.seek(0)

    fig, ax = plt.subplots(figsize=(6, 4))
    categories = ['Цель', 'Потреблено', 'Сожжено', 'Баланс']
    values = [calorie_goal, logged_calories, burned_calories, balance_calories]
    colors = ['green', 'orange', 'red', 'purple' if balance_calories >= 0 else 'brown']

    ax.bar(categories, values, color=colors)
    ax.set_title("Калории: цель, потребление, сжигание и баланс")
    ax.set_ylabel("Ккал")
    ax.set_ylim(min(balance_calories, 0) - 500, max(calorie_goal, logged_calories, burned_calories, balance_calories) + 500)

    calorie_img = io.BytesIO()
    plt.tight_layout()
    fig.savefig(calorie_img, format='png')
    calorie_img.seek(0)

    await message.answer("Вот ваши достижения по воде и калориям:")
    await message.answer_photo(BufferedInputFile(water_img.getvalue(), 'water_goal.png'))
    await message.answer_photo(BufferedInputFile(calorie_img.getvalue(), 'calories.png'))

    plt.close('all')
