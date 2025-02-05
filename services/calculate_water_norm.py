from config import WEATHER_API_KEY
from services.get_current_temperature import get_current_temperature


def calculate_water_norm(weight, activity_minutes, city):
    """
    Рассчитывает норму потребления воды в миллилитрах на основе веса, физической активности и температуры в городе.

    Формула:
    - Базовая норма: вес (кг) * 30 мл/кг
    - Дополнительно: +500 мл за каждые 30 минут активности
    - При жаркой погоде (> 25°C):
      - +500 мл, если 25°C ≤ температура < 30°C
      - +1000 мл, если температура ≥ 30°C

    :param weight: Вес пользователя в кг
    :param activity_minutes: Время физической активности в минутах
    :param city: Город пользователя (для определения температуры)
    :return: Рекомендуемая суточная норма воды в миллилитрах
    """
    base_water = weight * 30  # мл/кг
    extra_activity = (activity_minutes // 30) * 500  # 500 мл за каждые 30 мин активности

    temperature = get_current_temperature(city, WEATHER_API_KEY)

    # Добавляем дополнительный объем воды за жаркую погоду
    extra_heat = 0
    if temperature and not isinstance(temperature, dict) and temperature > 25:
        extra_heat = 500 if 25 <= temperature < 30 else 1000

    return base_water + extra_activity + extra_heat
