from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from data import update_user_data, load_user_data, save_user_data
from services.calculate_calories_norm import calculate_calories_norm
from services.calculate_water_norm import calculate_water_norm

router = Router()


class ProfileSetup(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity = State()
    city = State()
    water_goal = State()
    calorie_goal = State()


@router.message(Command("set_profile"))
async def start_profile_setup(message: Message, state: FSMContext):
    await message.answer("Введите ваш вес (в кг):")
    await state.set_state(ProfileSetup.weight)


@router.message(ProfileSetup.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text)
        update_user_data(message.from_user.id, "weight", weight)

        await message.answer("Введите ваш рост (в см):")
        await state.set_state(ProfileSetup.height)
    except ValueError:
        await message.answer("Введите корректное число (например, 80).")


@router.message(ProfileSetup.height)
async def process_height(message: Message, state: FSMContext):
    try:
        height = int(message.text)
        update_user_data(message.from_user.id, "height", height)

        await message.answer("Введите ваш возраст:")
        await state.set_state(ProfileSetup.age)
    except ValueError:
        await message.answer("Введите корректное число (например, 180).")


@router.message(ProfileSetup.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        update_user_data(message.from_user.id, "age", age)

        await message.answer("Сколько минут активности у вас в день?")
        await state.set_state(ProfileSetup.activity)
    except ValueError:
        await message.answer("Введите корректное число (например, 25).")


@router.message(ProfileSetup.activity)
async def process_activity(message: Message, state: FSMContext):
    try:
        activity = int(message.text)
        update_user_data(message.from_user.id, "activity", activity)

        await message.answer("В каком городе вы находитесь?")
        await state.set_state(ProfileSetup.city)
    except ValueError:
        await message.answer("Введите корректное число (например, 45).")


@router.message(ProfileSetup.city)
async def process_city(message: Message, state: FSMContext):
    update_user_data(message.from_user.id, "city", message.text)

    await message.answer("Введите вашу цель по калориям (например, 2000) или 'auto' для автоматического расчета:")
    await state.set_state(ProfileSetup.calorie_goal)


@router.message(ProfileSetup.calorie_goal)
async def process_calorie_goal(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = load_user_data(user_id)

    if message.text.lower() == "auto":
        # Авторасчёт калорий
        weight = user_data.get("weight")
        height = user_data.get("height")
        age = user_data.get("age")
        activity_minutes = user_data.get("activity", 0)

        if not (weight and height and age):
            await message.answer("Для автоматического расчёта укажите ваш вес, рост и возраст в профиле.")
            return

        calorie_goal = calculate_calories_norm(weight, height, age, activity_minutes)
        await message.answer(f"Ваша норма калорий рассчитана автоматически: {int(calorie_goal)} ккал.")
    else:
        try:
            calorie_goal = int(message.text)
        except ValueError:
            await message.answer("Введите корректное число (например, 2000) или 'auto' для автоматического расчета:")
            return

    update_user_data(user_id, "calorie_goal", calorie_goal)
    await message.answer("Введите вашу цель по воде (в мл, например, 2000) или 'auto' для автоматического расчета:")
    await state.set_state(ProfileSetup.water_goal)


@router.message(ProfileSetup.water_goal)
async def process_water_goal(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = load_user_data(user_id)

    if message.text.lower() == "auto":
        # Авторасчёт воды
        weight = user_data.get("weight")
        activity_minutes = user_data.get("activity", 0)
        city = user_data.get("city")

        if not weight or not city:
            await message.answer("Для автоматического расчета укажите ваш вес и город в профиле.")
            return

        water_goal = calculate_water_norm(weight, activity_minutes, city)
        await message.answer(f"Ваша норма воды рассчитана автоматически: {int(water_goal)} мл.")
    else:
        try:
            water_goal = int(message.text)
        except ValueError:
            await message.answer("Введите корректное число (например, 2000) или 'auto' для автоматического расчета:")
            return

    update_user_data(user_id, "water_goal", water_goal)
    await message.answer("✅ Профиль сохранён!")
    await state.clear()


@router.message(Command("profile"))
async def show_profile(message: Message):
    user_id = message.from_user.id
    user_data = load_user_data(user_id)

    if not user_data:
        await message.answer("Ваш профиль пока не заполнен. Используйте /set_profile для настройки.")
        return

    profile_text = (
        f"📋 Ваш профиль:\n"
        f"🔹 Вес: {user_data.get('weight', 'Не указано')} кг\n"
        f"🔹 Рост: {user_data.get('height', 'Не указано')} см\n"
        f"🔹 Возраст: {user_data.get('age', 'Не указано')} лет\n"
        f"🔹 Активность: {user_data.get('activity', 'Не указано')} минут в день\n"
        f"🔹 Город: {user_data.get('city', 'Не указано')}\n"
        f"🔹 Цель по калориям: {user_data.get('calorie_goal', 'Не указано')} ккал\n"
        f"🔹 Цель по воде: {user_data.get('water_goal', 'Не указано')} мл\n"
        f"🔹 Воды выпито: {user_data.get('logged_water', 0)} мл\n"
        f"🔹 Потребленные калории: {user_data.get('logged_calories', 0)} ккал\n"
        f"🔹 Сожжённые калории: {user_data.get('burned_calories', 0)} ккал"
    )
    await message.answer(profile_text)


class EditProfile(StatesGroup):
    choosing_field = State()
    editing_value = State()


@router.message(Command("edit_profile"))
async def edit_profile_start(message: Message, state: FSMContext):
    await message.answer(
        "Что вы хотите изменить?\n"
        "Введите:\n"
        "🔹 вес\n"
        "🔹 рост\n"
        "🔹 возраст\n"
        "🔹 активность\n"
        "🔹 город\n"
        "🔹 цель по калориям\n"
        "🔹 цель по воде\n"
    )
    await state.set_state(EditProfile.choosing_field)


@router.message(EditProfile.choosing_field)
async def choose_field_to_edit(message: Message, state: FSMContext):
    field_map = {
        "вес": "weight",
        "рост": "height",
        "возраст": "age",
        "активность": "activity",
        "город": "city",
        "цель по калориям": "calorie_goal",
        "цель по воде": "water_goal"
    }

    field_name = message.text.lower()
    if field_name not in field_map:
        await message.answer(
            "Некорректный параметр. Введите один из: вес, рост, возраст, активность, город, цель по калориям, цель по воде."
        )
        return

    await state.update_data(editing_field=field_map[field_name])
    await message.answer(f"Введите новое значение для {field_name}:")
    await state.set_state(EditProfile.editing_value)


@router.message(EditProfile.editing_value)
async def edit_field_value(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    field = data.get("editing_field")

    if field in ["weight", "height", "age", "activity", "calorie_goal", "water_goal"]:
        try:
            value = int(message.text)
        except ValueError:
            await message.answer("Введите корректное число.")
            return
    else:
        value = message.text

    save_user_data(user_id, field, value)
    await message.answer("✅ Данные обновлены!")
    await state.clear()
