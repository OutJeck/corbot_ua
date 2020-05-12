import json

import requests


def get_data(country):
    url = f"https://api.covid19api.com/dayone/country/{country}/status/confirmed"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response


def read_data(file_name: str) -> dict:
    """Return data read from a json file."""
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_data(data: dict, file_name: str) -> None:
    """Write data to a json file."""
    with open(file_name, "w+", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
