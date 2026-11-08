
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load the .env file
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Load the News API key
api_key = os.getenv("NEWS_API_KEY")

if not api_key:
    print("News API key not found. Check your .env file.")
    raise SystemExit

print("News API key loaded successfully!")

# News API endpoint
url = "https://newsapi.org/v2/everything"

# Request parameters
params = {
    "q": "Kenya",
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 5
}

# API authentication
headers = {
    "X-Api-Key": api_key
}

try:
    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=15
    )

    print("Status code:", response.status_code)

    if response.status_code == 200:
        result = response.json()
        articles = result.get("articles", [])

        print(f"\nTotal results: {result.get('totalResults', 0)}")

        if articles:
            for number, article in enumerate(articles, start=1):
                title = article.get("title") or "No title"
                source = article.get("source", {}).get("name", "Unknown")
                description = article.get("description") or "No description"
                published = article.get("publishedAt", "Unknown")
                link = article.get("url", "No link")

                print(f"\n--- Article {number} ---")
                print(f"Title: {title}")
                print(f"Source: {source}")
                print(f"Published: {published}")
                print(f"Description: {description}")
                print(f"Link: {link}")
        else:
            print("No articles found.")

    else:
        print("Request failed:", response.status_code)
        print("API response:", response.text)

except requests.exceptions.RequestException as error:
    print("Request error:", error)
