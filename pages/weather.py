import requests
from django.core.cache import cache

CITY = "Missoula, MT"
LATITUDE = 46.87
LONGITUDE = -113.99

# WMO weather codes -> readable text (https://open-meteo.com/en/docs)
WEATHER_CODES = {
    0: "Clear",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog", 48: "Fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    56: "Freezing drizzle", 57: "Freezing drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    66: "Freezing rain", 67: "Freezing rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow", 77: "Snow grains",
    80: "Rain showers", 81: "Rain showers", 82: "Heavy rain showers",
    85: "Snow showers", 86: "Heavy snow showers",
    95: "Thunderstorms", 96: "Thunderstorms with hail", 99: "Thunderstorms with hail",
}


def get_weather():
    weather = cache.get("weather")
    if weather is not None:
        return weather

    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": LATITUDE,
                "longitude": LONGITUDE,
                "current": "temperature_2m,weather_code",
                "temperature_unit": "fahrenheit",
                "timezone": "America/Denver",
            },
            timeout=3,
        )
        response.raise_for_status()
        current = response.json()["current"]
    except (requests.RequestException, KeyError, ValueError):
        return None

    weather = {
        "city": CITY,
        "temperature": round(current["temperature_2m"]),
        "description": WEATHER_CODES.get(current["weather_code"], "Unknown"),
    }
    cache.set("weather", weather, 60 * 15)
    return weather