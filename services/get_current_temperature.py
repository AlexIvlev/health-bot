from pyowm import OWM


def get_current_temperature(city, api_key):
    """Получение текущей погоды через pyowm"""
    owm = OWM(api_key)
    mgr = owm.weather_manager()

    try:
        observation = mgr.weather_at_place(city)
        current_temp = observation.weather.temperature('celsius')["temp"]
        return current_temp
    except Exception as e:
        return {"error": str(e)}
