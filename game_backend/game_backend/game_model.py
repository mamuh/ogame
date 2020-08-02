#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List

from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class Building(JsonSchemaMixin):
    pass

@dataclass
class Mine(Building, JsonSchemaMixin):
    pass

@dataclass
class Factory(Building, JsonSchemaMixin):
    pass

@dataclass
class Cannon(Building, JsonSchemaMixin):
    pass

@dataclass
class Planet(JsonSchemaMixin):
    id: str
    name: str
    size: int
    buildings: List[Building]    


@dataclass
class World(JsonSchemaMixin):
    planets: Dict[str, Planet]


@dataclass
class Player(JsonSchemaMixin):
    id: str
    name: str


@dataclass
class GameState(JsonSchemaMixin):
    world: World
    players: Dict[str, Player]

