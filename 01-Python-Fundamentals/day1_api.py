
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load the API key from .env
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("REST_COUNTRIES_API_KEY")

if not api_key:
    print("API key not found. Check your .env file.")
    raise SystemExit

# REST Countries API v5
url = "https://api.restcountries.com/countries/v5/names.common/Kenya"

headers = {
    "Authorization": f"Bearer {api_key}"
}

try:
    response = requests.get(url, headers=headers, timeout=15)

    print("Status code:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        print("Data received:")
        print(data)
    else:
        print("Request failed. Status:", response.status_code)
        print(response.text)

except requests.exceptions.RequestException as e:
    print("Request failed:", e)
