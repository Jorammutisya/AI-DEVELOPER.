
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Find and load the .env file
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Use the WEATHER key, not the REST COUNTRIES key
api_key = os.getenv("OPENWEATHER_API_KEY")

if not api_key:
    print("Weather API key not found.")
    print("Looking for .env at:", env_path)
    print("Does .env exist?", env_path.exists())
    raise SystemExit

print("Weather API key loaded successfully!")

# OpenWeatherMap current weather endpoint
url = "https://api.openweathermap.org/data/2.5/weather"

# Request weather for Nairobi, Kenya
params = {
    "q": "Nairobi,KE",
    "appid": api_key,
    "units": "metric"
}

try:
    response = requests.get(url, params=params, timeout=15)

    print("Status code:", response.status_code)

    if response.status_code == 200:
        result = response.json()

        city = result.get("name", "Unknown")
        temperature = result.get("main", {}).get("temp", "Unknown")
        humidity = result.get("main", {}).get("humidity", "Unknown")

        weather_list = result.get("weather", [])
        description = (
            weather_list[0].get("description", "Unknown")
            if weather_list else "Unknown"
        )

        print(f"City: {city}")
        print(f"Temperature: {temperature} °C")
        print(f"Humidity: {humidity}%")
        print(f"Weather: {description}")

    else:
        print("API response:", response.text)

except requests.exceptions.RequestException as e:
    print("Request error:", e)
