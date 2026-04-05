import requests
from matplotlib import pyplot as plt
from datetime import datetime

url_open = 'https://api.open-meteo.com/v1/forecast?latitude=49.25&longitude=19.93&hourly=temperature_2m&forecast_days=1'

print('fetching data')
response_open = requests.get(url_open)

response_open_data = response_open.json()
print(response_open_data)

print(f"location: lat: {response_open_data['latitude']}, lon: {response_open_data['longitude']}")

hourly_forecast_open = response_open_data['hourly']
print('plotting...')
plt.figure(figsize=(15,5))
plt.plot(hourly_forecast_open['time'], hourly_forecast_open['temperature_2m'])
plt.grid(color='lightgrey')
plt.ylim(round(min(hourly_forecast_open['temperature_2m'])) - 2,
         round(max(hourly_forecast_open['temperature_2m'])) + 2)
plt.show()


