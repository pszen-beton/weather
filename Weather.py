from functions import *
from datetime import datetime
from matplotlib import pyplot as plt


class Weather:
    def __init__(self, locations):
        # 1. locations
        if locations is None:
            self.locations = []

        items = locations if isinstance(locations, list) else [locations]

        if all(isinstance(loc, Location) for loc in items):
            self.locations = items
        else:
            raise TypeError("Input must be a Location object or a list of Location objects.")

        self.geocoded = False
        self.forecast_ran = False
        self.forecast_open = None
        self.forecast_yr = None

    def find_coordinates(self):
        for location in self.locations:
            if location.lat is None or location.lon is None:
                location.find_coordinates()
        self.geocoded = True

    def print_locations(self):
        for location in self.locations:
            print(location)

    def forecast(self, days):
        headers = {
            'User-Agent': 'weather/1.0 https://github.com/pszen-beton/weather'
        }
        if self.geocoded:
            for location in self.locations:
                lat = str(location.lat)
                lon = str(location.lon)

                url_open = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&forecast_days={days}"
                url_yr = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"

                response_open = requests.get(url_open)
                response_yr = requests.get(url_yr, headers=headers)

                response_open_data = response_open.json()
                response_yr_data = response_yr.json()

                hourly_forecast_open = response_open_data['hourly']
                hourly_forecast_open["time"] = [datetime.fromisoformat(t) for t in hourly_forecast_open["time"]]
                hourly_forecast_yr = parse_yr_response(response_yr_data)

                self.forecast_open = hourly_forecast_open
                self.forecast_yr = hourly_forecast_yr

                self.forecast_ran = True
        else:
            raise RuntimeError("Locations not geocoded")

    def plot_forecast(self):
        if self.forecast_ran:
            plt.figure(figsize=(15, 5))
            plt.plot((self.forecast_open['time']), self.forecast_open['temperature_2m'])
            plt.plot(self.forecast_yr['time'], self.forecast_yr['temperature'])
            plt.grid(color='lightgrey')
            plt.show()
        else:
            raise RuntimeError("Weather not forecasted. Run forecast method first.")


