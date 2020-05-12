import json

import requests


def dump_data(data, file_name):
    data = data.json()
    with open(f"data/{file_name}.json", "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


def load_data(file_name):
    with open(f"data/{file_name}.json", "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


def get_sum_data():
    url = "https://api.covid19api.com/summary"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    dump_data(response, "summary")


def get_day_one_data(country):
    url = f"https://api.covid19api.com/dayone/country/{country}"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    dump_data(response, country)


if __name__ == "__main__":
    get_sum_data()
    get_day_one_data("ukraine")
