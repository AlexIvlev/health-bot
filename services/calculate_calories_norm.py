

def calculate_calories_norm(weight, height, age, activity_minutes):
    """
    Рассчитывает дневную норму калорий.
    :param weight: вес в кг
    :param height: рост в см
    :param age: возраст в годах
    :param activity_minutes: уровень активности (в минутах в день)
    :return: рекомендуемая норма калорий
    """
    base_calories = 10 * weight + 6.25 * height - 5 * age
    activity_addition = (activity_minutes / 30) * 100

    return round(base_calories + activity_addition)
