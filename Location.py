from functions import find_location
from typing import Optional


class Location:
    name: str
    lat: Optional[float]
    lon: Optional[float]

    def __init__(self, name: str, lat: Optional[float] = None, lon: Optional[float] = None) -> None:
        self.name = name
        self.lat = lat
        self.lon = lon

    def set_coordinates(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon

    def get_coordinates(self) -> tuple[float | None, float | None]:
        return self.lat, self.lon

    def find_coordinates(self) -> None:
        coordinates = find_location(self.name)

        self.lat = coordinates["lat"]
        self.lon = coordinates["lon"]

    def __str__(self) -> str:
        return f"{self.name} ({self.lat}, {self.lon})"
