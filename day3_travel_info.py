
import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

weather_api_key = os.getenv("OPENWEATHER_API_KEY")
country_api_key = os.getenv("REST_COUNTRIES_API_KEY")


# Function to save data to a JSON file
def save_to_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")


def get_weather(city):
    if not weather_api_key:
        print("OpenWeatherMap API key not found in .env.")
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=15)

        if response.status_code == 200:
            return response.json()

        print("Weather API error:", response.status_code)
        print(response.text)
        return None

    except requests.exceptions.RequestException as error:
        print("Weather request failed:", error)
        return None


def get_country_info(country_code):
    if not country_api_key:
        print("REST Countries API key not found in .env.")
        return None

    url = (
        "https://api.restcountries.com/countries/v5/"
        f"codes.alpha_2/{country_code}"
    )

    headers = {
        "Authorization": f"Bearer {country_api_key}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print("Country API error:", response.status_code)
            print(response.text)
            return None

        result = response.json()
        countries = result.get("data", {}).get("objects", [])

        if countries:
            return countries[0]

        print("No country information found.")
        return None

    except requests.exceptions.RequestException as error:
        print("Country request failed:", error)
        return None


def run_tool():
    print("Travel Weather Tool")
    print("-------------------")

    city = input("Enter a city name: ").strip()

    if not city:
        print("No city entered. Exiting.")
        return

    print(f"\nFetching data for {city}...")

    weather_data = get_weather(city)

    if not weather_data:
        print(f"Could not retrieve weather for '{city}'.")
        return

    # Save weather data to a JSON file
    save_to_file(
        weather_data,
        f"{city.lower()}_weather.json"
    )

    country_code = weather_data.get("sys", {}).get("country", "Unknown")
    main = weather_data.get("main", {})
    weather_list = weather_data.get("weather", [])
    wind = weather_data.get("wind", {})

    temperature = main.get("temp", "Unknown")
    humidity = main.get("humidity", "Unknown")
    wind_speed = wind.get("speed", "Unknown")

    condition = (
        weather_list[0].get("description", "Unknown").title()
        if weather_list
        else "Unknown"
    )

    print(f"\n=== {weather_data.get('name', city)}, {country_code} ===")
    print(f"Temperature : {temperature} °C")
    print(f"Condition   : {condition}")
    print(f"Humidity    : {humidity}%")
    print(f"Wind        : {wind_speed} m/s")

    country_data = get_country_info(country_code)

    if country_data:
        name = country_data.get("names", {}).get("common", city)
        population = country_data.get("population", 0)
        region = country_data.get("region", "Unknown")

        currencies_list = country_data.get("currencies", [])
        currencies = ", ".join(
            item.get("code", "Unknown")
            for item in currencies_list
        ) or "Unknown"

        print("\n=== Country Info ===")
        print(f"Country     : {name}")
        print(f"Region      : {region}")
        print(f"Population  : {population:,}")
        print(f"Currency    : {currencies}")


if __name__ == "__main__":
    run_tool()
