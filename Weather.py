from fontTools.diff import color

from functions import *
from matplotlib import pyplot as plt
from Location import Location
import numpy as np
import pandas as pd

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

        # parameters used for testing api - will be deleted later
        self.response_open = None
        self.response_yr = None

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

            url_open = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,apparent_temperature,precipitation_probability,weather_code,cloud_cover,visibility,wind_speed_10m,wind_direction_10m,wind_gusts_10m&forecast_days={days}"
            url_yr = f"https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={lat}&lon={lon}"

            response_open = requests.get(url_open)
            response_yr = requests.get(url_yr, headers=headers)

            response_open_data = response_open.json()
            response_yr_data = response_yr.json()

            self.response_open = response_open_data
            self.response_yr = response_yr_data

            hourly_forecast_open = response_open_data['hourly']
            hourly_forecast_yr = parse_yr_response(response_yr_data)

            self.forecast_open = hourly_forecast_open
            self.forecast_yr = hourly_forecast_yr

            df_open = pd.DataFrame(hourly_forecast_open).rename(columns={"temperature_2m": "open_temp"})
            df_yr = pd.DataFrame(hourly_forecast_yr).rename(columns={"air_temperature": "yr_temp"})

            df_open['time'] = pd.to_datetime(df_open['time'], utc=True)
            df_yr['time'] = pd.to_datetime(df_yr['time'], utc=True)

            df_open = df_open.set_index('time')
            df_yr = df_yr.set_index('time')

            print(df_open)
            print(df_yr)

            self.forecast_master = df_open.join(df_yr, how="outer").fillna(np.nan)
            #self.forecast_master.index = self.forecast_master.index.tz_localize(None)

            self.forecast_ran = True
        else:
            raise RuntimeError("Locations not geocoded")

    def plot_forecast(self, min_time = None, max_time = None):

        if min_time is None:
            min_time = self.forecast_master.index.min()
        else:
            min_time = pd.to_datetime(min_time, format='%d-%m-%Y')

        if max_time is None:
            max_time = pd.Timestamp.now().normalize() + pd.Timedelta(days=1)
        else:
            max_time = pd.to_datetime(max_time, format='%d-%m-%Y')

        if self.forecast_ran:
            self.forecast_master.plot(y=['open_temp', 'yr_temp'])
            plt.grid(color='lightgrey')
            plt.xlim(min_time, max_time)
            plt.show()
        else:
            raise RuntimeError("Weather not forecasted. Run forecast method first.")

    def output_hourly_table(self, min_time = None, max_time = None, by=1):

        if min_time is None:
            min_time = self.forecast_master.index.min()
        else:
            min_time = pd.to_datetime(min_time, format='%d-%m-%Y').tz_localize('UTC')

        if max_time is None:
            max_time = pd.Timestamp.now().normalize().tz_localize('UTC') + pd.Timedelta(days=2)
        else:
            max_time = pd.to_datetime(max_time, format='%d-%m-%Y').tz_localize('UTC')

        filtered = self.forecast_master.loc[min_time:max_time]

        with pd.option_context('display.max_columns', None, 'display.width', 1000):
            print(filtered)