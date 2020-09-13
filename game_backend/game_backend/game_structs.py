#!/usr/bin/env python3
from dataclasses import dataclass
from dataclasses_jsonschema import JsonSchemaMixin


class PlanetLocation(str):
    def __new__(cls, galaxy: int, system: int, position: int):
        instance = super(PlanetLocation, cls).__new__(
            cls, f"{galaxy}_{system}_{position}"
        )
        instance.galaxy = galaxy
        instance.system = system
        instance.position = position
        return instance

    @staticmethod
    def from_str(location_string: str):
        galaxy, system, position = location_string.split("_")
        return PlanetLocation(int(galaxy), int(system), int(position))

    def distance_from(self, other: "PlanetLocation"):
        if self.galaxy != other.galaxy:
            return 20000 * abs(self.galaxy - other.galaxy)
        elif self.system != other.system:
            return 2700 + 95 * abs(self.system - other.system)
        else:
            return 1000 + 5 * abs(self.position - other.position)
