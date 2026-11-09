
import json

with open("nairobi_weather.json", "r") as f:
    data = json.load(f)

print(data["main"]["temp"])
