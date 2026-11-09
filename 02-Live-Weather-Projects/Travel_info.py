
"""
Travel Weather Tool
-------------------
Shows live weather and country information for any city.
Combines data from two API calls and saves the results to one JSON file.

Usage:
    python travel_info.py

Requirements:
    pip install requests python-dotenv

Environment variables:
    OPENWEATHER_API_KEY in .env
    REST_COUNTRIES_API_KEY in .env

APIs:
    OpenWeatherMap API
    REST Countries API
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the .env file
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

weather_api_key = os.getenv("OPENWEATHER_API_KEY")
country_api_key = os.getenv("REST_COUNTRIES_API_KEY")


def save_to_file(data, filename):
    """Save combined weather and country data to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"\nCombined data saved to {filename}")
    except OSError as error:
        print(f"Could not save the JSON file: {error}")


def get_weather(city):
    """Fetch live weather data for the entered city."""
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

        if response.status_code == 401:
            print("Weather API authentication failed. Check your API key.")
        elif response.status_code == 404:
            print(f"City '{city}' was not found. Check the spelling.")
        else:
            print(f"Weather API error: {response.status_code}")

        return None

    except requests.exceptions.Timeout:
        print("The weather request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as error:
        print(f"Weather request failed: {error}")
        return None
    except ValueError:
        print("The weather API returned invalid JSON.")
        return None


def get_country_info(country_code):
    """Fetch country information using the country code from the weather API."""
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
            if response.status_code == 401:
                print("Country API authentication failed. Check your API key.")
            else:
                print(f"Country API error: {response.status_code}")
            return None

        result = response.json()
        countries = result.get("data", {}).get("objects", [])

        if countries:
            return countries[0]

        print("No country information was found.")
        return None

    except requests.exceptions.Timeout:
        print("The country request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as error:
        print(f"Country request failed: {error}")
        return None
    except ValueError:
        print("The country API returned invalid JSON.")
        return None


def run_tool():
    """Run the travel weather command-line application."""
    print("Travel Weather Tool")
    print("-------------------")

    city = input("Enter a city name: ").strip()

    if not city:
        print("No city entered. Please run the tool again.")
        return

    print(f"\nFetching data for {city}...")

    # API call 1: retrieve weather data
    weather_data = get_weather(city)

    if not weather_data:
        print("Could not retrieve weather. The tool will now exit.")
        return

    country_code = weather_data.get("sys", {}).get("country")

    # API call 2: use the first API's country code
    # to retrieve related country information.
    country_data = None
    if country_code:
        country_data = get_country_info(country_code)
    else:
        print("Country code was unavailable in the weather response.")

    # Combine both API responses into one result.
    combined_data = {
        "city": weather_data.get("name", city),
        "country_code": country_code,
        "weather": weather_data,
        "country": country_data
    }

    # Save the combined results to one JSON file.
    filename = f"{city.lower()}_travel_info.json"
    save_to_file(combined_data, filename)

    # Display a readable weather summary.
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

    print(f"\n=== Weather in {weather_data.get('name', city)} ===")
    print(f"Country code : {country_code or 'Unknown'}")
    print(f"Temperature  : {temperature} °C")
    print(f"Condition    : {condition}")
    print(f"Humidity     : {humidity}%")
    print(f"Wind         : {wind_speed} m/s")

    # Display country information when available.
    if country_data:
        country_name = country_data.get("names", {}).get(
            "common", "Unknown"
        )
        population = country_data.get("population", "Unknown")
        region = country_data.get("region", "Unknown")

        currencies_list = country_data.get("currencies", [])
        currencies = ", ".join(
            item.get("code", "Unknown")
            for item in currencies_list
        ) or "Unknown"

        print("\n=== Country Information ===")
        print(f"Country      : {country_name}")
        print(f"Region       : {region}")

        if isinstance(population, int):
            print(f"Population   : {population:,}")
        else:
            print(f"Population   : {population}")

        print(f"Currency     : {currencies}")
    else:
        print("\nCountry information could not be retrieved.")
        print("The available weather data has still been saved.")


if __name__ == "__main__":
    run_tool()
