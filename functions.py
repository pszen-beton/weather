from datetime import datetime
import requests


def parse_yr_response(body):
    properties = body['properties']
    timeseries = properties["timeseries"]

    times = [datetime.fromisoformat(t['time']) for t in timeseries]
    temperatures = [t['data']['instant']['details']['air_temperature'] for t in timeseries]

    temperature_predictions = {"time": times, "temperature": temperatures}

    return temperature_predictions


def find_location(name):
    headers = {
        'User-Agent': 'weather/1.0 https://github.com/pszen-beton/weather'
    }

    base_url = 'https://nominatim.openstreetmap.org/search?format=json&q='

    output_body = requests.get(f"{base_url}{name}", headers=headers).json()[0]

    location = {"lat": output_body["lat"], "lon": output_body["lon"]}

    return location
