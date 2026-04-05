from datetime import datetime

def parse_yr_response(body):
    properties = body['properties']
    timeseries = properties["timeseries"]

    times = [datetime.fromisoformat(t['time']) for t in timeseries]
    temperatures = [t['data']['instant']['details']['air_temperature'] for t in timeseries]

    temperature_predictions = {"time" : times, "temperature" : temperatures}

    return temperature_predictions


