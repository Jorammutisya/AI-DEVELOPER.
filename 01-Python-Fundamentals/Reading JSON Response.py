
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Find the .env file beside this Python script
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("REST_COUNTRIES_API_KEY")

if not api_key:
    print("API key not found.")
    print("Looking for .env at:", env_path)
    print("Does .env exist?", env_path.exists())
    raise SystemExit

print("API key loaded successfully!")

url = "https://api.restcountries.com/countries/v5/names.common/Kenya"

headers = {
    "Authorization": f"Bearer {api_key}"
}

try:
    response = requests.get(url, headers=headers, timeout=15)
    print("Status code:", response.status_code)
    response.raise_for_status()

    result = response.json()
    countries = result.get("data", {}).get("objects", [])

    if countries:
        country = countries[0]

        name = country.get("names", {}).get("common", "Unknown")

        capitals = country.get("capitals", [])
        capital = capitals[0].get("name", "Unknown") if capitals else "Unknown"

        population = country.get("population", 0)

        currencies = country.get("currencies", [])
        currency = currencies[0].get("code", "Unknown") if currencies else "Unknown"

        print(f"Country: {name}")
        print(f"Capital: {capital}")
        print(f"Population: {population:,}")
        print(f"Currency: {currency}")
    else:
        print("No country data found.")
        print(result)

except requests.exceptions.RequestException as e:
    print("Request failed:", e)
