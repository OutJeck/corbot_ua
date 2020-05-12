import json

import requests

url = "https://api.covid19api.com/dayone/country/ukraine/status/confirmed"  # Get day one info about Ukraine

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

data = response.json()


def write_data(data: dict, file_name: str) -> None:
    """Write data to a json file."""
    with open(file_name, "w+", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


write_data(data, "ukraine_day_one.json")
