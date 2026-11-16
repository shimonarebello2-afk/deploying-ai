
import requests
from langchain_core.tools import tool
@tool
def get_weather(location: str) -> str:
    """
    Fetch current weather for a city using Open-Meteo
    and transform the API response into a readable summary.
    """

    # Find the city's coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_response = requests.get(
        geo_url,
        params={"name": location, "count": 1, "language": "en"},
        timeout=10
    )
    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if not geo_data.get("results"):
        return f"I couldn't find the location {location}."

    city = geo_data["results"][0]
    latitude = city["latitude"]
    longitude = city["longitude"]
    city_name = city["name"]
    country = city.get("country", "")

    # Retrieve current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "timezone": "auto"
        },
        timeout=10
    )
    weather_response.raise_for_status()

    weather = weather_response.json()["current"]

    # Transform structured API data into natural language
    return (
        f"Here's your weather update for {city_name}, {country}: "
        f"it's currently {weather['temperature_2m']}°C, "
        f"with {weather['relative_humidity_2m']}% humidity "
        f"and winds of {weather['wind_speed_10m']} km/h. "
        f"Check local conditions before heading out!"
    )