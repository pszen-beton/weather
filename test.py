import requests
import os
from matplotlib import pyplot as plt
from dotenv import load_dotenv
from functions import parse_yr_response
from datetime import datetime

load_dotenv()
api_key = os.getenv("API_KEY")

headers = {
    'User-Agent': 'weather/1.0 https://github.com/pszen-beton/weather'
}

url_open = 'https://api.open-meteo.com/v1/forecast?latitude=49.25&longitude=19.93&hourly=temperature_2m&forecast_days=10'
#url_mb = f"https://my.meteoblue.com/packages/basic-1h_basic-day?apikey={api_key}&lat=49.2509&lon=19.9343&asl=1895&format=json&forecast_days=1"
url_yr = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=49.25&lon=19.93'


print('fetching data')
response_open = requests.get(url_open)
#response_mb = requests.get(url_mb)
response_yr = requests.get(url_yr, headers=headers)

response_open_data = response_open.json()
#response_mb_data = response_mb.json()
response_yr_data = response_yr.json()
print(response_open_data)
#print(response_mb_data)
print(response_yr_data)

#print(f"location: lat: {response_open_data['latitude']}, lon: {response_open_data['longitude']}")

hourly_forecast_open = response_open_data['hourly']
#hourly_forecast_mb = response_mb_data['data_1h']
hourly_forecast_yr = parse_yr_response(response_yr_data)


hourly_forecast_open["time"] = [datetime.fromisoformat(t) for t in hourly_forecast_open["time"]]
##open
print('plotting open')
plt.figure(figsize=(15,5))
plt.plot((hourly_forecast_open['time']), hourly_forecast_open['temperature_2m'])
plt.grid(color='lightgrey')
plt.ylim(round(min(hourly_forecast_open['temperature_2m'])) - 2,
         round(max(hourly_forecast_open['temperature_2m'])) + 2)
plt.show()

#print('plotting mb')
#plt.figure(figsize=(15,5))
#plt.plot(hourly_forecast_mb['time'], hourly_forecast_mb['temperature'])
#plt.grid(color='lightgrey')
#plt.ylim(round(min(hourly_forecast_mb['temperature'])) - 2,
#         round(max(hourly_forecast_mb['temperature'])) + 2)
#plt.show()



print('plotting yr')
plt.figure(figsize=(15,5))
plt.plot(hourly_forecast_yr['time'], hourly_forecast_yr['temperature'])
plt.grid(color='lightgrey')
plt.ylim(round(min(hourly_forecast_yr['temperature'])) - 2,
         round(max(hourly_forecast_yr['temperature'])) + 2)
plt.show()



