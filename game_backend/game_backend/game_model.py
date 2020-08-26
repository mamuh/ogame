#!/usr/bin/env python3

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum

from dataclasses_jsonschema import JsonSchemaMixin

from game_backend.resources import Resources
from game_backend.entity import Entity


@dataclass
class Planet(JsonSchemaMixin):
    id: str
    name: str
    size: int
    buildings: List[Entity]
    owner_id: str


@dataclass
class World(JsonSchemaMixin):
    planets: Dict[str, Planet]


@dataclass
class Player(JsonSchemaMixin):
    id: str
    name: str
    resources: Dict[Resources, float] = field(
        default_factory=lambda: {resource: 0 for resource in Resources}
    )


@dataclass
class GameState(JsonSchemaMixin):
    world: World
    players: Dict[str, Player]

    def get_player_planets(player_id: str) -> List[Planet]:
        return [planet for planet in world.planets if planet.owner_id == player_id]
