#!/usr/bin/env python3
from dataclasses import dataclass, astuple
import random
from typing import Dict, List

from game_backend.components import PlanetComponent
from game_backend.entities.entities import Planet
from game_backend.game_structs import PlanetLocation


class PositionSystem:
    def __init__(self):
        self.planets_index: Dict[PlanetLocation, str] = {}
        self.player_planets: Dict[str, List[PlanetLocation]] = {}

    def register_planet(self, planet_id: PlanetLocation, planet: Planet):
        planet_comp = planet.components[PlanetComponent]
        location = planet_comp.location

        assert (
            location not in self.planets_index
        ), "Trying to register a planet at an already taken location"
        self.planets_index[location] = planet_id
        self.player_planets.setdefault(planet_comp.owner_id, []).append(planet_id)

    def is_location_free(self, location: PlanetLocation):
        return location not in self.planets_index

    def get_random_free_location(
        self, galaxy_range=5, system_range=500, position_range=9
    ) -> PlanetLocation:
        all_locations = set(
            (g + 1, s + 1, p + 1)
            for g in range(galaxy_range)
            for s in range(system_range)
            for p in range(position_range)
        )
        taken_locations = set(astuple(loc) for loc in self.planets_index)
        free_locations = all_locations - taken_locations
        random_free_location = random.choice(list(free_locations))

        return PlanetLocation(*random_free_location)

    def get_player_planets(self, player_id: str) -> List[str]:
        assert (
            player_id in self.player_planets
        ), f"player with id {player_id} is not in the index"
        return self.player_planets[player_id]

    def reset(self):
        self.planets_index = {}


PositionSystem = PositionSystem()
