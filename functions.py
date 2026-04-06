import requests
from typing import Any


def parse_yr_response(body: dict[str, Any]) -> dict[str, list[str]]:
    properties = body['properties']
    timeseries = properties['timeseries']

    yr_response_parameters = timeseries[0]['data']['instant']['details'].keys()
    temperature_predictions = {'time': [t['time'] for t in timeseries]}

    for param in yr_response_parameters:
        temperature_predictions[param] = [t['data']['instant']['details'].get(param) for t in timeseries]

    return temperature_predictions


def find_location(name: str) -> dict:
    headers = {
        'User-Agent': 'weather/1.0 https://github.com/pszen-beton/weather'
    }

    base_url = 'https://nominatim.openstreetmap.org/search?format=json&q='

    output_body = requests.get(f"{base_url}{name}", headers=headers).json()[0]

    location = {"lat": output_body["lat"], "lon": output_body["lon"]}

    return location
