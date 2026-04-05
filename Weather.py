from fontTools.diff import color

from functions import *
from datetime import datetime, date, timedelta
from matplotlib import pyplot as plt
from Location import Location
import numpy as np

class Weather:
    def __init__(self, location):
        # 1. locations
        if isinstance(location, Location):
            self.location = location
        else:
            raise RuntimeError("Location has to be Location type")

        self.geocoded = False
        self.forecast_ran = False
        self.forecast_open = None
        self.forecast_yr = None
        self.forecast_master = {}

    def find_coordinates(self):
        lat, lon = self.location.get_coordinates()
        if lat is None or lon is None:
            self.location.find_coordinates()
        self.geocoded = True

    def print_locations(self):
        print(self.location)

    def forecast(self, days):
        headers = {
            'User-Agent': 'weather/1.0 https://github.com/pszen-beton/weather'
        }
        if self.geocoded:
            lat = str(self.location.lat)
            lon = str(self.location.lon)

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

            for t, v in zip(hourly_forecast_open["time"], hourly_forecast_open["temperature_2m"]):
                self.forecast_master[t] = {"open": v, "yr": "N/A"}

            for t, v in zip(hourly_forecast_yr["time"], hourly_forecast_yr["temperature"]):
                if t in self.forecast_master:
                    self.forecast_master[t]["yr"] = v
                else:
                    self.forecast_master[t] = {"open": "N/A", "yr": v}

            self.forecast_ran = True
        else:
            raise RuntimeError("Locations not geocoded")

    def plot_forecast(self, min_time = None, max_time = None):


        if min_time is None:
            min_time = min(self.forecast_master.keys())
        elif not isinstance(min_time, datetime):
            min_time = datetime.combine(datetime.strptime(min_time, '%d-%m-%Y').date(), datetime.min.time())

        if max_time is None:
            max_time = (datetime.combine(date.today() + timedelta(days=1),
                                         datetime.min.time()))
        elif not isinstance(max_time, datetime):
            max_time = datetime.combine(datetime.strptime(max_time, '%d-%m-%Y').date(), datetime.min.time())

        if self.forecast_ran:
            plt.figure(figsize=(15, 5))
            plt.plot((self.forecast_open['time']), self.forecast_open['temperature_2m'], color='blue')
            plt.plot(self.forecast_yr['time'], self.forecast_yr['temperature'], color='red')
            plt.grid(color='lightgrey')
            plt.xlim(min_time, max_time)
            plt.show()
        else:
            raise RuntimeError("Weather not forecasted. Run forecast method first.")

    def output_hourly_table(self, max_time = None, by=1):
        if max_time is None:
            max_time = (datetime.combine(date.today() + timedelta(days=1),
                                         datetime.min.time()))
        elif not isinstance(max_time, datetime):
            max_time = datetime.combine(datetime.strptime(max_time, '%d-%m-%Y').date(), datetime.min.time())

        sorted_times = np.array(sorted(self.forecast_master.keys()))
        target_times = sorted_times[sorted_times < max_time][::by]

        times_list = [f"{t:%Y-%m-%d %H:%M}" for t in target_times]

        open_list = []
        yr_list = []

        for t in target_times:
            p1 = self.forecast_master[t]["open"]
            p2 = self.forecast_master[t]["yr"]

            open_list.append(f"{p1:>14.1f}°C" if isinstance(p1, float) else f"{p1:>16}")
            yr_list.append(f"{p2:>14.1f}°C" if isinstance(p2, float) else f"{p2:>16}")

        print(f"{'Time':<6} | " + " | ".join(times_list))
        print("-" * (8 + len(times_list) * 19))
        print(f"{'open':<6} | " + " | ".join(open_list))
        print(f"{'Yr':<6} | " + " | ".join(yr_list))