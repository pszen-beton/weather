from functions import find_location

class Location:
    def __init__(self, name, lat=None, lon=None):
        self.name = name
        self.lat = lat
        self.lon = lon

    def set_coordinates(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def get_coordinates(self):
        return self.lat, self.lon

    def find_coordinates(self):
        coordinates = find_location(self.name)

        self.lat = coordinates["lat"]
        self.lon = coordinates["lon"]

    def __str__(self):
        return f"{self.name} ({self.lat}, {self.lon})"