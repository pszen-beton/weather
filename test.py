import requests
import os
from matplotlib import pyplot as plt
from dotenv import load_dotenv
from functions import parse_yr_response
from datetime import datetime
from Weather import Location

load_dotenv()
api_key = os.getenv("API_KEY")

headers = {
    'User-Agent': 'weather/1.0 https://github.com/pszen-beton/weather'
}

url_open = 'https://api.open-meteo.com/v1/forecast?latitude=49.25&longitude=19.93&hourly=temperature_2m&forecast_days=10'
url_yr = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=49.25&lon=19.93'


response_open = requests.get(url_open)
response_yr = requests.get(url_yr, headers=headers)

response_open_data = response_open.json()
response_yr_data = response_yr.json()


hourly_forecast_open = response_open_data['hourly']

hourly_forecast_yr = parse_yr_response(response_yr_data)


hourly_forecast_open["time"] = [datetime.fromisoformat(t) for t in hourly_forecast_open["time"]]

plt.figure(figsize=(15,5))
plt.plot((hourly_forecast_open['time']), hourly_forecast_open['temperature_2m'])
plt.plot(hourly_forecast_yr['time'], hourly_forecast_yr['temperature'])
plt.grid(color='lightgrey')
plt.show()





